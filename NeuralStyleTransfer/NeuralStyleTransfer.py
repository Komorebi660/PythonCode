# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2022 Komorebi660 All rights reserved.
# THIS FILE IS A PYSTORCH VERSION OF NERUAL STYLE TRANSFER
# ----------------------------------------------------------
import sys
import itertools
from collections import OrderedDict

import matplotlib.pyplot as plt
from PIL import Image
from tqdm.auto import tqdm

import torch
from torch import nn, optim
from torch.nn.functional import mse_loss
from torchvision import transforms
from torchvision.models import vgg19
from torchvision.transforms.functional import resize

# 用户可修改的参数
NUM_STEPS = 500  # 循环步数
IMAGE_SIZE = 500  # 图片尺寸
CONTENT_WEIGHT = 1e0  # 权重
STYLE_WEIGHT = 1e5

# 从命令行获取图像文件路径
CONTENT_IMAGE_PATH = None
STYLE_IMAGE_PATH = None
RESULT_IMAGE_PATH = None
argv = sys.argv[1:]
if(len(argv) < 2):
    print("Too little parameters, the command should be like this:")
    print(
        "python NeuralStyleTransfer.py <content image path> <style image path> [result image path]")
    exit(-1)
elif(len(argv) > 3):
    print("Too much parameters, the command should be like this:")
    print(
        "python NeuralStyleTransfer.py <content image path> <style image path> [result image path]")
    exit(-1)
else:
    CONTENT_IMAGE_PATH = argv[0]
    STYLE_IMAGE_PATH = argv[1]
    if(len(argv) == 3):
        RESULT_IMAGE_PATH = argv[2]


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"using {device}")


class MultiLayerEncoder(nn.Sequential):
    # 处理vgg,在layer后插入image
    def forward(self, image, *layer_cfgs):
        storage = {}
        deepest_layer = self._find_deepest_layer(*layer_cfgs)
        for layer, module in self.named_children():
            image = storage[layer] = module(image)
            if layer == deepest_layer:
                break
        return [[storage[layer] for layer in layers] for layers in layer_cfgs]

    def children_names(self):
        for name, module in self.named_children():
            yield name

    def _find_deepest_layer(self, *layer_cfgs):
        # find all unique requested layers
        req_layers = set(itertools.chain(*layer_cfgs))
        try:
            # find the deepest requested layer by indexing the layers within
            # the multi layer encoder
            children_names = list(self.children_names())
            return sorted(req_layers, key=children_names.index)[-1]
        except ValueError as error:
            layer = str(error).split()[0]
        raise ValueError(
            f"Layer {layer} is not part of the multi-layer encoder.")

    # 删除不必要的层
    def trim(self, *layer_cfgs):
        deepest_layer = self._find_deepest_layer(*layer_cfgs)
        children_names = list(self.children_names())
        del self[children_names.index(deepest_layer) + 1:]


class Normalize(nn.Module):
    # VGG在训练的时候对RGB三个通道做了归一化，
    # 使用的均值和方差是[0.485, 0.456, 0.406]和[0.229, 0.224, 0.225]，
    # 因此我们输入的图片也要用同样的参数做归一化。
    def __init__(self, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
        super().__init__()
        self.register_buffer("mean", torch.tensor(mean).view(1, -1, 1, 1))
        self.register_buffer("std", torch.tensor(std).view(1, -1, 1, 1))

    def forward(self, image):
        return (image - self.mean) / self.std


class VGGMultiLayerEncoder(MultiLayerEncoder):
    def __init__(self, vgg_net):
        # 构造normalize层
        modules = OrderedDict((("preprocessing", Normalize()),))
        # 遍历vgg
        block = depth = 1
        for module in vgg_net.features.children():
            if isinstance(module, nn.Conv2d):
                layer = f"conv{block}_{depth}"
            elif isinstance(module, nn.BatchNorm2d):
                layer = f"bn{block}_{depth}"
            elif isinstance(module, nn.ReLU):
                # without inplace=False the encodings of the previous layer would no
                # longer be accessible after the ReLU layer is executed
                module = nn.ReLU(inplace=False)
                layer = f"relu{block}_{depth}"
                # each ReLU layer increases the depth of the current block by one
                depth += 1
            elif isinstance(module, nn.MaxPool2d):
                layer = f"pool{block}"
                # each max pooling layer marks the end of the current block
                block += 1
                depth = 1
            else:
                msg = f"Type {type(module)} is not part of the VGG architecture."
                raise RuntimeError(msg)

            modules[layer] = module

        super().__init__(modules)


# 求损失函数的基类
class MultiLayerLoss(nn.Module):
    def __init__(self, score_weight=1e0):
        super().__init__()
        self.score_weight = score_weight
        self._numel_target_encs = 0

    def _target_enc_name(self, idx):
        return f"_target_encs_{idx}"

    def set_target_encs(self, target_encs):
        self._numel_target_encs = len(target_encs)
        for idx, enc in enumerate(target_encs):
            self.register_buffer(self._target_enc_name(idx), enc.detach())

    @property
    def target_encs(self):
        return tuple(
            getattr(self, self._target_enc_name(idx))
            for idx in range(self._numel_target_encs)
        )

    # 计算loss, 接入vgg
    def forward(self, input_encs):
        if len(input_encs) != self._numel_target_encs:
            msg = (
                f"The number of given input encodings and stored target encodings "
                f"does not match: {len(input_encs)} != {self._numel_target_encs}"
            )
            raise RuntimeError(msg)

        layer_losses = [
            self.calculate_score(input, target)
            for input, target in zip(input_encs, self.target_encs)
        ]
        return sum(layer_losses) / len(layer_losses) * self.score_weight

    def calculate_score(self, input, target):
        raise NotImplementedError


# 计算content loss
class ContentLoss(MultiLayerLoss):
    def calculate_score(self, input, target):
        return mse_loss(input, target)


# 计算gram矩阵
def channelwise_gram_matrix(x, normalize=True):
    x = torch.flatten(x, 2)
    G = torch.bmm(x, x.transpose(1, 2))
    if normalize:
        return G / x.size()[-1]
    else:
        return G


# 计算style loss
class StyleLoss(MultiLayerLoss):
    def calculate_score(self, input, target):
        return mse_loss(channelwise_gram_matrix(input), channelwise_gram_matrix(target))


# 将图片转化为tensor
import_from_pil = transforms.Compose(
    (
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.unsqueeze(0)),
        transforms.Lambda(lambda x: x.to(device)),
    )
)


