import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_log_filter(img, sigma):
    """Applies the Laplacian of Gaussian filter to an image.

    Args:
        img: The input image.
        sigma: The standard deviation of the Gaussian kernel.

    Returns:
        The filtered image.
    """

    # Create a Gaussian kernel
    kernel_size = 2 * int(3 * sigma + 0.5) + 1
    gaussian_kernel = cv2.GaussianBlur(np.ones((kernel_size, kernel_size)), (kernel_size, kernel_size), sigma)

    # Calculate the Laplacian of the Gaussian kernel
    laplacian_kernel = cv2.Laplacian(gaussian_kernel, cv2.CV_64F)

    # Apply the filter to the image
    filtered_img = cv2.filter2D(img, -1, laplacian_kernel)

    return filtered_img

def plot_histograms(img1, img2, title1, title2):
    """Plots the histograms of two images and their difference histogram.

    Args:
        img1: The first image.
        img2: The second image.
        title1: The title for the first histogram.
        title2: The title for the second histogram.
    """

    # Calculate histograms
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])

    # Calculate the difference histogram
    hist_diff = np.abs(hist1 - hist2)

    # Plot the histograms
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.plot(hist1)
    plt.title(title1)
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 2)
    plt.plot(hist2)
    plt.title(title2)
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 3)
    plt.plot(hist_diff)
    plt.title('Difference Histogram')
    plt.xlabel('Intensity')
    plt.ylabel('Difference')

    plt.show()

# Load an image
img = cv2.imread('pr1/images/p2.jpg', 0)  # Load as grayscale

# Apply the LoG filter
filtered_img = apply_log_filter(img, .25)  # Adjust sigma as needed

# Plot the histograms
plot_histograms(img, filtered_img, 'Original Image Histogram', 'Filtered Image Histogram')