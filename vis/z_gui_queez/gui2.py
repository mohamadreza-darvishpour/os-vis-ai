import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QSpinBox, QFileDialog, QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
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
        self.params = params
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left side (input)
        left_layout = QVBoxLayout()
        self.drop_label = ImageDropLabel(self)
        left_layout.addWidget(self.drop_label)

        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.open_file_dialog)
        left_layout.addWidget(self.upload_btn)

        self.param_widgets = []
        for param in self.params:
            hbox = QHBoxLayout()
            label = QLabel(param['name'])
            spin = QSpinBox()
            spin.setRange(param['min'], param['max'])
            spin.setValue(param.get('default', param['min']))
            self.param_widgets.append(spin)
            hbox.addWidget(label)
            hbox.addWidget(spin)
            left_layout.addLayout(hbox)

        self.transform_btn = QPushButton("Transform")
        self.transform_btn.clicked.connect(self.apply_transform)
        left_layout.addWidget(self.transform_btn)

        # Right side (output)
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

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.main_window.load_image(path)

    def update_original_display(self, img):
        self.show_image(img, self.original_display)

    def show_image(self, img, label):
        if img is not None:
            # Convert image to RGB format for proper display
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img.shape
            bytes_per_line = ch * w
            q_img = QImage(img.data.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def apply_transform(self):
        if self.main_window.current_image is not None:
            try:
                params = [w.value() for w in self.param_widgets]
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
        self.setGeometry(0, 0, screen.width()//2, int(screen.height()*(0.9)))

        self.tabs = QTabWidget()

        transforms = [
            ("Crop Half", self.crop_half, []),
            ("Rotate", self.rotate_image, [{'name': 'Angle', 'min': 0, 'max': 360}]),
            ("Resize", self.resize_image, [{'name': 'Percentage', 'min': 1, 'max': 200}]),
            ("Sobel Filter", self.sobel_filter, [{'name': 'Kernel Size', 'min': 1, 'max': 7, 'default': 3, 'step': 2}])        ]

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
                for i in range(self.tabs.count()):
                    tab = self.tabs.widget(i)
                    if isinstance(tab, ImageTab):
                        tab.drop_label.setStyleSheet("background-color: green; border: 2px dashed black;")
            else:
                raise ValueError("Invalid image file")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def crop_half(self, img):
        return img[:, :img.shape[1]//2]

    def rotate_image(self, img, angle):
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
        return cv2.warpAffine(img, M, (w, h))

    def resize_image(self, img, percent):
        width = int(img.shape[1] * percent / 100)
        height = int(img.shape[0] * percent / 100)
        return cv2.resize(img, (width, height))



    def sobel_filter(self, img, ksize):
        # Ensure kernel size is odd and within valid range
        ksize = max(1, min(7, ksize))
        ksize = ksize if ksize % 2 == 1 else ksize + 1
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Calculate Sobel gradients
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        
        # Convert to absolute values and combine
        abs_sobelx = cv2.convertScaleAbs(sobelx)
        abs_sobely = cv2.convertScaleAbs(sobely)
        combined = cv2.addWeighted(abs_sobelx, 0.5, abs_sobely, 0.5, 0)
        
        # Convert back to 3-channel for display
        return cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())