# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2022 Komorebi660 All rights reserved.
# THIS FILE IS THE CORE FUNCTION OF FRACTAL PAINTING
# ----------------------------------------------------------
from math import sin, cos, pi
import numpy as np
from matplotlib import cm, collections
import matplotlib.pyplot as pl

# 蕨类植物叶子的迭代函数和其概率值
p_array = [0.01, 0.07, 0.07, 0.85]
func_array = [
    np.array([[0, 0, 0], [0, 0.16, 0]]),
    np.array([[0.2, -0.26, 0], [0.23, 0.22, 1.6]]),
    np.array([[-0.15, 0.28, 0], [0.26, 0.24, 0.44]]),
    np.array([[0.85, 0.04, 0], [-0.04, 0.85, 1.6]])
]

# L系统迭代规则
rules = [
    {
        "F": "F+F--F+F", "f": "F--F--F", "S": "f",
        "direct": 180,
        "angle": 60,
        "title": "Koch"
    },
    {
        "X": "X+YF+", "Y": "-FX-Y", "S": "FX",
        "direct": 0,
        "angle": 90,
        "title": "Dragon"
    },
    {
        "f": "F-f-F", "F": "f+F+f", "S": "f",
        "direct": 0,
        "angle": 60,
        "title": "Triangle"
    },
    {
        "X": "F-[[X]+X]+F[+FX]-X", "F": "FF", "S": "X",
        "direct": -45,
        "angle": 25,
        "title": "Plant"
    },
    {
        "S": "X", "X": "-YF+XFX+FY-", "Y": "+XF-YFY-FX+",
        "direct": 0,
        "angle": 90,
        "title": "Hilbert"
    },
    {
        "S": "L--F--L--F", "L": "+R-F-R+", "R": "-L+F+L-",
        "direct": 0,
        "angle": 45,
        "title": "Square"
    },
]


# 生成朱丽叶集
def get_Julia(x0, x1, y0, y1, c, n, m):
    """
        进行函数迭代
        x0: 图片横坐标min
        x1: 图片横坐标max
        y0: 图片纵坐标min
        y0: 图片纵坐标max
        c:  迭代方程中c的值
        n:  迭代次数及分辨率
        m:  z的指数

        返回值：朱丽叶集
    """
    # 迭代函数
    def iter_point(z, c):
        for i in range(0, n):  # 最多迭代n次
            if abs(z) > 2:
                break  # 半径大于2则认为逃逸
            z = pow(z, m)+c
        return i  # 返回迭代次数
    # 均分为n*n个点
    y, x = np.ogrid[y0:y1:1j*n, x0:x1:1j*n]
    # 设置为复数
    z = x + y*1j
    # 获取Julia集的迭代次数，作为绘图的灰度信息
    julia = np.frompyfunc(iter_point, 2, 1)(z, c).astype(np.float)
    return julia


# 绘制朱丽叶集
def draw_Julia(n=512, c=0.400, cx=0.0, cy=0.0, d=1.5):
    x0, x1, y0, y1 = cx-d, cx+d, cy-d, cy+d
    julia = get_Julia(x0, x1, y0, y1, c, n, 3)
    pl.imshow(julia, cmap=cm.jet, extent=[x0, x1, y0, y1])
    pl.gca().set_axis_off()
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 绘制c的实部a变化时的动态朱丽叶集
def draw_Julia_1(a=0.0, cx=0.0, cy=0.0, d=1.5):
    x0, x1, y0, y1 = cx-d, cx+d, cy-d, cy+d
    julia = get_Julia(x0, x1, y0, y1, a, 256, 2)
    pl.imshow(julia, cmap=cm.jet, extent=[x0, x1, y0, y1])
    pl.gca().set_axis_off()
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 绘制c的虚部b变化时的动态朱丽叶集
def draw_Julia_2(b=0.0, cx=0.0, cy=0.0, d=1.5):
    x0, x1, y0, y1 = cx-d, cx+d, cy-d, cy+d
    julia = get_Julia(x0, x1, y0, y1, 0.0+1j*b, 256, 2)
    pl.imshow(julia, cmap=cm.jet, extent=[x0, x1, y0, y1])
    pl.gca().set_axis_off()
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 生成曼德勃罗集
def get_Mandelbrot(x0, x1, y0, y1, n, m):
    """
        进行函数迭代
        x0: 图片横坐标min
        x1: 图片横坐标max
        y0: 图片纵坐标min
        y0: 图片纵坐标max
        n:  迭代次数及分辨率
        m:  z的指数

        返回值：曼德勃罗集
    """
    # 迭代函数
    def iter_point(c):
        z = c
        for i in range(0, n):  # 最多迭代n次
            if abs(z) > 2:
                break  # 半径大于2则认为逃逸
            z = pow(z, m)+c
        return i  # 返回迭代次数
    # 均分为n*n个点
    y, x = np.ogrid[y0:y1:1j*n, x0:x1:1j*n]
    # 设置为复数
    c = x + y*1j
    # 获取mandelbrot集的迭代次数，作为绘图的灰度信息
    mandelbrot = np.frompyfunc(iter_point, 1, 1)(c).astype(np.float)
    return mandelbrot


