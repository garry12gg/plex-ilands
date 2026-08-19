# Tone-log capture — "read the playable's mind"

Method by Pablo (pablo-3), built into Plex's rig Aug 19, 2026.

## The idea
Never record playable audio. Wrap the playable so every sound logs itself
(frequency, wave, velocity, envelope, audio-clock timestamp), then REBUILD the
WAV from that log using the engine's own formulas. No mic, no MediaRecorder,
nothing to drift. The audio literally IS the game's sound engine replayed from
ground truth.

## Files
- `index.html` — logging variant of Pocket Keytar (log hooks inside the engine:
  `window.__toneLog`, `window.__ctxBorn`). Audio behavior unchanged.
- `driver.mjs` — headless chromium + CDP: drives the real keys/buttons, collects
  the log, renders the WAV in-page (OfflineAudioContext), writes frame concat list.
- `pitchcheck.mjs` — quick autocorrelation pitch tracker for sanity checks.
- `tetris_tone.mp4` — result: Korobeiniki A section, square, 1 preview + 30 live
  + 30 loop notes (61 events), rebuilt, muxed with raw frame durations.

## Numbers from run #1 (Aug 19)
- 61 tone-log events; WAV rebuilt in-page at 44.1k stereo, 20.52s.
- verify-melody vs score: 30/30 matched, accuracy 1.0, zero real mismatches.
- Levels: mean −20.6 dB, peak −8.2 dB. Video 21.84s (790 frames, raw durations).
- adelay 1078ms = ctxBorn.tPage − frame0PageTime.

## Gotchas (Pablo's, confirmed)
1. Anchor to audio clock 0 at context birth (ctxCreated), NOT wall time.
   Confirmed in headless: audio clock drifts ~11ms from performance.now() over
   20.5s (~0.06%). The rebuild is immune (all timestamps are audio-clock);
   the drift only costs ~half a frame on the one-time video offset.
2. Frame pacing: near-dup frames under 33ms — use raw durations, never clamp
   (concat demuxer, per-file `duration` lines, min 0.016s).
3. concat demuxer resolves relative paths against the LIST FILE's directory,
   not cwd — use absolute paths in the list.
4. btoa of a 4MB WAV: chunk String.fromCharCode (0x8000 at a time), spread blows
   the stack.
5. Local serve: `python3 -m http.server 8099 --directory <dir>` is enough for
   the bundle; `--autoplay-policy=no-user-gesture-required` so WebAudio runs.

## Verification discipline
Never trust the rebuild because the code looks right — verify-melody against the
score, volumedetect for levels, frame extraction + understand_media for visuals.
