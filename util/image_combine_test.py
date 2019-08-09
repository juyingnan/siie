import os
import numpy as np
from skimage import io, segmentation, color
from skimage.future import graph

image_normal_folder = r'C:\Users\bunny\Desktop\iu_normal_result'
image_depth_folder = r'C:\Users\bunny\Desktop\iu_normal_result'
image_combine_folder = r'C:\Users\bunny\Desktop\iu_combine_result'

img_path_list = list()
for (dirpath, dirnames, filenames) in os.walk(image_depth_folder):
    img_path_list += [os.path.join(dirpath, file) for file in filenames if
                      file.endswith('outputs.png') or file.endswith('targets.png')]

for img_path in img_path_list:
    base_img = io.imread(img_path)
    normal_img = io.imread(img_path.replace(image_depth_folder, image_normal_folder))

    # labels1 = segmentation.slic(img, compactness=30, n_segments=400)
    #
    # g = graph.rag_mean_color(img, labels1, mode='similarity')
    # labels2 = graph.cut_normalized(labels1, g)
    # out2 = color.label2rgb(labels2, img, kind='avg')

    depth_layer = 255 - base_img[..., 0]
    base_img[..., :3] = normal_img[..., :3]
    base_img = np.dstack((base_img, depth_layer))
    io.imsave(img_path.replace(image_depth_folder, image_combine_folder), base_img)
