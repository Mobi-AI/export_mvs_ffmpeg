ffmpegPath="/home/jinxinqi/ffmpeg_sources/export_mvs_ffmpeg"
videoPath="./video"

currentDir=$(pwd)
cd $ffmpegPath
PATH="$HOME/bin:$PATH" make -j4 & make install
cd $currentDir

for idx in $(seq 0 229)
do
	if [ $idx -ge 100 ]
	then
		idx="$idx"
	elif [ $idx -ge 10 ]
	then
		idx="0$idx"
	else
		idx="00$idx"
	fi
	subdir="$videoPath/$idx"
	if [ ! -d $subdir ]; then
		mkdir $subdir
	fi
	cd $subdir
	ffmpeg -i "../$idx.mp4" -vsync 0 -vf codecview=bf+pf+bb -f image2 "%08d.jpg"
	cd $currentDir
done