import sys
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QMessageBox, QTextEdit, QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def read_input_matrix(file_path):
    """Read the adjacency matrix from a file, removing empty lines and extra whitespaces."""
    with open(file_path, 'r') as file:
        return [
            list(map(int, line.split())) 
            for line in file.readlines() 
            if line.strip()  # Ignore empty lines
        ]


def read_output_colors(file_path):
    """Read node colors from a file."""
    with open(file_path, 'r') as file:
        color_data = file.read().strip().split(',')
        return {int(item.split('=')[0]): item.split('=')[1] for item in color_data if '=' in item}


class GraphApp(QMainWindow):
    def __init__(self, input_file, output_file):
        super().__init__()
        self.setWindowTitle("Graph Drawer")
        self.resize(1000, 600)

        self.input_file = input_file
        self.output_file = output_file

        self.init_ui()
        self.draw_graph()

    def init_ui(self):
        """Set up the UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with horizontal split: left side for matrix, right side for graph
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Left side: Display adjacency matrix (with scroll)
        matrix_display_widget = QWidget()
        matrix_layout = QVBoxLayout(matrix_display_widget)

        self.matrix_display = QTextEdit()
        self.matrix_display.setReadOnly(True)
        self.matrix_display.setFixedWidth(200)  # Limit width to make it compact
        matrix_layout.addWidget(self.matrix_display)

        # Scroll area for adjacency matrix
        scroll_area = QScrollArea()
        scroll_area.setWidget(matrix_display_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Right side: Display the graph
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        self.canvas = FigureCanvas(Figure())
        right_layout.addWidget(self.canvas)

        # Button to reread files
        reread_button = QPushButton("Reread Files")
        reread_button.clicked.connect(self.draw_graph)
        right_layout.addWidget(reread_button)

        # Button to remake input (calls an external function)
        remake_button = QPushButton("Remake Input File")
        remake_button.clicked.connect(self.remake_input_file)
        right_layout.addWidget(remake_button)

    def draw_graph(self):
        """Read files and draw the graph."""
        try:
            matrix = read_input_matrix(self.input_file)
            colors = read_output_colors(self.output_file)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read files: {e}")
            return

        # Display the adjacency matrix on the left side
        matrix_text = "\n".join(["\t".join(map(str, row)) for row in matrix])
        self.matrix_display.setText(matrix_text)

        # Create the graph
        graph = nx.Graph()

        # Add nodes with colors
        for node, color in colors.items():
            graph.add_node(node, color=color)

        # Add edges based on the adjacency matrix
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value == 1:
                    graph.add_edge(i, j)

        # Draw the graph
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.set_axis_off()

        # Extract node colors
        node_colors = [data['color'] for _, data in graph.nodes(data=True)]
        nx.draw_networkx(
            graph, 
            ax=ax, 
            node_color=node_colors, 
            with_labels=True,
            node_size=500, 
            font_color='white'
        )

        self.canvas.draw()

    def remake_input_file(self):
        """Placeholder function to call an external function."""
        QMessageBox.information(self, "Remake Input", "Call your external function here to remake the input file.")
        # Replace with your actual external function call


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # File paths for the input and output files
    input_file = "input.txt"
    output_file = "output.txt"

    main_window = GraphApp(input_file, output_file)
    main_window.show()

    sys.exit(app.exec_())
