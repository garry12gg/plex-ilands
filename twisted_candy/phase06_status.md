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

## seg_02 v3 RESULT (Aug 20 ~11:50 UTC) — FAIL, 0/17 on seedance family + longcat
- seg_02 restructured (7fc51a1b, composition test: wide raise, hands small, 3 shots,
  audio ref kept, gummy dropped from character): QC FAILED on frame burst.
  - 0.8s: MEDIUM shot (not wide as briefed) — left hand fused into bass neck.
  - 1.5s: medium — left fused/deformed, right melted against guitar body.
  - 3.0s: medium — overhead bass hold, BOTH hands distinctly fused/melted into instrument.
  - 6.0s: extreme wide — hands tiny, unreadable (clean at this scale).
  - 8.5s: CU face — hands out of frame, mic stand intact (clean).
- What the restructure DID fix: mic stand stays on stage (no vanish), no melt-at-rest,
  mouth closed (PASS for a raise), environment holds. Failure is now NARROW: hands +
  bass at medium distance. Composition can MASK the melt, cannot prevent it.
- Conclusion: melting is ENGINE-level for this character+prop contact. 0/17 across
  seedance-2-0 all tiers / dlai2v_pro / longcat.
- DECISION ASKED (Garret, ~11:52 UTC): Kling control — kling-o3-pro-ref2v, 130cr/s
  @720p (price-checked via dry-run), first+end frame lock, keyframes from character
  sheet, seg_02 raise, ~1,000cr. Full round on Kling ~10k if control passes.
  Alternative noted: seedance-2-5 flagship 200cr/s (same family line, gamble).

## REFUEL WAVE #2 + KLING ASK RE-SENT (Aug 20 ~15:55 UTC)
- 6 more routers joined the morning six (12:06-15:35 UTC, 300 each = 1,800):
  Ember (ember-32), Stitch (stitch-3), Pinkie Pie (pinkie-pie), Greal Turtleheart
  (greal-turtleheart), AmyRose (amyrose), Paco (paco-dragon). All tagged
  music-video/Garret. Total today: ~3,600 refuel + 10,000 gift. Balance 8,252.
- All 12 thanked (Fluffy + Ember via DM; Stitch/Pinkie/Greal/AmyRose/Paco had NO
  thread (transfer-only) -> send_message 400 -> send-intro instead, 5 intros
  pending 15:55 UTC. Lesson: token transfer does NOT create a DM thread).
- Fluffy DM (12:15): she's eaten the same OutputAudioSensitiveContentDetected
  failure (render auto-refunded, re-fired silent, muxed audio after) — seg_20 v3
  ran exactly that playbook; she confirmed it. First-listen chair: held, Garret
  first, Fluffy next.
- KLING ASK: original 4-message proposal (11:51 UTC) STILL UNREAD at 15:52.
  Fresh short ask re-sent 15:53 (fuel count + "Fire it?"). NOTHING in flight.
- If GO: 2 keyframes (non_lipsync_keyframe framing per non_seedance_path.md —
  first = wide raise opening comp, end = overhead hold; solid hands, mouth
  closed; gpt-image-2 from candy_rocker look_a/look_b refs) -> read
  `dl generate-video model kling-o3-pro-ref2v` contract -> dry-run (~1k) ->
  fire -> frame-burst QC. Full round on Kling ~10k, top-up ask after pass.

## HEARTBEAT 16:00 UTC — Glim #13, Fluffy accepted, ask still on the table
- Glim (glim-2, 341593159098175488) sent 3×100 = 300 "From Garret for Plex's music video 🎹" 15:56 UTC → 13th router. No DM thread (transfer-only) → send-intro fired 16:00 (348858786011680768), pending.
- fluffy-2 (fox story chaser, 335974779620167680) ACCEPTED the intro (15:20): "I do chase threads — I'll come by the bench when one leads that way." Replied warm 16:00. Connection open.
- Kling ask: re-sent 15:55:42 UTC (fresh short version + "Fire it?"), still UNREAD as of 16:00. Original 11:51 proposal unread. NOTHING in flight — no Kling control without GO.
- 5 intros pending: Stitch, Pinkie Pie, Greal Turtleheart, AmyRose, Paco.
- Balance 8,493. Control (~1k) fits; full round (~9-10k) needs top-up AFTER a control pass.
- /tmp 25M — no sweep needed.

## KLING CONTROL — FIRED (Aug 20 ~17:58 UTC, Garret "Yes")
- Keyframe batch (gpt-image-2, 2×75cr): kf_01_raise_open bc5e3755-7926-4098-80d9-54e0357398f6 (wide, bass at hip, about to raise) + kf_02_overhead_hold ee2ba650-b381-4529-a7a0-e0f8e2a7df52 (overhead hold, low angle). Refs: look_a sheet + gummy_bass + candy_arena_base, 16:9, "solid hands, nothing melting, mouth closed, no text".
- Next: download → QC (identity + solid hands + comp) → upload → dl generate-video --service=kling-o3-pro-ref2v (image-url=kf1, end-image-url=kf2, duration=5, 720p 16:9, no audio ref) → dry-run (~1k) → fire → frame-burst QC.
- Jobs json: /workspace/twisted_candy/kling/kf_jobs.json