# 绘制曼德勃罗集
def draw_Mandelbrot(n=512, cx=-0.5, cy=0.0, d=1.5):
    x0, x1, y0, y1 = cx-d, cx+d, cy-d, cy+d
    mandelbrot = get_Mandelbrot(x0, x1, y0, y1, n, 2)
    pl.imshow(mandelbrot, cmap=cm.jet, extent=[x0, x1, y0, y1])
    pl.gca().set_axis_off()
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 绘制指数n变化时的曼德勃罗集
def draw_Mandelbrot_(n=2, cx=0.0, cy=0.0, d=1.5):
    x0, x1, y0, y1 = cx-d, cx+d, cy-d, cy+d
    mandelbrot = get_Mandelbrot(x0, x1, y0, y1, 256, n)
    pl.imshow(mandelbrot, cmap=cm.jet, extent=[x0, x1, y0, y1])
    pl.gca().set_axis_off()
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 生成分形树叶(x,y)坐标
def get_LeafDots(p, func, init, n):
    """
        进行函数迭代
        p: 每个函数的选择概率列表
        func: 迭代函数列表
        init: 迭代初始点
        n: 迭代次数

        返回值：迭代所得的X坐标数组, Y坐标数组
    """
    # 迭代向量的初始化为[init, 1]
    pos = np.ones(3, dtype=np.float)
    pos[:2] = init
    # 结果的初始化
    result = np.zeros((n, 2), dtype=np.float)
    # 通过函数概率选择相应函数进行坐标计算
    np.random.seed(0)
    probility = np.array(p)
    for i in range(0, n):
        # 根据概率生成函数选择
        index = np.random.choice([0, 1, 2, 3], p=probility.ravel())
        temp = np.dot(func[index], pos)  # 计算坐标
        pos[:2] = temp  # 更新迭代向量
        result[i] = temp  # 保存结果
    return result[:, 0], result[:, 1]


# 绘制分形树叶
def draw_Leaf(n=150000):
    x, y = get_LeafDots(p_array, func_array, [0, 0], n)
    pl.scatter(x, y, s=1, c="g", marker=".", linewidths=0)
    pl.axis("off")
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 获取L系统构造的分形图线条信息
def get_lines(rule, n):
    """
        根据规则生成边信息
        rule: 生成规则

        返回值：每次迭代所得的X坐标数组, Y坐标数组
    """
    # 初始化
    info = rule['S']
    # 按rule中的定义展开构造规则
    for i in range(n):
        temp_info = []
        for c in info:
            if c in rule:
                temp_info.append(rule[c])
            else:
                temp_info.append(c)
        info = "".join(temp_info)
    d = rule['direct']
    a = rule['angle']
    p = (0.0, 0.0)  # 初始坐标
    l = 1.0  # 步长
    lines = []
    stack = []
    # 开始生成边信息
    for c in info:
        # 绘制一条边
        if c in "Ff":
            r = d * pi / 180
            t = p[0] + l*cos(r), p[1] + l*sin(r)
            lines.append(((p[0], p[1]), (t[0], t[1])))
            p = t
        # 旋转
        elif c == "+":
            d += a
        # 旋转
        elif c == "-":
            d -= a
        elif c == "[":
            stack.append((p, d))
        elif c == "]":
            p, d = stack[-1]
            del stack[-1]
    return lines


