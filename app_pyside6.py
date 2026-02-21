"""
app_pyside6.py
A minimal PySide6 application that visualizes a queue/list and the 'people' graph
from findJob.py in real time (timer hook), up to step 4 as requested.
"""

import sys
from typing import Any

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListView, QPushButton,
    QVBoxLayout, QHBoxLayout, QSplitter, QGraphicsView, QGraphicsScene,
)
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, QTimer
from PySide6.QtGui import QColor, QPen, QBrush, QFont

# Import domain data
from findJob import people, Person

# Optional networkx import (used for layout if available)
try:
    import networkx as nx  # type: ignore
    HAS_NX = True
except Exception:
    HAS_NX = False

class QueueModel(QAbstractListModel):
    """A simple list model to represent a queue (front at index 0)."""
    def __init__(self, items: list[Any] | None = None):
        super().__init__()
        self.items: list[Any] = items or []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.items)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        i = index.row()
        if role == Qt.DisplayRole:
            return str(self.items[i])
        if role == Qt.BackgroundRole and i == 0 and self.items:
            return QColor("#FFF2CC")  # highlight front
        return None

    # queue operations
    def enqueue(self, item: Any):
        self.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
        self.items.append(item)
        self.endInsertRows()

    def dequeue(self):
        if not self.items:
            return None
        self.beginRemoveRows(QModelIndex(), 0, 0)
        val = self.items.pop(0)
        self.endRemoveRows()
        return val

class GraphView(QGraphicsView):
    """Graphics view for visualizing the people graph."""
    def __init__(self, people_dict: dict[str, Person]):
        super().__init__()
        self.people = people_dict
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.node_items: dict[str, tuple] = {}  # name -> (ellipseItem, labelItem)
        self.edge_items: list = []
        self.use_networkx_layout = HAS_NX  # toggle: use nx layout if available
        self._build_scene()

    def _clear_scene(self):
        self.scene.clear()
        self.node_items.clear()
        self.edge_items.clear()

    def _build_scene(self):
        self._clear_scene()
        # Compute positions: networkx spring layout if available, else simple hierarchical
        positions: dict[str, tuple[float, float]]
        if self.use_networkx_layout:
            G = self._to_networkx()
            positions = nx.spring_layout(G)
            # scale positions to reasonable scene coordinates
            positions = {n: (x * 300.0, y * 300.0) for n, (x, y) in positions.items()}
        else:
            positions = self._hierarchical_positions()

        # Draw nodes
        for name, (x, y) in positions.items():
            self._add_node(name, x, y)

        # Draw edges
        pen = QPen(QColor("#999999"))
        for src_name, src_person in self.people.items():
            if src_name not in self.node_items:
                continue
            src_ellipse, _ = self.node_items[src_name]
            sx, sy = src_ellipse.rect().center().x(), src_ellipse.rect().center().y()
            for friend in src_person.friends:
                dst_name = friend.name
                if dst_name not in self.node_items:
                    continue
                dst_ellipse, _ = self.node_items[dst_name]
                dx, dy = dst_ellipse.rect().center().x(), dst_ellipse.rect().center().y()
                line = self.scene.addLine(sx, sy, dx, dy, pen)
                self.edge_items.append(line)

    def _add_node(self, name: str, x: float, y: float):
        radius = 18
        ellipse = self.scene.addEllipse(x - radius, y - radius, radius*2, radius*2,
                                        QPen(Qt.black), QBrush(QColor("#4C78A8")))
        label = self.scene.addText(f"{name}\n({self.people[name].job})", QFont("", 8))
        label.setDefaultTextColor(Qt.black)
        label.setPos(x - label.boundingRect().width()/2, y + radius + 4)
        self.node_items[name] = (ellipse, label)

    def _hierarchical_positions(self) -> dict[str, tuple[float, float]]:
        # Simple BFS-depth-based levels: root at 'you' if present, else first key
        from collections import deque, defaultdict
        names = list(self.people.keys())
        if not names:
            return {}
        root = 'you' if 'you' in self.people else names[0]
        depth: dict[str, int] = {root: 0}
        q = deque([root])
        while q:
            cur = q.popleft()
            d = depth[cur]
            for fr in self.people[cur].friends:
                n = fr.name
                if n not in depth:
                    depth[n] = d + 1
                    q.append(n)
        # assign remaining (disconnected) to next depths
        rem = [n for n in names if n not in depth]
        while rem:
            r = rem.pop(0)
            depth[r] = max(depth.values()) + 1
        # group by depth
        levels: dict[int, list[str]] = {}
        for name, d in depth.items():
            levels.setdefault(d, []).append(name)
        # positions: y from -150 to 150, x spread per level
        maxd = max(levels.keys()) if levels else 0
        positions: dict[str, tuple[float, float]] = {}
        for d, nodes in levels.items():
            y = -150 + (300 * (d / max(1, maxd))) if maxd > 0 else 0
            count = len(nodes)
            if count == 1:
                positions[nodes[0]] = (0.0, y)
            else:
                for i, n in enumerate(nodes):
                    x = -200 + (400 * i / (count - 1))
                    positions[n] = (x, y)
        return positions

    def _to_networkx(self):
        G = nx.DiGraph()
        for name, person in self.people.items():
            G.add_node(name, job=person.job)
        for name, person in self.people.items():
            for fr in person.friends:
                G.add_edge(name, fr.name)
        return G

    def tick(self):
        # Placeholder for periodic updates. For now, we just keep the scene.
        # You can toggle layout mode dynamically or animate positions here.
        pass

class MainWindow(QMainWindow):
    def __init__(self, people_dict: dict[str, Person]):
        super().__init__()
        self.setWindowTitle("PySide6: Queue + Graph Viewer")

        # Left: queue view + controls
        self.queue_model = QueueModel(items=["you", "ana", "bob", "cat"])
        self.queue_view = QListView()
        self.queue_view.setModel(self.queue_model)

        btn_enq = QPushButton("Enqueue")
        btn_deq = QPushButton("Dequeue")
        btn_enq.clicked.connect(lambda: self.queue_model.enqueue(f"p{len(self.queue_model.items)}"))
        btn_deq.clicked.connect(lambda: self.queue_model.dequeue())

        left = QWidget()
        vl = QVBoxLayout(left)
        vl.addWidget(self.queue_view)
        hl = QHBoxLayout()
        hl.addWidget(btn_enq)
        hl.addWidget(btn_deq)
        vl.addLayout(hl)

        # Right: graph view
        self.graph_view = GraphView(people_dict)

        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(self.graph_view)
        self.setCentralWidget(splitter)

        # Timer hook (200ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.graph_view.tick)
        self.timer.start(200)


def main():
    app = QApplication(sys.argv)
    w = MainWindow(people)
    w.resize(1000, 640)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