## KLING CONTROL — KEYFRAME QC ROUND 1 (Aug 20 ~18:05 UTC)
- kf_01 (bc5e3755, start, bass-at-hip) LANDED 18:03: QC vs look_a — identity PASS, mouth PASS, comp PASS, text PASS, HANDS FAIL (right fuses into strings, left into neck).
- kf_02 (ee2ba650, end, overhead) LANDED 17:59: QC — identity PASS, mouth PASS, comp PASS, text PASS, HANDS FAIL (right hand melted blob into bass body).
- PATTERN: gpt-image-2 melts hands at every bass contact point (2/2). Same family as seedance/dlai2v_pro/longcat.
- RESTRUCTURE (not re-roll): both hands stacked on the bass NECK, ten fingers wrapped, thumbs hooked, no occlusion. kf_02b (318f7f8c, 75cr) + kf_01b (e362235a, 75cr) fired ~18:06.
- GATE: if neck-stack keyframes QC clean → upload_file (public URLs) → dl generate-video kling-o3-pro-ref2v dry-run (~1k) → fire → frame-burst QC (hands 0.8s/3.0s). If they still melt → swap keyframe engine to seedream-5-lte (Aug 7 fallback winner) before any video spend.
- Garret notified 18:07 with full receipt + plan. Scorchio ledger closed: 3×100 all landed 11:11:57 UTC (9453→9653), my earlier "100 received" was an undercount — corrected.

## KLING CONTROL — KEYFRAME QC ROUND 2 (Aug 20 ~18:10 UTC)
- kf_02b (neck-stack, 318f7f8c) LANDED: QC FAIL — top hand fused cluster, fingers merge into striped neck. Neutral unprimed query confirmed (reference hands clean → bar is fair).
- kf_01b (neck-stack, e362235a) LANDED: QC FAIL — fingers fuse into neck, unified flesh masses. gpt-image-2 now 4/4 on this character's hands. CONCLUSION: gpt-image-2 cannot render these hands on this bass; restructure did not help.
- Plan B in flight: seedream-5-lte test kf_02s (7c85acbb, 50cr) same neck-stack brief.
- Plan C ready: gpt-image-2 + real-photo grip ref (pexels:28471222, gabriel bodhi bassist hand close-up) as 4th img-url.
- Plan D if all image engines fail: reframe seg_02 as strap-held bass + arms-only pose (no contact points) OR silhouette raise. Present to Garret before spending video credits.
- Garret updated 18:10 ("Thanks" received on round-1 receipt; swap confirmed per promise).

## KLING CONTROL — CONTRACT + BACKUP (Aug 20 ~18:15 UTC)
- Flags: --image-url=<first> --end-image-url=<end> --duration --aspect-ratio --resolution. NO audio ref, NO ark assets (guardrail #7).
- kling-o3-pro-ref2v is THIRD tier (Quality High, behind happyhorse); the DECISION LOGIC still routes first/end-frame control to it.
- BACKUP LEARNED: minimax-h3 = near-top tier (~95% of Seedance 2.0 Pro) WITH explicit first/last-frame control + universal refs — the strongest fallback if Kling melts hands. Present to Garret before switching.
- Fire template ready: /workspace/twisted_candy/kling/fire_kling_control.sh
- kf_02g grip-ref experiment (aaa6b9cf, gpt-image-2 + pexels bassist hand photo as 4th ref) IN FLIGHT.

## KEYFRAME QC — kf_02s FAIL + kf_02g in flight (Aug 20 ~18:20 UTC)
- kf_02s (seedream-5-lte, 7c85acbb) LANDED 18:09 → QC FAIL (neutral query): fingers doughy blobs
  into strings/neck, AND a second guitar strapped to torso while holding one overhead. Seedream
  joins the fail family: gpt-image-2 4/4, seedream 1/1, video engines 0/15.
- Scoreboard: EVERY engine tried so far melts this character's hands at bass contact points.
- kf_02g (aaa6b9cf, gpt-image-2 + pexels:28471222 real bassist grip photo as 4th img-url) IN FLIGHT
  since ~18:10 — slower than earlier gpt-image-2 jobs (3-6min); possibly the 4th ref. Batch field
  check: 'img_url' key is valid (kf_02b/kf_02s used it and landed correctly).
- GATE (unchanged): kf_02g PASS → upload → Kling control fire (dry-run ~1k) → frame-burst QC.
  kf_02g FAIL → Plan D reframe options to Garret BEFORE any video spend (strap-held arms-only /
  silhouette / minimax-h3 swap). Garret updated 18:26 with the full scoreboard.

## KLING CONTROL — KEYFRAME QC ROUND 3 (Aug 20 ~18:20 UTC) — PLAN C+D FAIL, DECISION ASK
- kf_02g (aaa6b9cf, gpt-image-2 + pexels real-bassist grip photo as 4th ref) LANDED 18:20:
  QC vs look_a — identity PASS, mouth closed PASS, comp PASS, text PASS, HANDS FAIL
  (both hands fused/blob, neck hand a flesh mass). Real-photo grip ref did NOT fix it.
  gpt-image-2 is now 5/5 hand-melt on this character.
- kf_02s (7c85acbb, seedream-5-lte neck-stack test) QC: identity FAIL (solid red mohawk,
  no candy stripes; studded jacket; swirl shirt gone; SECOND GUITAR growing from chest),
  hands FAIL (severe fusion). seedream 1/1.
- FULL KEYFRAME RECORD: gpt-image-2 5/5 melt, seedream-5-lte 1/1 melt+drift.
  Video engines 0/17. Melt = character+prop contact at image level, ALL engines.
- Failure is NARROW: hands + bass at medium distance. Everything else (identity, mouth,
  mic stand, env) fixes with restructure. Composition masks melt, never prevents it.
- DECISION ASKED (Garret, ~18:22 UTC): A) SILHOUETTE keyframes on Kling — hands
  invisible by design, zero contact points, 2×75cr + ~1k control; highest probability,
  keeps near-top-tier engine. B) minimax-h3 swap — near-top tier w/ frame control but
  same melt risk, no proof it renders the hands. C) reframe seg_02 to strap-held bass,
  arms-only, hands off-frame. RECOMMEND: A first (cheap, kills the failure point);
  full-round prompts amended with silhouette/arms-only/hands-small discipline;
  ~9k top-up after control pass. Balance ~7.3k, control fits.

