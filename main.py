import os
import random
import sys
from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QFont, QFontMetrics, QPaintEvent, QColor, Qt
from FeedParsing import parse_feeds_to_list

class MyRibbon(QWidget):
    def __init__(self):
        super().__init__()
        self.counter=-1
        self.news_list=[]
        self.font = QFont("Ubuntu", 14)
        self.font.setBold(True)
        self.metrics = QFontMetrics(self.font)
        self.news_item=self.get_next_news_item()
        self.text_width = self.metrics.horizontalAdvance(self.news_item[0])

        self.shown_text=None

        
        self.timer=QTimer()
        self.timer.timeout.connect(self.update_text_position)
        self.timer.start(16)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        

        self.screen_geo=QApplication.primaryScreen().availableGeometry()
        self.x_location=self.screen_geo.width()
        self.window_height=40
        self.setGeometry(0,self.screen_geo.height(),self.screen_geo.width(),self.window_height)
        
                


    def update_text_position(self):
        

        self.x_location -= 2
        if self.x_location < -(self.text_width):
            self.x_location = self.screen_geo.width()
            self.news_item=self.get_next_news_item()
            self.text_width = self.metrics.horizontalAdvance(self.news_item[0])

            print(self.news_item)
        self.update()
    def paintEvent(self, event):
        
            
        painter = QPainter(self)

        painter.setPen(QColor("White"))
        painter.fillRect(self.rect(), QColor("Blue"))
        painter.setFont(self.font)
        y=(self.metrics.ascent()+self.window_height//2-(self.metrics.ascent()//2))
        painter.drawText(self.x_location,y, self.news_item[0])
    
    def get_next_news_item(self):
        
        self.counter+=1
        print(self.counter)
        if self.counter >= len(self.news_list) or not self.news_list:# if reached end or not loaded
            self.news_list=parse_feeds_to_list() #get new list of news and reset counter
            random.shuffle(self.news_list)
            self.counter=0
        if not self.news_list:
            return ["looking for news",""]
        return self.news_list[self.counter]
        #return 1 item of the list which itself a list of two items [string, link]
        
        
    def mousePressEvent(self, event):
        print("mousePressEvent")
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None
if __name__ == '__main__':
    if sys.platform.startswith("linux"):
        if os.environ.get("XDG_SESSION_TYPE") == "wayland":
            os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication(sys.argv)

    window = MyRibbon()
    window.show()
    sys.exit(app.exec())

# from PySide6.QtWidgets import QColorDialog
#
# color = QColorDialog.getColor()
#
# if color.isValid():
#     print(color.name())