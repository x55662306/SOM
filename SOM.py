# -*- coding: utf-8 -*-
import numpy as np;
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import math
from PyQt5 import QtWidgets, QtCore
import time

            
#Training
class Thread(QtCore.QThread):

    update = QtCore.pyqtSignal(int)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.rate = 0.0
        self.count = 0
        self.count = 0
        self.progress_bar = QtWidgets.QProgressBar()
        self.train_acc_text = ""
        self.test_acc_text = ""
        self.weight = ""
    
    def __del__(self):
        self.wait()

    
    def set(self, rate, rnd, count, rpp, figure, canvas):
        self.rate = rate
        self.round = rnd
        self.count = count
        self.canvas = canvas
        self.figure = figure
        self.rpp = rpp

    def run(self):
        self.progress_bar.setValue(0)
        
        #Set iteration
        it = self.round
        #Set learning rate
        lr = self.rate
        lr_o = self.rate
        #計算維度
        dim = 3
        #拿資料
        data = get_data(10, 10)
        #Set Weight 
        w = [random.uniform(-1, 1)] * (dim)
        #改資料型態
        train_data = np.empty(shape=[0, dim + 1])
        
        for i in range(len(data)):
                train_data = np.row_stack((train_data, data[i]))
        #best accuracy
        b_acc = 0
        
        #Training
        plot_cnt = 0
        for i in range(it):
            for k in range(len(train_data)):
                y = np.dot(train_data[k, 0:3], w)
                if sgn(y) == 2 and train_data[k, 3] == 1 :
                    w = w - lr*train_data[k, 0:3]
                    plot_cnt += 1
                    if i%self.rpp==0:
                        self.plot(train_data, w)
                        print('Times: ', plot_cnt)
                        self.plot2(train_data, w)
                        time.sleep(0.02)
                elif sgn(y) == 1 and train_data[k, 3] == 2 :
                    w = w + lr*train_data[k, 0:3]
                    plot_cnt += 1
                    if i%self.rpp==0:
                        self.plot(train_data, w)
                        print('Times: ', plot_cnt)
                        self.plot2(train_data, w)
                        time.sleep(0.02)
            #計算最佳訓練精準度
            cnt = 0
            for k in range(len(train_data)):
                y = np.dot(train_data[k, 0:3], w)
                if sgn(y) == train_data[k, 3]:
                    cnt = cnt + 1
            acc = cnt/len(train_data)
            if acc > b_acc :
                b_acc = acc
                b_w = w
            if acc == 1:
                break
            ###################
            
            #調整訓練速率
            lr = lr_o * ( ( it - i ) / it)
            self.progress_bar.setValue((i/it)*100) 
        #顯示權重
        self.weight = str(b_w)
        self.progress_bar.setValue(100)
            
        #顯示精準度
        self.train_acc_text = str(b_acc * 100)

        self.plot(train_data, b_w)
        
    
    def get_pic(self):
        return self.dr
    
        
    def plot(self, data, w):
        self.figure.clear()

        # create an axis
        axes = self.figure.add_subplot(111)
        #Plot point 
        color = {
                    1:'red',
                    2:'blue',
                    3:'yellow',
                    4:'green'
                }
        for i in range(len(data)):
            axes.scatter(data[i, 1], data[i, 2], color=color[data[i, 3]], s = 15, alpha=0.8)
        #Plot line
        a = np.arange(-15, 15, 0.1)
        b =( w[0] + -1*w[1]*a ) / w[2] 
        axes.plot(a, b)
        axes.set_xlim(max(data[:, 1]) + 1, min(data[:, 1]) - 1)
        axes.set_ylim(max(data[:, 2]) + 1, min(data[:, 2]) - 1)
        self.canvas.draw()
    def plot2(self, data, w):
        #Plot point 
        color = {
                    1:'red',
                    2:'blue',
                    3:'yellow',
                    4:'green'
                }
        for i in range(len(data)):
            plt.scatter(data[i, 1], data[i, 2], color=color[data[i, 3]], s = 15, alpha=0.8)
        #Plot line
        a = np.arange(-15, 15, 0.1)
        b =( w[0] + -1*w[1]*a ) / w[2] 
        plt.plot(a, b)
        plt.xlim(max(data[:, 1]) + 1, min(data[:, 1]) - 1)
        plt.ylim(max(data[:, 2]) + 1, min(data[:, 2]) - 1)
        plt.show()
        
    
    
