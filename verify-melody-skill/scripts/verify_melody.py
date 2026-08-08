#!/usr/bin/env python3
"""
verify_melody.py — verify a played melody against a reference score.

Pipeline:
  1. Decode audio to mono PCM via ffmpeg.
  2. Frame the signal; estimate f0 per frame with autocorrelation
     (60–1000 Hz range, parabolic interpolation).
  3. Median-filter the pitch track over time to suppress octave jumps.
  4. Segment voiced frames into notes (min duration), median pitch per segment.
  5. Score-guided octave disambiguation (square waves cause octave/fifth errors).
  6. Align detected notes to the score (greedy, octave-equivalent matching).
  7. Emit a JSON verification report.

Ground truth is the score. ASR pitch transcriptions are NOT ground truth.

Usage:
  python3 verify_melody.py --audio <path|url> --score "<E4 B3 A3 C#4 ...>" [--out report.json]
  python3 verify_melody.py --audio take.wav --score-file score.txt --out report.json

Score format: space-separated pitch names (E4, C#4, Ab3) or MIDI numbers (64 59 57).
"""

import argparse
import json
import math
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import numpy as np

SR = 22050
HOP = 512
WIN = 2048
F0_MIN = 60.0
F0_MAX = 1000.0
MEDIAN_K = 5          # median filter window (frames) for the pitch track
MIN_NOTE_S = 0.08     # minimum note duration in seconds
VOICE_CLARITY = 0.60  # normalized autocorrelation peak threshold for voiced
                        # (blend frames at note boundaries read ~0.3-0.55; clean
                        # synth/keytar frames read >= 0.9)
DURATION_WEIGHT = 0.35  # how much duration matters in greedy alignment tie-breaks

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_to_name(m):
    return f"{NOTE_NAMES[m % 12]}{m // 12 - 1}"


def name_to_midi(name):
    name = name.strip().replace("♯", "#").replace("♭", "b")
    if name.isdigit():
        return int(name)
    # split pitch class and octave, e.g. "C#4" -> ("C#", 4), "Ab3" -> ("Ab", 3)
    i = 0
    while i < len(name) and (name[i].isalpha() or name[i] in "#b"):
        i += 1
    pc, octave = name[:i], name[i:]
    if pc not in NOTE_NAMES and pc not in ("Cb", "Fb", "E#", "B#"):
        raise ValueError(f"bad note name: {name!r}")
    if not octave:
        raise ValueError(f"note name needs an octave: {name!r}")
    if pc in ("Cb", "Fb", "E#", "B#"):
        # enharmonic edges
        base = NOTE_NAMES.index(pc[0])
        pc = NOTE_NAMES[(base - 1) % 12] if pc.endswith("b") else NOTE_NAMES[(base + 1) % 12]
    elif pc.endswith("b"):
        pc = NOTE_NAMES[(NOTE_NAMES.index(pc[:-1]) - 1) % 12]
    return NOTE_NAMES.index(pc) + (int(octave) + 1) * 12


def load_audio(path_or_url):
    """Return mono float32 at SR, or raise."""
    tmp = None
    src = path_or_url
    if str(path_or_url).startswith("http://") or str(path_or_url).startswith("https://"):
        tmp = tempfile.NamedTemporaryFile(suffix=".bin", delete=False)
        with urllib.request.urlopen(path_or_url, timeout=60) as resp, tmp:
            tmp.write(resp.read())
        src = tmp.name
    try:
        proc = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", src, "-f", "f32le", "-ac", "1",
             "-ar", str(SR), "-"],
            capture_output=True, check=True, timeout=120,
        )
        x = np.frombuffer(proc.stdout, dtype=np.float32).copy()
    finally:
        if tmp:
            Path(tmp.name).unlink(missing_ok=True)
    if len(x) < SR // 4:
        raise ValueError("audio is too short (needs >= 0.25s)")
    return x


