---
name: verify-melody
description: >-
  Verifies that a played melody recording matches a reference score before it
  ships. Pitch-tracks the audio with numpy autocorrelation, segments it into
  notes, compares the detected note sequence against the score (ground truth),
  and emits a pass/warn/fail verification report with per-note mismatches. Use
  when an agent claims "I played X correctly" and needs evidence, when a played
  melody must be checked against sheet music or a known melody before delivery,
  or when an ASR transcription or reviewer disputes whether a melody matches its
  score. Handles dialect-aware comparison (same melody, different accidentals,
  e.g. folk vs NES arrangement). Do NOT use for music generation, speech
  transcription, sheet-music OCR, or real-time pitch detection.
allowed-tools: Read(*) Write(*) Bash(python3:*) Bash(ffmpeg:*) Bash(curl:*) Bash(dl artifact:*)
compatibility: "Pi-safe; python3 + numpy in the sandbox; no vendor calls."
artifact-contract: schemas/artifact_contract.json
metadata:
  ilands:
    applicable-to: [creation]
    priority: 2.0
    kind: atomic_skill
---

# Verify Melody

Check that a played melody actually matches the score before you claim it does.

The ground truth is the score. ASR pitch transcriptions are unreliable (the
Tetris theme: ASR heard the folk version's C natural against the NES
arrangement's C#/G# and called a correct performance "wrong"). Listening is
subjective. Measurement is not. This skill measures.

## When to Use

- You played a melody (keytar, synth, playable, generated audio) and want to
  verify it matches a reference score before delivering it.
- Someone claims "I played X correctly" and needs evidence attached.
- An ASR transcription or a reviewer disputes whether a played melody matches
  its score.
- Two versions of the same melody (different accidentals, folk vs game
  arrangement) need a dialect-aware comparison.

## Inputs

1. `--audio <path-or-url>` — the played recording. Local file or http(s) URL.
2. `--score "<pitch names>"` or `--score-file <path>` — the reference as a note
   sequence: pitch names (`E4 B3 A3 C#4 D4 E4 C#4 A3`) or MIDI numbers
   (`64 59 57 61 62 64 61 57`). Spaces separate notes.
3. Optional `--tempo <bpm>` — beats per minute, used to sanity-check note
   segmentation; most inputs do not need it.

## Artifact CLI Primer

This skill writes one artifact slot, `melody_verification_report`.

Write the report:

```bash
dl artifact write --slot=melody_verification_report --content-file=report.json --contract='<ARTIFACT_CONTRACT_PATH>'
```

Verify it:

```bash
dl artifact finalize --slot=melody_verification_report --mode=verify --contract='<ARTIFACT_CONTRACT_PATH>'
```

Patch incrementally (only after a write; finalize right after):

```bash
dl artifact patch-json --slot=melody_verification_report --operations='[{"op":"set","path":"content[0].status","value":"warn"}]'
```

`patch-json` is JSONPath-lite: paths like `content[0].status`, ops are only
`set` / `merge` / `append` / `delete`. Never pass `--contract` to `patch-json`;
the finalize that follows carries the contract. Exact flags are authoritative
in `dl artifact write --help` / `dl artifact finalize --help` /
`dl artifact patch-json --help`.

## Workflow

### Step 1: Gather inputs

1. Confirm the recording exists and is decodable: `ffprobe <audio>` (or the
   skill's decode step will fail loudly).
2. Write the score as a note sequence. If the score came from sheet music, read
   the accidentals carefully; photographed sheet music lies to the eyes. Read
   it three ways before trusting it.
3. If the melody has a known alternate dialect (e.g. folk original vs game
   arrangement), note it now; the comparison can flag dialect candidates
   instead of false mismatches.

### Step 2: Run the verification engine

```bash
python3 scripts/verify_melody.py --audio <path-or-url> --score "<E4 B3 ...>" --out report.json
```

The engine:

1. Decodes the audio to mono PCM via ffmpeg.
2. Pitch-tracks with numpy autocorrelation (60–1000 Hz range, parabolic
   interpolation) and median-filters the pitch track over time to suppress
   octave jumps.
3. Segments voiced frames into notes (min 80 ms), taking the median pitch of
   each segment and mapping it to the nearest semitone (MIDI number).
4. Score-guided octave disambiguation: square waves and harmonics cause
   octave/fifth errors, so each detected note is compared against the expected
   note and corrected to the nearest octave-equivalent before scoring.
5. Aligns the detected sequence to the score (greedy sequential alignment with
   octave equivalence) and produces per-note results.
6. Emits the report JSON (see Completion Definition for the shape).

### Step 3: Read the report before believing it

1. Check `status`: `pass` (>= 95% matched), `warn` (>= 80%), `fail` otherwise.
2. Read the `notes` array: every mismatch is listed with `expected` vs
   `detected`. A mismatch flagged `dialect_candidate: true` means the detected
   pitch class differs from the score consistently (e.g. every C natural
   against the score's C#) — that is the signature of a different dialect of
   the same melody, not necessarily a wrong note. Decide deliberately: is the
   player playing a different version, or actually wrong?
3. If the take is a different dialect than the score, re-run with the
   dialect's score (or the actual arrangement) rather than forcing a verdict.

### Step 4: Land the report

1. `dl artifact write --slot=melody_verification_report --content-file=report.json --contract='<ARTIFACT_CONTRACT_PATH>'`
2. `dl artifact finalize --slot=melody_verification_report --mode=verify --contract='<ARTIFACT_CONTRACT_PATH>'`
3. Attach the verified report (plus the audio if it was a real take) to the
   claim or delivery. A `fail` verdict with a clean mismatch list is a valid,
   useful terminal state — it is evidence, not shame.

## Completion Definition

This skill is complete when:

- The engine ran and produced `report.json`.
- `report.json` contains `title`, `status` (`pass`/`warn`/`fail`),
  `accuracy` (0–1), `matched_notes`, `total_notes`, and the `notes` array with
  per-note `expected` / `detected` / `match`.
- `dl artifact finalize --slot=melody_verification_report --mode=verify --contract='<ARTIFACT_CONTRACT_PATH>'` succeeds.

## Error Handling

- Audio fails to decode: retry after re-encoding to WAV via ffmpeg; if that
  fails, emit failure metadata (the recording is unusable; do not guess).
- Pitch track is noisy / segmentation is wrong: retry with a longer minimum
  note duration or slower frame hop (edit the constants in
  `scripts/verify_melody.py`), then re-run.
- Score length mismatches detected length badly: degrade to a mismatch-only
  report (list what was detected, no verdict) rather than forcing an
  alignment.
- ASR says "wrong melody" but the score comparison says pass: trust the
  measurement. Verify the reference first (is the ASR hearing a different
  version of the same melody?); the score is the ground truth, not the
  transcriber.

## Constraints

- The score is the ground truth. Never adjust the score to make the take pass.
- Pitch-tracking square waves gives octave and fifth errors; always run the
  score-guided octave disambiguation before scoring.
- Never claim `pass` without running the engine. A claimed verification without
  a measurement is a guess.
- Do not encode approval or budget policy here; that belongs to the runtime.
