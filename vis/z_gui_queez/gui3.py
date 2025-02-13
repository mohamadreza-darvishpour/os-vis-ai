import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QDoubleSpinBox, QFileDialog, QMessageBox,
    QSizePolicy, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent


class ImageDropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.setStyleSheet("background-color: lightyellow; border: 2px dashed black;")
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag & Drop Image Here")
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("background-color: green; border: 2px dashed black;")
    
    def dragLeaveEvent(self, event):
        # Reset style if no image is loaded
        if not self.parent().main_window.current_image:
            self.setStyleSheet("background-color: lightyellow; border: 2px dashed black;")
    
    def dropEvent(self, event: QDropEvent):
        url = event.mimeData().urls()[0]
        self.parent().main_window.load_image(url.toLocalFile())


class ImageTab(QWidget):
    def __init__(self, transform_func, params, main_window, parent=None):
        super().__init__(parent)
        self.transform_func = transform_func
        self.main_window = main_window
        self.params = params  # List of parameter dictionaries
        self.init_ui()
    
    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left side: controls
        left_layout = QVBoxLayout()

        # Image drop area
        self.drop_label = ImageDropLabel(self)
        left_layout.addWidget(self.drop_label)

        # Upload button
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.open_file_dialog)
        left_layout.addWidget(self.upload_btn)

        # Parameter widget container (built dynamically)
        self.param_widget_container = QVBoxLayout()
        left_layout.addLayout(self.param_widget_container)
        self.param_widgets = []
        self.load_transform_params()

        # Transform button
        self.transform_btn = QPushButton("Transform")
        self.transform_btn.clicked.connect(self.apply_transform)
        left_layout.addWidget(self.transform_btn)

        # Right side: output displays
        right_layout = QVBoxLayout()
        self.original_display = QLabel()
        self.original_display.setAlignment(Qt.AlignCenter)
        self.original_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.transformed_display = QLabel()
        self.transformed_display.setAlignment(Qt.AlignCenter)
        self.transformed_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addWidget(self.original_display)
        right_layout.addWidget(self.transformed_display)

        main_layout.addLayout(left_layout, 40)
        main_layout.addLayout(right_layout, 60)
        self.setLayout(main_layout)
    
    def load_transform_params(self):
        """
        For each parameter in self.params (a list of dicts), create a label and a spin box.
        Example dict: {'name': 'Angle', 'min': 0, 'max': 360, 'default': 0, 'step': 1}
        """
        for param in self.params:
            hbox = QHBoxLayout()
            label = QLabel(param['name'])
            # For simplicity we use QSpinBox (if needed, you could check for float values and use QDoubleSpinBox)
            spin = QSpinBox()
            spin.setRange(param['min'], param['max'])
            spin.setValue(param.get('default', param['min']))
            if 'step' in param:
                spin.setSingleStep(param['step'])
            self.param_widgets.append(spin)
            hbox.addWidget(label)
            hbox.addWidget(spin)
            self.param_widget_container.addLayout(hbox)
    
    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            self.main_window.load_image(path)
    
    def update_original_display(self, img):
        self.show_image(img, self.original_display)
    
    def show_image(self, img, label):
        if img is not None:
            # Convert image to RGB for display
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img_rgb.shape
            bytes_per_line = ch * w
            q_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def apply_transform(self):
        if self.main_window.current_image is not None:
            try:
                # Get parameters from all spin boxes
                params = [widget.value() for widget in self.param_widgets]
                transformed = self.transform_func(self.main_window.current_image.copy(), *params)
                self.show_image(transformed, self.transformed_display)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Transformation error: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "Please load an image first")


