# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# THIS FILE IS USED TO TEST PAINTING KOCH SNOWFLAKE
# ----------------------------------------------------------
import matplotlib.animation as animation
from DrawFractal import *

# 绘制科赫雪花的动图
figure = pl.figure()
iter = np.arange(1, 8, 1)

# 绘制动图并保存
anims = animation.FuncAnimation(
    fig=figure, func=draw_Koch, frames=iter, interval=500, repeat=True)
anims.save('./Koch.gif')
print("Done!")
pl.show()
