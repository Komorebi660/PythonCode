# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# THIS FILE IS USED TO GENERATE GUI
# ----------------------------------------------------------
import ctypes
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import ImageTk
import time
import threading
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DrawFractal import*


# 关闭GUI
def close():
    root.quit()
    root.destroy()


img = None  # 避免图像闪烁
img_file = None  # 生成图像变量
anims = None  # 全局变量，用于保存gif


class Fractal_Painting:

    def __init__(self):
        pl.switch_backend('agg')  # 解决 not in main thread 问题

        #--------------------------- "图片格式"控件 ---------------------------#
        self.Var_format = IntVar()
        self.format_label = LabelFrame(sidebar,
                                       text="Format",
                                       bg='#F5F5F5',
                                       font=("Helvetica", 10, "bold"))
        self.format_label.place(relx=0.05,
                                rely=0.17,
                                relwidth=0.9,
                                relheight=0.2)
        self.stable = ttk.Radiobutton(self.format_label,
                                      text="Stable",
                                      variable=self.Var_format,
                                      value=1,
                                      command=self.update)
        self.stable.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.4)
        self.dynamic = ttk.Radiobutton(self.format_label,
                                       text="Dynamic",
                                       variable=self.Var_format,
                                       value=2,
                                       command=self.update)
        self.dynamic.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.4)
        self.Var_format.set(1)
        #--------------------------- "图片内容"控件 ---------------------------#
        self.Var_content = StringVar()
        self.lab = Label(sidebar,
                         text='Content:',
                         bg='#F5F5F5',
                         font=("Helvetica", 12))
        self.lab.place(relx=0.05, rely=0.4, relwidth=0.3, relheight=0.06)
        self.sel = ttk.Combobox(sidebar, textvariable=self.Var_content,
                                font=("Helvetica", 12))
        self.sel['value'] = ('Mandelbrot',
                             'Julia',
                             'Leaf',
                             'Koch',
                             'Dragon',
                             'Triangle',
                             'Tree',
                             'Hilbert',
                             'Square')
        self.sel.current(0)  # 设置初始值
        self.sel.place(relx=0.35, rely=0.4, relwidth=0.6, relheight=0.06)
        #----------------------------- "开始"按钮 -----------------------------#
        self.btn_start = ttk.Button(sidebar,
                                    text='start',
                                    style="Accent.TButton",
                                    command=self.start)
        self.btn_start.place(relx=0.1, rely=0.5,
                             relwidth=0.35, relheight=0.06)
        #----------------------------- "保存"按钮 -----------------------------#
        self.btn_save = ttk.Button(sidebar,
                                   text='save',
                                   style="TButton",
                                   command=self.save)
        self.btn_save.place(relx=0.55, rely=0.5,
                            relwidth=0.35, relheight=0.06)

    def draw_gif(self):
        global anims
        # 清空canvas
        for widget in root.winfo_children():
            if widget != sidebar:
                if widget != info:
                    widget.destroy()
        info['text'] = "Processing..."
        pl.clf()  # 清空图片
        func_ = CONTENT.get(self.Var_content.get())[0]
        iter = ITERATION.get(self.Var_content.get())
        time_ = GIF_TIME.get(self.Var_content.get())
        # 放置图像
        figure = pl.figure()
        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=280, rely=0.01, relwidth=0.71, relheight=0.98)
        # 重定向
        if(func_ == CONTENT.get('Mandelbrot')[0]):
            anims = animation.FuncAnimation(fig=figure,
                                            func=draw_Mandelbrot_,
                                            frames=iter,
                                            interval=500,
                                            repeat=False)
        else:
            # 要赋值，否则会报错
            anims = animation.FuncAnimation(fig=figure,
                                            func=func_,
                                            frames=iter,
                                            interval=500,
                                            repeat=False)
        time.sleep(time_)
        self.btn_start['state'] = NORMAL
        self.btn_save['state'] = NORMAL

    def save_gif(self):
        global anims
        save_path = asksaveasfilename(title='Please choose a path',
                                      initialdir='',
                                      filetypes=[('GIF file', '*.gif')])
        # 清空canvas
        for widget in root.winfo_children():
            if widget != sidebar:
                if widget != info:
                    widget.destroy()
        try:
            info['text'] = "Processing..."
            anims.save(save_path)
            self.btn_start['state'] = NORMAL
            self.btn_save['state'] = NORMAL
            info['text'] = "Save successfully!"
        except:
            self.btn_start['state'] = NORMAL
            self.btn_save['state'] = NORMAL
            info['text'] = "You should enter a path to save the photo."

    def draw_picture(self):
        # 清空canvas
        for widget in root.winfo_children():
            if widget != sidebar:
                if widget != info:
                    widget.destroy()
        info['text'] = "Processing..."
        # 清空图片
        pl.clf()
        # 从字典中查找迭代次数
        quality_ = QUALITY[CONTENT.get(self.Var_content.get())[1]]
        # 从字典中查找调用函数
        func_ = CONTENT.get(self.Var_content.get())[0]
        # 调用函数绘图
        func_(quality_)
        # 放置图像
        figure = pl.gcf()  # 获取生成的图片
        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=280, rely=0.01, relwidth=0.71, relheight=0.98)
        self.btn_start['state'] = NORMAL
        self.btn_save['state'] = NORMAL

    def save_picture(self):
        save_path = asksaveasfilename(title='Please choose a path',
                                      initialdir='',
                                      filetypes=[('Image file', '*.jpg')])
        # 清空canvas
        for widget in root.winfo_children():
            if widget != sidebar:
                if widget != info:
                    widget.destroy()
        try:
            info['text'] = "Processing..."
            pl.savefig(save_path, bbox_inches='tight', dpi=512, pad_inches=0.0)
            self.btn_start['state'] = NORMAL
            self.btn_save['state'] = NORMAL
            info['text'] = "Save successfully!"
        except:
            self.btn_start['state'] = NORMAL
            self.btn_save['state'] = NORMAL
            info['text'] = "You should enter a path to save the photo."

    # start to draw
    def start(self):
        self.btn_start['state'] = DISABLED
        self.btn_save['state'] = DISABLED
        if(self.Var_format.get() == 1):
            # 多线程
            t = threading.Thread(target=self.draw_picture)
            # 开启守护线程，这样在GUI意外关闭时线程能正常退出
            t.setDaemon(True)
            t.start()
        else:
            # 多线程
            t = threading.Thread(target=self.draw_gif)
            # 开启守护线程，这样在GUI意外关闭时线程能正常退出
            t.setDaemon(True)
            t.start()

    # start to save
    def save(self):
        self.btn_start['state'] = DISABLED
        self.btn_save['state'] = DISABLED
        if(self.Var_format.get() == 1):
            # 多线程
            t = threading.Thread(target=self.save_picture)
            # 开启守护线程，这样在GUI意外关闭时线程能正常退出
            t.setDaemon(True)
            t.start()
        else:
            # 多线程
            t = threading.Thread(target=self.save_gif)
            # 开启守护线程，这样在GUI意外关闭时线程能正常退出
            t.setDaemon(True)
            t.start()

    # change select label
    def update(self):
        format = self.Var_format.get()
        if(format == 1):
            self.sel['value'] = ('Mandelbrot',
                                 'Julia',
                                 'Leaf',
                                 'Koch',
                                 'Dragon',
                                 'Triangle',
                                 'Tree',
                                 'Hilbert',
                                 'Square')
            self.sel.current(0)
        else:
            self.sel['value'] = ('Mandelbrot',
                                 'Julia(R)',
                                 'Julia(I)',
                                 'Leaf',
                                 'Koch',
                                 'Dragon',
                                 'Triangle',
                                 'Tree',
                                 'Hilbert',
                                 'Square')
            self.sel.current(0)


