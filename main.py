from PIL import Image
import numpy as np
import re

img_index = 24
print_ranges=[100*i for i in range(20)]

cur_img = np.array(Image.open("./video/"+"0"*(8-len(str(img_index+1)))+str(img_index+1)+".jpg"))
cur_file = open("./video/exported{}".format(img_index*2), "r")
lines = cur_file.readlines()

for i, line in enumerate(lines):
	if i in ranges:
		pattern = "\[block size\] w = (\d+)  h = (\d+) \[ref frame\] poc = (\d+) x = (\d+) y = (\d+) \[cur frame\] poc = (\d+) x = (\d+) y = (\d+)"
		matches = re.match(pattern, line.strip())
		w       = int(matches.group(1))
		h       = int(matches.group(2))
		ref_poc = int(matches.group(3))
		ref_x   = int(matches.group(4))
		ref_y   = int(matches.group(5))
		cur_poc = int(matches.group(6))
		cur_x   = int(matches.group(7))
		cur_y   = int(matches.group(8))
		cur_patch = cur_img[cur_y-h//2:cur_y+h//2, cur_x-w//2:cur_x+w//2, :]
		ref_patch = np.array(Image.open("./video/"+"0"*(8-len(str(ref_poc//2+1)))+str(ref_poc//2+1)+".jpg"))[ref_y-h//2:ref_y+h//2, ref_x-w//2:ref_x+w//2, :]
		Image.fromarray(cur_patch).show()
		Image.fromarray(ref_patch).show()
		input("Print any key to go on\n")
