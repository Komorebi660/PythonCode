# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# THIS FILE IS USED TO TEST PAINTING LEAF
# ----------------------------------------------------------
from src.DrawFractal import *

pl.figure(figsize=(6, 8))
draw_Leaf(150000)  # 绘制分形树叶
pl.gcf().patch.set_facecolor("black")  # 设置背景为黑色
pl.savefig("./leaf_black.png", dpi=1024)  # 保存
print("Done!")
pl.show()
