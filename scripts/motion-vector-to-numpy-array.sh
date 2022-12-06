ffmpegPath="/home/jinxinqi/ffmpeg_sources/export_mvs_ffmpeg"
videoPath="./video"

cp "$ffmpegPath/main.py" .

for idx in $(seq 0 229)
do
    python main.py --video_idx $idx --dir $videoPath
done

rm main.py