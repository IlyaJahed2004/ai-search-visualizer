# All GUI components (GraphCanvas + UninformedWindow + InformedWindow)

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QSizePolicy
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx

# IMPORT UNINFORMED & INFORMED ALGORITHMS
from uninformed_search import (
    BFS_with_metrics, DFS_with_metrics, UCS_with_metrics,
    DLS_with_metrics, IDS_with_metrics, Backtracking_with_metrics,
    Bidirectional_with_metrics, extract_path, path_cost_expression,
)


from informed_search import (
    Greedy_Search, AStar_Search, IDAStar_Search, RBFS_Search,
    extract_path as informed_extract_path,
    path_cost_expression as informed_path_cost_expression,
)

from romania_problem import (
    neighbors, distances, city_positions
)

#GRAPH CANVAS
class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(7, 6))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        # Build graph using distances
        self.G = nx.Graph()
        for (u, v), w in distances.items():
            if not self.G.has_edge(u, v):
                self.G.add_edge(u, v, weight=w)

    def draw_base_graph(self):
        self.ax.clear()
        nx.draw(
            self.G, pos=city_positions, with_labels=True,
            node_size=700, node_color="#90CAF9",
            edge_color="#B0BEC5", font_size=8, ax=self.ax
        )
        edge_labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(
            self.G, pos=city_positions, edge_labels=edge_labels,
            font_size=8, label_pos=0.5, ax=self.ax
        )
        self.ax.set_title("Romania Map")
        self.ax.set_axis_off()
        self.draw()

    def draw_path(self, path):
        self.draw_base_graph()
        if not path or len(path) < 2:
            return

        edges = list(zip(path, path[1:]))

        nx.draw_networkx_edges(
            self.G, pos=city_positions, edgelist=edges,
            width=3, edge_color="red", ax=self.ax
        )
        nx.draw_networkx_nodes(
            self.G, pos=city_positions, nodelist=path,
            node_size=800, node_color="#FFCC80", ax=self.ax
        )
        self.draw()


#UNINFORMED SEARCH WINDOW
class UninformedWindow(QMainWindow):
    switch_to_menu = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uninformed Search")
        self.setMinimumSize(1200, 750)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Canvas
        self.canvas = GraphCanvas(self)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.draw_base_graph()
        layout.addWidget(self.canvas, 2)

        # Side panel
        panel = QWidget()
        v = QVBoxLayout(panel)
        v.setAlignment(Qt.AlignTop)

        self.combo = QComboBox()
        self.combo.addItems(["BFS", "DFS", "UCS", "DLS", "IDS", "Backtracking", "Bidirectional"])

        self.start = QLineEdit("Arad")
        self.goal = QLineEdit("Bucharest")
        self.depth = QLineEdit("10")

        btn_run = QPushButton("Run")
        btn_run.clicked.connect(self.run)

        btn_back = QPushButton("Back to Menu")
        btn_back.clicked.connect(self.switch_to_menu.emit)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        v.addWidget(QLabel("Algorithm:"))
        v.addWidget(self.combo)
        v.addWidget(QLabel("Start:"))
        v.addWidget(self.start)
        v.addWidget(QLabel("Goal:"))
        v.addWidget(self.goal)
        v.addWidget(QLabel("Depth Limit (DLS/IDS):"))
        v.addWidget(self.depth)
        v.addWidget(btn_run)
        v.addWidget(QLabel("Log:"))
        v.addWidget(self.log)
        v.addWidget(btn_back)

        layout.addWidget(panel, 1)

    def run(self):
        algo = self.combo.currentText()
        start = self.start.text().strip()
        goal = self.goal.text().strip()

        if start not in neighbors or goal not in neighbors:
            QMessageBox.warning(self, "Error", "Invalid city")
            return

        try:
            depth = int(self.depth.text())
        except:
            depth = 10

        if algo == "BFS":
            res = BFS_with_metrics(start, goal)
            path = extract_path(res["goal_node"])
        elif algo == "DFS":
            res = DFS_with_metrics(start, goal)
            path = extract_path(res["goal_node"])
        elif algo == "UCS":
            res = UCS_with_metrics(start, goal)
            path = extract_path(res["goal_node"])
        elif algo == "DLS":
            res = DLS_with_metrics(start, goal, depth)
            path = extract_path(res["goal_node"])
        elif algo == "IDS":
            res = IDS_with_metrics(start, goal, max_limit=depth)
            path = extract_path(res["goal_node"])
        elif algo == "Backtracking":
            res = Backtracking_with_metrics(start, goal)
            path = extract_path(res["goal_node"])
        else:  # Bidirectional
            res = Bidirectional_with_metrics(start, goal)
            path = res.get("path")

        # Draw path
        if path:
            self.canvas.draw_path(path)
        else:
            self.canvas.draw_base_graph()

        # Log
        self.log.append(f"\n=== {algo} ===")
        self.log.append(f"Path: {path}")
        if path:
            self.log.append(path_cost_expression(path))
        self.log.append(str(res))


# INFORMED SEARCH WINDOW
class InformedWindow(QMainWindow):
    switch_to_menu = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Informed Search")
        self.setMinimumSize(1200, 750)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        self.canvas = GraphCanvas(self)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.draw_base_graph()
        layout.addWidget(self.canvas, 2)

        panel = QWidget()
        v = QVBoxLayout(panel)
        v.setAlignment(Qt.AlignTop)

        self.combo = QComboBox()
        self.combo.addItems(["Greedy", "A*", "IDA*", "RBFS"])

        self.start = QLineEdit("Arad")
        self.goal = QLineEdit("Bucharest")

        btn_run = QPushButton("Run")
        btn_run.clicked.connect(self.run)

        btn_back = QPushButton("Back to Menu")
        btn_back.clicked.connect(self.switch_to_menu.emit)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        v.addWidget(QLabel("Informed Algorithm:"))
        v.addWidget(self.combo)
        v.addWidget(QLabel("Start:"))
        v.addWidget(self.start)
        v.addWidget(QLabel("Goal:"))
        v.addWidget(self.goal)
        v.addWidget(btn_run)
        v.addWidget(QLabel("Log:"))
        v.addWidget(self.log)
        v.addWidget(btn_back)

        layout.addWidget(panel, 1)

    def run(self):
        algo = self.combo.currentText()
        start = self.start.text().strip()
        goal = self.goal.text().strip()

        if start not in neighbors or goal not in neighbors:
            QMessageBox.warning(self, "Error", "Invalid city")
            return

        if algo == "Greedy":
            res = Greedy_Search(start, goal)
        elif algo == "A*":
            res = AStar_Search(start, goal)
        elif algo == "IDA*":
            res = IDAStar_Search(start, goal)
        else:
            res = RBFS_Search(start, goal)

        node = res.get("goal_node")
        path = informed_extract_path(node) if node else None

        if path:
            self.canvas.draw_path(path)
        else:
            self.canvas.draw_base_graph()

        self.log.append(f"\n=== {algo} ===")
        self.log.append(f"Path: {path}")
        if path:
            self.log.append(informed_path_cost_expression(path))
        self.log.append(str(res))
