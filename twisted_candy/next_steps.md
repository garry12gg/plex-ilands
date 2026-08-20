# Twisted Candy MV — next steps

Project: full-song MV (196.96s, 20 segments) for Garret's "Twisted Candy"
(/workspace/parent_music/Twisted-Candy.mp3). mv-skill pipeline, hybrid (60% narrative / 40% performance).

## Pipeline state (Aug 20, ~09:50 UTC)

| Phase | Slot | State |
|---|---|---|
| 01 audio analysis | audio_analysis | v2 verified (audio_analysis_v2.json) |
| 02 creative proposal | creative_proposal | v3 verified (creative_proposal.draft.json, 20 segs, seedance-2-0-mini) |
| 03 visual config | visual_config | v1 verified (16:9, 720p, Inside Out 3D CGI style) |
| 04 reference list | reference_list | v1 verified + PROMOTED (reference_list.json, 11 entries, NO ARK — cartoon chars) |
| 05a video prep | — | NEXT |

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

Original sour_worms job (71fd5c78) completed with NO media — re-submitted (cf643c5d), landed fine.

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
