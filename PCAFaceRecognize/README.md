# PCA降维实现人脸识别

PCA(主成分分析)是一种主流的线性降维方法。以“最小重构误差”为目标导向，通过降维(投影)，用数据中最主要的信息表达原数据，压缩数据存储空间，同时减轻噪声的影响。本仓库将通过PCA方法对人脸图像进行降维压缩，并利用压缩后的数据进行人脸识别，在此过程中将探索PCA过程对图像质量以及对分类识别的准确度的影响。

## 依赖安装

```bash
pip install numpy matplotlib sklearn pandas PIL
```

## 数据集准备

实验所使用的数据来自[PubFig人脸数据集](https://www.cs.columbia.edu/CAVE/databases/pubfig/)，该数据集包含 $200$ 个名人的人脸图像，共 $58,797$ 张图像。我们从中抽取`Alyssa Milano`、`Barack Obama`、`Daniel Craig`的人脸图像作为实验数据，每人各取 $36$ 张作为训练集， $12$ 张作为测试集，共 $144$ 张图像。为了便于后续处理，我们将原始图片中的人脸部分裁剪出来，并缩放至 $64\times 64$ 的灰度图像。

```bash
cd dataset
# 图像抓取
python download.py
# 数据集划分与打包
python split.py
```

实验图像的一些示例如下所示：

<div align="center">
<img src=./dataset/images/Alyssa_Milano_1.jpg width=19%/>
<img src=./dataset/images/Alyssa_Milano_6.jpg width=19%/>
<img src=./dataset/images/Alyssa_Milano_13.jpg width=19%/>
<img src=./dataset/images/Alyssa_Milano_20.jpg width=19%/>
<img src=./dataset/images/Alyssa_Milano_53.jpg width=19%/>
</div>

<div align="center">
  <img src=./dataset/images/Barack_Obama_2.jpg width=19%/>
  <img src=./dataset/images/Barack_Obama_5.jpg width=19%/>
  <img src=./dataset/images/Barack_Obama_6.jpg width=19%/>
  <img src=./dataset/images/Barack_Obama_17.jpg width=19%/>
  <img src=./dataset/images/Barack_Obama_88.jpg width=19%/>
</div>

<div align="center">
  <img src=./dataset/images/Daniel_Craig_1.jpg width=19%/>
  <img src=./dataset/images/Daniel_Craig_7.jpg width=19%/>
  <img src=./dataset/images/Daniel_Craig_8.jpg width=19%/>
  <img src=./dataset/images/Daniel_Craig_10.jpg width=19%/>
  <img src=./dataset/images/Daniel_Craig_27.jpg width=19%/>
</div>

## PCA降维

主成分特征值占比曲线：

<div align="center">
  <img src=./figs/eigenvalues.jpg width=60%/>
</div>

第1、2、5、10、20、50、80、100个特征向量(特征脸)：

<div align="center">
  <img src=./figs/eigenface_1.jpg width=11%/>
  <img src=./figs/eigenface_2.jpg width=11%/>
  <img src=./figs/eigenface_5.jpg width=11%/>
  <img src=./figs/eigenface_10.jpg width=11%/>
  <img src=./figs/eigenface_20.jpg width=11%/>
  <img src=./figs/eigenface_50.jpg width=11%/>
  <img src=./figs/eigenface_80.jpg width=11%/>
  <img src=./figs/eigenface_100.jpg width=11%/>
</div>

原始图像和使用100、80、50、20、10、5、1个主成分降维后重构的图像：

<div align="center">
  <img src=./figs/ori_Alyssa_Milano.jpg width=11%/>
  <img src=./figs/reconstruct_Alyssa_Milano_100.jpg width=11%/>
  <img src=./figs/reconstruct_Alyssa_Milano_80.jpg width=11%/>
  <img src=./figs/reconstruct_Alyssa_Milano_50.jpg width=11%/>
  <img src=./figs/reconstruct_Alyssa_Milano_20.jpg width=11%/>
  <img src=./figs/reconstruct_Alyssa_Milano_10.jpg width=11%/>
  <img src=./figs/reconstruct_Alyssa_Milano_5.jpg width=11%/>
  <img src=./figs/reconstruct_Alyssa_Milano_1.jpg width=11%/>
  <p>Alyssa Milano</p>
</div>

<div align="center">
  <img src=./figs/ori_Barack_Obama.jpg width=11%/>
  <img src=./figs/reconstruct_Barack_Obama_100.jpg width=11%/>
  <img src=./figs/reconstruct_Barack_Obama_80.jpg width=11%/>
  <img src=./figs/reconstruct_Barack_Obama_50.jpg width=11%/>
  <img src=./figs/reconstruct_Barack_Obama_20.jpg width=11%/>
  <img src=./figs/reconstruct_Barack_Obama_10.jpg width=11%/>
  <img src=./figs/reconstruct_Barack_Obama_5.jpg width=11%/>
  <img src=./figs/reconstruct_Barack_Obama_1.jpg width=11%/>
  <p>Barack Obama</p>
</div>

<div align="center">
  <img src=./figs/ori_Daniel_Craig.jpg width=11%/>
  <img src=./figs/reconstruct_Daniel_Craig_100.jpg width=11%/>
  <img src=./figs/reconstruct_Daniel_Craig_80.jpg width=11%/>
  <img src=./figs/reconstruct_Daniel_Craig_50.jpg width=11%/>
  <img src=./figs/reconstruct_Daniel_Craig_20.jpg width=11%/>
  <img src=./figs/reconstruct_Daniel_Craig_10.jpg width=11%/>
  <img src=./figs/reconstruct_Daniel_Craig_5.jpg width=11%/>
  <img src=./figs/reconstruct_Daniel_Craig_1.jpg width=11%/>
  <p>Daniel Craig</p>
</div>

可以看出，随着主成分数量的增加，重建的图片越来越清晰，同时也越来越接近原始图片。

## 人脸识别

在使用PCA对图片进行降维后，我们在训练集上计算每一类图片降维后的中心向量作为该类别的表征向量。然后，在测试集上，我们将每一张图片降维后与三个类别的表征向量计算欧氏距离，将距离最小的类别作为该图片的预测类别，若最小距离大于一定阈值，则认为图片中不包含人脸。

```bash
python predict.py
```

表征向量重构后的图片：

<div align="center">
  <img src=./figs/reconstruct_mean_Alyssa_Milano.jpg width=30%/>
  <img src=./figs/reconstruct_mean_Barack_Obama.jpg width=30%/>
  <img src=./figs/reconstruct_mean_Daniel_Craig.jpg width=30%/>
</div>

使用不同数量主成分降维后的人脸识别错误率：

| **主成分数量** | 1   | 2   | 5   | 10  | 20  | 50  | 80  | *90* | 100 |
| -------------- | --- | --- | --- | --- | --- | --- | --- | ---- | --- |
| **预测错误数** | 16  | 16  | 13  | 8   | 4   | 2   | 1   | *0*  | 2   |

可以看出，随着主成分数量的增加，预测准确率逐渐提高，当主成分数量为90时，预测准确率达到了100%。这说明，随着主成分数量的增加，重建的图片所包含的信息越来越多，越来越接近原始图片，分类的准确率也越来越高。然而，进一步增加主成分数量，预测准确率反而下降了，这是因为随着主成分数量的进一步增加，越来越多的噪声被引入，这些噪声对分类造成了干扰，从而导致了预测准确率的下降。