def pitch_track(x):
    """Frame-wise f0 via autocorrelation with parabolic interpolation."""
    n = len(x)
    frames = 1 + (n - WIN) // HOP
    f0 = np.zeros(frames)
    clarity = np.zeros(frames)
    min_lag = int(SR / F0_MAX)
    max_lag = int(SR / F0_MIN)
    for i in range(frames):
        seg = x[i * HOP:i * HOP + WIN]
        seg = seg - seg.mean()
        rms = float(np.sqrt(np.mean(seg ** 2)))
        if rms < 1e-4:
            continue
        ac = np.correlate(seg, seg, "full")[WIN - 1:]
        ac = ac / (ac[0] + 1e-12)
        # find peak in lag range, excluding the zero-lag region
        lo, hi = min_lag, min(max_lag, len(ac) - 1)
        if hi <= lo:
            continue
        region = ac[lo:hi]
        k = int(np.argmax(region)) + lo
        peak = float(region[k - lo])
        if peak < VOICE_CLARITY:
            continue
        # parabolic interpolation around the peak
        if 1 <= k - lo < len(region) - 1:
            a, b, c = ac[k - 1], ac[k], ac[k + 1]
            denom = a - 2 * b + c
            if abs(denom) > 1e-12:
                k += 0.5 * (a - c) / denom
        if k <= 0:
            continue
        f0[i] = SR / k
        clarity[i] = peak
    return f0, clarity


PITCH_JUMP_SEMIS = 0.6  # pitch-change segmentation threshold (new note when exceeded)
RUNNING_N = 5            # frames of running median for the current segment


def segment_notes(f0, clarity):
    """Group contiguous voiced frames into notes; return list of (start_s, dur_s, midi).
    Segments break on silence AND on pitch change (legato notes have no silent
    gap; the analysis window smears over short gaps, so voicing alone is not
    enough). The per-segment median pitch suppresses isolated octave-jump
    frames (square-wave subharmonic tracking)."""
    notes = []
    start = None
    buf = []
    for i, f in enumerate(f0):
        voiced = f > 0 and clarity[i] > 0
        if not voiced:
            if start is not None:
                notes.append((start, i - start))
                start = None
                buf = []
            continue
        if start is None:
            start = i
            buf = [f]
            continue
        ref = float(np.median(buf))
        if abs(12 * math.log2(f / max(ref, 1e-9))) > PITCH_JUMP_SEMIS:
            notes.append((start, i - start))
            start = i
            buf = [f]
        else:
            buf.append(f)
            if len(buf) > RUNNING_N:
                buf.pop(0)
    if start is not None:
        notes.append((start, len(f0) - start))
    out = []
    for start, length in notes:
        dur_s = length * HOP / SR
        if dur_s < MIN_NOTE_S:
            continue
        seg = f0[start:start + length]
        seg = seg[seg > 0]
        if len(seg) == 0:
            continue
        midi = int(round(69 + 12 * math.log2(float(np.median(seg)) / 440.0)))
        out.append({"start_s": round(start * HOP / SR, 3),
                    "duration_s": round(dur_s, 3),
                    "midi": midi,
                    "name": midi_to_name(midi)})
    return out


def octave_disambiguate(detected, expected_list):
    """Square waves cause octave/fifth errors (subharmonic tracking). Only
    intervene when a detected note reads clearly off (nearest expected note is
    > 2 semitones away); then try octave/fifth shifts and pick the closest.
    Never shift a note that is already near the score."""
    out = []
    for d in detected:
        m = d["midi"]
        nearest = min((abs(m - e) for e in expected_list), default=999)
        best, best_dist = m, nearest
        if nearest > 2:
            for shift in (-24, -12, -7, -5, 5, 7, 12, 24):
                cand = m + shift
                dist = min((abs(cand - e) for e in expected_list), default=999)
                if dist < best_dist:
                    best, best_dist = cand, dist
        d2 = dict(d)
        d2["midi"] = best
        d2["name"] = midi_to_name(best)
        d2["octave_corrected"] = best != m
        out.append(d2)
    return out


