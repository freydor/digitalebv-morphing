# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1023, 888)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1021, 821))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 10, 0, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 10, -1, 5)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btnLoadImage1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLoadImage1.sizePolicy().hasHeightForWidth())
        self.btnLoadImage1.setSizePolicy(sizePolicy)
        self.btnLoadImage1.setMaximumSize(QtCore.QSize(120, 32))
        self.btnLoadImage1.setObjectName("btnLoadImage1")
        self.verticalLayout_3.addWidget(self.btnLoadImage1)
        self.btnBbox1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBbox1.sizePolicy().hasHeightForWidth())
        self.btnBbox1.setSizePolicy(sizePolicy)
        self.btnBbox1.setObjectName("btnBbox1")
        self.verticalLayout_3.addWidget(self.btnBbox1)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btnSetPointPic1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnSetPointPic1.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnSetPointPic1.setObjectName("btnSetPointPic1")
        self.verticalLayout_4.addWidget(self.btnSetPointPic1)
        self.btnTri1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTri1.sizePolicy().hasHeightForWidth())
        self.btnTri1.setSizePolicy(sizePolicy)
        self.btnTri1.setObjectName("btnTri1")
        self.verticalLayout_4.addWidget(self.btnTri1)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btnLoadImage2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnLoadImage2.setMaximumSize(QtCore.QSize(120, 37))
        self.btnLoadImage2.setObjectName("btnLoadImage2")
        self.horizontalLayout_5.addWidget(self.btnLoadImage2)
        self.btnSetPointPic2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnSetPointPic2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnSetPointPic2.setObjectName("btnSetPointPic2")
        self.horizontalLayout_5.addWidget(self.btnSetPointPic2)
        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 5, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plot1 = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.plot1.setMinimumSize(QtCore.QSize(400, 0))
        self.plot1.setMouseTracking(True)
        self.plot1.setObjectName("plot1")
        self.horizontalLayout.addWidget(self.plot1)
        self.plot2 = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.plot2.setMinimumSize(QtCore.QSize(400, 0))
        self.plot2.setMouseTracking(True)
        self.plot2.setObjectName("plot2")
        self.horizontalLayout.addWidget(self.plot2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, 10, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.openGLWidget_3 = QtWidgets.QOpenGLWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openGLWidget_3.sizePolicy().hasHeightForWidth())
        self.openGLWidget_3.setSizePolicy(sizePolicy)
        self.openGLWidget_3.setMinimumSize(QtCore.QSize(0, 200))
        self.openGLWidget_3.setObjectName("openGLWidget_3")
        self.verticalLayout_2.addWidget(self.openGLWidget_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.horizontalSlider.setGeometry(QtCore.QRect(80, 30, 841, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setMinimumSize(QtCore.QSize(400, 0))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(120, 60, 116, 37))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnCalc = QtWidgets.QPushButton(self.groupBox)
        self.btnCalc.setObjectName("btnCalc")
        self.horizontalLayout_3.addWidget(self.btnCalc)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.scal = QtWidgets.QLineEdit(self.groupBox)
        self.scal.setObjectName("scal")
        self.horizontalLayout_3.addWidget(self.scal)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.rot = QtWidgets.QLineEdit(self.groupBox)
        self.rot.setObjectName("rot")
        self.horizontalLayout_3.addWidget(self.rot)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.trans = QtWidgets.QLineEdit(self.groupBox)
        self.trans.setObjectName("trans")
        self.horizontalLayout_3.addWidget(self.trans)
        self.verticalLayout.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1023, 34))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.loadImage1 = QtWidgets.QAction(MainWindow)
        self.loadImage1.setObjectName("loadImage1")
        self.loadImage2 = QtWidgets.QAction(MainWindow)
        self.loadImage2.setObjectName("loadImage2")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.loadImage1)
        self.menuFile.addAction(self.loadImage2)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.btnLoadImage2.clicked.connect(self.loadImage2.trigger)
        self.btnLoadImage1.clicked.connect(self.loadImage1.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnLoadImage1.setText(_translate("MainWindow", "Load Image"))
        self.btnBbox1.setText(_translate("MainWindow", "BBox"))
        self.btnSetPointPic1.setText(_translate("MainWindow", "Clear Points"))
        self.btnTri1.setText(_translate("MainWindow", "Triangulate"))
        self.btnLoadImage2.setText(_translate("MainWindow", "Load Image "))
        self.btnSetPointPic2.setText(_translate("MainWindow", "Clear Points"))
        self.groupBox_2.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.btnCalc.setText(_translate("MainWindow", "Calc"))
        self.label.setText(_translate("MainWindow", "Scale"))
        self.label_2.setText(_translate("MainWindow", "Rot"))
        self.label_3.setText(_translate("MainWindow", "Trans"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.loadImage1.setText(_translate("MainWindow", "Load (Image 1)"))
        self.loadImage2.setText(_translate("MainWindow", "Load (Image 2)"))