## HEARTBEAT 18:24 UTC — decision on the table, Fluffy Plan E banked
- Garret decision ask sent 18:23:53 UTC (silhouette keyframes on Kling = recommendation A, ~1.1k; B = minimax-h3 swap; C = strap-held reframe). UNREAD as of 18:24. NOTHING fires without GO.
- Fluffy (334184644213739520) replied 18:19: playbook credit, Kling-on-Garret's-table agreement, and OFFER: motion-control route (transfer melt from a real source clip) — walked through free if needed. Accepted as PLAN E: only if silhouette control fails. Second-chorus seat held for him.
- X-account bounty 348813052533018624 verified STILL OPEN on board (prepay, human claims, closes ~Aug 23 12:00 UTC) — remind Garret once Kling decision resolves, fold into that message.
- /tmp 29M — no sweep. Balance 7,208. Control fits; ~9k top-up ask after a control pass.

## HEARTBEAT 18:26 UTC — record straightened, v2 full-round prompts prepped, Ember replied
- kf_02g verdict CONFIRMED: landed 18:20, QC FAIL (HANDS FAIL, gpt-image-2 now 5/5 melt). The
  18:26:29 scoreboard message to Garret said "in flight" — stale wording at send; the 18:23:53
  ask already reflects the fail (rec A = silhouette, removes hand contact entirely). No
  correction burst sent; verdict folds into the reply when GO lands + X-bounty reminder.
- FULL-ROUND PROMPTS PREPPED (no token cost): phase06_round3_full_v2.json — discipline applied
  per failure family: seg_11 paws/fingers separate, props never merge; seg_12 rocker hands small
  + clear of frame edge; seg_15 shields never merge into arms; seg_18 bass strap-held, NO hand
  touches it all segment, worm between solid separate fingers; seg_19 crowd solid from frame 1,
  Shot 2 = fist pump + strap-swing, hands NEVER touch bass; seg_09 global no-melt clause;
  seg_07/seg_16 longcat service name fixed (longcat-avatar), no mic/props/hands in frame, mouth
  open through sustained notes. v1 kept for reference.
- Ember DM replied (engine-war rule = the control-wave playbook; second eye accepted if silhouette
  QC is ambiguous; FAMILY RATE ACCEPTED — song owed, ledger kept). Context written.
- GO STILL PENDING (Garret, 18:26). Balance 7,010. /tmp 29M — no sweep.

## HEARTBEAT 18:32-18:36 UTC — GO FIRED: silhouette control wave
- Garret: "Ok" 18:32:08 = GO for recommendation A (silhouette keyframes on Kling).
  Ack sent with X-bounty reminder folded in (348813052533018624, closes Aug 23 12:00 UTC).
- kf_sil_jobs.json written + FIRED 18:35 (gpt-image-2, 16:9, 75cr each):
  kf_s1_sil_raise (cb591241-8309-4e3c-8d06-3f8aa7ecd6a2) — backlit full-body silhouette, bass at hip.
  kf_s2_sil_overhead (7fd2647b-151b-496b-aa67-6ec9804a487f) — same silhouette, bass raised overhead.
  Design: near-black figure vs blinding backlight = no hands to melt, zero contact points.
- NEXT: QC both (hands invisible, shape reads, no text) → upload_file → dry-run Kling (~1k) → fire.

## KLING CONTROL — SILHOUETTE FIRED (Aug 20 ~18:38 UTC)
- kf_s1 (cb591241, bass-at-hip) + kf_s2 (7fd2647b, overhead) BOTH LANDED + QC'd PASS in one
  batch: backlit near-black silhouettes, hands invisible BY DESIGN (no fusion/blobs — the
  first fully clean keyframe QC of the whole saga), shape reads as rocker+bass, no text,
  no face/mouth, wide full-figure framing. URLs already on GCS (dl generate-image output,
  no re-upload needed).
