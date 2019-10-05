import os
import numpy as np
from skimage import transform, io


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


file_root_dir = r'C:\Users\bunny\Desktop\forIndiana\RGB'
max_crop_seg = 4

output_dir = os.path.join(file_root_dir, 'test')
make_dir(output_dir)
file_names = [file for file in os.listdir(file_root_dir) if file.endswith('.png')]
for file_name in file_names:
    file_path = os.path.join(file_root_dir, file_name)
    image = io.imread(file_path)
    for crop_seg in range(max_crop_seg):
        if crop_seg != 2:
            rows = np.split(image, crop_seg + 1, axis=0)
            for i in range(len(rows)):
                row = rows[i]
                blocks = np.split(row, crop_seg + 1, axis=1)
                for j in range(len(blocks)):
                    block = blocks[j]
                    block = transform.resize(block, (256, 256), anti_aliasing=True)
                    block = np.concatenate((block, 1 - np.zeros(block.shape)), axis=1)
                    output_file_name = ('_'.join([file_name[:-4], str(crop_seg + 1), str(i), str(j)])) + '.png'
                    io.imsave(os.path.join(output_dir, output_file_name), block)

#
# import os
# import numpy as np
# from skimage import transform, io
#
#
# def make_dir(path):
#     if not os.path.exists(path):
#         os.makedirs(path)
#
#
# file_root_dir = r'C:\Users\bunny\Desktop\helsinki_test'
# horizontal_crop_seg = 20
# vertical_crop_seg = 14
#
# output_dir = os.path.join(file_root_dir, 'test')
# make_dir(output_dir)
# file_names = [file for file in os.listdir(file_root_dir) if file.endswith('.png')]
# for file_name in file_names:
#     file_path = os.path.join(file_root_dir, file_name)
#     image = io.imread(file_path)
#     rows = np.split(image, horizontal_crop_seg, axis=0)
#     for i in range(len(rows)):
#         row = rows[i]
#         blocks = np.split(row, vertical_crop_seg, axis=1)
#         for j in range(len(blocks)):
#             block = blocks[j]
#             block = transform.resize(block, (256, 256), anti_aliasing=True)
#             block = np.concatenate((block, 1 - np.zeros(block.shape)), axis=1)
#             output_file_name = ('_'.join([file_name[:-4], str(horizontal_crop_seg + 1), str(i), str(j)])) + '.png'
#             io.imsave(os.path.join(output_dir, output_file_name), block)
