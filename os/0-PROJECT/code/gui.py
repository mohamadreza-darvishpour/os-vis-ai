import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QRectF


class GanttChartWidget(QWidget):
    def __init__(self, gantt_chart, parent=None):
        super().__init__(parent)
        self.gantt_chart = gantt_chart
        self.setMinimumSize(800, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define colors for processes
        colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255), QColor(255, 255, 0), QColor(255, 0, 255)]

        # Draw the Gantt chart
        y = 50  # Y position for the chart
        bar_height = 30  # Height of each bar
        time_scale = 10  # Scale for time units (pixels per unit time)

        # Draw process bars
        for process, start, end in self.gantt_chart:
            x1 = start * time_scale
            x2 = end * time_scale
            width = x2 - x1
            color = colors[process % len(colors)]
            painter.setBrush(color)
            painter.drawRect(QRectF(x1, y, width, bar_height))

            # Draw process number
            painter.setPen(Qt.black)
            painter.drawText(x1 + 5, y + bar_height // 2, f"P{process}")

        # Draw timeline
        painter.setPen(Qt.black)
        max_time = max(end for _, _, end in self.gantt_chart)
        for t in range(0, max_time + 1, 5):
            x = t * time_scale
            painter.drawLine(x, y + bar_height + 10, x, y + bar_height + 20)
            painter.drawText(x - 10, y + bar_height + 40, str(t))


class MainWindow(QMainWindow):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gantt Chart Viewer")
        self.setGeometry(100, 100, 800, 400)
        self.file_path = file_path

        # Create layout
        self.layout = QVBoxLayout()

        # Add reload button
        self.reload_button = QPushButton("Reload Data")
        self.reload_button.clicked.connect(self.reload_data)
        self.layout.addWidget(self.reload_button)

        # Initialize metrics and Gantt chart
        self.metrics_label = QLabel()
        self.metrics_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.metrics_label)

        self.gantt_chart_widget = None

        # Load initial data
        self.reload_data()

        # Set layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def reload_data(self):
        """Reload data from the file and update the UI."""
        # Clear previous Gantt chart widget
        if self.gantt_chart_widget:
            self.layout.removeWidget(self.gantt_chart_widget)
            self.gantt_chart_widget.deleteLater()
            self.gantt_chart_widget = None

        # Read the file
        self.best_quantum = None
        self.avg_turnaround_time = None
        self.cpu_utilization = None
        self.avg_response_time = None
        self.avg_waiting_time = None
        self.best_gantt_chart = None
        self.read_file(self.file_path)

        # Update metrics label
        self.metrics_label.setText(
            f"Best Quantum: {self.best_quantum}\n"
            f"Avg Turnaround Time: {self.avg_turnaround_time}\n"
            f"CPU Utilization: {self.cpu_utilization}\n"
            f"Avg Response Time: {self.avg_response_time}\n"
            f"Avg Waiting Time: {self.avg_waiting_time}"
        )

        # Draw Gantt chart
        if self.best_gantt_chart:
            self.gantt_chart_widget = GanttChartWidget(self.best_gantt_chart)
            self.layout.addWidget(self.gantt_chart_widget)

    def read_file(self, file_path):
        """Read the file and extract scheduling data."""
        try:
            with open(file_path, "r") as file:
                for line in file:
                    if "best_quantum" in line:
                        self.best_quantum = float(line.split(":")[1].strip())
                    elif "avg_turnaround_time" in line:
                        self.avg_turnaround_time = float(line.split(":")[1].strip())
                    elif "cpu_utilization" in line:
                        self.cpu_utilization = float(line.split(":")[1].strip())
                    elif "avg_response_time" in line:
                        self.avg_response_time = float(line.split(":")[1].strip())
                    elif "avg_waiting_time" in line:
                        self.avg_waiting_time = float(line.split(":")[1].strip())
                    elif "best_gantt_chart" in line:
                        chart_data = line.split(":")[1].strip().strip("[]")
                        self.best_gantt_chart = [
                            tuple(map(int, item.strip("()").split(",")))
                            for item in chart_data.split("), (")
                        ]
        except Exception as e:
            print(f"Error reading file: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Path to the file
    file_path = "output.txt"  # Replace with the actual path to your file

    # Create and show the main window
    window = MainWindow(file_path)
    window.show()

    sys.exit(app.exec_())