def Home():
    label1 = Label(sidebar,
                   text="Fractal Paint",
                   bg='#F5F5F5',
                   fg="#202020",
                   font=("Helvetica", 25, "bold"))
    label1.place(x=0, rely=0.02, relwidth=1, relheight=0.12)
    label2 = Label(sidebar,
                   text="Copyright 2022 Yaoqi Chen",
                   bg='#F5F5F5',
                   fg="#A0A0A0",
                   font=("Helvetica", 10))
    label2.place(x=0, rely=0.95, relwidth=1, height=20)
    info['text'] = "Welcome to use Fractal Painter.\nYou can choose content from the sidebar to start."
    temp = Fractal_Painting()


root = Tk()
# 高dpi
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor/75)
# 设置主题
root.call("source", "theme.tcl")
root.call("set_theme", "light")

root.title('Fractal Painter')
root.geometry('1000x800')
root.protocol('WM_DELETE_WINDOW', close)  # 覆盖"x"按钮

sidebar = Frame(root, bg='#F5F5F5', width=280, height=0)
sidebar.pack(expand=False, fill='both', side='left')
info = Label(root,
             text="",
             fg="#A0A0A0",
             font=("Helvetica", 10))
info.place(x=280, rely=0.43, relwidth=0.8, height=50)
Home()
root.mainloop()
