# Twisted Candy MV — next steps

Project: full-song MV (196.96s, 20 segments) for Garret's "Twisted Candy"
(/workspace/parent_music/Twisted-Candy.mp3). mv-skill pipeline, hybrid (60% narrative / 40% performance).

## Pipeline state (Aug 20, ~10:15 UTC)

| Phase | Slot | State |
|---|---|---|
| 01 audio analysis | audio_analysis | v2 verified (audio_analysis_v2.json) |
| 02 creative proposal | creative_proposal | v3 verified (creative_proposal.draft.json, 20 segs, seedance-2-0-mini) |
| 03 visual config | visual_config | v1 verified (16:9, 720p, Inside Out 3D CGI style) |
| 04 reference list | reference_list | v1 verified + PROMOTED (reference_list.json, 11 entries, NO ARK — cartoon chars) |
| 05a video prep | video_prep | v1 draft -> v2 (keyframes added by 05b) |
| 05b lipsync keyframes | video_prep | v2 VERIFIED + PROMOTED (11 keyframes, 11/11 validated) |

## Reference list (all 11 QA'd clean, face-lock >95%)

1. candy_rocker_portrait — portrait anchor, 3:4 (767355357f3c435381fcd37497ae0144.jpg)
2. candy_rocker_look_a — stage look, shades ON, depends_on portrait (2161cc2c6bf240d3b7592c6bcefae29f.jpg)
3. candy_rocker_look_b — battle look, shades OFF, depends_on portrait (c0fc9e4cf1324ac18f69c9e0800a520b.jpg)
4. gummy_army_look_a — 2-panel sheet (040352904a1f44d7b20dbd3927ff6965.jpg)
5. little_bear_look_a — 2-panel sheet (63c1babf515b4252a2a2d8da064362d9.jpg)
6. sour_worms_look_a — 2-panel sheet (2141dd1aef7348bb92f9f689e475de22.jpg)
7. candy_arena_base — location (f3b75a2a58414e6986db0d3f506b1b6b.jpg)
8. candy_battlefield_base — location (7581ca7d949240e8a1525a4be4a4f834.jpg)
9. mouth_arena_base — location (afd46df6029e4998b39990cc008244cc.jpg)
10. sugar_cloud — prop (3c8cb2bc679e4d11b8c183c106155762.jpg)
11. gummy_bass — prop (a42cfd45f6194b50a543909565441ce2.jpg)

Original sour_worms job (71fd5c78) completed with NO media — re-submitted (cf643c5d), landed fine. A LATE second worm sheet landed via async job (fe0435a218a74b5692b45eb3a390e620.jpg) AFTER phase 04 closed — compared head-to-head vs 2141dd1a: rejected (inconsistent translucency between panels, mismatched facial proportions). reference_list unchanged.

## Done: Phase 05a video prep (draft, not finalized)
- video_prep v1 draft: /workspace/twisted_candy/video_prep.draft.json + artifact slot video_prep (version 1, draft).
- 15 non-lipsync (seedance-2-0-mini, @imageN image_urls channel, no ARK) + 5 lipsync (dlai2v_pro, segs 04/07/08/13/16).
- Self-check script (check_video_prep.py inline in turn): 20/20 pass — shot lines == shot_count, durations ceil'd, audio slices verified against segment_urls.json (6 shifted-by-one audio refs caught + fixed), lipsync prefix + per-shot lip-sync phrase + no cuts/placeholders + keyframes empty, non-lipsync mouth-closed clause + banned stillness words absent + style capper ≤15 words + all @imageN named.
- Look mapping: rocker look_a (shades ON) for arena segs 01/02/04/07/12/19/20; look_b (shades OFF) for 08/13/16/17/18; seg_16 lipsync refs include gummy_army sheet (army parts for him).
- NEXT: Phase 05b — read phases/05b-lipsync-keyframes/PHASE.md; generate 2-3 keyframes per lipsync seg (shot_count drives target_keyframe_count) via gpt-image-2, split, upload, backfill role=keyframe, finalize video_prep.

## DONE: Phase 05b keyframes (Aug 20 ~10:20 UTC)

