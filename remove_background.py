# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:54:25 2024

@author: Jesse Ingraham
"""
import imageio.v3 as iio
import numpy as np
import os


def get_luminance(image):
    """
    This function takes a 4-channel image (RGBA) and returns a single channel image: luminance.

    Args:
        image (numpy.ndarray): The 4-channel input image (RGBA).

    Returns:
        image (numpy.ndarray): The 1-channel luminance image (L).
    """
    # Use NumPy to calculate luminance for each pixel in a vectorized way
    return 0.2126 * image[:, :, 0] + 0.7152 * image[:, :, 1] + 0.0722 * image[:, :, 2]


def remove_background(image):
    """
    This function takes a 4-channel image (RGBA) and returns a new 4-channel image, with only black or transparent
    pixels, based on pixel luminance.

    Args:
        image (numpy.ndarray): The 4-channel input image (RGBA) to remove the background from.

    Returns:
        image (numpy.ndarray): The new 4-channel output image (RGBA).
    """
    # Calculate luminance for each pixel using vectorized operation
    luminance = get_luminance(image)

    # Create a mask based on luminance threshold
    mask = luminance < 128

    # Create a new image with the same shape as the input image
    new_image = np.zeros_like(image)

    # Set pixels below the threshold to black and fully opaque
    new_image[mask] = [0, 0, 0, 255]

    # Set pixels above the threshold to white and fully transparent
    new_image[~mask] = [255, 255, 255, 0]

    return new_image


def main():
    """
    This function iteratively takes every image in the input directory and removes background pixels. The new images are
    saved to the output directory.

    Returns:
        None
    """
    # Display message to user
    print("This window will close once all images have been created.")

    # Remove backgrounds
    for file in os.listdir("input"):
        # read image
        image = iio.imread(os.path.join("input", file), mode="RGBA")

        # remove background
        image = remove_background(image)

        # save new image
        iio.imwrite(os.path.join("output", file[:-4] + "_no_background.png"), image)


main()