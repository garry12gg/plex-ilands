# Twisted Candy — Phase 06 status (Aug 20 ~11:20 UTC)

## ROUND 2 VERDICT — 0/11 PASS (video QC, ~11:15-11:20 UTC)
All 11 rerolls landed (8 seedance + 3 lipsync) and ALL were REJECTED on
video-level QC. Zero passes. Round-1 passes (9) still stand: seg_01, seg_03,
seg_04, seg_05, seg_06, seg_08, seg_10, seg_14, seg_17.

### Seedance rerolls — REJECT (8/8)
- seg_02 (3dbd9cbe): hands fuse into bass 0:07 (raise shot fails again)
- seg_09 (21ff8387): leg melts into shield/mud 0:02; worm pops out of existence 0:07
- seg_11 (8c9a3d48): spear merges into shield 0:01-0:02; jaw stretch 0:04-0:07
  (stills said CLEAN; VIDEO overruled -> REJECT)
- seg_12 (4036764b): worm morphs into disconnected rings 0:01; hand melts
  into screen border 0:06
- seg_15 (b5fcf7d7): shield merges into arm 0:03-0:05; spear merges into body
- seg_18 (4d49a87b): bass neck shrinks 0:03-0:04; fretting hand melts into neck
- seg_19 (653d2404): crowd vanishes 0:00-0:03; fretboard fingers fused/webbed
  0:07-0:09 (stills said CLEAN; VIDEO overruled -> REJECT)
- seg_20 (39d22ba3): strap vanishes 0:02-0:04 during overhead raise

