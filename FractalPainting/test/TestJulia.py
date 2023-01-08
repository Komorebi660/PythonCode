# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2023 Komorebi660 All rights reserved.
# THIS FILE IS USED TO TEST PAINTING JULIA SET
# ----------------------------------------------------------
from src.DrawFractal import *

# 绘制朱丽叶集
C = [0.279, 0.400, 0.484, 0.544, 0.590, 0.626]


def draw_Julia_(n, c=0.400):
    julia = get_Julia(-1.5, 1.5, -1.5, 1.5, c, 1024, n)
    pl.imshow(julia, cmap=cm.jet, extent=[-1.5, 1.5, -1.5, 1.5])
    pl.gca().set_axis_off()
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


for i in range(1, 7):
    pl.subplot(230+i)
    draw_Julia_(i+1, C[i-1])

# 保存
pl.savefig("./julia.png", bbox_inches='tight', dpi=2048, pad_inches=0.0)
print("Done!")
pl.show()
