# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# THIS FILE IS USED TO GENERATE GUI
# ----------------------------------------------------------
from tkinter import *
from tkinter import ttk
import time
import threading
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DrawFractal import *

CONTENT = {
    '曼德勃罗集': [draw_Mandelbrot, 0],
    '朱丽叶集': [draw_Julia, 1],
    '分形叶': [draw_Leaf, 2],
    '科赫雪花': [draw_Koch, 3],
    '分形龙': [draw_Dragon, 4],
    '谢尔宾斯基三角': [draw_Triangle, 5],
    '分形树': [draw_Plant, 6],
    '希尔伯特曲线': [draw_Hilbert, 7],
    '谢尔宾斯基正方形': [draw_Square, 8],
    '朱丽叶集(实部变化)': [draw_Julia_1, 9],
    '朱丽叶集(虚部变化)': [draw_Julia_2, 10],
}

QUALITY = {
    '速度优先': [256, 512, 30000, 8, 15, 10, 8, 7, 14],  # LOW <1s
    '均衡': [400, 1024, 100000, 9, 18, 12, 9, 7, 14],  # MIDDLE <4s
    '画质优先': [800, 1500, 500000, 10, 20, 13, 10, 9, 18]  # HIGH <30s
}

ITERATION = {
    '曼德勃罗集': np.arange(2, 4.2, 0.2),
    '分形叶': np.arange(10000, 100000, 20000),
    '科赫雪花': np.arange(1, 8, 1),
    '分形龙': np.arange(5, 18, 1),
    '谢尔宾斯基三角': np.arange(4, 12, 2),
    '分形树': np.arange(1, 9, 1),
    '希尔伯特曲线': np.arange(1, 8, 1),
    '谢尔宾斯基正方形': np.arange(1, 14, 1),
    '朱丽叶集(实部变化)':  np.arange(-1.0, 1.1, 0.1),
    '朱丽叶集(虚部变化)': np.arange(-1.0, 1.1, 0.1)
}

GIF_TIME = {
    '曼德勃罗集': 22,
    '分形叶': 10,
    '科赫雪花': 5,
    '分形龙': 10,
    '谢尔宾斯基三角': 5,
    '分形树': 7,
    '希尔伯特曲线': 5,
    '谢尔宾斯基正方形': 8,
    '朱丽叶集(实部变化)': 30,
    '朱丽叶集(虚部变化)': 28
}

anims = None  # 全局变量，用于保存gif


# 绘制动图
def draw_gif():
    global anims
    pl.clf()  # 清空图片
    func_ = CONTENT.get(Var_content.get())[0]
    iter = ITERATION.get(Var_content.get())
    time_ = GIF_TIME.get(Var_content.get())
    # 放置图像
    figure = pl.figure()
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.1, y=230, relwidth=0.8, relheight=0.75)
    # 重定向
    if(func_ == CONTENT.get('曼德勃罗集')[0]):
        anims = animation.FuncAnimation(
            fig=figure, func=draw_Mandelbrot_, frames=iter, interval=500, repeat=False)
    else:
        # 要赋值，否则会报错
        anims = animation.FuncAnimation(
            fig=figure, func=func_, frames=iter, interval=500, repeat=False)
    time.sleep(time_)
    btn_start['state'] = NORMAL
    btn_save['state'] = NORMAL
    state['text'] = "完成！"


# 保存动图
def save_gif():
    path = './'+Var_content.get()+'.gif'
    anims.save(path)
    text = '保存成功！文件 '+Var_content.get()+'.gif'+' 位于当前目录中.'
    state['text'] = text
    btn_start['state'] = NORMAL
    btn_save['state'] = NORMAL


# 绘制图像
def draw_picture():
    # 清空图片
    pl.clf()
    # 从字典中查找迭代次数
    quality_ = QUALITY.get(Var_quality.get())[
        CONTENT.get(Var_content.get())[1]]
    # 从字典中查找调用函数
    func_ = CONTENT.get(Var_content.get())[0]
    # 调用函数绘图
    func_(quality_)
    # 放置图像
    figure = pl.gcf()  # 获取生成的图片
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.1, y=230, relwidth=0.8, relheight=0.75)
    btn_start['state'] = NORMAL
    btn_save['state'] = NORMAL
    state['text'] = "完成！"


# 保存图像
def save_picture():
    path = './'+Var_content.get()+'.png'
    pl.savefig(path, bbox_inches='tight', dpi=512, pad_inches=0.0)
    text = '保存成功！文件 '+Var_content.get()+'.png'+' 位于当前目录中.'
    state['text'] = text
    btn_start['state'] = NORMAL
    btn_save['state'] = NORMAL


# 开始绘图，分配新线程
def start():
    state['text'] = "计算中......"
    btn_start['state'] = DISABLED
    btn_save['state'] = DISABLED
    if(Var_format.get() == '静态图片'):
        # 多线程
        t = threading.Thread(target=draw_picture)
        # 开启守护线程，这样在GUI意外关闭时线程能正常退出
        t.setDaemon(True)
        t.start()
    else:
        # 多线程
        t = threading.Thread(target=draw_gif)
        # 开启守护线程，这样在GUI意外关闭时线程能正常退出
        t.setDaemon(True)
        t.start()


# 保存图片，分配新线程
def save():
    btn_start['state'] = DISABLED
    btn_save['state'] = DISABLED
    state['text'] = "处理中......"
    if(Var_format.get() == '静态图片'):
        # 多线程
        t = threading.Thread(target=save_picture)
        # 开启守护线程，这样在GUI意外关闭时线程能正常退出
        t.setDaemon(True)
        t.start()
    else:
        # 多线程
        t = threading.Thread(target=save_gif)
        # 开启守护线程，这样在GUI意外关闭时线程能正常退出
        t.setDaemon(True)
        t.start()


