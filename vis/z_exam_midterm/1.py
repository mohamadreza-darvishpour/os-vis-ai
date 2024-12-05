import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the grayscale image
image_path = "pr1/images/p2.jpg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Apply power-law transformation (adjust gamma as needed)
gamma = 2.0  # Adjust gamma to control the degree of transformation
stretched_image = np.power(image / 255.0, gamma) * 255

# Compute the original and transformed histograms
original_histogram, bins = np.histogram(image.ravel(), bins=256, range=(0, 256))
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

# Display the original and transformed images
cv2.imshow("Original Image", image)
cv2.imshow("Transformed Image", stretched_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()