import sys
from PyQt6 import QtGui
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QLabel, QLineEdit
from widgets import *
import yaml
import os
import platform


class setting(tabWidget):
    def __init__(self):
        super().__init__()
        # 获取配置
        with open("config.yml", "r") as fp:
            config = fp.read()
        self.config = yaml.load(config, yaml.SafeLoader)
        self.config_backup = yaml.load(config, yaml.SafeLoader)
        # btn
        self.save_btn.setText("保存")
        self.cancel_btn.setText("返回")
        self.setSaveMethod(self.save)
        self.setCancelMethod(self.cancel)
        # 基础设置
        basic_i = QListWidgetItem("启动器")
        basic_layout = QGridLayout()
        # 程序
        basic_program_label = QLabel("程序：")

        self.basic_program_input = QLineEdit()
        self.basic_program_input.setStyleSheet("background-color: white")
        self.basic_program_input.setText(self.config["basic"]["program"])
        self.basic_program_input.textChanged.connect(self.config_change("basic", "program"))

        self.basic_program_file_btn = QPushButton("...")
        self.basic_program_file_btn.setFixedWidth(30)
        self.basic_program_file_btn.setStyleSheet("background-color: white")
        self.basic_program_file_btn.clicked.connect(self.choice_file_path(
            None, self.basic_program_input, "basic", "program"
        ))

        basic_layout.addWidget(basic_program_label, 0, 0)
        basic_layout.addWidget(self.basic_program_input, 0, 1)
        basic_layout.addWidget(self.basic_program_file_btn, 0, 2)
        # 参数
        basic_arguments_label = QLabel("参数：")

        self.basic_arguments_input = QLineEdit()
        self.basic_arguments_input.setStyleSheet("background-color: white")
        if isinstance(self.config["basic"]["arguments"], list):
            self.basic_arguments_input.setText(",".join(self.config["basic"]["arguments"]))
        else:
            self.basic_arguments_input.setText(self.config["basic"]["arguments"])
        self.basic_arguments_input.textChanged.connect(self.config_change("basic", "arguments"))

        basic_layout.addWidget(basic_arguments_label, 1, 0)
        basic_layout.addWidget(self.basic_arguments_input, 1, 1)
        # 工作目录
        basic_work_dir_label = QLabel("工作目录：")

        self.basic_work_dir_input = QLineEdit()
        self.basic_work_dir_input.setStyleSheet("background-color: white")
        self.basic_work_dir_input.setText(self.config["basic"]["work_dir"])
        self.basic_work_dir_input.textChanged.connect(self.config_change("basic", "work_dir"))

        self.basic_work_dir_btn = QPushButton("...")
        self.basic_work_dir_btn.setFixedWidth(30)
        self.basic_work_dir_btn.setStyleSheet("background-color: white")
        self.basic_work_dir_btn.clicked.connect(self.choice_file_path(
            None, self.basic_work_dir_input, "basic", "work_dir"
        ))

        basic_layout.addWidget(basic_work_dir_label, 2, 0)
        basic_layout.addWidget(self.basic_work_dir_input, 2, 1)
        basic_layout.addWidget(self.basic_work_dir_btn, 2, 2)

        self.addItem(basic_i, basic_layout)

    def choice_file_path(self, filter: str, widget: QLineEdit, first: str, second: str):
        def wrapper():
            # if platform.system() == "Windows":
            #     url = r".\\"
            # else:
            #     url = r"./"
            file_url, _ = QFileDialog().getOpenFileUrl(self, "Open File", QUrl(),
                                                       filter)
            self.config[first][second] = file_url.path()
            widget.setText(file_url.path())
        return wrapper

    def save(self):
        config = yaml.dump(self.config, Dumper=yaml.SafeDumper)
        print(config)
        with open("config.yml", "w") as fp:
            fp.write(config)
        self.hide()

    def cancel(self):
        self.config = self.config_backup
        print(self.config)
        print(self.config_backup)
        self.hide()

    def config_change(self, first: str, second: str):
        def on_textChange(s):
            if len(s.split(",")) > 1:
                self.config[first][second] = s.split(",")
            else:
                self.config[first][second] = s
        return on_textChange

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        # 修改show事件，再次打开后修改为原配置的数值
        self.basic_program_input.setText(self.config["basic"]["program"])
        if isinstance(self.config["basic"]["arguments"], list):
            self.basic_arguments_input.setText(",".join(self.config["basic"]["arguments"]))
        else:
            self.basic_arguments_input.setText(self.config["basic"]["arguments"])

    def test_interpreter(self):
        text = os.popen(f'{self.config["basic"]["arguments"]} -V').read()
        if "Python" in text and len(text.split(" ")) == 2:
            version = text.split(" ")[1]
            QMessageBox.information(self, "成功", f"\n成功\nPython\n版本：{version}")
        else:
            QMessageBox.warning(self, "失败", f"失败\n不是有效的Python解释器")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = setting()
    window.show()
    app.exec()
