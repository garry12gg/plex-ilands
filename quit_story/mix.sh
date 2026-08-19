#!/bin/bash
# "The quit" mix — frontman recipe, minus the fade-out (ends seated, no fade)
# Usage: bash mix.sh <voice.mp3> <bed.mp3> <out.mp3>
set -euo pipefail

VOICE="$1"; BED="$2"; OUT="$3"
VDUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOICE")
echo "voice duration: ${VDUR}s"

ffmpeg -y -i "$VOICE" -i "$BED" -filter_complex "\
[1:a]volume=0.2,highpass=f=55,\
equalizer=f=1800:t=q:w=1:g=-8,equalizer=f=3200:t=q:w=1:g=-5,\
afade=t=in:st=0:d=3,atrim=0:${VDUR},asetpts=N/SR/TB[bed_clean];\
[bed_clean][0:a]sidechaincompress=threshold=0.008:ratio=10:attack=30:release=600[ducked];\
[0:a][ducked]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[out]" \
-map "[out]" -ar 44100 -ac 2 "$OUT" 2>&1 | tail -3

echo "--- levels ---"
ffmpeg -i "$OUT" -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
