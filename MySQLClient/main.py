# ----------------------------------------------------------
# -*- coding: UTF-8 -*-
# Copyright © 2023 Komorebi660 All rights reserved.
# ----------------------------------------------------------
from src.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
