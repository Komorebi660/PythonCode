# 分形图的绘制

- [分形图的绘制](#分形图的绘制)
  - [分形简介](#分形简介)
  - [目录结构](#目录结构)
  - [内容简介](#内容简介)
    - [Julia集](#julia集)
    - [Mandelbrot集](#mandelbrot集)
    - [分形叶](#分形叶)
    - [Koch雪花](#koch雪花)
  - [代码使用](#代码使用)

## 分形简介

1967年, 本华·曼德博(`Benoît B. Mandelbrot`)在其论文《英国的海岸线有多长? 统计自相似性与分数维数》中首次创造性地阐述了分形的理论。1982年, `Mandelbrot`利用拉丁文`fractus`(有“零碎”、“破裂”之意)创造了`fractal`这个英文、法文、德文共用的词, 中文将其译为“分形”。`Mandelbrot`成功地发展了分形几何学的理论, 也因此被称为“分形之父”。一般来说, 分形通常被定义为“一个粗糙或零碎的几何形状, 可以分成数个部分, 且每一部分都(至少近似地)是整体缩小后的形状”, 即具有“精细的结构”、“无限不规则”、“自相似”的性质。分形在数学中是一种抽象的物体, 用于描述自然界中存在的事物。

分形几何学自从诞生到现在, 无论是在理论方面还是在应用方面都取得了巨大进步。分形几何不仅展示了数学之美, 也揭示了世界的本质, 还改变了人们理解自然奥秘的方式; 可以说分形几何是真正描述大自然的几何学, 对它的研究也极大地拓展了人类的认知疆域。分形几何学建立以后, 很快就引起了许多学科的关注, 这是因为它不仅在理论上, 而且在物理学、化学、地质学、生物学等领域内都具有重要的应用价值和广阔的发展前景。

近年来, 随着计算机及编程语言的兴起与成熟, 人们可以通过简单编程获取分形图案, 从而极大地方便了工程上对于分形理论的应用。本仓库就是利用`Python`实现了三类经典分形的可视化。

## 目录结构

```
root
│   README.md               #仓库介绍(本文件)    
│
└───demo                    #一些分形图像绘制的结果
│   │   Julia_im.gif
│   │   Koch.png
│   │   Mandelbrot.gif
│   │   ...
│   
└───src                     #源文件及说明文档
│   │   DrawFractal.py      #核心代码
│   │   GUI.py              #GUI界面
|   |   theme.tcl           #主题配置文件
│   │   FunctionScripts.md  #DrawFractal.py中函数的说明
|   └───theme               #主题核心配置
|
└───test                    #测试文件
    │   TestJulia.py        #测试Julia集的绘制
    │   TestKoch.py         #测试Koch雪花的绘制
    │   TestMandelbrot.py   #测试Mandelbrot集的绘制
```

## 内容简介

本仓库的主要内容为分形图的绘制，包含静态图片与动态图片的绘制。可绘制的分形图有：

- **`Julia`集与`Mandelbrot`集**
- **基于概率生成的分形叶片**
- **基于L系统生成的分形树、分形龙、`Koch`雪花、`Hilbert`曲线、`Sierpinski`三角形及四边形**

`/src/DrawFractal.py`中包含了完整且丰富的接口可供调用，可以将其看成一个库文件，使用：

```python
from DrawFractal import *
```

即可调用其中的所有函数。

`src/GUI.py`则提供了一种对`DrawFractal.py`的封装，它简化了一些参数以获得更好的人机交互体验。运行该文件，你可以使用鼠标选择控件来绘制静态图片以及动态图片。

<div align="center">
<img src=./demo/demo.png width=70%/>
</div>

`/test`文件夹中的文件则是对`DrawFractal.py`直接调用的示例，它使用了更多的参数，这样能绘制更为丰富的图像。

使用本代码绘制的一些示例图像如下：

### Julia集

<div align="center">
<img src=./demo/Julia_im.gif width=30%/>
<img src=./demo/Julia_real.gif width=30%/>
</div>

<div align="center">
<img src=./demo/julia.png width=60%/>
</div>

### Mandelbrot集

<div align="center">
<img src=./demo/Mandelbrot.png width=60%/>
</div>

### 分形叶

<div align="center">
<img src=./demo/leaf_black.png width=30%>
<img src=./demo/leaf_white.png width=30%>
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

接下来就可以运行`./test`文件夹下的所有文件或者`./src/GUI.py`来绘制分形图案，你也可以在新的`Python`文件中导入`DrawFractal`使用更加完整且丰富的功能。

`DrawFractal.py`中所有`draw_*`函数都是绘制图像的函数，详细说明见`src/FunctionScripts.md`.