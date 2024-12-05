import cv2
img = cv2.imread('pr1/images/p2.jpg', 0)
import numpy as np
import matplotlib.pyplot as plt

# بارگذاری تصویر

# تعریف هسته لاپلاسیان
kernel = np.array([[0, 1, 0],
                   [1, -4, 1],
                   [0, 1, 0]])

# اعمال کانولوشن
laplacian = cv2.filter2D(img, cv2.CV_64F, kernel)

# تنظیم آستانه
threshold = 50
edges = np.where(np.abs(laplacian) > threshold, 255, 0)
edges = edges.astype(np.uint8)

# نمایش تصاویر
plt.subplot(1, 2, 1), plt.imshow(img, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(1, 2, 2), plt.imshow(edges, cmap='gray')
plt.title('Laplacian 1  Edges'), plt.xticks([]), plt.yticks([])
plt.show()