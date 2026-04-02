import sys
from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QFont, QFontMetrics, QPaintEvent, QColor


class MyRibbon(QWidget):
    def __init__(self):
        super().__init__()
        self.test_text="this is a demo text to show if the project works"
        self.timer=QTimer()
        self.timer.timeout.connect(self.update_text_position)
        self.timer.start(16)

        self.font = QFont("Ubuntu", 14)
        self.font.setBold(True)
        self.metrics = QFontMetrics(self.font)
        self.text_width=self.metrics.horizontalAdvance(self.test_text)

        self.screen_geo=QApplication.primaryScreen().geometry()
        self.x_location=self.screen_geo.width()
        self.setFixedSize(self.screen_geo.width(),40)
    def update_text_position(self):
        self.x_location -= 2
        if self.x_location < -(self.text_width):
            self.x_location = self.screen_geo.width()

        self.update()
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor("Red"))
        painter.setBrush(QColor("white"))
        painter.font=self.font
        painter.drawText(self.x_location,30, self.test_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyRibbon()
    window.show()
    sys.exit(app.exec())
