import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the grayscale image
image_path = "pr1/images/p2.jpg"  # Update path as necessary
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    raise FileNotFoundError(f"Image not found at path: {image_path}")

# Compute the original histogram
original_histogram, bins = np.histogram(image.ravel(), bins=256, range=(0, 256))

# Define a function to stretch pixel values in the range [200, 250] to [1, 255]
def stretch_pixel(value):
    if 200 <= value <= 250:
        return np.clip((value - 200) * 254 // (250 - 200) + 1, 1, 255)
    return 0

# Apply the transformation
vectorized_stretch = np.vectorize(stretch_pixel)
stretched_image = vectorized_stretch(image)

# Compute the transformed histogram
stretched_histogram, bins = np.histogram(stretched_image.ravel(), bins=256, range=(0, 256))

# Plot histograms
plt.figure(figsize=(14, 7))

# Original Histogram
plt.subplot(1, 2, 1)
plt.bar(range(256), original_histogram, color='blue', alpha=0.7)
plt.title("Original Histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")

# Transformed Histogram
plt.subplot(1, 2, 2)
plt.bar(range(256), stretched_histogram, color='green', alpha=0.7)
plt.title("Transformed Histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()