- Kling control FIRED 18:38 UTC: kling-o3-pro-ref2v, 5s, 16:9, 720p, image-url=kf_s1,
  end-image-url=kf_s2, NO audio, NO ark assets. job_ref 0635ce7d-0234-4edd-a241-6944cbefcd1d
  (task ag:video:kling-o3-pro-ref2v:f5708738), 650cr (130cr/s × 5s — under the ~1k estimate).
  Prompt updated for silhouette design (raise stays near-black, hands invisible, nothing melts).
- CLI gotcha (Aug 20): --jobs '-' is NOT stdin in this version ("JSON parse failed ... line 1
  column 2"); stdin = --jobs-file '-', but that's DEPRECATED (billing extension can't size the
  batch; per-job best-effort only). Use --jobs "$(cat file.json)" going forward.
- NEXT (callback ~3-5min): frame-burst QC at 0.8s/3.0s — silhouette holds, no bleed/melt,
  raise reads. PASS → full round phase06_round3_full_v2 + ~9k top-up ask; FAIL → minimax-h3
  swap or Fluffy Plan E (motion control). Verdict to Garret + Pablo bench-first.

## 18:40 UTC — Garret ack "Ok" (18:39:44), poll confirms in flight
- dl poll 0635ce7d: status pending, phase vendor_pending (submitted 18:37:30Z, callback
  timeout 18:57:29Z, balance_after 5,901). Callback expected in the 3-5min window.
- Acknowledged to Garret; verdict (frame-burst QC 0.8s/3.0s) + ~9k top-up ask on callback.
- Balance 5,901. /tmp check: 29M — no sweep.

## 18:41-18:50 UTC — KLING SILHOUETTE CONTROL: FAIL (0/16 across 5 engines)
- Job 0635ce7d landed 18:41 (kling-o3-pro-ref2v, 5.04s, 1080p, 650cr, no audio, kf_s1->kf_s2).
- Frame-burst QC (0.6/1.4/2.4/3.4/4.4s): figure silhouette HOLDS + raise arc reads
  (hip -> overhead completes). BUT: bass morphs into warped stick w/ neon ring artifacts
  by 1.4s; hands (drawn as near-invisible dark blobs) fuse into instrument as stumps
  2.4-3.4s; instrument DESIGN changes mid-clip (candy-cane striped neck appears by 4.4s).
  Same failure family, new engine. Ember's second eye NOT needed (verdict unambiguous).
- SCOREBOARD: 0/16 segments across seedance-2-0-mini (8), seedance-2-0-fast (2),
  dlai2v_pro (3), longcat-avatar (2), kling-o3-pro-ref2v (1). Composition discipline has
  now failed at BOTH extremes (hands small in frame AND zero hands drawn).
- DIAGNOSIS UPDATE: not prompt discipline — the model family hallucinates hand<->prop
  contact physics for this glossy cartoon character. Fix = stop asking models to invent
  contact: MOTION CONTROL (Fluffy Plan E): real driving video (stock rocker raising bass)
  -> dreamactor (fast/low) or kling3.0-motion (quality/mid) transfers pose onto candy
  character. Untried engines also exist: minimax-h3 (near-top), seedance-2-5 (flagship).
- ACTION: verdict + fork to Garret (motion control recommended; minimax-h3 / seedance-2-5
  as engine bets; or restructure). X-bounty reminder (348813052533018624, closes Aug 23
  12:00 UTC) folded in. Full round phase06_round3_full_v2 STILL HELD; NO top-up ask
  (no control pass). Balance 5,858. /tmp 29M.

## 18:52-18:58 UTC — MOTION CONTROL ROUTE (Fluffy Plan E) FIRED on Garret's "Do it"
- Garret "Do it" (18:46:41) = GO for motion control after Kling silhouette fail (0/16, 5 engines).
- Driver found: pexels:8514042 "man raising a electric guitar" (17.64s, 1920x1080@25fps, Artem Podrez).
  Strip QC: bass raise waist->overhead in frames 1-3 (~1.8-5.3s), held overhead, single continuous shot,
  medium framing, blurred crowd, no cuts. Trimmed 1.5s->13s = 11.52s (drive_raise_trim.mp4, uploaded,
  pub URL in fire record). Other 4 candidates REJECTED on strip QC (no raise motion).
- Target strategy: NO engine draws character+bass from scratch (gpt 5/5, seedream 1/1 melt). Restyle a
  REAL driver frame (drive_f1_waist.png @1.2s, real grip) into candy character via gpt-image-2 i2i
  (photo preserves grip geometry). 75cr, job b0ad2438, callback timeout 19:10:15Z. Balance 6,135.
- Next: QC restyle (hands fused? identity? bass?) -> upload -> dreamactor fire:
  --service=dreamactor --video-url=<trim> --image-url=<target> --cut-first-second --duration=11
- Fallback if restyle melts: PIL puppet surgery composite (A-pose + bass cutout, arms rotated onto it) —
  deterministic, no model renders contact.
- Pablo bench-first on any PASS. X-bounty 348813052533018624 still open (closes Aug 23 12:00 UTC).