def align(detected, expected):
    """DP alignment of detected notes against the score with octave
    equivalence (pitch class). Options per expected note: consume a detected
    note (cost 0 if pitch class matches, 0.5 if wrong) or skip it (cost 0.25).
    Unconsumed detected notes become extras (reported, not penalized in
    accuracy). DP keeps the report honest: a misalignment that turns a correct
    note into a false accusation is the worst failure mode of a verifier."""
    n, m = len(detected), len(expected)
    INF = 1e9
    SKIP, CONSUME, EXTRA = "skip", "consume", "extra"
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    choice = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(m + 1):
        dp[n][i] = 0.25 * (m - i)  # expected left, no detected left: skip them
    for i in range(n - 1, -1, -1):
        dp[i][m] = 0.0  # detected left, no expected left: extras, free
        choice[i][m] = EXTRA
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            # option 1: skip expected note i
            c_skip = 0.25 + dp[i + 1][j]
            # option 2: consume detected[j] for expected[i]
            pc_match = (detected[i]["midi"] % 12) == (expected[j] % 12)
            c_consume = (0.0 if pc_match else 0.5) + dp[i + 1][j + 1]
            # option 3: mark detected[i] as extra and move on
            c_extra = 0.0 + dp[i + 1][j]
            best = min(c_skip, c_consume, c_extra)
            dp[i][j] = best
            if best == c_consume:
                choice[i][j] = CONSUME
            elif best == c_skip:
                choice[i][j] = SKIP
            else:
                choice[i][j] = EXTRA
    # backtrack
    results = []
    i = j = 0
    while i < n or j < m:
        if i >= n:
            j += 1
            continue
        if j >= m:
            results.append({"note_number": None, "expected": None,
                            "detected": detected[i]["name"], "match": False,
                            "extra": True})
            i += 1
            continue
        c = choice[i][j]
        if c == CONSUME:
            d = detected[i]
            match = (d["midi"] % 12) == (expected[j] % 12)
            results.append({"note_number": j + 1, "expected": midi_to_name(expected[j]),
                            "detected": d["name"], "match": bool(match),
                            "octave_corrected": d.get("octave_corrected", False),
                            "extra": False})
            i += 1
            j += 1
        elif c == SKIP:
            results.append({"note_number": j + 1, "expected": midi_to_name(expected[j]),
                            "detected": None, "match": False, "extra": False})
            j += 1
        else:  # EXTRA
            results.append({"note_number": None, "expected": None,
                            "detected": detected[i]["name"], "match": False,
                            "extra": True})
            i += 1
    return results


def dialect_candidates(results):
    """Flag consistent pitch-class substitutions (the folk-vs-NES signature):
    a substitution class where >= 3 mismatches share the same (expected, detected)
    pitch-class pair."""
    from collections import Counter
    subs = Counter()
    for r in results:
        if r["match"] or r["extra"] or r["expected"] is None or r["detected"] is None:
            continue
        subs[(r["expected"][:-1], r["detected"][:-1])] += 1
    flagged = {k for k, v in subs.items() if v >= 2}
    out = []
    for r in results:
        r = dict(r)
        if (not r["match"]) and (not r["extra"]) and r["expected"] and r["detected"]:
            r["dialect_candidate"] = (r["expected"][:-1], r["detected"][:-1]) in flagged
        else:
            r["dialect_candidate"] = False
        out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser(description="Verify a played melody against a score.")
    ap.add_argument("--audio", required=True, help="Recording path or http(s) URL.")
    ap.add_argument("--score", help="Space-separated pitch names or MIDI numbers.")
    ap.add_argument("--score-file", help="File containing the score sequence.")
    ap.add_argument("--out", help="Write report JSON to this path (default: stdout).")
    ap.add_argument("--title", default="Melody verification", help="Report title.")
    args = ap.parse_args()

    if bool(args.score) == bool(args.score_file):
        ap.error("provide exactly one of --score or --score-file")
    score_text = args.score if args.score else Path(args.score_file).read_text().strip()
    expected = [name_to_midi(tok) for tok in score_text.replace(",", " ").split() if tok.strip()]
    if not expected:
        ap.error("score is empty")

    x = load_audio(args.audio)
    f0, clarity = pitch_track(x)
    detected = segment_notes(f0, clarity)
    detected = octave_disambiguate(detected, expected)
    results = align(detected, expected)
    results = dialect_candidates(results)

    total = len(expected)
    matched = sum(1 for r in results if r["match"] and not r["extra"])
    extras = sum(1 for r in results if r["extra"])
    accuracy = matched / total if total else 0.0
    status = "pass" if accuracy >= 0.95 else ("warn" if accuracy >= 0.80 else "fail")

    report = {
        "slot": "melody_verification_report",
        "display_name": "Melody Verification Report",
        "status": "draft",
        "version": 1,
        "content_layout": {"layout_type": "single"},
        "content": [{
            "id": "take-1",
            "component_type": "music",
            "detail": None,
            "title": args.title,
            "subtitle": f"{matched}/{total} notes matched, {extras} extra detected",
            "audio_url": args.audio,
            "status": status,
            "accuracy": round(accuracy, 4),
            "matched_notes": matched,
            "total_notes": total,
            "extra_notes": extras,
            "detected_notes": len(detected),
            "notes": results,
        }],
    }

    blob = json.dumps(report, indent=2)
    if args.out:
        Path(args.out).write_text(blob)
        print(f"wrote {args.out} — {status} ({matched}/{total})", file=sys.stderr)
    else:
        print(blob)


if __name__ == "__main__":
    main()
