# 基于神经网络的图像风格迁移

## 目录结构

```
root
│
├─README.md                 #说明文档(本文件)
│  
├─images                    #存储demo图片以及其它需要在README中使用的图片
│   | content.jpg
│   | result.jpg
│   | style.jpg
|     ......
│      
└─src                       #本项目源码
    | PysticheVersion.py    #基于pystiche的实现
    | PytorchVersion.py     #基于pytorche的实现
```

## Nerual Style Transfer介绍

我们认为画家的作品包含两部分内容——内容(`Content`)和风格(`Style`)，`Nerual Style Transfer`要做的事就是把图片的`Content`和`Style`剥离，然后重新组合，实现把一个图像的风格和另一个图像的内容相结合。

深度卷积网络通过层次化的表示，每一层建立在前一层的基础上，因此逐层学习到越来越高层，越来越抽象的特征。高层的网络丢弃掉了和识别物体无关的一些细节，它们更加关注图片的内容和而不是像素级的细节，我们称之为内容特征(`Content Features`)。而风格是与具体内容无关的一种作者个性化的特征，我们可以通过计算同一层神经网络的`Filter`的相关性来提取风格特征(`Style Features`)。

更详细的介绍参看下面两篇文章：

- [Nerual Style Transfer](http://fancyerii.github.io/books/neural-style-transfer/)
- [图像风格迁移(Neural Style)简史](https://zhuanlan.zhihu.com/p/26746283)

## 源码介绍

### 基于Pytorch的版本(`PytorchVersion.py`)

本代码利用训练好的`VGG16`神经网络，基于`Gatys`教授的论文[A Neural Algorithm of Artistic Style](https://arxiv.org/abs/1508.06576)，使用`Python`实现。

使用本代码需要安装以下库：

- **matplotlib**
- **pytorch**

其中`pytorch`库分为`CPU`和`GPU`版本，安装`GPU`版本前需要安装`CUDA`及`CUDNN`. 详情参见[pytorch 官网](https://pytorch.org/)，选择合适的版本，如下图所示：

<div align="center">
<img src=./images/pytorch.png width=80%/>
</div>

由于`pytorch`较大，下载过程可能需要花费较长时间。

运行代码你需要输入两张图片——内容图片和风格图片，并进入`src--PytorchVersion.py`修改以下内容：

- **CONTENT_IMAGE_PATH**: 内容图片保存路径
- **STYLE_IMAGE_PATH**: 风格图片保存路径
- **RESULT_IMAGE_PATH**: 结果保存路径
- **NUM_STEPS**: 迭代次数，默认`500`
- **IMAGE_SIZE**: 图像压缩尺寸，如使用`GPU`，建议设为`500`；如使用`CPU`，建议设为`200`
- **CONTENT_WEIGHT**: 内容权重
- **STYLE_WEIGHT**: 风格权重

然后直接运行代码，在运行过程中会依次打印版本、当前使用`GPU`还是`CPU`、图片生成进度等信息，生成结束后会弹窗展示图片并保存在制定路径中(**第一次运行可能需要较长时间，因为需要下载`VGG16`神经网络，大约`548MiB`**)。

本代码参考[这篇文章](https://docs.pystiche.org/en/latest/galleries/examples/beginner/example_nst_without_pystiche.html)

### 基于Pystiche的版本(`PysticheVersion.py`)

`Pystiche`是对上面`Pytorch`的实现进行了一层封装，用户可以更加方便的使用相关函数，使得代码更为简洁。

在终端中输入：

```
pip install pystiche
```

即可安装`pystiche`及其依赖库。**注意，如果之前没有安装`pytorch`，这里默认安装的`pytorch`版本是`CPU`版，如果要使用`GPU`加速，需要按照上面的方法重新安装。**

运行代码同上。

本代码参考[这篇文章](https://docs.pystiche.org/en/latest/galleries/examples/beginner/example_nst_with_pystiche.html)

## 效果展示

- content image

<div align="center">
<img src=./images/content.jpg width=50%/>
</div>

- style image

<div align="center">
<img src=./images/style.jpg width=50%/>
</div>

- result

<div align="center">
<img src=./images/result.jpg width=50%/>
</div>

整个训练过程花费大约`1min 45secs`，消耗大约`2500MiB`内存。测试机器的配置为：

- Intel i7-9750H
- Nvidia RTX2060
- Memory: 16GiB
- SSD: 512GiB