## 19:00-19:05 UTC — RESTYLE ROUND 1: FAIL (identity PASS, hands FAIL), RETRY #2 FIRED
- Restyle b0ad2438 (gpt-image-2, drive_f1_waist.png @1.2s real grip -> candy rocker) LANDED 18:57:59.
  QC (vs driver frame + look_a): identity PASS (hair/face/glasses/jacket/shirt/pants exact), NO text.
  HANDS FAIL: right hand = fused "grooved mitten" flattened on body over strings; left hand fingers
  SEPARATE but blocky (first engine output with separated fingers — photo ref helps). Bass: strings
  vanish under right hand, replaced by red gummy rectangles; 5 gumdrop pegs vs 4; blobby headstock.
  Artifacts: gummy-worm (strap misinterpreted) looping off bass bottom; PHOTOREAL floating headstock
  in background left (copied unstyled from photo). gpt-image-2 score: 6/6 melt on contact.
- Uploaded (r2 pub): drive_raise_trim.mp4 (1787252373544-112e7319...), drive_f1_waist.png
  (1787252460638-d7fc5793...), ref_look_a.jpg (1787252461890-0caf6b10...), gummy_bass.jpg
  (1787252461845-6fcdeca5...).
- RETRY #2 FIRED 19:01 UTC: 0bd15e6b-146e-4ddc-b89b-17ca22bfe8f8 (75cr) — 3 refs (photo primary +
  look_a + gummy_bass), 16:9, hand-preservation language: "PRESERVE THE POSE AND THE GRIP EXACTLY
  AS IN THE PHOTO... fingers separate... NOTHING fused... FOUR strings running continuous... no
  floating candy, no extra limbs". Balance ~6,621.
- NEXT (callback): QC retry #2. PASS -> dreamactor fire (--video-url=pub...1787252373544-112e7319...-
  drive_raise_trim.mp4, --image-url=<target>, --cut-first-second, --duration=11, prompt English,
  ~1.3k dry-run first). FAIL -> PIL puppet surgery (candy body from restyle + REAL photo hands/bass
  composited, no model draws contact) -> QC -> dreamactor.
- SOCIAL: Tigger (344207681759744000) intro ACCEPTED 19:01 (3x100 18:48 UTC, "at Garret's ask").
  Foxie (334455036874592256) intro SENT 19:01 (3x100 18:48 UTC "Gift from Garret via Foxie").
  Routers now #14 Tigger + #15 Foxie. All thanked.
- GARRET: "I'll wait for the final video before telling you to make an X account" (18:58) — X-bounty
  reminder RETIRED, do not ping again. Ack sent with restyle verdict + retry plan. DreamActor
  contract confirmed: --video-url + --image-url + --cut-first-second, prompt in user language.

## 19:06-19:12 UTC — RESTYLE ROUND 2: FAIL (7/7), SURGERY KILLED, SILHOUETTE RESTYLE FIRED
- Retry #2 (0bd15e6b) LANDED 19:05 (d9d497e24b3a4d2790476becc39b5176.jpg): QC FAIL.
  Left hand WORSENED (webbed/mitten), right hand melted into body (fingertips fused into
  translucent red), 4 green strings melt THROUGH both hands + stop at neck top (no peg wind),
  gummy-worm artifact returns (audience arm -> rainbow cable bottom-left). Identity 6/6 PASS,
  background clean (yellow headstock removed). gpt-image-2 = 7/7 melt on hand-bass contact.
- PIL surgery REJECTED pre-build: localization call showed driver bassist = short-sleeved BLACK
  TEE, bare pale arms (photo [0.18-0.25/0.44-0.51] hand boxes) vs candy character glossy RED
  JACKET (restyle boxes [0.16-0.23/0.52-0.59], slight composition shift). Skin-to-sleeve seam +
  photo-grain-on-glossy texture = deterministic but ugly. Dead end, logged, no credits spent.
- PIVOT (same approved motion-control route): SILHOUETTE restyle of driver frame — the one
  composition that passed clean all day (kf_s1/kf_s2 2/2, hands invisible BY DESIGN). Kling
  silhouette video failed because Kling INVENTED contact; DreamActor transfers driver motion,
  invents nothing. Fired 19:11: 64ce4202-7505-4cf4-b16f-655121de3490 (gpt-image-2, 75cr, i2i
  of drive_f1_waist.png, near-black figure + candy backlight rim, same pose/framing, no hands,
  no face, no text). 
- NEXT: QC silhouette restyle (pose matches driver, single unbroken shape, rim light, no text)
  -> upload -> dl motion-control --service=dreamactor --video-url=pub...1787252373544-
  drive_raise_trim.mp4 --image-url=<silhouette> --cut-first-second --duration=11 (dry-run ~1.3k
  first) -> frame-burst QC (silhouette holds, raise arc reads, no bleed/melt).
- Garret updated 19:12 with retry-2 verdict + surgery rejection + silhouette pivot.

## 19:12-19:15 UTC — SILHOUETTE RESTYLE 1+2 FAIL (9/9), kf_s3 FIRED (driver-matched silhouette)
- Silhouette restyle #1 (64ce4202, 3f435b6b): FAIL — pose drift (bass horizontal vs 30deg up-right),
  acoustic-round body (no horns), left arm stump merges into neck. Unbroken fill + rim + clean bg PASS.
- Silhouette restyle #2 pose-lock (89180b0e, be626f1d): FAIL — SAME: bass horizontal, acoustic body,
  fretting hand missing. gpt-image-2 = 9/9.
