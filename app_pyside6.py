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
    QLabel, QListWidget, QListWidgetItem, QGraphicsPathItem,
)
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, QTimer, Signal
from PySide6.QtGui import (
    QColor, QPen, QBrush, QFont,
    QPainterPath,
    QWheelEvent, QMouseEvent,
)

# Style constants
MIN_SCALE = 0.2
MAX_SCALE = 5.0
EDGE_COLOR = QColor("#999999")
EDGE_HIGHLIGHT_COLOR = QColor("#FF6600")
NODE_SELECTED_BRUSH = QColor("#FFDD88")
NODE_NEIGHBOR_BRUSH = QColor("#AAFFAA")
LABEL_BG = QColor(255, 255, 255, 180)
LABEL_BG_SELECTED = QColor(255, 255, 200, 200)
LABEL_BG_NEIGHBOR = QColor(200, 255, 200, 200)

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
    nodeSelected = Signal(str)

    def __init__(self, people_dict: dict[str, Person]):
        super().__init__()
        self.people = people_dict
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.node_items: dict[str, tuple] = {}  # name -> (ellipseItem, labelItem, rectItem)
        self.edge_items: list[dict] = []  # dict with keys: path_item, arrow_item, src, dst
        self.use_networkx_layout = HAS_NX  # toggle: use nx layout if available
        self.selected_name: str | None = None
        self._panning = False
        self._pan_start_pos = None
        self.setRenderHint(self.RenderHint.Antialiasing, True)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self._build_scene()

    def _job_color(self, job: str) -> QColor:
        # Map jobs to distinct colors, default gray
        colormap = {
            "engineer": QColor("#4C78A8"),
            "designer": QColor("#F58518"),
            "artist": QColor("#E45756"),
            "scientist": QColor("#72B7B2"),
            "manager": QColor("#54A24B"),
            "temp": QColor("#B279A2"),
        }
        return colormap.get(job.lower(), QColor("#999999"))

    def _clear_scene(self):
        self.scene.clear()
        self.node_items.clear()
        self.edge_items.clear()
        self.selected_name = None

    def _build_scene(self):
        local_people = dict(self.people)
        self._clear_scene()
        # Compute positions: networkx spring layout if available, else simple hierarchical
        positions: dict[str, tuple[float, float]]
        if self.use_networkx_layout:
            try:
                G = self._to_networkx()
                positions = nx.spring_layout(G)
                positions = {n: (x * 300.0, y * 300.0) for n, (x, y) in positions.items()}
            except Exception:
                positions = self._hierarchical_positions()
        else:
            positions = self._hierarchical_positions()

        # Draw nodes
        for name, (x, y) in positions.items():
            self._add_node(name, x, y)

        # Draw edges with curved lines and arrowheads
        pen = QPen(EDGE_COLOR)
        pen.setWidthF(1.0)
        arrow_brush = QBrush(EDGE_COLOR)
        for src_name, src_person in local_people.items():
            if src_name not in self.node_items:
                continue
            src_ellipse, _, _ = self.node_items[src_name]
            # ellipse rect center is relative to scene coordinates already set
            src_center = src_ellipse.rect().center()
            sx = src_ellipse.pos().x() + src_center.x()
            sy = src_ellipse.pos().y() + src_center.y()
            for friend in src_person.friends:
                dst_name = friend.name
                if dst_name not in self.node_items:
                    continue
                dst_ellipse, _, _ = self.node_items[dst_name]
                dst_center = dst_ellipse.rect().center()
                dx = dst_ellipse.pos().x() + dst_center.x()
                dy = dst_ellipse.pos().y() + dst_center.y()

                # Create curved path from (sx, sy) to (dx, dy)
                path = QPainterPath()
                path.moveTo(sx, sy)
                mid_x = (sx + dx) / 2
                mid_y = (sy + dy) / 2
                # Calculate perpendicular offset for curve
                offset = 30
                vx = dx - sx
                vy = dy - sy
                length = (vx**2 + vy**2)**0.5
                if length == 0:
                    length = 1
                # Perp unit vector
                px = -vy / length
                py = vx / length
                cx = mid_x + px * offset
                cy = mid_y + py * offset
                path.quadTo(cx, cy, dx, dy)

                path_item = QGraphicsPathItem(path)
                path_item.setPen(pen)
                self.scene.addItem(path_item)

                # Arrowhead at (dx, dy)
                arrow_size = 10
                # Direction vector from control point to end point
                dir_x = dx - cx
                dir_y = dy - cy
                dir_len = (dir_x**2 + dir_y**2) ** 0.5
                if dir_len == 0:
                    dir_len = 1
                dir_x /= dir_len
                dir_y /= dir_len
                # Compute two points for arrowhead base
                left_x = dx - dir_x * arrow_size - dir_y * (arrow_size / 2)
                left_y = dy - dir_y * arrow_size + dir_x * (arrow_size / 2)
                right_x = dx - dir_x * arrow_size + dir_y * (arrow_size / 2)
                right_y = dy - dir_y * arrow_size - dir_x * (arrow_size / 2)

                arrow_path = QPainterPath()
                arrow_path.moveTo(dx, dy)
                arrow_path.lineTo(left_x, left_y)
                arrow_path.lineTo(right_x, right_y)
                arrow_path.closeSubpath()

                arrow_item = QGraphicsPathItem(arrow_path)
                arrow_item.setBrush(arrow_brush)
                arrow_item.setPen(QPen(Qt.NoPen))
                self.scene.addItem(arrow_item)

                self.edge_items.append({
                    "path_item": path_item,
                    "arrow_item": arrow_item,
                    "src": src_name,
                    "dst": dst_name,
                })

    def _add_node(self, name: str, x: float, y: float):
        radius = 18
        job = self.people[name].job
        color = self._job_color(job)
        ellipse = self.scene.addEllipse(-radius, -radius, radius*2, radius*2,
                                        QPen(Qt.black), QBrush(color))
        ellipse.setToolTip(f"{name}\n{job}")
        ellipse.setFlag(ellipse.ItemIsSelectable, True)
        ellipse.setData(0, name)  # store name for retrieval
        ellipse.setPos(x, y)

        # Create label with white semi-transparent background
        label_text = f"{name}\n({job})"
        label = self.scene.addText(label_text, QFont("", 8))
        label.setDefaultTextColor(Qt.black)
        label.setZValue(1)  # Above background rect
        # Position label under node horizontally centered
        label_x = x - label.boundingRect().width()/2
        label_y = y + radius + 4
        label.setPos(label_x, label_y)

        # Background rect behind label
        rect_item = self.scene.addRect(label.boundingRect())
        rect_item.setBrush(QBrush(LABEL_BG))  # use style constant
        rect_item.setPen(QPen(Qt.NoPen))
        rect_item.setPos(label_x, label_y)
        rect_item.setZValue(0)  # beneath text

        self.node_items[name] = (ellipse, label, rect_item)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self.setCursor(Qt.ClosedHandCursor)
            self._pan_start_pos = event.pos()
            event.accept()
            return
        pos = event.position() if hasattr(event, "position") else event.pos()
        scene_pos = self.mapToScene(pos.toPoint())
        items = self.scene.items(scene_pos)
        # Find first ellipse item
        selected_name = None
        for item in items:
            if hasattr(item, "data"):
                name = item.data(0)
                if isinstance(name, str) and name in self.node_items:
                    selected_name = name
                    break
        if selected_name is not None:
            self._highlight_node(selected_name)
            self.nodeSelected.emit(selected_name)
        else:
            self._clear_highlight()
            self.nodeSelected.emit("")
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._panning and self._pan_start_pos is not None:
            delta = event.pos() - self._pan_start_pos
            self._pan_start_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        # Zoom in/out around mouse pointer
        angleDelta = event.angleDelta().y()
        if angleDelta == 0:
            event.ignore()
            return
        factor = 1.15 if angleDelta > 0 else 1 / 1.15
        current_scale = self.transform().m11()
        new_scale = current_scale * factor
        if new_scale < MIN_SCALE:
            factor = MIN_SCALE / current_scale
        elif new_scale > MAX_SCALE:
            factor = MAX_SCALE / current_scale
        if factor == 1.0:
            event.ignore()
            return
        self.scale(factor, factor)
        event.accept()

    def _highlight_node(self, name: str):
        if self.selected_name == name:
            return  # already selected
        self._clear_highlight()
        ellipse, label, rect = self.node_items.get(name, (None, None, None))
        if ellipse:
            pen = QPen(Qt.red, 3)
            ellipse.setPen(pen)
            ellipse.setBrush(QBrush(NODE_SELECTED_BRUSH))
            # highlight label background as well
            rect.setBrush(QBrush(LABEL_BG_SELECTED))
            self.selected_name = name

        # Highlight edges connected to this node & neighbor nodes
        for edge in self.edge_items:
            pi = edge["path_item"]
            ai = edge["arrow_item"]
            src = edge["src"]
            dst = edge["dst"]
            if src == name or dst == name:
                # Thicker pen and brighter arrow
                pi.setPen(QPen(EDGE_HIGHLIGHT_COLOR, 3))
                ai.setBrush(QBrush(EDGE_HIGHLIGHT_COLOR))
                # Highlight neighbor node(s)
                neighbor = dst if src == name else src
                n_ellipse, n_label, n_rect = self.node_items.get(neighbor, (None, None, None))
                if n_ellipse:
                    n_ellipse.setPen(QPen(Qt.darkGreen, 3))
                    n_ellipse.setBrush(QBrush(NODE_NEIGHBOR_BRUSH))
                    n_rect.setBrush(QBrush(LABEL_BG_NEIGHBOR))
            else:
                pi.setPen(QPen(EDGE_COLOR, 1))
                ai.setBrush(QBrush(EDGE_COLOR))
        # Reset nodes not selected or neighbors
        for n, (e, l, r) in self.node_items.items():
            if n != name and not (
                any((edge["src"] == name and edge["dst"] == n) or (edge["dst"] == name and edge["src"] == n) for edge in self.edge_items)
            ):
                e.setPen(QPen(Qt.black))
                e.setBrush(QBrush(self._job_color(self.people[n].job)))
                r.setBrush(QBrush(LABEL_BG))

    def _clear_highlight(self):
        if self.selected_name is None:
            return
        # Reset node
        ellipse, label, rect = self.node_items.get(self.selected_name, (None, None, None))
        if ellipse:
            ellipse.setPen(QPen(Qt.black))
            ellipse.setBrush(QBrush(self._job_color(self.people[self.selected_name].job)))
            rect.setBrush(QBrush(LABEL_BG))
        # Reset edges
        for edge in self.edge_items:
            pi = edge["path_item"]
            ai = edge["arrow_item"]
            pi.setPen(QPen(EDGE_COLOR, 1))
            ai.setBrush(QBrush(EDGE_COLOR))
        # Reset neighbor node highlights
        for n, (e, l, r) in self.node_items.items():
            e.setPen(QPen(Qt.black))
            e.setBrush(QBrush(self._job_color(self.people[n].job)))
            r.setBrush(QBrush(LABEL_BG))

        self.selected_name = None

    def toggle_layout(self):
        self.use_networkx_layout = not self.use_networkx_layout
        self._build_scene()

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
        self.people = people_dict

        # Left: queue view + controls
        self.queue_model = QueueModel(items=["you", "ana", "bob", "cat"])
        self.queue_view = QListView()
        self.queue_view.setModel(self.queue_model)

        btn_enq = QPushButton("Enqueue")
        btn_deq = QPushButton("Dequeue")

        def on_enqueue():
            btn_enq.setEnabled(False)
            btn_deq.setEnabled(False)
            new_name = f"p{len(self.queue_model.items)}"
            self.queue_model.enqueue(new_name)
            # Add dummy node to graph for demo
            if new_name not in self.people:
                # Create Person with job 'temp'
                p = Person(new_name, "temp")
                self.people[new_name] = p
                # Link from currently selected node if exists, else from 'you' if exists
                src_node = self.graph_view.selected_name if self.graph_view.selected_name else ("you" if "you" in self.people else None)
                if src_node and src_node in self.people:
                    self.people[src_node].friends.append(p)
                self.graph_view._build_scene()
            btn_enq.setEnabled(True)
            btn_deq.setEnabled(True)

        btn_enq.clicked.connect(on_enqueue)
        btn_deq.clicked.connect(lambda: self.queue_model.dequeue())

        left = QWidget()
        vl = QVBoxLayout(left)
        vl.addWidget(self.queue_view)
        hl = QHBoxLayout()
        hl.addWidget(btn_enq)
        hl.addWidget(btn_deq)
        vl.addLayout(hl)

        # Right: graph view + inspector + toggle layout button

        right = QWidget()
        right_vl = QVBoxLayout(right)
        # Toolbar area for toggle button
        btn_toggle_layout = QPushButton("Toggle Layout")
        btn_toggle_layout.setToolTip("Toggle between NetworkX layout and Hierarchical layout")
        right_vl.addWidget(btn_toggle_layout)

        self.graph_view = GraphView(people_dict)
        right_vl.addWidget(self.graph_view)

        # Inspector widget below graph view
        self.inspector = QWidget()
        inspector_layout = QVBoxLayout(self.inspector)
        self.label_name = QLabel("<b>Name:</b> ")
        self.label_job = QLabel("<b>Job:</b> ")
        self.list_friends = QListWidget()
        inspector_layout.addWidget(self.label_name)
        inspector_layout.addWidget(self.label_job)
        inspector_layout.addWidget(QLabel("<b>Friends:</b>"))
        inspector_layout.addWidget(self.list_friends)
        right_vl.addWidget(self.inspector)

        # Splitter vertical for graph + inspector in right panel
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(self.graph_view)
        right_splitter.addWidget(self.inspector)
        right_splitter.setSizes([400, 200])

        # Replace right layout to include toggle button above splitter
        right_layout = QVBoxLayout()
        right_layout.addWidget(btn_toggle_layout)
        right_layout.addWidget(right_splitter)
        right.setLayout(right_layout)

        # Main splitter: left + right
        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(right)
        self.setCentralWidget(splitter)

        # Connect signals
        btn_toggle_layout.clicked.connect(self.graph_view.toggle_layout)
        self.graph_view.nodeSelected.connect(self.update_inspector)

        # Timer hook (200ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.graph_view.tick)
        self.timer.start(200)

        # Initialize inspector empty
        self.update_inspector("")

    def update_inspector(self, name: str):
        if not name or name not in self.people:
            self.label_name.setText("<b>Name:</b> ")
            self.label_job.setText("<b>Job:</b> ")
            self.list_friends.clear()
            return
        person = self.people[name]
        self.label_name.setText(f"<b>Name:</b> {person.name}")
        self.label_job.setText(f"<b>Job:</b> {person.job}")
        self.list_friends.clear()
        for friend in person.friends:
            item = QListWidgetItem(friend.name)
            self.list_friends.addItem(item)


def main():
    app = QApplication(sys.argv)
    w = MainWindow(people)
    w.resize(1000, 640)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

