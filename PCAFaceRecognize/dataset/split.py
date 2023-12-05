import os
from PIL import Image
import numpy as np
import pickle
import pandas as pd


train_data = {"vector": [], "label": []}
test_data = {"vector": [], "label": []}
train_count = {"Alyssa_Milano": 0, "Barack_Obama": 0, "Daniel_Craig": 0}

for filename in os.listdir("./images/"):
    name = filename.split("_")[0] + "_" + filename.split("_")[1]
    file_path = os.path.join("./images/", filename)
    image = Image.open(file_path).convert("L")  # gray image
    image = image.resize((64, 64))
    image_array = np.array(image, dtype=np.uint8)
    vector = image_array.flatten()
    # 3*12=36 images for training, 12 images for testing
    if train_count[name] < 36:
        train_data["vector"].append(vector)
        train_data["label"].append(name)
        train_count[name] += 1
    else:
        test_data["vector"].append(vector)
        test_data["label"].append(name)

pickle.dump(train_data, open("train.pt", "wb"))
pickle.dump(test_data, open("test.pt", "wb"))

with open("train.pt", "rb") as f:
    train_data = pickle.load(f)
    train_data = pd.DataFrame(train_data)
    print(train_data.describe())
with open("test.pt", "rb") as f:
    test_data = pickle.load(f)
    test_data = pd.DataFrame(test_data)
    print(test_data.describe())
