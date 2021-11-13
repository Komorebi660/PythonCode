# 分形图的绘制

- [分形图的绘制](#分形图的绘制)
  - [目录结构](#目录结构)
  - [内容简介](#内容简介)
    - [Julia集](#julia集)
    - [Mandelbrot集](#mandelbrot集)
    - [分形叶](#分形叶)
    - [Koch雪花](#koch雪花)
  - [代码使用](#代码使用)

**分形的数学原理及本代码的绘制算法见[此](https://zhuanlan.zhihu.com/p/413921568)**

## 目录结构

```
root
│   README.md               #代码介绍(本文件)    
│
└───demo                    #一些分形图像绘制的结果
│   │   Julia_im.gif
│   │   Koch.png
│   │   Mandelbrot.gif
│   │   ...
│   
└───src                     #源文件及说明文档
│   │   DrawFractal.py      #核心代码
│   │   GUI.py              #封装为GUI界面
│   │   FunctionScripts.md  #DrawFractal.py中函数的说明
│
└───test                    #测试文件
    │   TestJulia.py        #测试Julia集的绘制
    │   TestKoch.py         #测试Koch雪花的绘制
    │   TestMandelbrot.py   #测试Mandelbrot集的绘制
```

## 内容简介

本仓库的主要内容为分形图的绘制，包含静态图片与动态图片的绘制.可绘制的分形图有：

- **`Julia`集**
- **`Mandelbrot`集**
- **分形蕨类叶片**
- **分形树枝**
- **分形龙**
- **`Koch`雪花**
- **`Hilbert`曲线**
- **`Sierpinski`三角形及四边形**

`/src/DrawFractal.py`中包含了完整且丰富的接口可供调用，可以将其看成一个库文件，使用：

```python
from DrawFractal import *
```

即可调用其中的所有函数。

`src/GUI.py`则提供了一种对`DrawFractal.py`的封装，它简化了一些参数以获得更好的人机交互体验。运行该文件，你可以使用鼠标选择控件来绘制静态图片以及动态图片。

<div align="center">
<img src=./demo/demo.png width=70%/>
</div>

`/test`文件夹中的文件则是对`DrawFractal.py`更为直接的调用，它使用了更多的参数，这样能绘制更为丰富的图像。

使用本代码绘制的一些示例图像如下：

### Julia集

<div align="center">
<img src=./demo/Julia_im.gif width=40%/>
</div>

<div align="center">
<img src=./demo/Julia_real.gif width=40%/>
</div>

<div align="center">
<img src=./demo/julia.png width=80%/>
</div>

### Mandelbrot集

<div align="center">
<img src=./demo/Mandelbrot.png width=80%/>
</div>

### 分形叶

<div align="center">
<img src=./demo/leaf_black.png width=50%>
</div>

### Koch雪花

<div align="center">
<img src=./demo/koch.gif width=60%/>
</div>

## 代码使用

安装相关库：

```
pip install numpy
pip install matplotlib
```

还需要使用其它`Python`自带库:

- `tkinter`
- `time`
- `threading`
- `math`

接下来就可以运行`./test`文件夹下的所有文件或者`./src/GUI.py`来绘制分形图案，你也可以在新的`py`文件中导入`DrawFractal`使用更加完整且丰富的功能。

`DrawFractal.py`中所有`draw_*`函数都是绘制图像的函数，详细说明见`src/FunctionScripts.md`.

**打包**

在`Windows`环境下，你还可以将其打包为`.exe`文件，这样即使电脑不含`Python`也能运行，方法如下：

安装`pyinstaller`:

```
pip install pyinstaller
```

在源码所在目录执行：

```
pyinstaller -F -w GUI.py
```

即可生成`.exe`文件，位于`/dist`目录下