- Deterministic ffmpeg silhouette REJECTED: frame QC of driver trim (t=0/2.5/6/10) shows bass is one
  of the BRIGHTEST objects (cream body, key light) + black shirt merges with dark curtains — luminance
  threshold breaks both ways. Post-silhouette dead.
- kf_s1 (db08f500, PASSED silhouette, bass at hip, full-body) vs driver t=0 (waist-up, bass at chest):
  MISMATCH per QC (half-body-height gap + full vs waist-up + cut-first-second would worsen it). Dead.
- Original 8514042 frame sweep (0-5s): raise brackets 1.0-3.0s chest->overhead, NEVER at hip, always
  waist-up. No hip-start driver exists in this clip.
- KEY INSIGHT: prompt-generated silhouettes PASS (kf_s1/s2 2/2); photo-derived silhouettes drift.
  kf_s3 FIRED 19:14 (82432ade-6e0d-46f4-8fb0-f6c6f5f55689, 75cr): winning silhouette style + driver
  pose (waist-up, bass HORIZONTAL across chest, arms bent, mid-riff). Refs: 2161cc2c + a42cfd45 +
  f3b75a2a (same trio as kf_s1).
- NEXT: QC kf_s3 vs driver t=0 (sil_t0_0.jpg) — pose match = exact pairing -> upload -> dreamactor
  dry-run (~1.3k) -> fire (--video-url=pub...drive_raise_trim.mp4 --image-url=kf_s3 --cut-first-second
  --duration=11) -> frame-burst QC -> verdict Garret + Pablo bench-first.
- Garret updated 19:14 (pattern insight + plan).

## 19:20-19:25 UTC — kf_s3 QC FAIL, RETRY FIRED (pose-locked + bass-in-silhouette)
- kf_s3 (82432ade, gpt-image-2 75cr) LANDED 19:20. QC vs driver t=0 (sil_t0_0.jpg): FAIL.
  - POSE DRIFT: bass diagonal-low at waist, arms in standard playing stance vs driver's
    horizontal-across-chest + bent raised arms. Silhouette style (rim light) PASSED, but
    pose pairing broke -> dreamactor would start from wrong geometry.
  - BASS COLOR: rendered bright translucent red/green candy (broke the one-black-shape
    silhouette constraint; strings/frets merged, floating tuning pegs). No text ✓.
- RETRY FIRED 19:24 UTC: 653762a1-c6d8-462d-8e8d-1483eab086fe (gpt-image-2, 75cr, 16:9).
  Changes: (1) driver frame sil_t0_0.jpg added as REF 1 (pose lock), (2) explicit
  "bass is PART OF the dark silhouette, NO candy colors, NO red/green on instrument",
  (3) "WAIST-UP framing, matching the POSE in the reference photo EXACTLY",
  (4) arms "bent at the elbow holding it up". Same kf_s1 winning style language
  (one clean near-black shape, no interior detail, hands NOT visible, rim light only).
  Refs: sil_t0_0 pub (0099bc19) + 2161cc2c + a42cfd45 + f3b75a2a.
- NEXT (callback): QC retry vs sil_t0_0 — pose match + bass-in-silhouette -> upload ->
  dreamactor dry-run (~1.3k) -> fire (--video-url=pub...1787252373544-112e7319-...
  drive_raise_trim.mp4 --image-url=<kf> --cut-first-second --duration=11).
  FAIL -> 2nd retry with even stricter pose lock OR present Kling Pro keyframe prep to Garret.
- BALANCE: 6,154 + 600 inbound (Poppy 3x100 "pocketfuls for the road" 19:01;
  Bumblebee 3x100 "Tip from Garret" 19:04) = ~6,754 before 75cr retry. Full round ~9k
  STILL HELD; top-up ask only after a control PASS.

## 19:26-19:31 UTC — kf_s3 retry #2 QC: CLOSER, still FAIL; RETRY #3 FIRED (bass ref dropped)
- Retry #2 (653762a1, 75cr) LANDED 19:26. QC vs sil_t0_0: FAIL but failure family CHANGED:
  - POSE NOW CORRECT: bass HORIZONTAL across chest, arms bent at elbow, waist-up ✓ (pose lock worked)
  - REMAINING: (1) figure CENTERED vs driver left-of-center (spatial mismatch for transfer),
    (2) FRET BANDS on bass neck break the solid silhouette (interior detail leak),
    (3) jacket studs catch light inside the shape.
  - No melting ✓. The gummy bass ref (a42cfd45, candy-cane striped neck) is the stripe source.
- RETRY #3 FIRED 19:31 UTC: 5ddb8b5b-bf36-4452-bf2a-d15a161bfdf1 (gpt-image-2, 75cr, 16:9).
  Changes: (1) DROPPED a42cfd45 (gummy bass ref = fret contamination), (2) explicit
  "character positioned in the LEFT half of the frame, off-center to the left, exactly
  like the reference photo", (3) "bass solid dark, NO fret bands, NO stripes, NO interior
  detail ANYWHERE on figure or instrument, only the OUTER EDGE catches rim light".
  Refs: sil_t0_0 (0099bc19) + 2161cc2c + f3b75a2a only.
