import networkx as nx
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class NodeItem(QGraphicsItem):
    def __init__(self, node, radius=15, **args):
        QGraphicsItem.__init__(self, **args)

        self.node = node
        self.radius = radius

        x, y = pos[node]
        self.setPos(QPointF(x, y))

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange :
            point = value.toPointF()
            pos[self.node] = [point.x(), point.y()]
            scene.update()
        return QGraphicsItem.itemChange(self, change, value)

    def update(self, *__args):
        self.setPos(*pos[self.node])

    def boundingRect(self):
        return QRectF(-self.radius, -self.radius, 2*self.radius, 2*self.radius)

    def paint(self, painter, style, widget=None):
        assert isinstance(painter, QPainter)

        if self.isSelected():
            brush = QBrush(Qt.yellow)
        else:
            brush = QBrush(Qt.white)

        pen = QPen(Qt.black)

        circle_path = QPainterPath()
        circle_path.addEllipse(self.boundingRect())
        painter.fillPath(circle_path, brush)
        painter.strokePath(circle_path, pen)

        text_path = QPainterPath()
        text_path.addText(0, 0, QFont(), str(self.node))
        box = text_path.boundingRect()
        text_path.translate(-box.center())

        painter.fillPath(text_path, QBrush(Qt.black))


class EdgeItem(QGraphicsItem):
    def __init__(self, source, target,  **args):
        QGraphicsItem.__init__(self, **args)
        self.source = source
        self.target = target

    def boundingRect(self):
        x0, y0 = pos[self.source]
        x1, y1 = pos[self.target]
        return QRectF(min(x0, x1), min(y0, y1), abs(x1-x0), abs(y1-y0))

    def paint(self, painter, style, widget=None):
        assert(isinstance(painter, QPainter))
        x0, y0 = pos[self.source]
        x1, y1 = pos[self.target]
        painter.drawLine(x0, y0, x1, y1)

if __name__ == '__main__':
    g = nx.Graph()
    g.add_edge('a', 'b')
    g.add_edge('a', 'c')
    g.add_edge('a', 'd')
    g.add_edge('b', 'c')
    g.add_edge('c', 'd')

    pos = nx.spring_layout(g, scale=300)

    #scene = QGraphicsScene()

    '''
    for edge in g.edges():
        scene.addItem(EdgeItem(edge[0], edge[1]))

    for node in g.nodes():
        scene.addItem(NodeItem(node))


    app = QApplication(sys.argv)

    win = QGraphicsView()
    win.setDragMode(QGraphicsView.RubberBandDrag)
    win.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
    win.setScene(scene)
    win.show()
    sys.exit(app.exec_())
    '''
