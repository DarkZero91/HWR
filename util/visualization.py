import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import os
import types
from util.sliding_window import *


def visualize_extrema_windows(extrema, image, character_map, out="extrema/", window_size=50, step_size=1):
    try:
        os.makedirs(out)
    except:
        pass

    for coor in extrema:
        font = cv2.FONT_HERSHEY_SIMPLEX
        label = character_map[coor[0]][coor[1]]
        image_extreme = image.copy()
        image_coor = map_coordinate_to_image_coordinate(coor[0], coor[1],
                                                        window_size=window_size, step_size=step_size)
        filename = out + label + "(" + str(image_coor[1]) + ", " + str(image_coor[0]) + ").png"

        xx = int(image_coor[1] - window_size / 2.0)
        yy = int(image_coor[0] - window_size / 2.0)

        cv2.rectangle(image_extreme, (xx, yy), (xx + window_size, yy + window_size), (0, 0, 255), 1)
        cv2.putText(image_extreme, label, (1, len(image) - 5), font, .5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imwrite(filename, image_extreme)


def draw_plot(matrix, threshold=None, xlabel="x", ylabel="y", zlabel="z", title="Plot", threshold_label=None,
              plot_3d=False):
    if plot_3d:
        _plot_3d(matrix, threshold=threshold, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel, title=title)
    else:
        _plot_2d(matrix, threshold=threshold, xlabel=xlabel, ylabel=ylabel, title=title,
                 threshold_label=threshold_label)


def print_character_confidence(extrema, confidence_map, character_map):
    d = _get_character_confidence(extrema, confidence_map, character_map)
    for key in d.keys():
        print key + "]"
        print "\tavg: " + str(np.average(d[key]))
        print "\tmin: " + str(np.min(d[key]))
        print "\tmax: " + str(np.max(d[key]))
        print "\tcount: " + str(len(d[key])) + " instances"


def print_transcripts(transcripts):
    for transcript in transcripts:
        print transcript["word"] + " => "
        print "\tcnn_confidence_sum:\t" + str(transcript["cnn_confidence_sum"])
        print "\tngrams_likelihood:\t" + str(transcript["ngrams_likelihood"])


def print_information_loss(current_collection, previous_collection, original_collection=None, operation_label=None):
	current_collection_size = _get_collection_size(current_collection)
	previous_collection_size = _get_collection_size(previous_collection)
	loss = 0.0
	
	if previous_collection_size > 0:
		loss = 100.0 - current_collection_size / previous_collection_size * 100.0
	
	if operation_label == None:
		print "Relative information loss: " + str(loss) + "%"
	else:
		print "Relative information loss after " + operation_label + ": " + str(loss) + "%"

	if not type(original_collection) == types.NoneType:
		original_collection_size = _get_collection_size(original_collection)
		loss = 100.0 - current_collection_size / original_collection_size * 100.0
		print "Total information loss: " + str(loss) + "%"


#### HELPER FUNCTIONS ####

def _get_character_confidence(extrema, confidence_map, character_map):
    character_confidence = {}
    for coor in extrema:
        char = character_map[coor[0]][coor[1]]
        confidence = confidence_map[coor[0], coor[1]]
        if char in character_confidence.keys():
            character_confidence[char].append(confidence)
        else:
            character_confidence[char] = [confidence]
    return character_confidence


def _plot_2d(matrix, threshold=None, xlabel="x", ylabel="y", title="Plot", threshold_label=None):
    line_type = ('b-', 'g--', 'm-.', 'c:')
    for i in range(4):
        y = len(matrix) / 4 * i
        plt.plot(matrix[y, :], line_type[i], label="y = " + str(y))

        if threshold != None:
            idx = np.argwhere(np.diff(np.sign(threshold - matrix[y, :])) != 0).reshape(-1) + 0
            plt.plot(idx, np.ones_like(idx) * threshold, "ro")

    if threshold != None:
        t = np.ones((len(matrix[0]),)) * threshold
        if threshold_label == None:
            plt.plot(t, 'r--')
        else:
            plt.plot(t, 'r--', label=threshold_label)

    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc=3)
    plt.show()


def _plot_3d(matrix, threshold=None, xlabel="x", ylabel="y", zlabel="z", title="Plot"):
	padding = 5
	matrix = np.pad(np.transpose(matrix.copy()), padding, 'constant')	
	figure = plt.figure()
	axis = figure.gca(projection='3d')
	
	x = np.arange(padding*-1, len(matrix[0])-padding, 1)
	y = np.arange(padding*-1, len(matrix)-padding, 1)
	x, y = np.meshgrid(x, y)
	
	surface = axis.plot_surface(x, y, matrix, cmap=cm.coolwarm, linewidth=0, antialiased=True)
	figure.colorbar(surface)
	
	if threshold != None:
		threshold_plane = np.ones_like(matrix) * threshold
		axis.plot_surface(x, y, threshold_plane, color="green", alpha=.2, antialiased=True)

	plt.xlabel(ylabel)
	plt.ylabel(xlabel)
	axis.set_zlabel(zlabel)
	plt.title(title)
	plt.show()

def _get_collection_size(collection):
	elements = 0.0
	for i in range(len(collection)):
		if type(collection[i]) in [list, np.ndarray]:
			elements += _get_collection_size(collection[i])
		else:
			return len(collection) * 1.0
	return elements
