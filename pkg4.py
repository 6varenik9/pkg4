import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPixmap

def draw_stepwise_line(painter, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    dx /= steps
    dy /= steps
    x, y = x0, y0
    for _ in range(steps):
        painter.drawPoint(round(x), round(y))
        x += dx
        y += dy

def draw_CDA_line(painter, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    dx /= steps
    dy /= steps
    x, y = x0, y0
    for _ in range(steps):
        painter.drawPoint(round(x), round(y))
        x += dx
        y += dy

def draw_bresenham_line(painter, x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        painter.drawPoint(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_bresenham_circle(painter, xc, yc, r):
    x = 0
    y = r
    d = 3 - 2 * r
    while x <= y:
        painter.drawPoint(xc + x, yc + y)
        painter.drawPoint(xc - x, yc + y)
        painter.drawPoint(xc + x, yc - y)
        painter.drawPoint(xc - x, yc - y)
        painter.drawPoint(xc + y, yc + x)
        painter.drawPoint(xc - y, yc + x)
        painter.drawPoint(xc + y, yc - x)
        painter.drawPoint(xc - y, yc - x)
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1

class RasterizationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Алгоритмы растеризации")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItem("Пошаговый алгоритм")
        self.algorithm_selector.addItem("ЦДА")
        self.algorithm_selector.addItem("Брезенхем (отрезок)")
        self.algorithm_selector.addItem("Брезенхем (окружность)")
        self.layout.addWidget(self.algorithm_selector)

        self.run_button = QPushButton("Запуск")
        self.run_button.clicked.connect(self.run_algorithm)
        self.layout.addWidget(self.run_button)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.layout.addWidget(self.view)

    def run_algorithm(self):
        self.scene.clear()

        algorithm = self.algorithm_selector.currentText()

        pixmap = self.create_pixmap()

        painter = QPainter(pixmap)

        if algorithm == "Пошаговый алгоритм":
            painter.setPen(QColor(255, 0, 0))  
            draw_stepwise_line(painter, 50, 50, 300, 300)
        elif algorithm == "ЦДА":
            painter.setPen(QColor(0, 255, 0))  
            draw_CDA_line(painter, 50, 50, 300, 300)
        elif algorithm == "Брезенхем (отрезок)":
            painter.setPen(QColor(0, 0, 255))  
            draw_bresenham_line(painter, 50, 50, 300, 300)
        elif algorithm == "Брезенхем (окружность)":
            painter.setPen(QColor(255, 165, 0))  
            draw_bresenham_circle(painter, 200, 200, 100)
        
        painter.end()

        self.scene.addPixmap(pixmap)

    def create_pixmap(self):
        pixmap = QPixmap(800, 600)
        pixmap.fill(Qt.white)
        return pixmap

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RasterizationApp()
    window.show()
    sys.exit(app.exec_())
