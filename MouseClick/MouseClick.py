# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# ----------------------------------------------------------

import time
import threading
import pynput.mouse  # pynput和tkinter都有Button这个包，注意区分
from pynput.keyboard import Key, Listener
from tkinter import *

LEFT = 0
RIGHT = 1


# 鼠标连点控制类
class MouseClick:
    def __init__(self, button, time):
        self.mouse = pynput.mouse.Controller()
        self.running = False  # 确认是否在运行
        self.time = time
        self.button = button
        # 开启主监听线程
        self.listener = Listener(on_press=self.key_press)
        self.listener.start()

    def key_press(self, key):
        if key == Key.f8:
            if self.running:
                self.running = False
                state.delete('0.0', END)
                state.insert(INSERT, "Current State: Listening\n")
                state.insert(INSERT, "Press ESC to stop listening.\n")
                state.insert(INSERT, "Press F8 to start clicking.")
                # 停止连点也需要调用这个函数
                self.mouse_click()
            else:
                self.running = True
                state.delete('0.0', END)
                state.insert(INSERT, "Current State: Clicking\n")
                state.insert(INSERT, "Press F8 to stop clicking.\n")
                self.mouse_click()
        elif key == Key.esc:
            btn_start['state'] = NORMAL
            state.delete('0.0', END)
            state.insert(INSERT, "Current State: IDLE\n")
            state.insert(
                INSERT, "Choose which mouse button you want to click and set the time interval, then click START button to start clicking.")
            # 退出主监听线程
            self.listener.stop()

    def mouse_click(self):
        # 这里还需要额外线程进行监听，为了能够更新self.running，防止陷入死循环
        key_listener = Listener(on_press=self.key_press)
        key_listener.start()
        while self.running:
            self.mouse.click(self.button)
            time.sleep(self.time)
        key_listener.stop()


# 新线程处理函数
def new_thread_start(button, time):
    MouseClick(button, time)


# START按键处理函数
def start():
    try:
        # 将文本框读到的字符串转化为浮点数
        time = float(input.get())
        if mouse.get() == LEFT:
            button = pynput.mouse.Button.left
        elif mouse.get() == RIGHT:
            button = pynput.mouse.Button.right
        btn_start['state'] = DISABLED
        state.delete('0.0', END)
        state.insert(INSERT, "Current State: Listening\n")
        state.insert(INSERT, "Press ESC to stop listening.\n")
        state.insert(INSERT, "Press F8 to start clicking.")
        # 开启新线程，避免GUI卡死
        t = threading.Thread(target=new_thread_start, args=(button, time))
        # 开启守护线程，这样在GUI意外关闭时线程能正常退出
        t.setDaemon(True)
        t.start()
        # 不能使用 t.join()，否则也会卡死
    except:
        state.delete('0.0', END)
        state.insert(INSERT, "Time input ERROR!\n")
        state.insert(INSERT, "You should enter an integer or a float number.")


# -------------------------------- GUI界面 --------------------------------
root = Tk()
root.title('Mouse Clicker')
root.geometry('400x290')

mouse = IntVar()
lab1 = Label(root, text='Mouse Button', font=("微软雅黑", 11), fg="gray")
lab1.place(relx=0.05, y=10, relwidth=0.4, height=30)
r1 = Radiobutton(root, text='LEFT', font=("微软雅黑", 10), value=0, variable=mouse)
r1.place(relx=0.05, y=40, relwidth=0.15, height=30)
r2 = Radiobutton(root, text='RIGHT', font=(
    "微软雅黑", 10), value=1, variable=mouse)
r2.place(relx=0.2, y=40, relwidth=0.3, height=30)

lab2 = Label(root, text='Time Interval', font=("微软雅黑", 11), fg="gray")
lab2.place(relx=0.55, y=10, relwidth=0.4, height=30)
input = Entry(root, font=("微软雅黑", 10))
input.place(relx=0.55, y=40, relwidth=0.4, height=30)

label3 = Label(root, text='---------- Current State and Instruction ----------',
               font=("微软雅黑", 8), fg="gray")
label3.place(relx=0.05, y=90, relwidth=0.9, height=20)
state = Text(root, font=("微软雅黑", 10))
state.place(relx=0.05, y=110, relwidth=0.9, height=120)
state.insert(INSERT, "Current State: IDLE\n")
state.insert(INSERT, "Choose which mouse button you want to click and set the time interval, then click START button to start clicking.")

btn_start = Button(root, text='START', font=("微软雅黑", 12),
                   fg="white", bg="gray", command=start)
btn_start.place(relx=0.3, y=240, relwidth=0.4, height=30)

root.mainloop()
# -------------------------------- GUI界面 --------------------------------
