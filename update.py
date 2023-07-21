import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QColor, QDrag
from PyQt5.QtCore import Qt, QPoint, QMimeData

class Element(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(24, 24)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: red")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.pos().toString())
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)

class Canvas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(96, 128)
        self.setMinimumSize(96, 128)
        self.elements = []
        self.scale = 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 0, self.width(), self.height())

        # 绘制画布边框
        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(0, 0, 96, 128)

        # 缩放画布
        painter.scale(self.scale, self.scale)

    def dropEvent(self, event):
        pos = event.pos()
        element_pos = QPoint(int(event.mimeData().text().split(',')[0][1:]), int(event.mimeData().text().split(',')[1][:-1]))
        element_pos += pos
        self.elements.append(element_pos)
        self.update()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义")
        self.resize(800, 500)
        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)

        # 添加放大和缩小按钮
        self.zoom_in_button = QPushButton("+", self)
        self.zoom_in_button.move(10, 10)
        self.zoom_in_button.clicked.connect(self.zoomIn)

        self.zoom_out_button = QPushButton("-", self)
        self.zoom_out_button.move(60, 10)
        self.zoom_out_button.clicked.connect(self.zoomOut)

    def zoomIn(self):
        self.canvas.scale *= 2
        self.canvas.update()

    def zoomOut(self):
        self.canvas.scale /= 2
        self.canvas.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())