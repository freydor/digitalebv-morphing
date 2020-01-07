#!/bin/python
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import QThread
from Ui_MainWindow import Ui_MainWindow as ui
import numpy as np
from morph import warp
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

        self.plotting3 = plotframes()
        self.plotlayout3 = QtWidgets.QVBoxLayout()
        self.plotlayout3.addWidget(self.plotting3)
        self.plot3.setLayout(self.plotlayout3)
        self.connectEvents()
        self.plotting1.loadImage("angela-merkel.jpg")
        self.plotting2.loadImage("Horst-Seehofer.jpg")


    def connectEvents(self):
        print("Connecting Events")
        self.loadImage1.triggered.connect(self.loadFileAction)
        self.loadImage2.triggered.connect(self.loadFileAction)
        self.btnWarp.clicked.connect(self.warpImageAction)

    def loadFileAction(self,e):
        sender = self.sender()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            if "1" in sender.text():
                self.plotting1.loadImage(fileName)
            elif "2" in sender.text():
                self.plotting2.loadImage(fileName)

    def warpImageAction(self,e):
        print("Warping!")
        if not self.plotting1.pic_loaded:
            print("Picture 1 missing!")
        elif not self.plotting2.pic_loaded:
            print("Picture 2 missing!")
        else:
#            self.plotting1.warper.warp_steps(10,self.plotting2.warper)
            #self.plotting2.warper.boundingbox = self.plotting1.warper.boundingbox
            pics = self.plotting1.warper.warp_sequence(self.plotting2.warper,3)
            self.exportGIF(pics)
            self.plotextra(pics)
            self.plotting3.subplot_img(pics,self.plotting2.warper.pic)

    def exportGIF(self,pics):
        frames = []
        for i in range(0,len(pics),2):
            frames.append(Image.fromarray(pics[i]))
        for i in range(len(pics) - 1,1,-2):
            frames.append(Image.fromarray(pics[i]))
        frames[0].save('horsti.gif', format='GIF', append_images=frames[1:], save_all=True, duration=200, loop=0)

    def plotextra(self,pics):
        fig,ax = plt.subplots(4,10,sharey='row',figsize=(25,5))
        fig.subplots_adjust(left=0.1, bottom=0, right=0.9, top=0.9,hspace=0.01,wspace=0.1)
        print(pics)
        j = 0
        for i in range(0,len(pics),2):
            if j < 10:
                ax[0][j].imshow(pics[i])
                ax[1][j].imshow(pics[i+1])
                fig.show()
            j = j +1


class plotframes(FigureCanvas):
    def __init__(self,legend=True, parent=None, width=12, height=5,linewidth=0.50, dpi=100):
        self.legend= legend
        self.fig = Figure(figsize=(width, height), dpi=dpi,linewidth=linewidth,tight_layout="True")
        super(FigureCanvas, self).__init__(self.fig)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.MinimumExpanding,
                                    QtWidgets.QSizePolicy.MinimumExpanding)
        FigureCanvas.updateGeometry(self)

        self.sub = self.fig.subplots(1,5,sharey='row')
        self.setMouseTracking(False)

    def subplot_img(self, pix,pic2):
#        self.fig.delaxes(self.axes)
        j = 0
        l = np.logspace(0,2,len(pix))/len(pix)
        #print(l)
        for i in range(1,len(pix),2):
            img = 0.5 * pix[i] +  0.5 * pix[ i-1 ]
            fimg = Image.fromarray(img.astype(np.uint8))
            fimg.save("out/blended" + str(j) + ".jpg")
            if j < 5:
                self.sub[j].imshow(img.astype(np.uint8))
            j = j + 1
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=2,hspace=0,wspace=1)
        self.draw()

class plotting(FigureCanvas):
    def __init__(self,legend=True, parent=None, width=8, height=8,linewidth=2.0, dpi=100):
        self.points = [[400,400,'r'],[550,350,'r'],[400,200,'r'],[350,350,'r']]
        self.sel_point = False
        self.pic_loaded = False
        self.cur_point = []
        self.warper = ''
        self.legend= legend
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(plotting, self).__init__(self.fig)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.MinimumExpanding,
                                    QtWidgets.QSizePolicy.MinimumExpanding)
        FigureCanvas.updateGeometry(self)
        self.setMouseTracking(False)
        self.fig.patch.set_facecolor("grey")
        self.axes = self.fig.add_axes([0.1, 0.1 , 0.8, 0.8 ])
        self.axes.set_facecolor("grey")
        self.mpl_connect("button_press_event",self.on_click)

    def on_click(self,event):
        x = event.xdata
        y = event.ydata
#        print("Click in {} at point {} {}".format(event,x,y))
        if not self.sel_point:
            i = 0
            ra = 10
            for point in self.points:
                if point[0]-x  <= ra and point[0]-x >=-ra and point[1]-y <=ra and point[1]-y >=-ra:
                    point[2]='g'
                    self.cur_point = i
                    self.sel_point = True
                    self.facePointsSetup()
                i = i + 1
        elif self.sel_point:
            self.points[self.cur_point] = [x,y,'r']
            self.cur_point = -1
            self.sel_point = False
            self.facePointsSetup()

    def facePointsSetup(self):
        self.warper.updatePoints(np.copy(np.asarray(self.points)[:,:2].astype(np.float)))
        self.axes.cla()
        self.axes.imshow(self.pic)
        self.draw()
        for point in self.points:
            self.axes.plot(point[0],point[1], marker='X',markersize=15, markerfacecolor=point[2])
        for point in self.warper.boundingbox:
            self.axes.plot(point[0],point[1], marker='P', markerfacecolor=point[2])
        self.axes.plot(self.warper.cog[0],self.warper.cog[1], marker='^', markerfacecolor=point[2])
        self.axes.plot(self.warper.center[0],self.warper.center[1], marker='8', markerfacecolor=point[2])
        self.axes.plot(self.pic.size[0]/2,self.pic.size[1]/2, marker='x', markerfacecolor='b')
        self.draw()

    def loadImage(self,filename):
        self.imagefile = filename
        self.fig.suptitle(os.path.basename(filename) , fontsize=10)
        self.pic = Image.open(filename)
        self.pic_loaded = True
        self.warper = warp(self.points,self.imagefile)
        self.facePointsSetup()

def main():
    app = QtWidgets.QApplication(sys.argv)
    prog = morphgui()
    prog.show()
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())
