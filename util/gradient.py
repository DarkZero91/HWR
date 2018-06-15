import numpy as np
from scipy.signal import savgol_filter

def get_local_extrema(matrix, min_value=0, peak_estimation_threshold=0.001):
	gradient = _compute_gradient(matrix)
	extrema = []

	max_y, max_x = np.where(gradient <= peak_estimation_threshold)
	for i in range(len(max_y)):
		if(matrix[max_y[i], max_x[i]] >= min_value):
			extrema.append((max_y[i], max_x[i]))

	return extrema

def filter_extrema(extrema, character_map):
	filtered = list(extrema)
	for coor in extrema:
		# filter noise extrema
		if character_map[coor[0]][coor[1]] == "Noise":
			filtered.remove(coor)
	return filtered

def smooth(matrix, rounds=5):
	smoothed = matrix.copy()
	for _ in range(rounds):
		smoothed = savgol_filter(smoothed,5,2)
		smoothed = savgol_filter(smoothed,5,2, axis=0)
	return smoothed

#### HELPER FUNCTIONS ####

def _compute_gradient(matrix):
	nabla = np.gradient(matrix)
	dy = np.abs(nabla[0])
	dx = np.abs(nabla[1])
	return dx + dy