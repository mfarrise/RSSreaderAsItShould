from PySide6.QtGui import QIntValidator, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit

from WindowPositionManipulations import center_window
from colorPicker import pick_color
from editFeedsJson import edit_feeds_window
from getBaseDir import get_base_dir
from jsonResolve import load_json,write_json
import os
import sys


class SettingsWindow(QWidget):

    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window

        self.settings_dict = load_json(self.get_settings_path(), self.main_window.settings_dict)
        self.back_ground_color=""
        self.font_color=""
        self.window_opacity=1.0
        self.font_size=None
        self.window_height=40

        self.setFixedSize(300,300)
        self.setWindowTitle("CoryStream by M arise")
        self.layout = QGridLayout()
        self.setLayout(self.layout)


        self.back_ground_color_button = QPushButton("Background Color")
        self.back_ground_color_button.clicked.connect(self.pick_back_ground_color)

        self.font_color_button = QPushButton("Font Color")
        self.font_color_button.clicked.connect(self.pick_font_color)

        self.font_size_label = QLabel("Font size")
        self.font_size_line_edit = QLineEdit()
        self.font_size_line_edit.setText(str(self.main_window.font_size))
        self.font_size_line_edit.setValidator(QIntValidator())
        self.font_size_line_edit.returnPressed.connect(self.update_font_size)
        self.font_size_line_edit.textChanged.connect(self.update_font_size)

        self.opacity_label = QLabel("Opacity %")
        self.opacity_line_edit = QLineEdit()
        self.opacity_line_edit.setValidator(QIntValidator())
        self.opacity_line_edit.setText(str(int(self.main_window.window_opacity*100)))
        self.opacity_line_edit.returnPressed.connect(self.update_opacity)
        self.opacity_line_edit.textChanged.connect(self.update_opacity)


        self.window_height_label = QLabel("Window Height")
        self.window_height_line_edit = QLineEdit()
        self.window_height_line_edit.setValidator(QIntValidator())
        self.window_height_line_edit.setText(str(self.main_window.window_height))
        self.window_height_line_edit.textChanged.connect(self.update_window_height)

        self.edit_feeds_button = QPushButton("Edit Feeds")
        self.edit_feeds_button.clicked.connect(self.edit_feeds)

        self.okay_button = QPushButton("Okay")
        self.okay_button.clicked.connect(self.update_json_and_close)

        self.layout.addWidget(self.back_ground_color_button)
        self.layout.addWidget(self.font_color_button)
        self.layout.addWidget(self.font_size_label)
        self.layout.addWidget(self.font_size_line_edit)
        self.layout.addWidget(self.opacity_label)
        self.layout.addWidget(self.opacity_line_edit)
        self.layout.addWidget(self.window_height_label)
        self.layout.addWidget(self.window_height_line_edit)
        self.layout.addWidget(self.edit_feeds_button)
        self.layout.addWidget(self.okay_button)
        center_window(self)
    def pick_back_ground_color(self):
        self.back_ground_color = pick_color()
        self.main_window.back_ground_color = self.back_ground_color

    def pick_font_color(self):
        self.font_color = pick_color()
        self.main_window.font_color = self.font_color
        self.settings_dict["font_color"] = self.font_color

    def update_font_size(self  ):
        if self.font_size_line_edit:
            self.font_size=int(self.font_size_line_edit.text())
            self.main_window.font = QFont("Ubuntu", self.font_size)
            self.main_window.font.setBold(True)
            self.main_window.metrics = QFontMetrics(self.main_window.font)
            self.main_window.text_width = self.main_window.metrics.horizontalAdvance(self.main_window.news_item[0])
            self.settings_dict["font_size"] = self.font_size
    def update_opacity(self):
        if self.opacity_line_edit.text():
            if int(self.opacity_line_edit.text())>100:
                self.opacity_line_edit.setText("100")
            if int(self.opacity_line_edit.text())<1:
                self.opacity_line_edit.setText("10")
            self.window_opacity = float(int(self.opacity_line_edit.text())/100)
            self.main_window.setWindowOpacity(self.window_opacity)
            self.settings_dict["opacity"] = self.window_opacity
    def update_window_height(self):
        if self.window_height_line_edit.text():
            self.window_height=int(self.window_height_line_edit.text())
            self.main_window.setFixedHeight(self.window_height)
            self.settings_dict["window_height"] = self.window_height

    def edit_feeds(self):
        self.edit_feeds_window=edit_feeds_window()
        self.edit_feeds_window.show()
    def update_json_and_close(self):
        write_json(self.get_settings_path(), self.settings_dict)
        self.close()
    def get_settings_path(self):
        base = os.getenv("APPDATA")  # e.g. C:\Users\...\AppData\Roaming
        app_dir = os.path.join(base, "CoryStream")
        os.makedirs(app_dir, exist_ok=True)
        return os.path.join(app_dir, "settings.json")