import os
import numpy as np
from skimage import transform, io


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


file_root_dir = r'C:\Users\bunny\Desktop\forIndiana\test_depth_result\images'
output_dir = os.path.join(file_root_dir, 'output')
make_dir(output_dir)
max_crop_seg = 4
file_names = [file for file in os.listdir(file_root_dir) if file.endswith('outputs.png')]
img_max_seg_name = set(['_'.join(file_name.split('_')[:2]) for file_name in file_names])
# print(img_max_seg_name)
for img_seg in img_max_seg_name:
    img_id = img_seg.split('_')[0]
    crop_seg = int(img_seg.split('_')[1])
    result = None
    for i in range(crop_seg):
        row_blocks = list()
        for j in range(crop_seg):
            file_name = ('_'.join([img_seg, str(i), str(j)])) + '-outputs.png'
            file_path = os.path.join(file_root_dir, file_name)
            row_blocks.append(io.imread(file_path))
        row_merged = np.concatenate([row_blocks[index] for index in range(crop_seg)], axis=1)
        if result is None:
            result = row_merged
        else:
            result = np.concatenate((result, row_merged), axis=0)
    print(result.shape)
    io.imsave(os.path.join(output_dir, img_seg + '.png'), result)
