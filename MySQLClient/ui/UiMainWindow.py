# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/PyQt_UI/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(817, 608)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setMinimumSize(QtCore.QSize(0, 300))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.table.setFont(font)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)
        self.gridLayout_3.addLayout(self.verticalLayout, 5, 0, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 817, 26))
        self.menubar.setObjectName("menubar")
        self.Connect = QtWidgets.QMenu(self.menubar)
        self.Connect.setObjectName("Connect")
        self.Settings = QtWidgets.QMenu(self.menubar)
        self.Settings.setObjectName("Settings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogin = QtWidgets.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.actionLogout = QtWidgets.QAction(MainWindow)
        self.actionLogout.setObjectName("actionLogout")
        self.actionRender = QtWidgets.QAction(MainWindow)
        self.actionRender.setObjectName("actionRender")
        self.actionClean = QtWidgets.QAction(MainWindow)
        self.actionClean.setObjectName("actionClean")
        self.Connect.addAction(self.actionLogin)
        self.Connect.addAction(self.actionLogout)
        self.Settings.addAction(self.actionRender)
        self.Settings.addAction(self.actionClean)
        self.menubar.addAction(self.Connect.menuAction())
        self.menubar.addAction(self.Settings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DataBase"))
        self.Connect.setTitle(_translate("MainWindow", "连接"))
        self.Settings.setTitle(_translate("MainWindow", "界面"))
        self.actionLogin.setText(_translate("MainWindow", "登录"))
        self.actionLogout.setText(_translate("MainWindow", "登出"))
        self.actionRender.setText(_translate("MainWindow", "刷新"))
        self.actionClean.setText(_translate("MainWindow", "清空"))
