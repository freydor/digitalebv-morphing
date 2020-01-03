import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
# from PyQt5.QtGui import QPixmap
import numpy as np




    def saveLoc(self):
        filename = asksaveasfile() # show an "Open" dialog box and return the path to the selected file
        self.lineEdit.setText(filename)

    def LodePic1(self):        
        image_path = askopenfilename()
        # self.graphicsView_1.setText(image_path)
        image_profile = QtGui.QImage(image_path) #QImage object
        image_profile = image_profile.scaled(250,200, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration    
        self.graphicsView_1.setPixmap(QtGui.QPixmap.fromImage(image_profile)) 

    def LodePic2(self):
        image_path = askopenfilename()
        # self.graphicsView_1.setText(image_path)
        image_profile = QtGui.QImage(image_path) #QImage object
        image_profile = image_profile.scaled(250,200, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration    
        self.graphicsView_2.setPixmap(QtGui.QPixmap.fromImage(image_profile)) 


    def SetPointPic1(self):
        self.pointA = []

    def SetPointPic2(self):
        self.pointB = []

    def Export(self):
        pass

    def Calc(self):
        # Calc Trans
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        for p in self.pointA:
            x1 += p[0]
            y1 += p[1]

        for p in self.pointB:
            x2 += p[0]
            y2 += p[1]

        x = x2 - x1
        y = y2 - y1
        self.transVec = [x,y]

        self.trans.setText(str(self.transVec).strip('[]'))
    
    def mousePressEvent(self, event):
        # Exate positionen noch raus machen
        if event.pos().x()> 10 and event.pos().x()< 260 and event.pos().y()>30 and event.pos().y()< 230:
            #print(event.pos())
            self.addPic1Point(event.pos().x()-10,event.pos().y()-30)

        if event.pos().x()> 280 and event.pos().x()< 530 and event.pos().y()>30 and event.pos().y()< 230:
            #print(event.pos())
            self.addPic2Point(event.pos().x()-280,event.pos().y()-30)

    def addPic1Point(self, x, y):
        #print(x)
        #print(y)
        if len(self.pointA) <3:
            self.pointA.append([x,y])
        print(self.pointA)

    def addPic2Point(self, x, y):
        #print(x)
        #print(y)
        if len(self.pointB) <3:
            self.pointB.append([x,y])
        print(self.pointB)

    def printLable(parameter_list):
        pass




app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec()
