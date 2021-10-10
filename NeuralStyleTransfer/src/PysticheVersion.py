# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# THIS FILE IS A PYSTICHE VERSION OF NERUAL STYLE TRANSFER
# ----------------------------------------------------------
import pystiche
from pystiche import enc, loss, optim
from pystiche.image import show_image, read_image, write_image
from pystiche.misc import get_device, get_input_image

# 图像文件路径
CONTENT_IMAGE_PATH = "./content.jpg"
STYLE_IMAGE_PATH = "./style.jpg"
RESULT_IMAGE_PATH = "./result.jpg"
# 循环步数
NUM_STEPS = 500
# 图片尺寸
IMAGE_SIZE = 500
# 权重
CONTENT_WEIGHT = 1e0
STYLE_WEIGHT = 1e3

print(f"pystiche version: {pystiche.__version__}")

device = get_device()
print(f"using {device}")

# 构造模型
multi_layer_encoder = enc.vgg19_multi_layer_encoder()
# print(multi_layer_encoder)

# 计算content loss
content_layer = "relu4_2"
content_encoder = multi_layer_encoder.extract_encoder(content_layer)
content_weight = CONTENT_WEIGHT
content_loss = loss.FeatureReconstructionLoss(
    content_encoder, score_weight=content_weight
)

# 计算style loss
style_layers = ("relu1_1", "relu2_1", "relu3_1", "relu4_1", "relu5_1")
style_weight = STYLE_WEIGHT


def get_style_op(encoder, layer_weight):
    return loss.GramLoss(encoder, score_weight=layer_weight)


style_loss = loss.MultiLayerEncodingLoss(
    multi_layer_encoder, style_layers, get_style_op, score_weight=style_weight,
)

perceptual_loss = loss.PerceptualLoss(content_loss, style_loss).to(device)
# print(perceptual_loss)

content_image = read_image(CONTENT_IMAGE_PATH, size=IMAGE_SIZE, device=device)
#show_image(content_image, title="Content image")

style_image = read_image(STYLE_IMAGE_PATH, size=IMAGE_SIZE, device=device)
#show_image(style_image, title="Style image")

perceptual_loss.set_content_image(content_image)
perceptual_loss.set_style_image(style_image)

starting_point = "content"
input_image = get_input_image(starting_point, content_image=content_image)

# 梯度下降计算
output_image = optim.image_optimization(input_image,
                                        perceptual_loss,
                                        num_steps=NUM_STEPS)

write_image(output_image, RESULT_IMAGE_PATH)
