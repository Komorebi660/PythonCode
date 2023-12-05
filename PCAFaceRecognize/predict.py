import pickle
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.decomposition import PCA


# reshape vector and save image to disk
def save_image(data, path):
    plt.figure(figsize=(64, 64), dpi=1)
    plt.imshow(data.reshape((64, 64)), cmap='gray')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


# load data from disk
def load_data():
    with open("./dataset/train.pt", "rb") as f:
        data = pickle.load(f)
        data = pd.DataFrame(data)
        train_data = np.array(data['vector'].tolist(), dtype=np.float32)
        train_label = data['label'].values
        print(train_data.shape, len(train_label))
    with open("./dataset/test.pt", "rb") as f:
        data = pickle.load(f)
        data = pd.DataFrame(data)
        test_data = np.array(data['vector'].tolist(), dtype=np.float32)
        test_label = data['label'].values
        print(test_data.shape, len(test_label))
    return train_data, train_label, test_data, test_label

# draw mean image for each class
def draw_class_mean(train_data, train_label):
    for label in np.unique(train_label):
        mean_image = np.mean(train_data[train_label == label], axis=0)
        save_image(mean_image, f"./figs/mean_{label}.jpg")

# transform mean value to 0
def zero_mean(train_data, test_data):
    mean_value = np.mean(train_data, axis=0)
    #print(mean_value)
    save_image(mean_value, "./figs/mean_image.jpg")
    train_data_zero_mean = train_data - mean_value
    test_data_zero_mean = test_data - mean_value
    return train_data_zero_mean, test_data_zero_mean, mean_value

# compare image before and after zero mean
def compare_zero_mean(train_data, train_data_zero_mean):
    for label in np.unique(train_label):
        before_zero_mean = train_data[train_label == label][-1] # choose last image
        after_zero_mean = train_data_zero_mean[train_label == label][-1]
        save_image(before_zero_mean, f"./figs/{label}_before_zero_mean.jpg")
        save_image(after_zero_mean, f"./figs/{label}_after_zero_mean.jpg")

# PCA transform
def pca_transform(train_data_zero_mean, test_data_zero_mean, n_components):
    pca = PCA(n_components=n_components, whiten=True, random_state=0)
    pca.fit(train_data_zero_mean)
    train_data = pca.transform(train_data_zero_mean)
    test_data = pca.transform(test_data_zero_mean)
    return pca, train_data, test_data


# draw eigenvalue curve
def draw_eigenvalue_curve(eigenvalues):
    eigenvalues_ratio = np.cumsum(eigenvalues) / np.sum(eigenvalues)
    plt.plot(np.arange(1, len(eigenvalues)+1), eigenvalues_ratio)
    plt.xlabel("#components")
    plt.ylabel("eigenvalue ratio")
    plt.ylim(0, 1)
    plt.grid()
    plt.tight_layout()
    plt.savefig("./figs/eigenvalues.jpg")

# draw original and reconstruct image
def draw_reconstruct(pca, mean_value, train_data, train_label):
    for label in np.unique(train_label):
        ori_data = train_data[train_label == label][-1] # choose last image
        save_image(ori_data, f"./figs/ori_{label}.jpg")
        ori_data_zero_mean = ori_data - mean_value
        reconstruct_data = pca.inverse_transform( \
                           pca.transform( \
                                ori_data_zero_mean.reshape(1, -1)
                            )) + mean_value
        save_image(reconstruct_data, 
                   f"./figs/reconstruct_{label}_{pca.n_components_}.jpg")

# draw each dimension after PCA
def draw_scatter(train_data, train_label, dim):
    plt.figure(figsize=(8, 8))
    idx = 0
    for label in np.unique(train_label):
        plt.scatter(np.zeros_like(train_data[train_label == label, dim-1]) + idx, \
                    train_data[train_label == label, dim-1], \
                    label=label)
        #mean = np.mean(train_data[train_label == label, dim-1])
        #plt.plot(np.linspace(0, 2, 100), mean * np.ones(100))
        idx+=1
    #plt.legend()
    plt.grid()
    plt.xticks([0,1,2], ['Alyssa_Milano', 'Barack_Obama', 'Daniel_Craig'])
    plt.ylabel(f"dimension value")
    plt.tight_layout()
    plt.savefig(f"./figs/scatter_{dim}.jpg")
    plt.close()


# predict on test set
def predict(train_data, train_label, test_data, test_label, pca, mean_value):
    # calculate mean vector for each class
    class_mean_vectors = {}
    for label in np.unique(train_label):
        class_mean_vectors[label] = np.mean(train_data[train_label == label], axis=0)
    # draw mean vector
    for label in class_mean_vectors:
        mean_image = pca.inverse_transform(class_mean_vectors[label]) + mean_value
        save_image(mean_image, f"./figs/reconstruct_mean_{label}.jpg")
    # predict
    wrong = 0
    print("========predict========")
    for i in range(test_data.shape[0]):
        test_vector = test_data[i]
        predict_label = -1
        min_distance = 1e9
        for label in np.unique(train_label):
            distance = np.linalg.norm(test_vector - class_mean_vectors[label])
            if distance < min_distance:
                min_distance = distance
                predict_label = label
        if min_distance > 15.0:   # if too far, predict as "no face"
            predict_label = "no face"
        if predict_label != test_label[i]:
            print(f"predict: {predict_label}, true: {test_label[i]}")
            wrong += 1
    print(f"wrong: {wrong}")



if __name__ == "__main__":
    train_data, train_label, test_data, test_label = load_data()
    #draw_class_mean(train_data, train_label)
    train_data_zero_mean, test_data_zero_mean, mean_value = zero_mean(train_data, test_data)
    #compare_zero_mean(train_data, train_data_zero_mean)
    pca, train_data_pca, test_data_pca = pca_transform(train_data_zero_mean, test_data_zero_mean, 100)
    eigenvalues = pca.singular_values_**2    # eigenvalues
    eigenvectors = pca.components_           # eigenvectors
    for i in [1, 2, 5, 10, 20, 50, 80, 100]:
        print(eigenvalues[i-1])
    print(eigenvectors.shape)

    draw_eigenvalue_curve(eigenvalues)
    # draw eigenfaces
    for i in [1, 2, 5, 10, 20, 50, 80, 100]:
        save_image(eigenvectors[i-1], f"./figs/eigenface_{i}.jpg")
    draw_reconstruct(pca, mean_value, train_data, train_label)
    #for i in [1, 10, 100]:
    #   draw_scatter(train_data_pca, train_label, i)

    predict(train_data_pca, train_label, test_data_pca, test_label, pca, mean_value)
    