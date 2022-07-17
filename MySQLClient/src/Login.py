# ----------------------------------------------------------
# -*- coding: UTF-8 -*-
# Copyright © 2022 Komorebi660 All rights reserved.
# ----------------------------------------------------------
from ui.UiLogin import Ui_LoginDialog
from PyQt5.QtWidgets import QDialog
from src.Database import Database
from src.Message import critical


class LoginDialog(QDialog):
    ui = None
    parent = None

    def __init__(self, parent) -> None:
        super().__init__(parent)
        # 设置UI
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        self.ui.ipaddr.setText('127.0.0.1')
        self.ui.database.setText('test')
        self.ui.username.setText('root')
        # 设置父界面
        self.parent = parent
        # 绑定登陆按键
        self.ui.LoginBtn.clicked.connect(self.login)
        self.show()

    def login(self):
        ipaddr = self.ui.ipaddr.text()
        dbname = self.ui.database.text()
        username = self.ui.username.text()
        password = self.ui.password.text()

        db = Database()
        db.login(username, password, ipaddr, dbname)

        if db.isConnected():
            #information(self, "登陆成功")
            self.parent.db = db
            self.close()
        else:
            critical(self, "登陆失败" + str(db.getError()))
