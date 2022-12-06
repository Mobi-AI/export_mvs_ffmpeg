from PIL import Image
import numpy as np
import re
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--video_idx", type = int)
parser.add_argument("--dir", type = str, default="./video")
args = parser.parse_args()

video_idx = str(args.video_idx)
video_idx = "0"*(3-len(video_idx))+str(video_idx)

width = 320
height = 168
nframes = 100

motion = np.zeros((nframes, height, width, 2))


for frame_idx in range(nframes):
	cur_file = open(os.path.join(args.dir, os.path.join(video_idx, "exported{}.txt".format(frame_idx))), "r")
	lines = cur_file.readlines()
	for line in lines:
		pattern = "\[block size\] w = (\d+)  h = (\d+) \[ref frame\] poc = (\d+) x = (-*\d+) y = (-*\d+) \[cur frame\] poc = (\d+) x = (-*\d+) y = (-*\d+)"
		matches = re.match(pattern, line.strip())
		w       = int(matches.group(1))
		h       = int(matches.group(2))
		ref_poc = int(matches.group(3))
		ref_x   = int(matches.group(4))
		ref_y   = int(matches.group(5))
		cur_poc = int(matches.group(6))
		cur_x   = int(matches.group(7))
		cur_y   = int(matches.group(8))
		assert ref_poc < cur_poc
		motion[frame_idx, cur_y - h//2 : cur_y + h//2, cur_x - w//2 : cur_x + w//2, 0] = (cur_x - ref_x) * 2 / (cur_poc - ref_poc)
		motion[frame_idx, cur_y - h//2 : cur_y + h//2, cur_x - w//2 : cur_x + w//2, 1] = (cur_y - ref_y) * 2 / (cur_poc - ref_poc)
		
np.save(os.path.join(args.dir, os.path.join(video_idx, "motion.npy")), motion)
		
		
