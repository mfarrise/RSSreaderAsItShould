import os
import random
import re
import sys
import webbrowser

from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QFont, QFontMetrics, QPaintEvent, QColor, Qt
from feedParsing import parse_feeds_to_list
from settings import SettingsWindow
from jsonResolve import load_json

class MyRibbon(QWidget):
    def __init__(self):
        super().__init__()
        self.default_settings_dict = {
            "back_ground_color": "blue",
            "font_color": "yellow",
            "font_size": 21,
            "opacity": 1,
            "speed": 2,
            "window_height":40
        }

        self.settings_dict= load_json("settings.json",self.default_settings_dict)

        self.back_ground_color = self.settings_dict["back_ground_color"]
        self.scroll_speed=self.settings_dict["speed"] #the one from the settings
        self.applied_scroll_speed=self.scroll_speed    #the one applied ((needed for start and stop
        self.font_size=self.settings_dict["font_size"]
        self.font_color=self.settings_dict["font_color"]
        self.window_opacity=self.settings_dict["opacity"]
        self.window_height =self.settings_dict["window_height"]

        self.settings_window=None
        self.counter=-1
        self.news_list=[]
        self.setWindowOpacity(self.window_opacity)
        self.font = QFont("Ubuntu", self.font_size)
        self.font.setBold(True)
        self.metrics = QFontMetrics(self.font)
        self.news_item=self.get_next_news_item()
        self.text_width = self.metrics.horizontalAdvance(self.news_item[0])
        self.temp_speed=None
        self.shown_text=None

        
        self.timer=QTimer()
        self.timer.timeout.connect(self.update_text_position)
        self.timer.start(16)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        

        self.screen_geo=QApplication.primaryScreen().availableGeometry()
        self.x_location=self.screen_geo.width()

        self.setGeometry(0,self.screen_geo.height(),self.screen_geo.width(),self.window_height)
        
                


    def update_text_position(self):
        

        self.x_location -= self.applied_scroll_speed
        if self.x_location < -(self.text_width):
            self.x_location = self.screen_geo.width()
            self.news_item=self.get_next_news_item()
            self.text_width = self.metrics.horizontalAdvance(self.news_item[0])

            # print(self.news_item)
        self.update()
    def paintEvent(self, event):
        
            
        painter = QPainter(self)

        painter.setPen(QColor(self.font_color))
        painter.fillRect(self.rect(), QColor(self.back_ground_color))
        painter.setFont(self.font)
        y=(self.metrics.ascent()+self.window_height//2-(self.metrics.ascent()//2))
        painter.drawText(self.x_location,y, self.news_item[0])
    
    def get_next_news_item(self):
        
        self.counter+=1
        # print(self.counter)
        if self.counter >= len(self.news_list) or not self.news_list:# if reached end or not loaded
            self.news_list=parse_feeds_to_list() #get new list of news and reset counter
            random.shuffle(self.news_list)
            self.counter=0
        if not self.news_list:
            return ["looking for news",""]
        self.news_list[self.counter][0]=re.sub(r"<.*?>", "", self.news_list[self.counter][0])
        return self.news_list[self.counter]
        #return 1 item of the list which itself a list of two items [string, link]
        
        
    def mousePressEvent(self, event):
        print("mousePressEvent")
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

            if self.applied_scroll_speed !=0:
                self.temp_speed = self.applied_scroll_speed  # keep the value u for when moving again
                self.applied_scroll_speed = 0

            elif self.applied_scroll_speed ==0:
                self.applied_scroll_speed = self.temp_speed
        if event.button() ==Qt.RightButton:
            print("right clicked")
            self.settings_window=SettingsWindow(self)
            # self.settings_window.setParent(self)
            self.settings_window.show()
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        print("scroll spped:",self.applied_scroll_speed)
        print("Scroll:", delta)
        if self.applied_scroll_speed >=40 :
            self.applied_scroll_speed =39
        if self.applied_scroll_speed <40 :
            self.applied_scroll_speed+=delta//50
            if self.applied_scroll_speed <0:
                self.applied_scroll_speed=0

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def mouseDoubleClickEvent(self, event):
        webbrowser.open(self.news_item[1])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            print("Escape pressed")
            self.close()




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


#corystream
#
# pyinstaller main.py \
# --noconfirm \
# --onedir \
# --console \
# --copy-metadata PySide6 \
# --distpath build_output/dist \
# --workpath build_output/build \
# --specpath build_output