class MainWindow(QMainWindow):
    image_loaded = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.current_image = None
        self.init_ui()
        self.setWindowTitle("Image Processor")
    
    def init_ui(self):
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width() // 2, int(screen.height() * 0.9))
        self.tabs = QTabWidget()

        # List of transforms: each is a tuple (name, function, parameter list)
        transforms = [
            ("Crop Half", self.crop_half, []),
            ("Rotate", self.rotate_image, [{'name': 'Angle', 'min': 0, 'max': 360}]),
            ("Resize", self.resize_image, [{'name': 'Percentage', 'min': 1, 'max': 200}]),
            ("Sobel Filter", self.sobel_filter, [{'name': 'Kernel Size', 'min': 1, 'max': 7, 'default': 3, 'step': 2}]),
            # Chapter 9: Morphological Operations
            ("Dilation", self.dilation, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3},
                                          {'name': 'Iterations', 'min': 1, 'max': 10, 'default': 1}]),
            ("Erosion", self.erosion, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3},
                                        {'name': 'Iterations', 'min': 1, 'max': 10, 'default': 1}]),
            ("Grayscale Dilation", self.grayscale_dilation, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3},
                                                              {'name': 'Iterations', 'min': 1, 'max': 10, 'default': 1}]),
            ("Grayscale Erosion", self.grayscale_erosion, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3},
                                                            {'name': 'Iterations', 'min': 1, 'max': 10, 'default': 1}]),
            ("Opening", self.opening, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3}]),
            ("Closing", self.closing, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3}]),
            ("Hit or Miss", self.hit_or_miss_transformation, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3}]),
            # Chapter 8: Segmentation
            ("Histogram Segmentation", self.histogram_based_segmentation, []),
            ("Otsu Segmentation", self.otsu_threshholding_segmentation, []),
            ("Renyi Entropy Segmentation", self.renyi_entropy_segmentation, []),
            ("Local Adaptive Threshold", self.local_adoptive_threshhold, [
                {'name': 'Block Size', 'min': 3, 'max': 51, 'default': 11, 'step': 2},
                {'name': 'C', 'min': -10, 'max': 10, 'default': 2}
            ]),
            ("Watershed Segmentation", self.watershed_segmentation, []),
            ("Watershed Meyer Segmentation", self.watershed_meyer_segmentation, []),
            # Chapter 7: Frequency and Spatial Domain Filters
            ("Ideal Band Pass Filter", self.ideal_band_pass_filter, [
                {'name': 'Low Cut', 'min': 1, 'max': 50, 'default': 5},
                {'name': 'High Cut', 'min': 1, 'max': 100, 'default': 30}
            ]),
            ("Ideal Low Pass Filter", self.ideal_low_pass_filter, [{'name': 'Cutoff', 'min': 1, 'max': 100, 'default': 30}]),
            ("Ideal High Pass Filter", self.ideal_high_pass_filter, [{'name': 'Cutoff', 'min': 1, 'max': 100, 'default': 30}]),
            ("Gaussian High Pass Filter", self.gaussian_high_pass_filter, [{'name': 'Cutoff', 'min': 1, 'max': 100, 'default': 30}]),
            ("Gaussian Low Pass Filter", self.gaussian_low_pass_filter, [{'name': 'Cutoff', 'min': 1, 'max': 100, 'default': 30}]),
            ("Butterworth High Pass Filter", self.butterworth_high_pass_filter, [
                {'name': 'Cutoff', 'min': 1, 'max': 100, 'default': 30},
                {'name': 'Order', 'min': 1, 'max': 10, 'default': 2}
            ]),
            ("Butterworth Low Pass Filter", self.butterworth_low_pass_filter, [
                {'name': 'Cutoff', 'min': 1, 'max': 100, 'default': 30},
                {'name': 'Order', 'min': 1, 'max': 10, 'default': 2}
            ]),
            # Chapter 6: Affine Transformations
            ("Translation", self.translation, [
                {'name': 'Shift X', 'min': -100, 'max': 100, 'default': 10},
                {'name': 'Shift Y', 'min': -100, 'max': 100, 'default': 10}
            ]),
            ("Scaling", self.scaling, [{'name': 'Scale Factor', 'min': 1, 'max': 300, 'default': 100}]),
            # Chapter 5: Image Enhancement
            ("Log Transform", self.power_log_transform, []),
            ("Gamma Correction", self.power_law_transform, [{'name': 'Gamma', 'min': 1, 'max': 50, 'default': 10}]),
            ("CLAHE", self.CLAHE, [
                {'name': 'Clip Limit', 'min': 1, 'max': 10, 'default': 2},
                {'name': 'Tile Grid Size', 'min': 1, 'max': 16, 'default': 8}
            ]),
            ("Contrast Stretching", self.contrast_stretching, []),
            ("Sigmoid Correction", self.sigmoid_correction, [
                {'name': 'Gain', 'min': 1, 'max': 10, 'default': 5},
                {'name': 'Cutoff', 'min': 0, 'max': 255, 'default': 128}
            ]),
            ("Local Contrast Normalization", self.local_contrast_normalization, [
                {'name': 'Kernel Size', 'min': 3, 'max': 31, 'default': 15, 'step': 2}
            ]),
            # Chapter 4: Spatial Filters (using convolution)
            ("Mean Filter", self.mean_filter, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3}]),
            ("Gaussian Filter", self.gaussian_filter, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3}]),
            ("Median Filter", self.median_filter, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3}]),
            ("Max Filter", self.max_filter, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3}]),
            ("Min Filter", self.min_filter, [{'name': 'Kernel Size', 'min': 1, 'max': 15, 'default': 3}]),
            ("Prewitt Filter", self.prewitt_filter, []),
            ("Canny Filter", self.canny_filter, [
                {'name': 'Threshold1', 'min': 0, 'max': 255, 'default': 50},
                {'name': 'Threshold2', 'min': 0, 'max': 255, 'default': 150}
            ]),
            ("Laplacian Filter", self.laplacian_filter, [{'name': 'Kernel Size', 'min': 1, 'max': 7, 'default': 3}]),
            ("Laplacian of Gaussian Filter", self.laplacian_of_gaussian_filter, [{'name': 'Kernel Size', 'min': 1, 'max': 7, 'default': 3}]),
            ("Frangi Filter", self.frangi_filter, [])
        ]

        # Create a tab for each transform
        for name, func, params in transforms:
            tab = ImageTab(func, params, self)
            self.image_loaded.connect(tab.update_original_display)
            self.tabs.addTab(tab, name)
        
        self.setCentralWidget(self.tabs)
    
    def load_image(self, path):
        try:
            self.current_image = cv2.imread(path)
            if self.current_image is not None:
                self.image_loaded.emit(self.current_image)
                # Update drop label style on all tabs to indicate image loaded
                for i in range(self.tabs.count()):
                    tab = self.tabs.widget(i)
                    if isinstance(tab, ImageTab):
                        tab.drop_label.setStyleSheet("background-color: green; border: 2px dashed black;")
            else:
                raise ValueError("Invalid image file")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")
    
    # --- Basic Spatial Transformations ---
    def crop_half(self, img):
        return img[:, :img.shape[1] // 2]
    
    def rotate_image(self, img, angle):
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
        return cv2.warpAffine(img, M, (w, h))
    
    def resize_image(self, img, percent):
        width = int(img.shape[1] * percent / 100)
        height = int(img.shape[0] * percent / 100)
        return cv2.resize(img, (width, height))
    
    def sobel_filter(self, img, ksize):
        ksize = max(1, min(7, ksize))
        ksize = ksize if ksize % 2 == 1 else ksize + 1
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        abs_sobelx = cv2.convertScaleAbs(sobelx)
        abs_sobely = cv2.convertScaleAbs(sobely)
        combined = cv2.addWeighted(abs_sobelx, 0.5, abs_sobely, 0.5, 0)
        return cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)
    
    # --- Chapter 9: Morphological Operations ---
    def dilation(self, img, kernel_size=3, iterations=1):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(img, kernel, iterations=iterations)
    
    def erosion(self, img, kernel_size=3, iterations=1):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.erode(img, kernel, iterations=iterations)
    
    def grayscale_dilation(self, img, kernel_size=3, iterations=1):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dilated = cv2.dilate(gray, kernel, iterations=iterations)
        return cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
    
    def grayscale_erosion(self, img, kernel_size=3, iterations=1):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        eroded = cv2.erode(gray, kernel, iterations=iterations)
        return cv2.cvtColor(eroded, cv2.COLOR_GRAY2BGR)
    
    def opening(self, img, kernel_size=3):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    
    def closing(self, img, kernel_size=3):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    
    def hit_or_miss_transformation(self, img, kernel_size=3):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        kernel = np.array([[0, 1, 0],
                           [1, -1, 1],
                           [0, 1, 0]], dtype=np.int8)
        hitmiss = cv2.morphologyEx(binary, cv2.MORPH_HITMISS, kernel)
        return cv2.cvtColor(hitmiss, cv2.COLOR_GRAY2BGR)
    
    # --- Chapter 8: Segmentation ---
    def histogram_based_segmentation(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, seg = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.cvtColor(seg, cv2.COLOR_GRAY2BGR)
    
    def otsu_threshholding_segmentation(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, seg = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.cvtColor(seg, cv2.COLOR_GRAY2BGR)
    
    def renyi_entropy_segmentation(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, seg = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.cvtColor(seg, cv2.COLOR_GRAY2BGR)
    
    def local_adoptive_threshhold(self, img, block_size=11, C=2):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if block_size % 2 == 0:
            block_size += 1
        seg = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, block_size, C)
        return cv2.cvtColor(seg, cv2.COLOR_GRAY2BGR)
    
    def watershed_segmentation(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        opening_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        sure_bg = cv2.dilate(opening_img, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening_img, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(img, markers)
        img[markers == -1] = [255, 0, 0]
        return img
    
    def watershed_meyer_segmentation(self, img):
        return self.watershed_segmentation(img)
    
    # --- Chapter 7: Frequency and Spatial Domain Filters ---
    def ideal_low_pass_filter(self, img, cutoff=30):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dft = np.fft.fft2(gray)
        dft_shift = np.fft.fftshift(dft)
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.zeros((rows, cols), np.uint8)
        Y, X = np.ogrid[:rows, :cols]
        mask_area = (X - ccol) ** 2 + (Y - crow) ** 2 <= cutoff * cutoff
        mask[mask_area] = 1
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        img_back = np.uint8(np.clip(img_back, 0, 255))
        return cv2.cvtColor(img_back, cv2.COLOR_GRAY2BGR)
    
    def ideal_high_pass_filter(self, img, cutoff=30):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dft = np.fft.fft2(gray)
        dft_shift = np.fft.fftshift(dft)
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.ones((rows, cols), np.uint8)
        Y, X = np.ogrid[:rows, :cols]
        mask_area = (X - ccol) ** 2 + (Y - crow) ** 2 <= cutoff * cutoff
        mask[mask_area] = 0
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        img_back = np.uint8(np.clip(img_back, 0, 255))
        return cv2.cvtColor(img_back, cv2.COLOR_GRAY2BGR)
    
    def ideal_band_pass_filter(self, img, low_cut=5, high_cut=30):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dft = np.fft.fft2(gray)
        dft_shift = np.fft.fftshift(dft)
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.zeros((rows, cols), np.uint8)
        Y, X = np.ogrid[:rows, :cols]
        mask_area = (((X - ccol) ** 2 + (Y - crow) ** 2) >= low_cut ** 2) & \
                    (((X - ccol) ** 2 + (Y - crow) ** 2) <= high_cut ** 2)
        mask[mask_area] = 1
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        img_back = np.uint8(np.clip(img_back, 0, 255))
        return cv2.cvtColor(img_back, cv2.COLOR_GRAY2BGR)
    
    def gaussian_low_pass_filter(self, img, cutoff=30):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dft = np.fft.fft2(gray)
        dft_shift = np.fft.fftshift(dft)
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        X, Y = np.meshgrid(np.arange(cols), np.arange(rows))
        distance = np.sqrt((X - ccol) ** 2 + (Y - crow) ** 2)
        mask = np.exp(-(distance ** 2) / (2 * (cutoff ** 2)))
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        img_back = np.uint8(np.clip(img_back, 0, 255))
        return cv2.cvtColor(img_back, cv2.COLOR_GRAY2BGR)
    
    def gaussian_high_pass_filter(self, img, cutoff=30):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dft = np.fft.fft2(gray)
        dft_shift = np.fft.fftshift(dft)
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        X, Y = np.meshgrid(np.arange(cols), np.arange(rows))
        distance = np.sqrt((X - ccol) ** 2 + (Y - crow) ** 2)
        mask = 1 - np.exp(-(distance ** 2) / (2 * (cutoff ** 2)))
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        img_back = np.uint8(np.clip(img_back, 0, 255))
        return cv2.cvtColor(img_back, cv2.COLOR_GRAY2BGR)
    
    def butterworth_low_pass_filter(self, img, cutoff=30, order=2):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dft = np.fft.fft2(gray)
        dft_shift = np.fft.fftshift(dft)
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        X, Y = np.meshgrid(np.arange(cols), np.arange(rows))
        distance = np.sqrt((X - ccol) ** 2 + (Y - crow) ** 2)
        mask = 1 / (1 + (distance / cutoff) ** (2 * order))
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        img_back = np.uint8(np.clip(img_back, 0, 255))
        return cv2.cvtColor(img_back, cv2.COLOR_GRAY2BGR)
    
    def butterworth_high_pass_filter(self, img, cutoff=30, order=2):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dft = np.fft.fft2(gray)
        dft_shift = np.fft.fftshift(dft)
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        X, Y = np.meshgrid(np.arange(cols), np.arange(rows))
        distance = np.sqrt((X - ccol) ** 2 + (Y - crow) ** 2)
        mask = 1 / (1 + (cutoff / (distance + 1e-5)) ** (2 * order))
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        img_back = np.uint8(np.clip(img_back, 0, 255))
        return cv2.cvtColor(img_back, cv2.COLOR_GRAY2BGR)
    
    # --- Chapter 6: Affine Transformations ---
    def translation(self, img, shift_x=10, shift_y=10):
        rows, cols = img.shape[:2]
        M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        return cv2.warpAffine(img, M, (cols, rows))
    
    def scaling(self, img, scale_factor=1.0):
        # Here we assume 'scale_factor' is given as a percentage (e.g. 100 means 100%)
        width = int(img.shape[1] * scale_factor / 100)
        height = int(img.shape[0] * scale_factor / 100)
        return cv2.resize(img, (width, height))
    
    # --- Chapter 5: Image Enhancement ---
    def power_log_transform(self, img):
        c = 255 / np.log(1 + np.max(img))
        log_image = c * (np.log(img + 1))
        return np.uint8(np.clip(log_image, 0, 255))
    
    def power_law_transform(self, img, gamma=1.0):
        img_normalized = img / 255.0
        gamma_corrected = np.power(img_normalized, gamma)
        return np.uint8(np.clip(gamma_corrected * 255, 0, 255))
    
    def CLAHE(self, img, clipLimit=2.0, tileGridSize=8):
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize, tileGridSize))
        cl = clahe.apply(l)
        merged = cv2.merge((cl, a, b))
        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    
    def contrast_stretching(self, img):
        in_min = np.min(img)
        in_max = np.max(img)
        stretched = (img - in_min) * (255 / (in_max - in_min + 1e-5))
        return np.uint8(np.clip(stretched, 0, 255))
    
    def sigmoid_correction(self, img, gain=5, cutoff=128):
        img = img.astype(np.float32)
        sigmoid = 1 / (1 + np.exp(gain * (cutoff - img) / 255))
        return np.uint8(sigmoid * 255)
    
    def local_contrast_normalization(self, img, kernel_size=15):
        img_float = img.astype(np.float32)
        local_mean = cv2.blur(img_float, (kernel_size, kernel_size))
        local_std = cv2.blur((img_float - local_mean) ** 2, (kernel_size, kernel_size))
        local_std = np.sqrt(local_std)
        normalized = (img_float - local_mean) / (local_std + 1e-5)
        normalized = cv2.normalize(normalized, None, 0, 255, cv2.NORM_MINMAX)
        return np.uint8(normalized)
    
    # --- Chapter 4: Spatial Filters ---
    def mean_filter(self, img, kernel_size=3):
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
        return cv2.filter2D(img, -1, kernel)
    
    def gaussian_filter(self, img, kernel_size=3):
        if kernel_size % 2 == 0:
            kernel_size += 1
        kernel1d = cv2.getGaussianKernel(kernel_size, 0)
        kernel = kernel1d * kernel1d.T
        return cv2.filter2D(img, -1, kernel)
    
    def median_filter(self, img, kernel_size=3):
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.medianBlur(img, kernel_size)
    
    def max_filter(self, img, kernel_size=3):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(img, kernel)
    
    def min_filter(self, img, kernel_size=3):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.erode(img, kernel)
    
    def prewitt_filter(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernelx = np.array([[1, 0, -1],
                            [1, 0, -1],
                            [1, 0, -1]], dtype=np.float32)
        kernely = np.array([[1, 1, 1],
                            [0, 0, 0],
                            [-1, -1, -1]], dtype=np.float32)
        grad_x = cv2.filter2D(gray, cv2.CV_32F, kernelx)
        grad_y = cv2.filter2D(gray, cv2.CV_32F, kernely)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        prewitt = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        return cv2.cvtColor(prewitt, cv2.COLOR_GRAY2BGR)
    
    def canny_filter(self, img, threshold1=50, threshold2=150):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    def laplacian_filter(self, img, kernel_size=3):
        if kernel_size % 2 == 0:
            kernel_size += 1
        laplacian = cv2.Laplacian(img, cv2.CV_64F, ksize=kernel_size)
        laplacian = cv2.convertScaleAbs(laplacian)
        return laplacian
    
    def laplacian_of_gaussian_filter(self, img, kernel_size=3):
        blurred = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
        laplacian = cv2.Laplacian(blurred, cv2.CV_64F, ksize=kernel_size)
        laplacian = cv2.convertScaleAbs(laplacian)
        return laplacian
    
    def frangi_filter(self, img):
        # Placeholder implementation using Sobel filtering
        return self.sobel_filter(img, 3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
