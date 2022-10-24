from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, \
    QStackedLayout, QLayout, QGridLayout, QPushButton


class tabWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(600)
        self.setFixedHeight(400)

        self.tabs = []
        self.layouts = []
        self.containers = []

        main_layout = QVBoxLayout()  # 主布局（垂直

        top_layout = QHBoxLayout()  # 上布局（水平
        main_layout.addLayout(top_layout)

        self.tab_bar = QListWidget()
        self.tab_bar.setFixedHeight(300)
        self.tab_bar.setFixedWidth(150)
        self.tab_bar.clicked.connect(self.change_top_right)
        top_layout.addWidget(self.tab_bar)

        self.top_right = QWidget()
        top_layout.addWidget(self.top_right)
        self.top_right.setFixedWidth(400)
        self.top_right.setFixedHeight(300)
        self.top_right.setStyleSheet("background-color: #D6D6D6")

        self.top_right_layout = QStackedLayout()
        self.top_right.setLayout(self.top_right_layout)

        button_layout = QGridLayout()  # 下局部（水平
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedWidth(70)
        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedWidth(70)
        button_layout.addWidget(self.cancel_btn, 0, 0)
        button_layout.addWidget(self.save_btn, 0, 3)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def addItem(self, item: QListWidgetItem, layout: QLayout):
        self.tab_bar.addItem(item)
        self.tabs.append(item.text())
        self.layouts.append(layout)

        widget = QWidget()
        widget.setLayout(layout)

        self.containers.append(widget)
        self.top_right_layout.addWidget(widget)

    def change_top_right(self, index: QModelIndex):
        self.top_right_layout.setCurrentIndex(self.tabs.index(index.data()))

    def setCancelMethod(self, f):
        self.cancel_btn.clicked.connect(f)

    def setSaveMethod(self, f):
        self.save_btn.clicked.connect(f)
