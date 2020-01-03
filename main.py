#!/bin/python

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import QThread
from Ui_MainWindow import Ui_MainWindow as ui
import numpy as np
import csv
import os
import sys
import time

from PIL import Image
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.lines as mlines
import matplotlib.gridspec as gridspec
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib import patheffects

from scipy import ndimage
from scipy import misc


class morphgui(QtWidgets.QMainWindow, ui):
    def __init__(self):
        super(morphgui, self).__init__()
        self.setupUi(self)
        self.plotting1 = plotting()
        self.plotlayout1 = QtWidgets.QVBoxLayout()
        self.plotlayout1.addWidget(self.plotting1)
        self.plot1.setLayout(self.plotlayout1)

        self.plotting2 = plotting()
        self.plotlayout2 = QtWidgets.QVBoxLayout()
        self.plotlayout2.addWidget(self.plotting2)
        self.plot2.setLayout(self.plotlayout2)
        self.connectEvents()

    def connectEvents(self):
        print("Connecting Events")
        self.loadImage1.triggered.connect(self.loadFileAction)
        self.loadImage2.triggered.connect(self.loadFileAction)

    def loadFileAction(self,e):
        sender = self.sender()
        print(sender.text())
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            if "1" in sender.text():
                self.plotting1.loadImage(fileName)
            elif "2" in sender.text():
                self.plotting2.loadImage(fileName)


class plotting(FigureCanvas):
    points = [[400,400,'r'],[550,350,'r'],[400,200,'r'],[350,350,'r']]
    sel_point = False
    cur_point = []

    def __init__(self, parent=None, width=7, height=8,linewidth=2.0, dpi=100):
        self.legend= True
        self.full = False
        self.fig = Figure(figsize=(width, height),facecolor="grey", dpi=dpi)
        super(FigureCanvas, self).__init__(self.fig)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.MinimumExpanding,
                                    QtWidgets.QSizePolicy.MinimumExpanding)
        FigureCanvas.updateGeometry(self)
        self.setMouseTracking(False)
        self.fig.patch.set_facecolor("grey")
        self.axes = self.fig.add_axes([0.1, 0.1 , 0.8, 0.8 ])
        self.axes.set_facecolor("grey")
        self.axes.plot(range(1,10),range(1,10))
        self.mpl_connect("button_press_event",self.on_click)

    def on_click(self,event):
        print(event)
        x = event.xdata
        y = event.ydata
        print("{} {}".format(x,y))
        if not self.sel_point:
            i = 0
            ra = 10
            for point in self.points:
                if point[0]-x  <= ra and point[0]-x >=-ra and point[1]-y <=ra and point[1]-y >=-ra:
                    print("Point {} selected".format(point))
                    print(self.points)
                    point[2]='g'
                    self.cur_point = i
                    self.sel_point = True
                    self.facePointsSetup()
                i = i + 1
        elif self.sel_point:
            self.points[self.cur_point] = [x,y,'r']
            print(self.points)
            self.cur_point = -1
            self.sel_point = False
            self.facePointsSetup()



    def facePointsSetup(self):
        self.axes.cla()
        self.axes.imshow(self.pic)
        self.draw()
        for point in self.points:
            self.axes.plot(point[0],point[1], marker='o', markerfacecolor=point[2])
        self.draw()

    def loadImage(self,file):
        self.pic = Image.open(file)
        self.facePointsSetup()

    def mouseMoveEvent(self,e):
        x = e.x()
        y = e.y()
        text = "x: {0},  y: {1}".format(x, y)
        print(text)

def main():
    app = QtWidgets.QApplication(sys.argv)
    prog = morphgui()
    prog.show()
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())
