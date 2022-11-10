from skimage import io
import numpy as np
from pandas import DataFrame
from matplotlib import colors
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from sklearn.cluster import KMeans
from collections import Counter

def get_reddest_pixel(pixels, w):
    reddest_index = pixels['Red'].idxmax()
    x = reddest_index % w
    y = reddest_index // w
    return (x, y)

def get_greenest_pixel(pixels, w):
    greenest_index = pixels['Green'].idxmax()
    x = greenest_index % w
    y = greenest_index // w
    return (x, y)

def get_bluest_pixel(pixels, w):
    bluest_index = pixels['Blue'].idxmax()
    x = bluest_index % w
    y = bluest_index // w
    return (x, y)

def print_most_vibrant_pixels(pixels, w):
    reddest_pixel = get_reddest_pixel(pixels, w)
    print('Reddest pixel:' + str(reddest_pixel))
    greenest_pixel = get_greenest_pixel(pixels, w)
    print('Greenest pixel:' + str(greenest_pixel))
    bluest_pixel = get_bluest_pixel(pixels, w)
    print('Bluest pixel:' + str(bluest_pixel))
    
def get_info_from_image(image_url):
    image = io.imread(image_url)
    image_shape = image.shape
    image_size = image.size
    # if image has forth dimension alpha
    image_without_alpha = image[:,:,:3]
    # normalize values - transform to [0, 1]
    image_np = np.array(image_without_alpha, dtype=np.float64) / 255
    # get the current shape of an image
    w, h, d = original_shape = tuple(image_np.shape)
    # reshape to 2D
    image_array = np.reshape(image_np, (w * h, d))
    pixels = DataFrame(image_array, columns=['Red', 'Green', 'Blue'])
    
    print_most_vibrant_pixels(pixels, w)
    
    pixels['colour'] = [colors.to_hex(p) for p in image_array] # encoded colour string
    
    pixels_sample = pixels.sample(frac=0.1)
    
    return pixels, pixels_sample, original_shape, image

def plot_colours(df, c1, c2, c3):
    '''
    Given a DataFrame and three column names,
    plot the pairs against each other
    '''
    fig, ax = plt.subplots(1, 3)
    fig.set_size_inches(18, 6)
    df.plot.scatter(c1, c2, c=df['colour'], alpha=0.3, ax=ax[0])
    df.plot.scatter(c1, c3, c=df['colour'], alpha=0.3, ax=ax[1])
    df.plot.scatter(c2, c3, c=df['colour'], alpha=0.3, ax=ax[2])
    
def plot_colours_3D(df, c1, c2, c3):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel(c1)
    ax.set_ylabel(c2)
    ax.set_zlabel(c3)
    ax.scatter(df[c1], df[c2], df[c3], c=df["colour"])
    
def get_clusters_from_pixels(pixels, pixels_sample):
    kmeans = KMeans(n_clusters=10).fit(pixels_sample[["Red", "Green", "Blue"]])
    labels = kmeans.predict(pixels[["Red", "Green", "Blue"]])
    clusters = kmeans.cluster_centers_
    return clusters, labels

def plot_labels(labels, clusters):
    labels_count = Counter(labels)
    sorted_labels = dict(sorted(labels_count.items(), key=lambda i: i[0]))
    plt.bar(sorted_labels.keys(), sorted_labels.values(), color=clusters, edgecolor='black')
    
def plot_original_and_reduced_image(original, reduced):
    f, axarr = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(18, 9))
    axarr[0].imshow(original)
    axarr[0].set_title("Original")
    axarr[1].imshow(reduced)
    axarr[1].set_title("RGB clustered")
    
if __name__ == '__main__':
    main()