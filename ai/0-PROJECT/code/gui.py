import sys
import networkx as nx
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QWidget, QMessageBox, QTextEdit, QSplitter
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from colors_graph import color_points_ids, lines_of_input_file, make_out_file
from random_adj_mat import create_or_find_file_with_random_matrix

def read_input_matrix(file_path):
    """Read the adjacency matrix from a file, removing empty lines and extra whitespaces."""
    with open(file_path, 'r') as file:
        return [
            list(map(int, line.split())) 
            for line in file if line.strip()
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
        self.reload_all()

    def init_ui(self):
        """Set up the UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Use QSplitter to divide the window into two halves
        splitter = QSplitter()
        central_widget.setLayout(QVBoxLayout())
        central_widget.layout().addWidget(splitter)

        # Left side: Display adjacency matrix
        matrix_widget = QWidget()
        matrix_layout = QVBoxLayout(matrix_widget)
        self.matrix_display = QTextEdit()
        self.matrix_display.setReadOnly(True)
        matrix_layout.addWidget(self.matrix_display)
        splitter.addWidget(matrix_widget)

        # Right side: Display the graph
        graph_widget = QWidget()
        graph_layout = QVBoxLayout(graph_widget)

        self.canvas = FigureCanvas(Figure())
        graph_layout.addWidget(self.canvas)

        # Reload button
        reload_button = QPushButton("Reload")
        reload_button.clicked.connect(self.reload_all)
        graph_layout.addWidget(reload_button)

        # Remake input file button
        remake_button = QPushButton("Remake Input File")
        remake_button.clicked.connect(self.remake_input_file)
        graph_layout.addWidget(remake_button)

        splitter.addWidget(graph_widget)

        # Set the splitter to divide space equally
        splitter.setSizes([500, 500])

    def reload_all(self):
        """Reload and redraw all components."""
        try:
            # Read input and output files
            matrix = read_input_matrix(self.input_file)
            colors = read_output_colors(self.output_file)

            # Display adjacency matrix
            matrix_text = "\n".join([" ".join(map(str, row)) for row in matrix])
            self.matrix_display.setText(matrix_text)

            # Create and draw the graph
            self.draw_graph(matrix, colors)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reload files: {e}")

    def draw_graph(self, matrix, colors):
        """Draw the graph based on the adjacency matrix and colors."""
        graph = nx.Graph()

        # Add nodes with colors
        for node in range(len(matrix)):
            graph.add_node(node, color=colors.get(node, "gray"))

        # Add edges based on the adjacency matrix
        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix[i])):
                if matrix[i][j] == 1:
                    graph.add_edge(i, j)

        # Draw the graph
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.set_axis_off()

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
        """Remake the input file and reload everything."""
        try:
            # Create or find the input file
            create_or_find_file_with_random_matrix(self.input_file)

            # Perform graph coloring
            input_adjacency = lines_of_input_file(self.input_file)
            num_colors = 10
            print('\n\nsign 83')
            ids_obj = color_points_ids(input_adjacency, num_colors)
            print('\n\nsign 84')
            ids_obj.ids_coloring()
            print('\n\nsign 85')
            output_text = ids_obj.color_result()
            del ids_obj

            # Write the output file
            make_out_file(output_text)

            QMessageBox.information(self, "Success", "Input file remade and output file created successfully!")
            self.reload_all()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # File paths for the input and output files
    input_file = "input.txt"
    output_file = "output.txt"

    main_window = GraphApp(input_file, output_file)
    main_window.show()

    sys.exit(app.exec_())