# 绘制科赫雪花
def draw_Koch(n=9):
    lines = get_lines(rules[0], n)
    linecollections = collections.LineCollection(lines)
    pl.axes().add_collection(linecollections, autolim=True)
    pl.axis("equal")
    # 去除坐标轴坐标
    pl.xticks([])
    pl.yticks([])
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 绘制分形龙
def draw_Dragon(n=18):
    lines = get_lines(rules[1], n)
    linecollections = collections.LineCollection(lines)
    pl.axes().add_collection(linecollections, autolim=True)
    pl.axis("equal")
    # 去除坐标轴坐标
    pl.xticks([])
    pl.yticks([])
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 绘制谢尔宾斯基三角
def draw_Triangle(n=12):
    lines = get_lines(rules[2], n)
    linecollections = collections.LineCollection(lines)
    pl.axes().add_collection(linecollections, autolim=True)
    pl.axis("equal")
    # 去除坐标轴坐标
    pl.xticks([])
    pl.yticks([])
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 绘制分形树
def draw_Plant(n=9):
    lines = get_lines(rules[3], n)
    linecollections = collections.LineCollection(lines)
    pl.axes().add_collection(linecollections, autolim=True)
    pl.axis("equal")
    # 去除坐标轴坐标
    pl.xticks([])
    pl.yticks([])
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 绘制希尔伯特曲线
def draw_Hilbert(n=7):
    lines = get_lines(rules[4], n)
    linecollections = collections.LineCollection(lines)
    pl.axes().add_collection(linecollections, autolim=True)
    pl.axis("equal")
    # 去除坐标轴坐标
    pl.xticks([])
    pl.yticks([])
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


# 绘制谢尔宾斯基正方形
def draw_Square(n=14):
    lines = get_lines(rules[5], n)
    linecollections = collections.LineCollection(lines)
    pl.axes().add_collection(linecollections, autolim=True)
    pl.axis("equal")
    # 去除坐标轴坐标
    pl.xticks([])
    pl.yticks([])
    # 去除白边
    pl.gca().xaxis.set_major_locator(pl.NullLocator())
    pl.gca().yaxis.set_major_locator(pl.NullLocator())
    pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)


CONTENT = {
    'Mandelbrot': [draw_Mandelbrot, 0],
    'Julia': [draw_Julia, 1],
    'Leaf': [draw_Leaf, 2],
    'Koch': [draw_Koch, 3],
    'Dragon': [draw_Dragon, 4],
    'Triangle': [draw_Triangle, 5],
    'Tree': [draw_Plant, 6],
    'Hilbert': [draw_Hilbert, 7],
    'Square': [draw_Square, 8],
    'Julia(R)': [draw_Julia_1, 9],
    'Julia(I)': [draw_Julia_2, 10],
}

QUALITY = [400, 1024, 100000, 9, 18, 12, 9, 7, 14]

ITERATION = {
    'Mandelbrot': np.arange(2, 4.2, 0.2),
    'Leaf': np.arange(10000, 100000, 20000),
    'Koch': np.arange(1, 8, 1),
    'Dragon': np.arange(5, 18, 1),
    'Triangle': np.arange(4, 12, 2),
    'Tree': np.arange(1, 9, 1),
    'Hilbert': np.arange(1, 8, 1),
    'Square': np.arange(1, 14, 1),
    'Julia(R)':  np.arange(-1.0, 1.1, 0.1),
    'Julia(I)': np.arange(-1.0, 1.1, 0.1)
}

GIF_TIME = {
    'Mandelbrot': 22,
    'Leaf': 10,
    'Koch': 5,
    'Dragon': 10,
    'Triangle': 5,
    'Tree': 7,
    'Hilbert': 5,
    'Square': 8,
    'Julia(R)': 30,
    'Julia(I)': 28
}