# 关闭GUI
def close():
    root.quit()
    root.destroy()


# 更新Combobox2及Combobox3
def update1(event):
    format = Var_format.get()
    if(format == '动态图片'):
        sel2['state'] = 'disabled'
        sel2.current(1)
        comment2['text'] = '预计运行时间 < '+str(GIF_TIME.get('曼德勃罗集'))+'s'
        sel3['value'] = ('曼德勃罗集', '朱丽叶集(实部变化)', '朱丽叶集(虚部变化)', '分形叶', '科赫雪花', '分形龙',
                         '谢尔宾斯基三角', '分形树', '希尔伯特曲线', '谢尔宾斯基正方形')
        sel3.current(0)
    else:
        sel2['state'] = 'normal'
        sel2.current(1)
        comment2['text'] = '预计运行时间 < 4s'
        sel3['value'] = ('曼德勃罗集', '朱丽叶集', '分形叶', '科赫雪花', '分形龙',
                         '谢尔宾斯基三角', '分形树', '希尔伯特曲线', '谢尔宾斯基正方形')
        sel3.current(0)


# 更新Label2
def update2(event):
    quality = Var_quality.get()
    if(quality == '速度优先'):
        comment2['text'] = '预计运行时间 < 1s'
    elif(quality == '均衡'):
        comment2['text'] = '预计运行时间 < 4s'
    else:
        comment2['text'] = '预计运行时间 < 30s'


# 更新Label2
def update3(event):
    format = Var_format.get()
    content = Var_content.get()
    if(format == '动态图片'):
        comment2['text'] = '预计运行时间 < '+str(GIF_TIME.get(content))+'s'


root = Tk()
root.title('Fractal Painting')
root.geometry('880x1000')
root.protocol('WM_DELETE_WINDOW', close)  # 覆盖"x"按钮

figure = pl.gcf()
# 去除白边
pl.gca().xaxis.set_major_locator(pl.NullLocator())
pl.gca().yaxis.set_major_locator(pl.NullLocator())
pl.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
pl.switch_backend('agg')  # 解决 not in main thread 问题
# 放置初始化图像
canvas = FigureCanvasTkAgg(figure, master=root)
canvas.draw()
canvas.get_tk_widget().place(relx=0.1, y=230, relwidth=0.8, relheight=0.75)


#--------------------------- "图片格式"控件 ---------------------------#
Var_format = StringVar()
lab1 = Label(root, text='图片格式：', font=("微软雅黑", 11))
lab1.place(relx=0.2, y=20, relwidth=0.1, height=30)
sel1 = ttk.Combobox(root, textvariable=Var_format,
                    font=("微软雅黑", 11))
sel1['value'] = ('静态图片', '动态图片')
sel1.current(0)  # 设置初始值
sel1.bind('<<ComboboxSelected>>', update1)  # 绑定更新事件
sel1.place(relx=0.3, y=20, relwidth=0.2, height=30)
#--------------------------- "图片格式"控件 ---------------------------#
#--------------------------- "画质选择"控件 ---------------------------#
Var_quality = StringVar()
lab2 = Label(root, text='画质选择：', font=("微软雅黑", 11))
lab2.place(relx=0.2, y=60, relwidth=0.1, height=30)
sel2 = ttk.Combobox(root, textvariable=Var_quality,
                    font=("微软雅黑", 11))
sel2['value'] = ('速度优先', '均衡', '画质优先')
sel2.current(1)  # 设置初始值
sel2.bind('<<ComboboxSelected>>', update2)  # 绑定更新事件
sel2.place(relx=0.3, y=60, relwidth=0.2, height=30)
comment2 = Label(root, text='预计运行时间 < 4s',
                 font=("微软雅黑", 10), fg="gray")
comment2.place(relx=0.51, y=62, relwidth=0.2, height=25)
#--------------------------- "画质选择"控件 ---------------------------#
#--------------------------- "图片内容"控件 ---------------------------#
Var_content = StringVar()
lab3 = Label(root, text='图片内容：', font=("微软雅黑", 11))
lab3.place(relx=0.2, y=100, relwidth=0.1, height=30)
sel3 = ttk.Combobox(root, textvariable=Var_content,
                    font=("微软雅黑", 11))
sel3['value'] = ('曼德勃罗集', '朱丽叶集', '分形叶', '科赫雪花', '分形龙',
                 '谢尔宾斯基三角', '分形树', '希尔伯特曲线', '谢尔宾斯基正方形')
sel3.current(0)  # 设置初始值
sel3.bind('<<ComboboxSelected>>', update3)  # 绑定更新事件
sel3.place(relx=0.3, y=100, relwidth=0.2, height=30)
#--------------------------- "图片内容"控件 ---------------------------#
#----------------------------- "开始"按钮 -----------------------------#
btn_start = Button(root, text='开始', font=("微软雅黑", 12),
                   fg="red", command=start)
btn_start.place(relx=0.2, y=150, relwidth=0.25, height=30)
#----------------------------- "开始"按钮 -----------------------------#
#----------------------------- "保存"按钮 -----------------------------#
btn_save = Button(root, text='保存', font=("微软雅黑", 12),
                  fg="blue", command=save)
btn_save.place(relx=0.55, y=150, relwidth=0.25, height=30)
#----------------------------- "保存"按钮 -----------------------------#
#------------------------------ 状态显示 ------------------------------#
state = Label(root, font=("微软雅黑", 11))
state.place(relx=0.2, y=190, relwidth=0.6, height=30)
state['text'] = "按下\"开始\"按钮以开始生成图片"
#------------------------------ 状态显示 ------------------------------#

# 主循环
root.mainloop()
