# ----------------------------------------------------------
# -*- coding: UTF-8 -*-
# Copyright © 2022 Komorebi660 All rights reserved.
# ----------------------------------------------------------
from ui.UiMainWindow import Ui_MainWindow
from src.Login import LoginDialog
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem
from PyQt5 import QtCore
from src.SQL import book_gen, reader_gen, borrow_gen, table_del
import sys


class MainWindow(QMainWindow):
    ui = None
    db = None
    tab_ = None
    head_ = []

    def __init__(self) -> None:
        super().__init__()
        # 设置ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 初始化配置
        self.initLayout()
        self.initBinding()
        self.show()

    def closeEvent(self, event):
        #重写关闭事件, 每次关闭都自动退出数据库连接
        self.Logout()
        event.accept()
        sys.exit(0)

    def initLayout(self):
        self.ui.Settings.setEnabled(False)
        # 设置表格配置
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
        self.ui.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")

    def initBinding(self):
        #按钮绑定函数
        self.ui.actionLogin.triggered.connect(self.Login)
        self.ui.actionLogout.triggered.connect(self.Logout)

        self.ui.actionRender.triggered.connect(self.renderTable)
        self.ui.actionClean.triggered.connect(self.clearTable)

    def clearTable(self):
        self.ui.table.setColumnCount(0)
        self.ui.table.setRowCount(0)

    def renderTable(self):
        # 清空
        self.ui.table.setRowCount(0)
        # 设置表头
        self.ui.table.setColumnCount(len(self.head_))
        self.ui.table.setHorizontalHeaderLabels(self.head_)
        # 开始渲染表格
        currentRowCount = self.ui.table.rowCount()
        for row in self.tab_:
            self.ui.table.insertRow(currentRowCount)

            for i in range(len(row)):
                item = QTableWidgetItem(str(row[i]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.table.setItem(currentRowCount, i, item)

            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def Login(self):
        dialog = LoginDialog(self)
        dialog.exec_()
        if self.db != None:
            self.db.execute(book_gen)
            self.db.execute(reader_gen)
            self.db.execute(borrow_gen)
            self.ui.Settings.setEnabled(True)
            # 获取每个表的行数
            tabs = self.db.execute("SHOW TABLES;")
            self.tab_ = []
            for tab in tabs:
                row_cnt = self.db.execute("SELECT count(*) FROM " + tab[0])
                self.tab_.append((tab[0], row_cnt[0][0]))
            # 渲染数据库中所有表的信息
            self.head_ = ['Table Name', 'Row Count']
            self.renderTable()
        else:
            self.ui.Settings.setEnabled(False)

    def Logout(self):
        if self.db is not None:
            #删除表格
            self.db.execute(table_del)
            self.db.close()
            self.db = None
        self.ui.Settings.setEnabled(False)
        self.clearTable()
