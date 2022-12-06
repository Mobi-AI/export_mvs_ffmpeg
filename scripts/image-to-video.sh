dir="/data/zhuz/sr/train/train_sharp_bicubic/X4"

for idx in $(seq 0 229)
do
	if [ $idx -ge 100 ]
	then
		subdir="$idx"
	elif [ $idx -ge 10 ]
	then
		subdir="0$idx"
	else
		subdir="00$idx"
	fi
	#echo "${dir}/${subdir}/%08d.png"
	ffmpeg -f image2 -i "${dir}/${subdir}/%08d.png" -c:v libx264 -flags +cgop -x264opts bframes=0:sliced-threads=0 -crf 0 video/$subdir.mp4

done
