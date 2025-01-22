import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

# Create a simple window
class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Message Window")  # Set the title of the window

        # Create a label with a message
        label = QLabel("Hello, welcome to PyQt5!", self)
        label.setStyleSheet("font-size: 16px; color: blue;")

        # Create a layout and add the label
        layout = QVBoxLayout()
        layout.addWidget(label)

        # Set the layout to the window
        self.setLayout(layout)
        self.resize(300, 100)  # Set the initial window size

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    window = SimpleWindow()       # Create an instance of the window
    window.show()                 # Show the window
    sys.exit(app.exec_())         # Run the event loop