# 将tensor转化为图片
export_to_pil = transforms.Compose(
    (
        transforms.Lambda(lambda x: x.cpu()),
        transforms.Lambda(lambda x: x.squeeze(0)),
        transforms.Lambda(lambda x: x.clamp(0.0, 1.0)),
        transforms.ToPILImage(),
    )
)


# 读入图片
def read_image(file):
    try:
        image = Image.open(file)
        image = resize(image, IMAGE_SIZE)
        return import_from_pil(image)
    except:
        print("Open Image ERROR!")
        exit(-1)


# 展示图片
def show_image(image):
    _, ax = plt.subplots()
    ax.axis("off")
    image = export_to_pil(image)
    ax.imshow(image)
    # do not save
    if(RESULT_IMAGE_PATH == None):
        plt.show()
    # save
    else:
        try:
            plt.savefig(RESULT_IMAGE_PATH, bbox_inches='tight', pad_inches=0.0)
            plt.show()
            print("Save Successfully!")
        except:
            print("Can not Save Result Image!")
            exit(-1)


content_image = read_image(CONTENT_IMAGE_PATH)
style_image = read_image(STYLE_IMAGE_PATH)

content_layers = ("relu4_2",)
style_layers = ("relu1_1", "relu2_1", "relu3_1", "relu4_1", "relu5_1")

# 构造模型
multi_layer_encoder = VGGMultiLayerEncoder(vgg19(pretrained=True)).to(device)
multi_layer_encoder.trim(content_layers, style_layers)

with torch.no_grad():
    target_content_encs = multi_layer_encoder(content_image, content_layers)[0]
    target_style_encs = multi_layer_encoder(style_image, style_layers)[0]

# 计算损失
content_loss = ContentLoss(score_weight=CONTENT_WEIGHT)
content_loss.set_target_encs(target_content_encs)

style_loss = StyleLoss(score_weight=STYLE_WEIGHT)
style_loss.set_target_encs(target_style_encs)

# 通过梯度下降修改input_image, 使loss达到最低
input_image = content_image.clone()
optimizer = optim.LBFGS([input_image.requires_grad_(True)], max_iter=1)
with tqdm(desc="Image optimization", total=NUM_STEPS) as progress_bar:
    for _ in range(NUM_STEPS):
        def closure():
            optimizer.zero_grad()

            input_encs = multi_layer_encoder(input_image,
                                             content_layers,
                                             style_layers)
            input_content_encs, input_style_encs = input_encs

            content_score = content_loss(input_content_encs)
            style_score = style_loss(input_style_encs)

            perceptual_loss = content_score + style_score
            perceptual_loss.backward()

            '''
            progress_bar.set_postfix(
                loss=f"{float(perceptual_loss):.3e}", refresh=False)
            '''
            progress_bar.update()
            return perceptual_loss
        optimizer.step(closure)

# 获取结果
output_image = input_image.detach()
show_image(output_image)
