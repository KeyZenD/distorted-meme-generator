#!/bin/bash

echo $1

rm img/*.*
rm tmp/*.*
rm out/*.*

v=$(echo input.*)

if [[ $v =~ "\n" ]]; then
  echo "input files don't multiple"
else
  if [[ ${v##*.} =~ mov|mp4|avi|m4v|mkv|webm ]]; then
    ffmpeg -y -i ${v} -c:v mjpeg -r 15 img/%03d.jpg
    ffmpeg -y -i ${v} -vn audio.wav
  fi
fi

if [[ $1 = "" ]]; then
  a=50
  b=50
elif expr $1 : "^[0-9][0-9]$" >&/dev/null; then
  a=$1
  b=$((100-$a))
fi

ls img/ | while read f
do
  scale=$((a+b))x$((a+b))%\!
  w=$(identify -format '%w' img/${f})
  h=$(identify -format '%h' img/${f})
  convert img/${f} -liquid-rescale ${scale} tmp/lqr_${f}
  convert tmp/lqr_${f} -resize ${w}x${h} out/out_${f}
  deca=$(( $a * 99 ))
  a=$(( deca / 100 ))
done

python -u distort_audio.py

ffmpeg -y -r 15 -i out/out_%03d.jpg -i out_audio.wav -c:v libx264 -crf 22 -c:a aac -ab 160k output.mp4