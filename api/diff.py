import cv2
import cv2.cv as cv
import numpy as np
import os
import sys
import api
'''
	Finds the difference between the two images and retruns the output.

	@source_img_path: The image that is to be used as the reference. This is in .png format.
	@subject_img_path: The image that is being tested for differences with respect to source image. This is in .png format.

	Returns a tupple of differece image, contours overlapped on source, contours overlapped on subject.
'''


def compare(source_img_path, subject_img_path):
	source_img = cv2.imread(source_img_path, 1)
	subject_img = cv2.imread(subject_img_path, 1)

	# Compensate for different sizes of source and subject images.
	source_height, source_width, source_depth = source_img.shape
	subject_height, subject_width, subject_depth = subject_img.shape
	if source_height < subject_height:
		subject_img = subject_img[0:source_height, 0:subject_width]
	else:
		source_img = source_img[0:subject_height, 0:source_width]

	if source_width < subject_width:
		subject_img = subject_img[0:subject_height, 0:source_width]
	else:
		source_img = source_img[0:source_height, 0:subject_width]

	diff_img = source_img - subject_img
	imgray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
	contours, hierarchy = cv2.findContours(
	    imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(source_img, contours, -1, (0, 255, 0), 1)
	cv2.drawContours(subject_img, contours, -1, (255, 0, 0), 1)
	return (diff_img, source_img, subject_img)

'''
	Saves images on to disk.
	@img: The image object to save.
	@save_as: The path of the saved image.
'''


def write(img, save_as):
	d = os.path.dirname(save_as)
	if not os.path.exists(d):
		os.makedirs(d)
	cv2.imwrite(save_as, img)

'''
	Prints the usage of the module.
'''
def print_usage():
	print "Usage: python diff.py <source-file-path> <subject-file-path> <output-directory>"


'''
	The condition is true only when the program is run as a script.
'''
if __name__=="__main__":
	# Check if we have sufficient number of arguments.
	if len(sys.argv) < 3:
		print "Error: Argument list is less than expected."
		print_usage()
		exit()

	source = sys.argv[1];
	subject = sys.argv[2];
	output_path = sys.argv[3];

	diff_img, source_img, subject_img = compare(source, subject)
	cv2.imshow('Difference',diff_img)
	cv2.imshow('Contours On Source',source_img)
	cv2.imshow('Contours On Subject',subject_img)
	k = cv2.waitKey(0)
	if k == 27:         # wait for ESC key to exit
		cv2.destroyAllWindows()
	elif k == ord('s'): # wait for 's' key to save and exit
		write(diff_img, api.correct_path(output_path) + "diff.png")
		write(diff_img, api.correct_path(output_path) + "contours_on_source.png")
		write(diff_img, api.correct_path(output_path) + "contours_on_subject.png")
		cv2.destroyAllWindows()
