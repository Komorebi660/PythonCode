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
└─NeuralStyleTransfer.py    #本项目源码
```

## Nerual Style Transfer 介绍

我们认为画家的作品包含两部分内容——内容(`Content`)和风格(`Style`)，`Nerual Style Transfer`要做的事就是把图片的`Content`和`Style`剥离，然后重新组合，实现把一个图像的风格和另一个图像的内容相结合。

深度卷积网络通过层次化的表示，每一层建立在前一层的基础上，因此逐层学习到越来越高层，越来越抽象的特征。高层的网络丢弃掉了和识别物体无关的一些细节，它们更加关注图片的内容和而不是像素级的细节，我们称之为内容特征(`Content Features`)。而风格是与具体内容无关的一种作者个性化的特征，我们可以通过计算同一层神经网络的`Filter`的相关性来提取风格特征(`Style Features`)。

更详细的介绍参看下面两篇文章：

- [Nerual Style Transfer](http://fancyerii.github.io/books/neural-style-transfer/)
- [图像风格迁移(Neural Style)简史](https://zhuanlan.zhihu.com/p/26746283)

## 源码介绍

本代码利用训练好的`VGG16`神经网络，基于`Gatys`教授的论文[A Neural Algorithm of Artistic Style](https://arxiv.org/abs/1508.06576)，使用`Python`实现。

使用本代码需要安装以下库：

- **matplotlib**
- **pytorch**

其中`pytorch`库分为`CPU`和`GPU`版本，安装`GPU`版本前需要安装`CUDA`及`CUDNN`. 详情参见[pytorch 官网](https://pytorch.org/)，选择合适的版本，如下图所示：

<div align="center">
<img src=./images/pytorch.png width=80%/>
</div>

由于`pytorch`较大，下载过程可能需要花费较长时间。

为了运行代码，你需要准备两张图片——内容图片和风格图片，然后输入：

```
python NeuralStyleTransfer.py <content image path> <style image path> [result image path]
```

即可运行代码，其中，`content image path`是内容图片的路径；`style image path`是风格图片的路径；`result image path`是结果的存储路径，这个参数是可选的，若不指明，则最终的结果将不会存储。

你还可以在`NeuralStyleTransfer.py`中修改以下内容：

- **NUM_STEPS**: 迭代次数，默认`500`
- **IMAGE_SIZE**: 图像压缩尺寸，如使用`GPU`，建议设为`500`；如使用`CPU`，建议设为`200`
- **CONTENT_WEIGHT**: 内容权重
- **STYLE_WEIGHT**: 风格权重

以调整图片的最终效果。

在运行过程中会打印当前使用`GPU`还是`CPU`：

```
using cuda    //表明使用GPU
using cpu     //表明使用CPU
```

运行中还会打印代码运行的进度信息，如：

```
Image optimization:  74%|██████████████████████████████████████████████████████████████████████████████████▎                            | 371/500 [01:16<00:27,  4.73it/s] 
```

**注意：第一次运行可能需要较长时间，因为需要下载`VGG16`神经网络，大约`548MiB`**。

本代码参考[这篇文章](https://docs.pystiche.org/en/latest/galleries/examples/beginner/example_nst_without_pystiche.html)

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