#GUI
class Input(QtWidgets.QWidget):

    def __init__(self, parent = None):

        super().__init__(parent)
        self.progress_bar = []
        self.Thread_List = []      #初始化時指派一個線程
        self.progress_bar = []
        self.fileName = ""
        self.graphicscene = QtWidgets.QGraphicsScene()
        self.rate = 0.0
        self.round = 0
        self.count = 0
        self.group = 0
        self.count = 0
        
        self.layout = QtWidgets.QFormLayout()
        self.Label2 = QtWidgets.QLabel("Learning rate")
        self.tmp2 = QtWidgets.QLineEdit()
        self.layout.addRow(self.Label2, self.tmp2)
        
        self.Label3 = QtWidgets.QLabel("Round")
        self.tmp3 = QtWidgets.QLineEdit()
        self.layout.addRow(self.Label3, self.tmp3)
        
        self.Label5 = QtWidgets.QLabel("round per picture")
        self.tmp5 = QtWidgets.QLineEdit()
        self.layout.addRow(self.Label5, self.tmp5)

        self.btn = QtWidgets.QPushButton('Ok')
        self.btn.clicked.connect(self.grab)
        self.layout.addRow(self.btn)
        
        self.Label4 = QtWidgets.QLabel("Train")
        self.layout.addRow(self.Label4)
               
        self.figure = plt.figure(figsize=(7,7))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addRow(self.canvas)
        
        
        self.setLayout(self.layout)
        self.setWindowTitle("HW2")
        self.setGeometry(100, 150, 800, 800)


    def grab(self):             #多線程處理
        print("Get process!")
        self.rate = float(self.tmp2.text())
        self.round = int(self.tmp3.text())
        self.rpp = int(self.tmp5.text())
        self.arrange = False
        self.count += 1
        self.check()
            
    def check(self):
        if self.rate <= 0 or self.round <= 0:
            print("Invalid input")
            return None
    
        for Threads in self.Thread_List:
            if not Threads.isRunning():
                self.arrange = True
                Threads.set(self.rate, self.round, self.count,self.rpp, self.figure, self.canvas)
                Threads.start()
                break
        if not self.arrange:
            if len(self.Thread_List) <= 10:
                self.Thread_List.append(Thread())                    #新增一個Thread到最後面
                self.Thread_List[-1].set(self.rate, self.round, self.count, self.rpp, self.figure, self.canvas)
                self.layout.addRow(self.Thread_List[-1].progress_bar)
                self.Thread_List[-1].start()                         #將最後一個Thread指派程序

            else:
                print("Out of Process")

        
def sgn(x):
    if x >= 0 :
        return 2
    else :
        return 1
    
def sgn_bin(x):
    if x >= 0 :
        return 1
    else :
        return 0

def get_data(r, n):
     a = random.uniform(-r, r)
     b = random.uniform(-r, r)
     c = random.uniform(-r/2, r/2)
     data = []
     cls1 = 0
     cls2 = 0
     cnt = 0
     while cnt < n:
         tmp = [-1, random.uniform(-r, r), random.uniform(-r, r)]
         result = a*tmp[1] + b*tmp[2] + c
         if result > 0 :
             cls1 += 1
             tmp.append(1)
             data.append(tmp)
         elif result < 0:
             cls2 += 1
             tmp.append(2)
             data.append(tmp)   
         cnt += 1
     return data
        
def main():
    
    app = QtWidgets.QApplication(sys.argv)
    window = Input()
    window.show()
     
    #close window 
    app.exec_()
    
def dist(x, y):  #x,y:點
    d = 0
    for i in range(len(x)) :
        d += math.pow(x[i] - y[i], 2) 
    d = math.sqrt(d)
    return d
    
if __name__ == "__main__":  
    main()