# ----------------------------------------------------------
# -*- coding: UTF-8 -*-
# Copyright © 2023 Komorebi660 All rights reserved.
# ----------------------------------------------------------
from PyQt5.QtWidgets import QMessageBox


def information(self, alarm):
    self.alarm = alarm
    QMessageBox.information(self, '提示', self.alarm,
                            QMessageBox.Ok, QMessageBox.Ok)


def critical(self, alarm):
    self.alarm = alarm
    QMessageBox.critical(self, '错误', self.alarm,
                         QMessageBox.Ok, QMessageBox.Ok)


def warning(self, alarm):
    self.alarm = alarm
    QMessageBox.warning(self, '警告', self.alarm,
                        QMessageBox.Ok, QMessageBox.Ok)


# for testing
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QDialog
    import sys

    app = QApplication(sys.argv)
    w = QDialog()

    information(w, "test")
    critical(w, "test")
    warning(w, "test")

    sys.exit(app.exec_())
