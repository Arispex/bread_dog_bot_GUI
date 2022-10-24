from PyQt6.QtCore import Qt, QSize, QProcess
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QToolBar, QStatusBar, QTextBrowser, QVBoxLayout, QLineEdit, \
    QWidget, QMessageBox
import re
import models
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bread Dog Bot")
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.running = False  # 是否在运行
        # 菜单
        menu = self.menuBar()
        # 菜单-bdt
        btd = menu.addMenu("BreadDogBot")
        about = QAction("关于", self)
        about.triggered.connect(self.about)
        btd.addAction(about)

        self.textColor = "black"
        # 工具栏
        self.toolbar = QToolBar("main")
        self.toolbar.setIconSize(QSize(48, 48))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.addToolBar(self.toolbar)
        # 工具栏-开始按钮
        start = QAction(QIcon("img/start.png"), "开始", self)
        start.setStatusTip("开始运行Bread Dog Bot")
        start.triggered.connect(self.start)
        self.toolbar.addAction(start)
        # 工具栏-停止按钮
        stop = QAction(QIcon("img/stop.png"), "停止", self)
        stop.setStatusTip("停止运行Bread Dog Bot")
        stop.triggered.connect(self.stop)
        self.toolbar.addAction(stop)
        # 工具栏-设置
        setting = QAction(QIcon("img/setting.png"), "设置", self)
        setting.setStatusTip("修改机器人配置")
        setting.triggered.connect(self.show_setting)
        self.toolbar.addAction(setting)
        # 状态栏
        self.setStatusBar(QStatusBar(self))

        self.layout = QVBoxLayout()
        # 文本浏览器显示信息
        self.cli = QTextBrowser()
        self.layout.addWidget(self.cli)
        # 命令输入框
        self.command_input = QLineEdit()
        self.command_input.returnPressed.connect(self.exec_command)
        self.layout.addWidget(self.command_input)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        # 新进程
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.on_readyReadStandardOutput)
        # 设置页面
        self.setting = models.setting()

    def exec_command(self):
        self.cli.append(f"[Console]你执行了 /{self.command_input.text()}")
        if hasattr(self, self.command_input.text()):
            attr = getattr(self, self.command_input.text())
            self.add_text("<span style=\" color:#78BF64;\" >执行成功</span>")
            attr()
        else:
            self.add_text("<span style=\" color:#DEB368;\" >未知的命令</span>")
        self.command_input.setText("")

    def add_text(self, s):
        self.cli.append(f"[Console]{s}")

    def on_readyReadStandardOutput(self):
        try:
            text = self.process.readAllStandardOutput().data().decode()
        except Exception:
            self.add_text("似乎遇到了编码问题，这应该是go-cqhttp的消息，请在Web端查看。")
            return
        text = re.sub(r"\[[0-9]{1,3}[a-z]", "", text)  # 去除不生效的颜色代码
        # if re.match(r".*[0-9]+", text):
        #     text = f"[Console]{text}"
        text = re.sub(r"+", "", text)
        r = "<span style=\" color:#000000;\" >"

        # 替换时间颜色
        matcher = re.match(r"(\d+-\d+ \d+:\d+:\d+).*?", text)
        if matcher:
            text = text.replace(
                matcher.group(1), f'<span style=\" color:#78BF64;\" >{matcher.group(1)}</span>', 1
            )

        # 替换昵称颜色
        matcher = re.match(r".*?] (.*?) \|.*?", text)
        if matcher:
            text = text.replace(
                matcher.group(1), f'<span style=\" color:#27ACB6;\" >{matcher.group(1)}</span>', 1
            )

        # 替换 SUCCESS 颜色
        text = text.replace(
            "SUCCESS", f'<span style=\" color:#78BF64;\" >SUCCESS</span>', 1
        )

        # 替换 DEBUG 颜色
        text = text.replace(
            "DEBUG", f'<span style=\" color:#519DEA;\" >DEBUG</span>', 1
        )

        # 替换 WARNING 颜色
        text = text.replace(
            "WARNING", f'<span style=\" color:#DEB368;\" >WARNING</span>'
        )

        if text.startswith("Traceback"):  # 判断是否是报错
            self.textColor = "red"  # 报错则修改颜色

        if self.textColor == "red":  # 修改颜色
            r = "<span style=\" color:#ff0000;\" >"

        if "Error" in text:  # 报错结束
            self.textColor = "black"

        r += text
        r += "</span>"
        self.cli.append(r)

        if "Error" in text:  # 报错娱乐（doge
            self.add_text(
                "<span style=\" color:#DEB368;\" >好奇怪哦，怎么报错了呢，相信聪明的你，一定可以自己解决吧！</span>")
            self.textColor = "black"

    def start(self):
        if not self.running:
            self.add_text("正在设置工作目录...")
            os.chdir(self.setting.config["basic"]["work_dir"])
            self.add_text("正在启动...")
            if isinstance(self.setting.config["basic"]["arguments"], list):
                self.process.start(self.setting.config["basic"]["program"], self.setting.config["basic"]["arguments"])
            else:
                self.process.start(self.setting.config["basic"]["program"], [self.setting.config["basic"]["arguments"]])
            self.running = True
        else:
            QMessageBox.information(self, "提示", "Bread Dog Bot已经在运行了，\n请勿再次运行。")

    def stop(self):
        if self.running:
            self.add_text("正在关闭...")
            self.process.kill()
            self.add_text("关闭成功")
            self.running = False
        else:
            QMessageBox.information(self, "提示", "Bread Dog Bot还没有运行。")

    def about(self):
        QMessageBox.about(self, "关于", "Bread Dog Bot\n\n\n"
                                        "版本：v1.8 \t2022年10月24日\n\n"
                                        "Github: https://github.com/Qianyiovo/breadDogBot\n\n"
                                        "Copyright © 2022-present Qianyiovo"
                          )

    def show_setting(self):
        self.setting.show()
