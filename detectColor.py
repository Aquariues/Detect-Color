import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches as patches
from matplotlib import gridspec as gridspec

def rgb2hex(r,g,b):
	return "#{:02x}{:02x}{:02x}".format(r,g,b)

def center_square(height, width, squa_range = 2):
	if height <= width :
		p_range = int(height / squa_range)
	else :
		p_range = int(width / squa_range)

	y = int((height / 2) - (p_range / 2))
	x = int((width / 2) - (p_range / 2))
	return y, x, p_range

def resize_templ(templ, p_range):
  p_range = int(p_range)
  resized = cv.resize(templ, (p_range, p_range), interpolation=cv.INTER_AREA)
  return resized

def capture_image(path, frame):
  cv.imwrite(path, frame)

def compare_corrected_color(r, g, b, num):
	
	r_diff, g_diff, b_diff = 0, 0 ,0
	return r_diff, g_diff, b_diff

def detectcolor(url, cvt_color=cv.IMREAD_UNCHANGED):
	# imread stored image as BGR
	img = cv.imread(url, cvt_color)
	
	list_colors_hex = {}
	list_colors_rgb = {}
	y_point, x_point, p_range = center_square(img.shape[0], img.shape[1], squa_range=4)

	# take colors
	for i in range(x_point, x_point + p_range):
		for j in range(y_point, y_point + p_range):
			# image [ y, x ] return color BGR 
			[x,y,z] = img[j, i]
			color_hex = rgb2hex(z,y,x)
			color_rgb = "{} {} {}".format(z, y ,x)
			if (color_hex in list_colors_hex):
				list_colors_hex[color_hex] += 1
				list_colors_rgb[color_rgb] += 1
			else:
				list_colors_hex[color_hex] = 1
				list_colors_rgb[color_rgb] = 1

	# top number highest color
	num_show = 10
	list_colors_hex = sorted(list_colors_hex.items(), key=lambda x:x[1], reverse=True)
	list_colors_hex = dict(list_colors_hex[:num_show])
	list_colors_rgb = sorted(list_colors_rgb.items(), key=lambda x:x[1], reverse=True)
	list_colors_rgb = dict(list_colors_rgb[:num_show])

	gs = gridspec.GridSpec(2, 2)
	plt.figure(figsize=(16,8))

	# _, axs = plt.subplots(2, 1,figsize=(16,8), gridspec_kw={'height_ratios': [2, 2]})

	rect1 = patches.Rectangle((x_point, y_point), p_range, p_range, linewidth=0.5, edgecolor='g', facecolor='none')
	axs1 = plt.subplot(gs[0, 0]) # row 0, col 0
	axs1.set_title('RGB Image')
	axs1.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
	axs1.add_patch(rect1)
	rect2 = patches.Rectangle((x_point, y_point), p_range, p_range, linewidth=0.5, edgecolor='g', facecolor='none')
	axs2 = plt.subplot(gs[0, 1]) # row 0, col 0
	axs2.set_title("Iamge Channel {}".format(cvt_color))
	axs2.imshow(img)
	axs2.add_patch(rect2)
	
	axs3 = plt.subplot(gs[1, :]) # row 0, col 0
	axs3.set_title('Color Histogram')
	axs3.bar(list_colors_rgb.keys(), list_colors_hex.values(), color=list_colors_hex.keys())

	plt.show()