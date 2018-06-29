import numpy as np

#### MISC #####
show_information_loss = False
show_transcripts = False
# word_segment_images_directory = "data/MapStructure/"

#### CNN SETTINGS ####
cnn_model = "cnn/models/ModelTrainedWithNoise.model"
cnn_confidence_weight = 1
topN = 3                                                        # Use the top N character predictions
image_padding = 5

#### N-GRAM SETTINGS ####
bayesian_model = "ngrams/models/bayes_classifier.p"
ngrams_depth = 2
ngrams_likelihood_threshold = 0.0                               # determines the minimal ngrams likelihood for filtering transcripts
ngrams_likelihood_weight = 1
ngrams_weights = [.4,.6]

#### SLIDING WINDOW SETTINGS ####
window_size = 35
step_size = 1
visualize_sliding_window = False
sliding_window_delay = 20                                       # determines the sliding window visualization speed

#### HISTOGRAM SETTINGS ####
peak_estimation_threshold = lambda x: np.average(x) - x.std()
extreme_min_value = lambda x: np.average(x) + x.std()           # minimal confidence score filter
visualize_extrema = True
extrema_file_path = "extrema/"                                  # determines where to store the extrema window images
plot_histogram = False

#### GROUPING SETTINGS ####
min_group_size = 1
max_pixel_distance = 5                                          # determines what is considered a neighbouring window
max_windows = 450                                               # prevents the window grouping algorithm from stalling
min_character_distance = window_size/2                          # determines when a window group is considered overlapping

#### OUTPUT_FILE ####
transcript_output_filename = "Hebrew.txt"