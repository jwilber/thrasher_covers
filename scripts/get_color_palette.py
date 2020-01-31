from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_image(image_path):
    # read in image
    image = cv2.imread(image_path)
    # ensure pixels in correct rgb format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def extract_colors(image_path, number_of_colors, width=200, height=200, show_chart=True):
    """Extract top n colors from a gien image."""
    # read in image
    image = cv2.imread(image_path)
    # ensure pixels in correct rgb format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # resize image
    modified_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    print("modified_image shape:", modified_image.shape)
    plt.imshow(modified_image)
    # reshape image
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)
    # train kmeans on image pixels
    clf = KMeans(n_clusters = number_of_colors)
    # get labels for image
    labels = clf.fit_predict(modified_image)
    # count labels
    counts = Counter(labels)
    # sort to ensure correct color percentage
    counts = dict(sorted(counts.items())) 
    counts = {k: 1. * v / (width * height) for k,v in counts.items()}
    print("counts:", counts)
    center_colors = clf.cluster_centers_
    print("center_colors:", center_colors)
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
    
    return rgb_colors

extract_colors(cover, 4, width=100, height=100, show_chart=True)
