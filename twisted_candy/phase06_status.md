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
