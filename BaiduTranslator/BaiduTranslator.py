# ----------------------------------------------------------
# Copyright © 2021 Komorebi660 All rights reserved.
# ----------------------------------------------------------

import js2py
import requests
import re
from tkinter import *

# 以下内容请自行抓包获取
USER_AGENT = ''
COOKIE = ''
TOKEN = ''


class BaiDuTranslator:
    def __init__(self, query):
        self.query = query
        self.url = 'https://fanyi.baidu.com/v2transapi'
        self.headers = {
            "User-Agent": USER_AGENT,
            "Cookie": COOKIE
        }
        self.data = {
            'from': '',
            'to': '',
            'query': self.query,
            'simple_means_flag': 3,
            'transtype': 'enter',
            'sign': '',
            'token': TOKEN,
            'domain': 'common'
        }

    def GetSign(self):
        # 获取gtk
        response = requests.Session().get(
            'http://fanyi.baidu.com/', headers=self.headers)
        gtk = re.findall(";window.gtk = ('.*?');",
                         response.content.decode())[0]
        # 调用js
        context = js2py.EvalJs()
        #-------------------- 获取sign所调用的js --------------------#
        js = r'''
            function a(r) {
                if (Array.isArray(r)) {
                    for (var o = 0, t = Array(r.length); o < r.length; o++)
                        t[o] = r[o];
                    return t
                }
                return Array.from(r)
            }
            function n(r, o) {
                for (var t = 0; t < o.length - 2; t += 3) {
                    var a = o.charAt(t + 2);
                    a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
                        a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
                        r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
                }
                return r
            }
            function e(r) {
                var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
                if (null === o) {
                    var t = r.length;
                    t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
                } else {
                    for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
                        "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                        C !== h - 1 && f.push(o[C]);
                    var g = f.length;
                    g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
                }
                var u = void 0
                    , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
                u = 'null !== i ? i : (i = window[l] || "") || ""';
                for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
                    var A = r.charCodeAt(v);
                    128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
                        S[c++] = A >> 18 | 240,
                        S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
                        S[c++] = A >> 6 & 63 | 128),
                        S[c++] = 63 & A | 128)
                }
                for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
                    p += S[b],
                        p = n(p, F);
                return p = n(p, D),
                    p ^= s,
                0 > p && (p = (2147483647 & p) + 2147483648),
                    p %= 1e6,
                p.toString() + "." + (p ^ m)
            }
        '''
        #-------------------- 获取sign所调用的js --------------------#
        # js中添加一行gtk
        js = js.replace(
            '\'null !== i ? i : (i = window[l] || "") || ""\'', gtk)
        # 执行js
        context.execute(js)
        # 调用函数得到sign
        sign = context.e(self.query)
        self.data['sign'] = sign

    def Translate_From_en_To_zh(self):
        # 首先获取sign
        self.GetSign()
        # 设置中英次序
        self.data['from'] = 'en'
        self.data['to'] = 'zh'
        # 发送翻译请求
        response = requests.Session().post(
            self.url, data=self.data, headers=self.headers).json()
        # 解析数据
        result_array = response['trans_result']['data']
        result = ''
        for i in range(0, len(result_array)):
            for j in range(0, len(result_array[i]['result'])):
                result += result_array[i]['result'][j][1]
            result += '\n'
        # 输出
        output.delete('0.0', END)
        output.insert(INSERT, result)

    def Translate_From_zh_To_en(self):
        # 首先获取sign
        self.GetSign()
        # 设置中英次序
        self.data['from'] = 'zh'
        self.data['to'] = 'en'
        # 发送翻译请求
        response = requests.Session().post(
            self.url, data=self.data, headers=self.headers).json()
        # 解析数据
        result_array = response['trans_result']['data']
        result = ''
        for i in range(0, len(result_array)):
            for j in range(0, len(result_array[i]['result'])):
                result += result_array[i]['result'][j][1]
            result += '\n'
        # 输出
        output.delete('0.0', END)
        output.insert(INSERT, result)


TEXT = 'Welcome to use Translator. Powered by Baidu Translator.\n欢迎使用翻译器，由百度翻译提供技术支持'
REMINDER_EN = 'Waiting to response......'
REMINDER_ZH = '等待响应中......'


def getrans_zh_to_en():
    word = input.get('0.0', END)
    Trans = BaiDuTranslator(word)
    output.delete('0.0', END)
    output.insert(INSERT, str(REMINDER_ZH))
    root.update()
    Trans.Translate_From_zh_To_en()


def getrans_en_to_zh():
    word = input.get('0.0', END)
    Trans = BaiDuTranslator(word)
    output.delete('0.0', END)
    output.insert(INSERT, str(REMINDER_EN))
    root.update()
    Trans.Translate_From_en_To_zh()


def flush():
    input.delete('0.0', END)
    output.delete('0.0', END)


root = Tk()
root.title('Translator')
root.geometry('1000x600')

header = Label(root, text=TEXT, font=("微软雅黑", 11, "bold"))
header.place(relx=0.1, y=5, relwidth=0.8, height=50)

lab1 = Label(root, text='INPUT\n输入', font=("微软雅黑", 9))
lab1.place(relx=0.15, y=50, relwidth=0.2, height=40)

lab2 = Label(root, text='OUTPUT\n输出', fg="gray", font=("微软雅黑", 9))
lab2.place(relx=0.65, y=50, relwidth=0.2, height=40)

input = Text(root, font=("微软雅黑", 10))
input.place(relx=0.05, y=90, relwidth=0.4, relheight=0.8)

output = Text(root, fg="gray", font=("微软雅黑", 10))
output.place(relx=0.55, y=90, relwidth=0.4, relheight=0.8)

btn_zh_to_en = Button(root, text='zh-->en\n中-->英', font=("微软雅黑", 10), fg="white",
                      bg="gray", command=getrans_zh_to_en)
btn_zh_to_en.place(relx=0.46, rely=0.28, relwidth=0.08, height=40)

btn_zh_to_en = Button(root, text='en-->zh\n英-->中', font=("微软雅黑", 10), fg="white",
                      bg="gray", command=getrans_en_to_zh)
btn_zh_to_en.place(relx=0.46, rely=0.50, relwidth=0.08, height=40)

btn_flush = Button(root, text='FLUSH', font=(
    "微软雅黑", 10), fg="red", command=flush)
btn_flush.place(relx=0.46, rely=0.75, relwidth=0.08, height=20)

root.mainloop()
