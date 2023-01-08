# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2023 Komorebi660 All rights reserved.
# ----------------------------------------------------------

import random
from math import sin, cos, pi, log
from tkinter import *

CANVAS_WIDTH = 640  # 画布的宽
CANVAS_HEIGHT = 480  # 画布的高
CANVAS_CENTER_X = CANVAS_WIDTH / 2  # 画布中心的X轴坐标
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2  # 画布中心的Y轴坐标
IMAGE_ENLARGE = 11  # 放大比例
COLOR = "#ff2121"  # 中国红


def f(t, shrink_ratio: float = IMAGE_ENLARGE):
    """
    基本函数
    :param shrink_ratio: 放大比例
    :param t: 参数
    :return: 坐标
    """
    # 心型函数
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    # 放大
    x *= shrink_ratio
    y *= shrink_ratio

    # 移到画布中央
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    return int(x), int(y)


def scatter_inside(x, y, beta_low=0.05, beta_high=0.17, alpha=0.7):
    """
    随机内部扩散
    :param x: 原x
    :param y: 原y
    :param beta_low, beta_high: 指数随机分布参数
    :param alpha: 以alpha的概率选择beta_low, 1-alpha的概率选择beta_high
    :return: 新坐标
    """
    beta = beta_low if random.random() < alpha else beta_high

    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy


def shrink(x, y, ratio):
    """
    缩放(模拟跳动)
    :param x: 原x
    :param y: 原y
    :param ratio: 比例
    :return: 新坐标
    """
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)

    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy


def smooth(p):
    """
    自定义曲线函数, 调整跳动平滑度
    :param p: 参数
    :return: 正弦
    """
    return 4 * sin(4 * p) / (2 * pi)


class Curve:
    """
    生成图像的每一帧数据
    """

    def __init__(self, generate_frame=20):
        self._points = set()                    # 原始爱心坐标集合
        self._inside_diffusion_points = set()   # 内部扩散效果点坐标集合
        self._halo_points = set()               # 外层光晕点坐标集合
        self.all_points = {}                    # 每帧动态点坐标
        self.build(2000)

        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)  # 绘制每一帧

    def build(self, number):
        # 轮廓
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = f(t)
            self._points.add((x, y))

        # 向内扩散
        for _x, _y in list(self._points):
            for _ in range(5):
                x, y = scatter_inside(_x, _y, 0.05, 0.17, 0.7)
                self._inside_diffusion_points.add((x, y))

        # 外层光晕
        for _ in range(int(number/2.0)):
            t = random.uniform(0, 2 * pi)
            x, y = f(t, shrink_ratio=11.4)  # 放大
            # 离散化
            x += random.randint(-6, 6)
            y += random.randint(-6, 6)
            self._halo_points.add((x, y))

    def calc(self, generate_frame):
        ratio = 10 * smooth(generate_frame / 10 * pi)  # 圆滑的周期的缩放比例
        halo_ratio = int(4 + 6 * (1 + smooth(generate_frame / 10 * pi)))

        all_points = []

        # 轮廓
        for x, y in self._points:
            x, y = shrink(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        # 内部点
        for x, y in self._inside_diffusion_points:
            x, y = shrink(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # 外层光晕
        for x, y in self._halo_points:
            x, y = shrink(x, y, halo_ratio)
            # 进一步随机离散化
            x += random.randint(-8, 8)
            y += random.randint(-8, 8)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            # 绘制矩形
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=COLOR)


def draw(main: Tk, render_canvas: Canvas, render_curve: Curve, render_frame=0):
    render_canvas.delete('all')
    render_curve.render(render_canvas, render_frame)
    # 每160ms执行一次draw函数
    main.after(160, draw, main, render_canvas, render_curve, render_frame + 1)


if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    curve = Curve()
    draw(root, canvas, curve)
    root.mainloop()
