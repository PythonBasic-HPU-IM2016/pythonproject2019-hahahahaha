import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from game_calculate import GameCalculate
from number_rect import NumberRect


class GameCanvas(QLabel):
    # 只读的背景16个方格
    item_bgs = []
    # 背景16个方格的xy位置也是只读的
    item_bg_pos = []
    item_data = []

    parent_x = 20
    parent_y = 20
    split_width = 16
    rect_width = 105

    def __init__(self, parent):
        super(GameCanvas, self).__init__(parent)
        self.parent = parent

        self.resize(500, 500)
        self.move(self.parent_x, self.parent_y)
        self.setStyleSheet("QLabel{background-color:#bbada0;color:#bbada0;border-radius:6}")

        self.setFocusPolicy(Qt.StrongFocus)
        self.set_item_bg()
        self.set_init_rect()

    def set_init_rect(self):
        self.random_rect_item()
        self.random_rect_item()

    def set_item_bg(self):
        for i in range(1, 5):
            bgs = []
            pos = []
            ds = []
            for j in range(1, 5):
                x = self.parent_x + self.split_width * j + self.rect_width * (j - 1)
                y = self.parent_y + self.split_width * i + self.rect_width * (i - 1)
                label = QLabel(self.parent)
                label.resize(self.rect_width, self.rect_width)
                label.move(x, y)
                label.setStyleSheet("QLabel{background-color:#cdc1b4;color:#cdc1b4;border-radius:3}")
                bgs.append(label)
                pos.append({"x": x, "y": y})
                ds.append({"Item": None, "Number": 0})
            self.item_bgs.append(bgs)
            self.item_bg_pos.append(pos)
            self.item_data.append(ds)

   def random_rect_item(self):#产生随机数坐标
        zero_ds = []#定义一个空列表
        for i in range(0, 4):
            for j in range(0, 4):
                if self.item_data[i][j]["Number"] == 0:#如果出现空格
                    zero_ds.append({"i": i, "j": j})##将第i行j列的值加入到列表中

        if len(zero_ds) > 0:                 #列表非空
            rnd = int(random.uniform(0, len(zero_ds)))#在列表长度范围内随机产生一个整数
            k = int(random.uniform(0, 10))#k为0到10之间的随机整数
            number = 2                    #初始化number
            if k == 2 or k == 10:
                number = 4#产生随机数
            d = zero_ds[rnd]#将产生的随机数赋值给d
            d["num"] = number
            d["x"] = self.item_bg_pos[d["i"]][d["j"]]["x"]
            d["y"] = self.item_bg_pos[d["i"]][d["j"]]["y"]
                                                 #得到随机数的坐标位置
            rect = NumberRect(self.parent, self.rect_width, d)
            self.item_data[d["i"]][d["j"]]["Number"] = number
            self.item_data[d["i"]][d["j"]]["Item"] = rect
            rect.show()   #得到相对应的数字颜色，方格背景，最后显示出来

            return self.item_data[d["i"]][d["j"]]
        else:
            reply = QMessageBox.question(self.parent, '提示信息',
                                         "您已经输了，是否重新开始?", QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                print("OK")
            else:
                print("NO")
        return None
#没有空格，棋盘已满，输出提示窗口游戏失败
　　　　def keyPressEvent(self, QKeyEvent):#定义 keyPressEvent()函数获取按键信息
        if QKeyEvent.key() == Qt.Key_Up:
            self.reset_rect(1)#调用up_run()方法
        elif QKeyEvent.key() == Qt.Key_Down:
            self.reset_rect(2)
        elif QKeyEvent.key() == Qt.Key_Left:
            self.reset_rect(3)
        elif QKeyEvent.key() == Qt.Key_Right:
            self.reset_rect(4)

    def reset_rect(self, direction):#重置棋盘函数
        print("方向:" + str(direction))#打印方向+数字
        items = []
        for i in range(0, 4):
            for j in range(0, 4):
                item = self.item_data[i][j]["Item"]
                if item:
                    items.append(item)#将之前产生的随机数加入棋盘中

        calculate = GameCalculate(self.item_data)#调用GameCalculate类进行当前数字的合并计算
        calculate.calculate(direction)#得到方向确定应调用的函数
        self.item_data = calculate.get_data()

        for d in self.item_data:
            print(d)
        for p in self.item_bg_pos:
            print(p)

        self.redraw_rect(items)
        self.check_is_win()
        self.random_rect_item()

    def redraw_rect(self, items):#重新定义画布函数
        for i in range(0, 4):
            for j in range(0, 4):
                item = self.item_data[i][j]["Item"]
                if item:
                    items.remove(item)
                    x = self.item_bg_pos[i][j]["x"]
                    y = self.item_bg_pos[i][j]["y"]#得到当前数字坐标
                    ds = item.ds
                    ds["x"] = x
                    ds["y"] = y
                    ds["num"] = self.item_data[i][j]["Number"]
                    item.refresh_ds(ds)#得到更新后的数字颜色
        for k in items:
            if k: k.hide()
        del items

    def check_is_win(self):#再次检查游戏是否胜利
        for i in range(0, 4):
            for j in range(0, 4):
                item = self.item_data[i][j]["Item"]
                if item and item.ds["num"] == 2048:#每行每列遍历，如果存在方格中的数等于2048，
                    reply = QMessageBox.question(self.parent, '提示信息',
                                                 "真厉害，你已经赢了是否继续往上挑战？", QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        print("OK")
                    else:
                        print("NO")#输出提示信息
