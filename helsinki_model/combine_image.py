import os
import numpy as np
from skimage import transform, io

resized_shape = (256, 512)

file_root_dir = r'C:\Users\bunny\Desktop\region_image\normal'
output_file_names = ['left.png', 'right.png']
layout_matrix = [
    ['676497b3', '676497d1', '676497d3', '676498b1', '676498b3', '676498d1', '676498d3'],
    ['676497a4', '676497c2', '676497c4', '676498a2', '676498a4', '676498c2', '676498c4'],
    ['676497a3', '676497c1', '676497c3', '676498a1', '676498a3', '676498c1', '676498c3'],
    ['675497b4', '675497d2', '675497d4', '675498b2', '675498b4', '675498d2', '675498d4'],
    ['675497b3', '675497d1', '675497d3', '675498b1', '675498b3', '675498d1', '675498d3'],
    ['675497a4', '675497c2', '675497c4', '675498a2', '675498a4', '675498c2', '675498c4'],
    ['675497a3', '675497c1', '675497c3', '675498a1', '675498a3', '675498c1', '675498c3'],
    ['674497b4', '674497d2', '674497d4', '674498b2', '674498b4', '674498d2', '674498d4'],
    ['674497b3', '674497d1', '674497d3', '674498b1', '674498b3', '674498d1', '674498d3'],
    ['674497a4', '674497c2', '674497c4', '674498a2', '674498a4', '674498c2', '674498c4'],
    ['674497a3', '674497c1', '674497c3', '674498a1', '674498a3', '674498c1', '674498c3']
]

input_img_list = list()
for (dirpath, dirnames, filenames) in os.walk(os.path.join(file_root_dir, file_root_dir)):
    input_img_list += [file for file in filenames if (file.endswith('.png') and file.startswith('6'))]

position_list = list()
ori_img_list = list()
fea_img_list = list()
for img_name in input_img_list:
    position = img_name.split('_')[0]
    position_list.append(position)
    image = io.imread(os.path.join(file_root_dir, img_name))
    ori_img, feature_img = np.split(image, 2, axis=1)
    assert ori_img.shape == feature_img.shape
    # print(ori_img.shape)
    ori_img_list.append(ori_img)
    fea_img_list.append(feature_img)

for source, output_name in zip([ori_img_list, fea_img_list], output_file_names):
    result = None
    for line in layout_matrix:
        index_list = [position_list.index(pos) for pos in line]
        row_merged = np.concatenate([source[index] for index in index_list], axis=1)
        if result is None:
            result = row_merged
        else:
            result = np.concatenate((result, row_merged), axis=0)
    print(result.shape)
    # merge = np.concatenate((img_a, img_b), axis=1)

    io.imsave(os.path.join(file_root_dir, output_name), result)
