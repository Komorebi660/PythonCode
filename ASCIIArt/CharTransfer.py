# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# ----------------------------------------------------------
from PIL import Image, ImageDraw, ImageFont
from tqdm.auto import tqdm
import sys

# 用户可修改参数
MAX_SIZE = 800  # 图片最大尺寸
TYPEFACE_PATH = "javatext.ttf"  # 字符文件路径

# 字符列表
ascii_char = list(
    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


# 将256灰度映射到70个字符上
def get_char(r, b, g, alpha=256):
    # 透明则直接返回空格
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]


def CharTransfer(path):
    try:
        im = Image.open(path)
        # 调整图片至合适大小
        WIDTH, HEIGHT = im.size
        max = WIDTH if WIDTH > HEIGHT else HEIGHT
        if(max > MAX_SIZE):
            rate = MAX_SIZE/max
            WIDTH = int(WIDTH*rate)
            HEIGHT = int(HEIGHT*rate)
            im = im.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        # 创建新图片用来保存结果
        output = Image.new('RGB', (WIDTH*10, HEIGHT*10), (255, 255, 255))
        output_draw = ImageDraw.Draw(output)
        font = ImageFont.truetype(TYPEFACE_PATH, 13)
        # 转化
        with tqdm(desc="Transfering", total=HEIGHT) as progress_bar:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    ch = get_char(*im.getpixel((j, i)))
                    output_draw.text((j*10, i*10),
                                     ch,
                                     fill=(0, 0, 0),
                                     font=font)
                progress_bar.update()
            return output
    except:
        print("ERROR: Can not Open Image!")
        exit(-1)


input_image_path = None
output_image_path = None
argv = sys.argv[1:]
if(len(argv) < 1):
    print("Too little parameters, the command should be like this:")
    print(
        "python CharTransfer.py <input image path> [output image path]")
    exit(-1)
elif(len(argv) > 2):
    print("Too much parameters, the command should be like this:")
    print(
        "python CharTransfer.py <input image path> [output image path]")
    exit(-1)
else:
    input_image_path = argv[0]
    if(len(argv) == 2):
        output_image_path = argv[1]

output_image = CharTransfer(input_image_path)

if(len(argv) == 1):
    output_image.show()
else:
    output_image.save(output_image_path)
    print("Save Successfully!")
    output_image.show()
