# USAGE
# python test_network.py --model santa_not_santa.model --image images/examples/santa_01.png

# import the necessary packages

from keras.preprocessing.image import img_to_array
from keras.models import load_model
from util.character_map import char_map
import numpy as np
import argparse
import cv2

total = 0
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to trained model model")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
orig = image.copy()

# pre-process the image for classification
image = cv2.resize(image, (28, 28))
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model(args["model"])

# classify the input image
prediction = list(model.predict(image)[0])
results = {}

for i in range(len(prediction)):
    label = sorted(char_map.keys())[i]
    total += prediction[i]

    if prediction[i] in results.keys():
        results[prediction[i]].append(label)
    else:
        results[prediction[i]] = [label]

for result in sorted(results.items(), reverse=True):
    print result

argmax = np.argmax(prediction)

# build the label
label = char_map.keys()[char_map.values().index(argmax)]
probability = prediction[argmax]
print "{}: {:.2f}p".format(label, probability * 100)
print "Total: {:.2f}p".format(total*100)