from PIL import Image
import numpy as np
import re
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--video_idx", type = int)
parser.add_argument("--dir", type = str, default="./video")
parser.add_argument("--width", type = int, default=320)
parser.add_argument("--height", type = int, default=180)
args = parser.parse_args()

video_idx = str(args.video_idx)
video_idx = "0"*(3-len(video_idx))+str(video_idx)

width = args.width
height = args.height
nframes = 100

motion = np.zeros((nframes, height, width, 2))

error = False
for frame_idx in range(nframes):
	if error:
		break
	cur_file = open(os.path.join(args.dir, os.path.join(video_idx, "exported{}.txt".format(frame_idx))), "r")
	lines = cur_file.readlines()
	first_line = True
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
		if first_line:
			cur_poc_first = cur_poc
			first_line = False
		if ref_poc >= cur_poc or cur_poc_first != cur_poc:
			print("Error with video {}".format(video_idx))
			motion[:] = 0
			error = True
			break
		motion[frame_idx, max(0, cur_y - h//2) : min(cur_y + h//2, height), max(0, cur_x - w//2) : min(cur_x + w//2, width), 0] = (cur_x - ref_x) * 2 / (cur_poc - ref_poc)
		motion[frame_idx, max(0, cur_y - h//2) : min(cur_y + h//2, height), max(0, cur_x - w//2) : min(cur_x + w//2, width), 1] = (cur_y - ref_y) * 2 / (cur_poc - ref_poc)
		
np.save(os.path.join(args.dir, os.path.join(video_idx, "motion.npy")), motion)