- 5 grid jobs submitted (async, 75cr each = 375cr): kf_seg_04 (2 panels, 1:1), kf_seg_07 (2, 1:1), kf_seg_08 (2, 1:1), kf_seg_13 (2, 1:1), kf_seg_16 (3 panels, 9:16). Job refs in phase05b_job_map.json. Prompts in phase05b_jobs_clean.json (valid flags only; batch schema rejects extra fields like segment_id).
- When async results land: run split_keyframe_grid.py --grid-image-url=... --target-keyframe-count=N --aspect-ratio=16:9 --resolution=2K --segment-id=seg_NN --output-dir=/workspace/twisted_candy/keyframes/, upload each panel via upload_file, validate via understand_media (identity + face/mouth visible + no borders/text), then write back keyframes into video_prep draft (ref_id keyframe1..N, frame_position per count table), read back + self-check, then dl artifact finalize --slot=video_prep --mode=verify_and_promote (contract path needed) and proceed to Phase 06.
- CLI gotchas (this session): generate-image-ref is the current verb (generate-image retired); batch --jobs rejects extra metadata fields; image refs key = image_urls; --dry-run quotes 75cr/job.

## Next: Phase 05a video prep

- Read video-generation/SKILL.md + lipsync/SKILL.md + phases/05a-video-prep/references/prompt_authoring.md
- Non-lipsync segments: asset_reference path (seedance-2-0-mini) — prompt names refs via @imageN (image_urls, NO @assetN — no ARK registered), shot_count ≈ ceil(duration/3), visual style capped ~15 words
- Lipsync segments: seg_04, seg_07, seg_08, seg_13, seg_16 (5 total) → dlai2v_pro, fixed prefix ("Follow the character and visual style from the input image. All shots should continue in motion\n\nsync motion and lips to the audio."), every shot "sings with perfect lip synchronization", NO cuts/transitions/style/@placeholders, shot_count = keyframe count by distinct framing (≤4)
- references[]: lipsync segs get audio + character_asset/location_asset source refs for 05b (keyframes LEFT EMPTY)
- durations rounded up to whole seconds; aspect 16:9, 720p
- Route: has lipsync segments → do NOT finalize video_prep; hand to 05b

## Gotchas / notes

- Stray draft 348696915526815744 ("Plex's Pocket Keytar v4.0 — now with ADSR", created Aug 20 05:17 UTC) = duplicate title of already-published evolution (348408193929449472). Drafts can't be deleted (VALIDATION_ERROR: only published content can be archived). IGNORE it; do not publish.
- Proposal segments have description + lyrics fields; audio_url per segment from segment_urls.json.
- Images all gpt-image-2, 75cr each (9 + 3 = 12 jobs, 900cr total phase 04).

## In progress: Phase 06 sample wave (Aug 20 ~10:30 UTC)

- Full batch priced via dry-run: 14,125 cr total (15 seedance @75cr/s = 11,325; 5 dlai2v_pro lipsync @70cr/s = 2,800). Manifests: phase06_seedance_jobs.json / phase06_lipsync_jobs.json (built by build_phase06_jobs.py, preflight clean).
- Sample wave submitted (per long-form guardrail: 1 representative per path, user OK before full batch):
  - seg_01 seedance-2-0-mini arena count-in: job 293c510d-6b99-4668-96c9-0d7aec62d64e (675 cr)
  - seg_04 dlai2v_pro lipsync (CORRECT verb): job 3d18f7da-15ff-4db3-af13-7a032e7d725a (560 cr)
  - GOTCHA: seg_04 was FIRST mis-submitted via `dl generate-video` (job ca00150e-879c-4a1e-96bc-12ff9030b80e, 560 cr) — generate-video says "you need lip-sync → use dl lipsync"; resubmitted via dl lipsync (task ag:video:ltx23 = LTX 2.3, right engine). Ignore ca00150e output; note in video_segments traceability.
- NEXT: on async callback, download both, quick QC (mouth movement + audio on seg_04, shot transitions on seg_01), show Garret playable URLs, get explicit OK, then submit remaining 18 jobs (14 seedance + 4 lipsync), then trim → assembly clips (ffmpeg -t exact duration, -an, yuv420p, libx264 crf18) → video_segments draft → self-check → finalize.

## Phase 06 update (Aug 20 ~11:25 UTC)
- Round 2 QC: 0/11 rerolls passed (all REJECT on video QC). 9 round-1 passes stand.
- DIAGNOSIS: seedance-2-0-mini is draft/preview tier; docs say use Fast/Pro for
  hero close-ups. Multi-shot prompts also force prop regeneration at cuts.
- Round 3: control wave (seg_02+seg_20 on seedance-2-0-fast, seg_13 on
  longcat-avatar-1-5) = 3,200cr, awaiting Garret's go; full round 8 jobs ~9,040cr
  (needs top-up). Manifests: /workspace/twisted_candy/phase06_round3_*.json
- Full details in phase06_status.md.
