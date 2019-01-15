# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 16:21:58 2019

@author: Administrator
"""

class GameCalculate:#定义一个GameCalculate类
    def __init__(self, item_data):#当调用类的实例化方法时__init__()方法被调用进行初始化
        self.data = item_data

    def calculate(self, direction):#定义一个calculate()方法执行矩阵各个方向的操作，根据移动方向，计算矩阵的状态值
        if len(self.data) <= 0:
            return 0
        if direction == 1:
            self.up_run()
        if direction == 2:
            self.down_run()
        if direction == 3:
            self.left_run()
        if direction == 4:
            self.right_run()

    def get_data(self):#定义get_data()方法返回当前方格中的数值
        return self.data

    def up_run(self):#定义一个up_run()方法捕捉用户向上动作时所执行的操作
        for i in range(0, 4):#遍历每一行
            k = None
            for j in range(0, 4):
                l = self.data[j][i] #矩阵中的每一列复制到一个列表中然后处理
                if k and l["Number"] != 0:
                    k_v = self.data[k["j"]][k["i"]]
                    if k_v["Number"] == l["Number"]:
                        self.data[k["j"]][k["i"]]["Number"] = k_v["Number"] + l["Number"]#用处理后的列表中的数字覆盖掉原来矩阵中的值
                        self.data[j][i] = {"Item": None, "Number": 0}
                        k = None
                    else:
                        if l["Number"] != 0: k = {"i": i, "j": j}
                else:
                    k = {"i": i, "j": j}
#每一列从上到下开始遍历 ，有相邻的相同数字的话就向上叠加，下面的方格置为空，依次循环，没有相同的数字就加入字典中。
        for i in range(0, 4):
            for j in range(0, 4):
                if self.data[j][i]["Number"] != 0:#存在空白区域
                    if j != 0:
                        for k in range(0, j):
                            if self.data[k][i]["Number"] == 0:
                                swap = self.data[k][i]
                                self.data[k][i] = self.data[j][i]
                                self.data[j][i] = swap
                                break
#叠加完成之后，从剩余的空的方格中随机选取第k个方格填充随机生成的数字
    def down_run(self):
        for i in range(0, 4):
            k = None
            for j in range(3, -1, -1):#按列从下往上遍历每一行
                l = self.data[j][i]
                if k and l["Number"] != 0:
                    k_v = self.data[k["j"]][k["i"]]
                    if k_v["Number"] == l["Number"]:
                        self.data[k["j"]][k["i"]]["Number"] = k_v["Number"] + l["Number"]
                        self.data[j][i] = {"Item": None, "Number": 0}
                        k = None
                    else:
                        k = {"i": i, "j": j}
                else:
                    if l["Number"] != 0: k = {"i": i, "j": j}

        for i in range(0, 4):
            for j in range(0, 4):
                if self.data[3 - j][i]["Number"] != 0:
                    if 3 - j != 3:
                        for k in range(3, 3 - j - 1, -1):
                            if self.data[k][i]["Number"] == 0:
                                swap = self.data[k][i]
                                self.data[k][i] = self.data[3 - j][i]
                                self.data[3 - j][i] = swap
                                break

    def left_run(self):#定义方法捕捉用户向左滑动时所要执行的操作
        for i in range(0, 4):#遍历每一行
            k = None
            for j in range(0,4):#遍历每一列
                l = self.data[i][j]#将遍历到的数字存入二维列表中
                if k and l["Number"] != 0:#如果k不是0且列表非空
                    k_v = self.data[k["i"]][k["j"]]#将k中的数字复制给一个新列表
                    if k_v["Number"] == l["Number"]:#如果相邻两数相同
                        self.data[k["i"]][k["j"]]["Number"] = k_v["Number"] + l["Number"]#合并
                        self.data[i][j] = {"Item": None, "Number": 0}
                        k = None
                    else:
                        k = {"i": i, "j": j}
                else:
                    if l["Number"] != 0: k = {"i": i, "j": j}
        for i in range(0, 4):
            for j in range(0, 4):
                if self.data[i][j]["Number"] != 0:#还存在空格
                    if j != 0:
                        for k in range(0, j):
                            if self.data[i][k]["Number"] == 0:
                                swap = self.data[i][k]
                                self.data[i][k] = self.data[i][j]
                                self.data[i][j] = swap
                                break
#在剩下的空格中随机选取第k个填充一个随机产生的数字
    def right_run(self):
        for i in range(0, 4):
            k = None
            for j in range(3, -1, -1):#从右向左遍历每一列的每一个元素
                l = self.data[i][j]#将遍历到的非0的数放入列表
                if k and l["Number"] != 0:
                    k_v = self.data[k["i"]][k["j"]]#将第i行j列左边非0的数放入列表
                    if k_v["Number"] == l["Number"]:#相同
                        self.data[k["i"]][k["j"]]["Number"] = k_v["Number"] + l["Number"]#叠加合并
                        self.data[i][j] = {"Item": None, "Number": 0}#左边的数置0
                        k = None#清空
                    else:#两数不同，数值不变存入字典中
                        k = {"i": i, "j": j}
                else:
                    if l["Number"] != 0: k = {"i": i, "j": j}
        for i in range(0, 4):
            for j in range(0, 4):
                if self.data[i][3 - j]["Number"] != 0:
                    if 3 - j != 3:
                        for k in range(3, 3 - j - 1, -1):
                            if self.data[i][k]["Number"] == 0:
                                swap = self.data[i][k]
                                self.data[i][k] = self.data[i][3 - j]
                                self.data[i][3 - j] = swap
                                break