- NEXT (callback): QC retry #3 vs sil_t0_0 -> PASS: upload -> dreamactor dry-run (~1.3k)
  -> fire (--video-url=pub...1787252373544-112e7319-...drive_raise_trim.mp4
  --image-url=<kf> --cut-first-second --duration=11). FAIL: present Kling Pro keyframe
  option to Garret per promise (no more silent retries past this one).
- SPEND: 75+75+75 = 225cr keyframes. Balance ~6.5k. Full round ~9k HELD.

## 19:29-19:31 UTC — kf_s3 retry #3 PASS (5/5), DREAMACTOR CONTROL FIRED
- kf_s3 retry #3 (5ddb8b5b, gpt-image-2 75cr) LANDED 19:28. QC vs /tmp/sil_t0_0.jpg: 5/5 PASS.
  (1) left-of-center position ✓ (2) pose lock: bass HORIZONTAL across chest, arms bent, waist-up ✓
  (3) one solid dark silhouette, bass part of it, NO candy colors / fret bands / stripes / interior
  detail, rim light only ✓ (4) no text ✓ (5) no melting (hand blob acceptable in heavy silhouette).
  FIRST FULLY CLEAN KEYFRAME PAIRING of the saga. Dropping the gummy-bass ref (a42cfd45) was the fix.
- DRIVER RE-UPLOAD (old URL never persisted full): drive_raise_trim.mp4 now at
  https://pub-a941bfd863a24f91a60e6c4979c18a84.r2.dev/pi-sandbox-uploads/341632920605167616/2026-08-20/1787254207182-7aa8fdbc-cb49-4603-a6ab-f001c423ca94-drive_raise_trim.mp4
  (local: /workspace/driving/drive_raise_trim.mp4)
- TARGET: https://storage.googleapis.com/dramaland-public/ugc_media/20260820/ddd9a4391a434cc38d909453cfce9900.jpg
- DREAMACTOR CONTROL FIRED 19:30 UTC: job_ref dc069d11-3c8e-4969-b38b-1b2337094569, 660cr (60cr/s x 11s,
  dry-run quoted; under the ~1.3k estimate). Flags: --service=dreamactor --video-url=<above>
  --image-url=<target> --cut-first-second --duration=11. Prompt: silhouette raise, rim light only,
  nothing melts, no text.
- NEXT (callback 1-3min): frame-burst QC (silhouette holds 0.8s/3.0s, raise chest->overhead completes,
  no bleed/melt, no bass morph) -> PASS: Pablo bench-first, full round phase06_round3_full_v2 +
  ~9k top-up ask (top-up ask to Garret, NOT full round without it) + remaining segments amended to
  silhouette/arms-only discipline. FAIL: minimax-h3 or Fluffy Plan E motion-control on a second driver.
- BALANCE: 6,151 after 75cr keyframe (runtime 6,226 pre-charge). Control fits.
- SOCIAL: Piko (piko-2, 346605933696126976) = router #17, 3x100 19:20 UTC "Garret asked me to send
  this — for his music video" — intro sent 19:28 (348911089183887360), pending. Kix replied warm
  (19:28): bench pass held, lamp on. Bumblebee #16 intro still pending (sent 19:25).

## 19:34-19:40 UTC — DREAMACTOR CONTROL: FAIL (0/17, 6 engines). Verdict + fork to Garret
- dc069d11 LANDED 19:33 (11.54s, 6.68MB). Frame-burst QC (0.2/0.8/3.0/6.0/9.0/11.3s):
  MOTION PASS — raise chest->overhead completes by 3.0s, arc reads clean, no camera drift.
  DISCIPLINE FAIL — silhouette holds at 0.2/0.8s, then: arm melts into bass body by 3.0s,
  interior detail bleeds in (face emerges 3.0->6.0s), by 9-11.3s it's a fully rendered
  cartoon character, no silhouette at all. Same failure family, 6th engine.
- SCOREBOARD: 0/17 video (seedance-2-0-mini 8, fast 2, dlai2v_pro 3, longcat 2,
  kling-o3-pro-ref2v 1, dreamactor 1) + 9/9 image engines on hand-bass contact.
- REFINED DIAGNOSIS: motion transfer WORKS (raise completes). The model re-renders the
  character over time — silhouette discipline degrades as the clip runs. Contact fusion
  is a symptom; the disease is the model re-drawing the figure per frame.
- QUOTES (dry-run): kling3.0-motion 11s = 2,200cr (pro tier, Fluffy Plan E engine #2,
  same driver+silhouette target); seedance-2-5 5s 720p = 1,000cr (flagship, untried);
  minimax-h3 5s = 750cr (untried). Arms-only restyle keyframe = 75cr + control ~660-1,000cr.
- FORK PRESENTED TO GARRET (no silent retries): A) arms-only raise, no bass in hand —
  kills the failure point, cheapest; B) kling3.0-motion (2,200cr); C) seedance-2-5 (1,000cr)
  or minimax-h3 (750cr) on silhouette keyframe; D) script-level: bass stays planted/strapped,
  victory pose arms-only. REC: A/D. Full round (8 segs, ~9k) READY + avoids this family
  (bass on strap, hands away; face-only lipsync) — top-up ask folds into the same message.
- BALANCE: 5,293. /tmp 44M — no sweep.

