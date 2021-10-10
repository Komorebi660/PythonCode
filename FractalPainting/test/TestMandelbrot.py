# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# THIS FILE IS USED TO TEST PAINTING MANDELBROT SET
# ----------------------------------------------------------
from DrawFractal import *

# 绘制曼德勃罗集
pl.subplot(231)
draw_Mandelbrot(256, -0.5, 0, 1.5)
for i in range(2, 7):
    pl.subplot(230+i)
    draw_Mandelbrot(256, 0.27322626, 0.595153338, 0.2**(i-1))
pl.subplots_adjust(0.02, 0, 0.98, 1, 0.02, 0)
# 保存
pl.savefig("./mandelbrot.png", dpi=2048)
print("Done!")
pl.show()
