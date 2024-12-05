import cv2
import numpy as np
from matplotlib import pyplot as plt

def apply_sobel_filter(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Image not found at specified path.")

    # Define Sobel kernels
    sobel_kernel_x = np.array([[1, 0, -1],
                               [2, 0, -2],
                               [1, 0, -1]], dtype=np.float32)

    sobel_kernel_y = np.array([[1, 2, 1],
                               [0, 0, 0],
                               [-1, -2, -1]], dtype=np.float32)

    # Apply convolution with Sobel kernels
    gradient_x = cv2.filter2D(image, -1, sobel_kernel_x)
    gradient_y = cv2.filter2D(image, -1, sobel_kernel_y)

    # Compute the magnitude of gradients
    sobel_magnitude = cv2.magnitude(gradient_x.astype(np.float32), gradient_y.astype(np.float32))

    # Display the results
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.title('Original Image')
    plt.imshow(image, cmap='gray')

    plt.subplot(1, 3, 2)
    plt.title('Sobel Filter X')
    plt.imshow(gradient_x, cmap='gray')

    plt.subplot(1, 3, 3)
    plt.title('Sobel Filter Y')
    plt.imshow(gradient_y, cmap='gray')

    plt.figure()
    plt.title('Sobel Edge Magnitude')
    plt.imshow(sobel_magnitude, cmap='gray')
    plt.show()

# Example usage
apply_sobel_filter("./pr2/images/p1.png")