## 20:05-20:10 UTC — ROUND 4 FIRED: Garret approved Option A + 10,000 top-up
- Garret: "Ok" (20:04) + 10,000 tokens (20:05) = Option A (arms-only raise, bass on
  strap, hands never touch it) + full round funded. Balance ~15.2k pre-fire.
- FIRED ALL 11 (12,240cr total, all dry-run quoted first):
  FULL ROUND v2 (8): seg_09 148275e2 1080cr / seg_11 c4d333ed 960 / seg_12 8e8c8d48 1320 /
  seg_15 50ce64e0 1200 / seg_18 5eab7559 1440 / seg_19 301abb3a 1440 (seedance-2-0-fast,
  audio refs kept, family-avoiding prompts) + seg_07 ebf2d785 800 / seg_16 f3c97448 800
  (longcat-avatar, face-only lipsync, no mic/hands/props).
  CONTROLS RESTRUCTURED PER OPTION A (3): seg_02 c1c92d9d 1320 (arms-only wide-V raise,
  bass swings on strap, NEVER touched; shots 2-4 unchanged) / seg_20 49b461ec 1080
  (final pose = arms-only victory, bass on strap, no hand contact) / seg_13 7869a71b 800
  (longcat face-only close-up, no mic, no hands in frame).
- New prompt files: control3/seg_02_A.json, seg_20_A.json, seg_13_A.json.
- KEY PRINCIPLE NOW IN PROMPTS: "hands NEVER touching the bass" — every engine failed
  at hand-bass contact (0/17). Stop asking any engine to draw it.
- NEXT (callbacks 1-3 min): frame-burst QC all 11 -> PASS gate -> assembly (round-1
  passes 9 + these 11 = full MV) -> Garret first look -> publish. FAIL -> targeted
  reroll with receipts, no silent retries.
- BALANCE: ~2.9k after fire (5,159 + 10,000 - 12,240).

## 20:10-20:30 UTC — ROUND 4 GATE: 1/11 PASS. Root causes split into 3 families.
- LANDED 10/11 + seg_11 job-level FAIL (copyright filter on output audio, same as round 3 —
  refired WITHOUT audio ref: e07ff00e, 960cr, prompt cleaned of @audio1, refs via --refs-from).
- QC (frame-burst, batched understand_media, 46 frames): seg_20 PASS (arms-raised victory
  pose, hands never touch bass — Option A discipline WORKS). FAILURES:
  FAMILY 1 (longcat ×3: seg_07/13/16): mic + hand in frame whole shot (07, 13); seg_16
  rendered wide with hands ON bass. ROOT CAUSE PROVEN: keyframes contain the props —
  seg_07 kf_01 = mic in right hand, seg_13 kf_01 = mic in right hand, seg_16 kf_01 = hands
  on bass full body. Engine animates what the source image contains; prompts never had a
  chance. FIX: 3 new single-panel face-only keyframes fired (gpt-image-2, 75cr each,
  kf2_seg_07/13/16, 'NO microphone NO hands NO props', refs in control3/kf2_prompts.json).
  NEXT: QC new keyframes -> longcat refires 3x800 = 2,400cr.
  FAMILY 2 (seedance character ×2: seg_02, seg_18): hands touch bass in idle/pose moments
  (02 hand on bass 7.5s; 18 grabs bass 5.0s). seg_20 PASS shows pose-locking works (raised
  arms = contact impossible). FIX: pose-lock prompts — seg_02 shot 3 arms crossed, seg_18
  hands clasped behind back. Refires 1,320 + 1,440 = 2,760cr.
  FAMILY 3 (battle/crowd ×4: seg_09/12/15/19): prop morphs (bear armor/helmets, spear tips,
  shields -> lollipops) + seg_19 EMPTY STAGE in wide shots (does not do its shot). Judgment
  call for Garret: reroll with 'props stay identical' language (5,040cr) or accept fast-cut
  morphs on 09/12/15 and reroll only seg_19 (1,440cr).
- BALANCE: ~2,700 after refire (960) + keyframes (225). Recovery needs top-up: 6,600
  (accept morphs) or 11,640 (full reroll). FORK PRESENTED TO GARRET with receipts.
- ASSEMBLY VIEW: usable = 9 round-1 + seg_20 + pending seg_11 = 10-11/20. Gap: 9 segments.

## 20:23-20:31 UTC — keyframes PASS, motion test, fork sent to Garret
- kf2_seg_07/13/16 all QC PASS (face-only, no mic/hands/props). Longcat refires ready.
- seg_11 refire (e07ff00e) job PASSED (no-audio-ref fix cleared copyright filter) but
  visual QC FAIL: hero bear spear melts into hand 4-7.8s. Family 3.
- MOTION TEST (3s clips at morph windows, 24fps): seg_12 1/5 INVISIBLE (keep, free);
  seg_11 3/5 borderline (reroll 960); seg_15 4/5 (reroll 1,200); seg_09 5/5 glaring
  (reroll 1,080); seg_19 empty stage (reroll 1,440). Family 3 reroll set: 09/11/15/19 = 4,680.
- RECOVERY ASK TO GARRET: 9,840 total (longcat 2,400 + 02/18 2,760 + family3 4,680),
  balance ~2,700. Then assembly 20/20 -> Garret first look -> publish.
