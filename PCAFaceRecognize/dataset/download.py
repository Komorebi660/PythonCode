import os
import requests
from PIL import Image
from io import BytesIO


if not os.path.exists('./images'):
    os.mkdir('./images')

name_num = {'Alyssa_Milano': 0, 'Barack_Obama': 0, 'Daniel_Craig': 0}

with open('dev_urls.txt', 'r') as f:
    _ = f.readline()
    _ = f.readline()
    for line in f.readlines():
        # split line by \t
        line = line.strip().split('\t')
        name = str(line[0]).replace(' ', '_')
        index = int(line[1])
        url = str(line[2])
        x0,y0,x1,y1 = line[3].split(',')
        x0,y0,x1,y1 = int(x0),int(y0),int(x1),int(y1)

        if name not in name_num.keys():
            continue
        if name_num[name] > 100:
            continue

        file_name = f'./images/{name}_{index}.jpg'
        if os.path.exists(file_name):
            continue
        print(f'Downloading {url}')
        try:
            r = requests.get(url, timeout=10)
            image_data = BytesIO(r.content)
            image = Image.open(image_data)
            cropped_image = image.crop((x0, y0, x1, y1))
            gray_image = cropped_image.convert('L')
            final_image = gray_image.resize((128, 128))
            final_image.save(file_name)
            name_num[name] += 1
        except:
            print(f'Failed {url}')
            continue
