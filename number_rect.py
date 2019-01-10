import sys
#通过pip3 install pyqt5 在控制台下载PyQt5库
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class NumberRect(QLabel): #QLable类主要用来文本和图像的显示没有提供交互功能 实例化qlabel
    animation = None
#动画默认值为空
    color_dict = {"2": "#eee4da", "4": "#ede0c8", "8": "#f2b179", "16": "#f59563", "32": "#f67c5f",
                  "64": "#f65e3b", "128": "#edcf72", "256": "#edcc61", "512": "#EFCB52",
                  "1024": "#EFC739", "2048": "#EFC329", "4096": "#FF3C39"}
#通过color_dict字典设置每个数字背景色
    font_color_dict = {"2": "#776e65", "4": "#776e65", "8": "#ffffff", "16": "#ffffff", "32": "#ffffff",
                       "64": "#ffffff", "128": "#ffffff", "256": "#776e65", "512": "#776e65",
                       "1024": "#776e65", "2048": "#776e65", "4096": "#ffffff"}
#通过color_dict字典设置每个数字字体颜色
    def __init__(self, parent, width, ds):     #__init__是pytnon的构造方法，用其初始化新创建对象之后，可以直接被调用
        super(NumberRect, self).__init__(parent)  #super类似于嵌套的一种设计，子类在父类前，所有类不重复调用，从左往右，继承父类的构造方法
        self.ds = ds
        self.w = width  #窗口宽度
        self.resize(width, width)  #调整窗口大小
        self.setFont(QFont("\"Clear Sans\", \"Helvetica Neue\", Arial, sans-serif", 55, QFont.Bold))  #设置字体样式
        self.setAlignment(Qt.AlignCenter)  #设置对其方式（居中对其）
        self.refresh_ds(ds) #恢复函数

    def refresh_ds(self, ds):
        self.ds = ds
        self.setText(str(ds["num"]))    #设置文本格式
        self.move(ds["x"], ds["y"])    #移动位置
        color = self.color_dict[str(ds["num"])]           #背景颜色 
        font_color = self.font_color_dict[str(ds["num"])]             #字体颜色  把定义的字体颜色列表插入字典
        self.setStyleSheet("QLabel{background-color:" + color + ";color:" + font_color + ";border-radius:3}") #设置窗口表格格式
        font_size = 55                                                  #字体大小55号
        if 100 <= ds["num"] <= 999: font_size = 40                    #根据数字位数适当调整字体大小
        if 1000 <= ds["num"] <= 9999: font_size = 30
        if 10000 <= ds["num"] <= 99999: font_size = 20
        self.setFont(QFont("\"Clear Sans\", \"Helvetica Neue\", Arial, sans-serif", font_size, QFont.Bold))

    def move_animation(self):    #移动动画         #位置
        self.animation = QPropertyAnimation(self, "pos".encode())     #动画Qt属性的类 给予我们极大的自由度来动画修改那些已存在的widget和其它QObject。
        self.animation.setDuration(150)     #窗口出现速度0.15秒
        self.animation.setStartValue(QPoint(0, 0))
        self.animation.setEndValue(QPoint(300, 300))     #窗口出现位置
        self.animation.setEasingCurve(QEasingCurve.Linear)   #让动画按照线性移动 
        self.animation.start(QAbstractAnimation.DeleteWhenStopped)   #动画结束后进行清理原本位置数字

    def combine_animation(self):
        self.animation = QPropertyAnimation(self, "size".encode())
        self.animation.setDuration(150)
        self.animation.setStartValue(QSize(107, 107))
        self.animation.setEndValue(QSize(300, 300))
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animation.finished.connect(self.finish_com_anim)
        self.animation.start(QAbstractAnimation.DeleteWhenStopped)

    def finish_com_anim(self):
        self.animation = QPropertyAnimation(self, "size".encode())
        self.animation.setDuration(150)
        self.animation.setStartValue(QSize(300, 300))
        self.animation.setEndValue(QSize(107, 107))
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animation.start(QAbstractAnimation.DeleteWhenStopped)