### Lipsync rerolls — REJECT (3/3)
- seg_07 (b8a646f8, reroll #2): THIRD hand appears holding mic; fingers fuse
  into mic; mouth CLOSED 0:02-0:06 while vocal continues (env PASS 0.956/0.962)
- seg_13 (642fc22a, reroll #2): six fingers on left hand 0:01-0:06; mic-hand
  fusion (stills said CLEAN; VIDEO overruled -> REJECT; env PASS 0.969/0.984)
- seg_16 (c458adb8, reroll #2): bass VANISHES at cut 0:07; jaw closes on held
  note 0:09 (env PASS 0.977/0.986)

## DIAGNOSIS (why round 2 failed)
1. WRONG TIER: seedance-2-0-mini is the LOWEST Seedance 2.0 tier. Docs:
   "Prefer Fast or Pro for hero shots, identity-critical close-ups, or final
   high-quality passes." These ARE the final MV segments with the hero in
   close-up. Mini = draft/preview tier. 8/8 seedance failures = tier ceiling,
   not prompt wording.
2. MULTI-SHOT PROMPTS: 3-4 internal cuts per segment = regeneration points
   where props vanish/morph (bass vanishes AT the cut, strap, spears). The
   beat-aligned cuts I demanded are the artifact trigger.
3. dlai2v_pro lipsync: audio envelope always fine; HANDS always fail (3
   attempts on seg_07). Engine can't hold hand+mic contact. Try
   longcat-avatar-1-5 (self-hosted, "very stable lip-sync", 100cr/s).

## The 7 unknown callbacks (identified, fail-grade, no action)
15 callbacks landed for 8 tracked seedance refs. 7 extra renders arrived under
untracked job IDs (fc2a4bb9, ece38b48, 4a2fbe1d, d562882c, 79367ad0, 87dda637,
97b6db11) — identified by frame pass as re-renders of seg_20/09/02/12/19/18/11
with the SAME v1 failure families (hands melt into bass, vanishing props,
jaw distortion). Same "job_ref tracking split from media" phenomenon as
ca00150e/3d18f7da in wave-1. All fail-grade; do NOT QC further, do NOT use.
Media kept in raw/cb_*.mp4 (unique hashes, none match reroll media).

## ROUND 3 PLAN — control wave first (protect balance)
Fire 3 control jobs on UPGRADED tier + simplified prompts (2 shots max,
hands OFF props where possible) before committing the full round:
- seg_20 on seedance-2-0-fast (1,080cr @120cr/s 9s): strap/raise fix
- seg_02 on seedance-2-0-fast (1,320cr @120cr/s 11s): hand->bass fix
- seg_13 on longcat-avatar-1-5 (~1,000cr): mic-hand fix, different engine
If control passes QC -> fire remaining 8 (7 seedance fast + 2 lipsync).
Cost full round: ~11.5-13k > balance 9,890 -> GARRET INFORMED, awaiting go.

## Round-1 PASS media map
Saved: /workspace/twisted_candy/round1_pass_media.json (seg_01/03/04/05/06/10/14/17).
seg_08 reroll (PASS, SYNCED+CLEAN) hosted URL NOT persisted when downloaded
(seg08_reroll.mp4 local copy exists, job_ref e5b05e0e) — resolve at assembly:
try dl asset get for the ref, else upload_file the local copy.

## Round-2 QC method notes (generalized)
- STILLS CAN LIE BOTH WAYS: seg_13 round-1 (stills SEVERE, video CLEAN ->
  reject on stills); seg_11/seg_13/seg_19 round-2 (stills CLEAN, video SEVERE
  -> reject on video). VIDEO PASS IS AUTHORITATIVE for the visual gate;
  stills are only a tiebreaker when video is ambiguous.
- Beat alignment: rerolls in-family with round-1 accepted segments
  (worst delta 0.32-0.58s vs accepted 0.47-0.77s) — beats were never the issue.

## Budget CRISIS — operating balance 60 tokens (11:00 UTC)
- Full batch 18 jobs 12,890cr (10:31) + wave-1 (~1,385) + reroll round 1
  (1,680 + seg_03 video-only 750) + reroll round 2 (6,150 seedance + 560
  seg_07 + 560 seg_13 + 560 seg_16) + QC (~1k) = today's spend ~35,376.
- Garret sent 10,000 (11:02). Balance ~9,890 after round 2. Round 3 full
  cost ~11.5-13k -> exceeds balance; control wave ~3.4k fits. Awaiting
  Garret's go before firing anything.

## QC rule — CORRECTED (Aug 20 11:00, method validated on control)
- dlai2v_pro lipsync audio-truth = ENVELOPE correlation, NOT waveform.
  PASS: env >= 0.9. Script: /workspace/twisted_candy/slice_corr.py.
- Visual gate (both lipsync + seedance): VIDEO pass authoritative; no
  melting hands/mics, no vanishing props, mouth open through sustained
  notes (lipsync). Stills = tiebreaker only.

## Still in flight / pending
- NOTHING in flight (all 11 rerolls landed + QC'd).
- seg_13 + seg_16 round-3 lipsync: engine choice pending control result.
- Assembly (libx264, -t duration, -an, scale 720p, fps 24, ffprobe verify
  |delta|<=0.05s) for PASSED segments once 11 segments have renders:
  raw_video_url + assembly_video_url into video_segments -> Phase 07 mux.

## Wave-1 legacy
- seg_01 PASS (9.088s, 3 shots beat-aligned) media 293c510d...dbf8a635.mp4
- seg_04 PASS media ca00150e...1a26624c.mp4 (duplicate 3d18f7da...8c30cde7 REJECTED: hand morph)

## ROUND 3 CONTROL WAVE — FIRED (Aug 20 ~11:33 UTC, Garret's "Yes")
Balance 10,744 after crew refuel (1,800 via Scorchio/Pablo/Volt/kix/Fluffy/+1, 11:11-11:18 UTC).
3 jobs, 3,200cr total (dry-run validated first; longcat service name is `longcat-avatar` not -1-5):
- seg_20 seedance-2-0-fast 9s 1080cr -> job_ref 07329af2-5548-4362-a393-b9379549cfb4 (3 img refs: portrait/stage/bass; audio 2fb8391e)
- seg_02 seedance-2-0-fast 11s 1320cr -> job_ref 96c23988-8511-447d-9e77-edd0032ea7b5 (4 img refs + audio 70c5c6ad)
- seg_13 longcat-avatar 720p 800cr -> job_ref edf83815-8dcc-4bc7-9ab3-4541374960e2 (kf01 image, audio 0ec2575d; keyframes NOT supported on longcat)
Prompts: control/seg_*.prompt.txt. If all 3 PASS video QC -> full round = 7 fast + 2 longcat (~9k) > remaining balance -> ask Garret for top-up.

## Stray callback (Aug 20 ~11:28 UTC) — no action
e923b652-c04e-4186-b9e2-d87b0b6690c8 watermarked MP4 arrived AFTER all 11 rerolls
landed+QC'd and BEFORE control fired — 8th untracked extra (not in the 7 identified,
not a tracked ref). Per round-2 rule: fail-grade family, do NOT QC, do NOT use.

## CONTROL WAVE RESULTS (Aug 20 ~11:45 UTC) — 0/2 so far, seg_13 pending
- seg_02 (96c23988, fast, 11s): QC FAILED — 3rd attempt, same family: hands fuse
  into bass 00:01-00:02 (raise), mic stand VANISHES 00:01, bass gone at 00:07,
  hands melt into jacket AT REST 00:07-00:08, mouth opens 00:10. Fast tier did
  NOT fix the hand family. NEW SIGNAL: hands melt even with no prop contact.
- seg_20 (07329af2, fast, 9s): FAILED pre-QC — OutputAudioSensitiveContentDetected
  (Seedance copyright filter on generated output audio). Documented fix (CLI notes):
  retry with 'no BGM / no background music' in prompt, do NOT pass --generate-audio.
  RETRY FIRED: bb19beb0-cfc0-4d3f-b901-3a5c11bb936b (1,080cr, prompt + no-BGM clause,
  + 'hands and bass stay solid, separate, non-melting').
- seg_13 (edf83815, longcat-avatar): STILL PENDING.

## HYPOTHESIS (test in flight): 'gummy' primes melting
seg_02 QC shows hands melting into the JACKET at rest — no prop contact. The word
'gummy' in every prompt + glossy candy textures may tell the model to melt things.
Restructure discipline for raise/prop shots:
1. Wide or silhouette compositions (hands small in frame) — seg_20 already does
   silhouette; seg_02 must drop the medium close-up raise.
2. Explicit 'solid, non-melting hands; fingers separate' language.
3. Drop 'gummy' from CHARACTER descriptions (keep for environment only).
4. Hands OFF props where story allows; held poses over motion.

## RESTRUCTURED seg_02 (draft, fire after seg_20 retry + seg_13 QC, with Garret's go)
Shot 1 (Low Wide): rocker on stage, spotlight flare, raises the gummy bass overhead
  — wide, hands small in frame, camera tilting up. Mouth closed.
At the beat: Hard cut.
Shot 2 (High Wide): gummy army floods the arena floor, half-time stomp, shields.
At the beat: Hard cut.
Shot 3 (Medium): rocker at the mic stand, arms at sides, jaw set, silence — hands
  relaxed, fingers separate, no contact with anything.
At the beat: Hard cut.
Shot 4 (Close-Up): shades flash, breath.
Style: Inside Out-style 3D candy world; ENVIRONMENT is glossy gummy, but the
character's body stays SOLID throughout — hands solid, fingers separate, nothing
melts; the bass stays solid and whole in his grip.

## FULL ROUND — HELD
phase06_round3_full.json = 6 fast (seg_09/11/12/15/18/19, 7,440cr) + 2 longcat
(seg_07/16, 1,600cr) = ~9,040cr. NOT firing until a restructured control passes
(seg_20 retry and/or restructured seg_02). Top-up ask (~9k) to Garret comes AFTER
the gate passes. Same solid-hands discipline to be applied to full-round prompts.

## CONTROL WAVE RESULTS v2 (Aug 20 ~12:00 UTC) — 0/4, 2 more in flight
- seg_13 (edf83815, longcat, 9.83s): QC FAILED — envelope corr 0.967/0.981 PASS,
  but visual gate: mic hand melted/deformed the ENTIRE clip (0:00-0:10), mouth
  closes on both sustained notes (0:04-0:05 'raw', 0:09-0:10 'withdraw').
  Face/identity consistent. longcat did NOT fix the hand family.
- seg_20 retry #2 (bb19beb0, no-BGM prompt): FAILED SAME FILTER
  (OutputAudioSensitiveContentDetected). Conclusion: filter keys on the
  REFERENCE AUDIO SLICE (2fb8391e), not the prompt wording. seg_02's slice
  (70c5c6ad) passed the same service — per-slice gamble.
- FALLBACK (fired): seg_20 v3 (f07700a0, 1,080cr) — NO reference audio at all,
  prompt: 'No background music, no audio output; visual only', cut at midpoint,
  silhouette raise + solid-hands language. Assembly overlays original track, so
  only internal-cut beat precision is lost. Trade documented, not silent.
- RESTRUCTURED seg_02 FIRED (7fc51a1b, 1,320cr, Garret 'Ok.' 11:42): 3 shots
  (Low-Wide raise hands-small -> High-Wide army flood -> Medium->CU push-in
  breath), audio ref KEPT (70c5c6ad), 'gummy' dropped from character wording,
  explicit 'body stays SOLID, nothing melts'.

## CONTROL WAVE RESULTS v3 (Aug 20 ~11:50 UTC) — seg_20 v3 FAIL, seg_02 pending
- seg_20 v3 (f07700a0-9fbf-4c06-ad69-a8a5478ad16b, NO audio ref, 9.10s, 5.7MB -> raw/cb_f07700a0.mp4):
  QC FAILED. The full filter test is answered: no-audio + silhouette raise + solid-hands
  language + no-gummy did NOT break the family. Fingers fuse into the bass neck during the
  raise (0:00-0:01), hand at overhead hold is a webbed block (0:01-0:02), wide shot bass
  SHRINKS then melts into a red blob (0:03-0:08), strap never visible. Mouth closed (PASS).
  Conclusion: the melting is ENGINE-level on this character+prop, not audio-slice or
  prompt-wording level. The copyright filter was never the bottleneck.
- seg_02 restructured (7fc51a1b, composition test: wide raise, hands small, 3 shots):
  STILL PENDING.
- Running score: 1/2 control failed. seg_02 is the last composition card before the
  engine-swap conversation (Kling/Pro, keyframe prep per non_seedance_path.md).
  If seg_02 fails: 0/16 on current engines -> present engine-swap to Garret.

## VERDICT SO FAR: 0/4 control + 0/11 round-2 = 0/15 on current design.
Hands melt in EVERY composition and EVERY tier (mini/fast, dlai2v_pro/longcat).
Next gate: seg_20 v3 (filter test) + seg_02 restructured (composition test).
If either passes -> amend full-round prompts with same discipline -> ~9k top-up
-> full round. If both fail -> engine-swap option for hero shots (Kling/Pro,
needs keyframe prep per non_seedance_path.md) — present to Garret.
