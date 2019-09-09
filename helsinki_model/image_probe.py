from skimage import io
import os
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# path = r'C:\Users\bunny\Desktop\Data_region\674497a4\Tile_+029_+025_L21_0000000_MERGED_MERGED\00_d.png0001.png'
#
# img = io.imread(path)
#
# print(img.shape)
# print(np.amax(img))
# print(np.amin(img))

file_root_dir = r'C:\Users\bunny\Desktop\test'

functions = ['depth', 'normal']
min_value = 255
max_value = 0
input_img_a_list = list()
for (dirpath, dirnames, filenames) in os.walk(file_root_dir):
    input_img_a_list += [os.path.join(dirpath, file) for file in filenames if file.endswith('_d.png0001.png')]

# for function in functions[:1]:
#     output_img_b_list = list()
#     for input_img in input_img_a_list:
#         output_img = input_img.replace('.png', '_{}.png0001.png'.format(function[0]))
#         if os.path.exists(output_img):
#             output_img_b_list.append(output_img)
#     # print('files: {}'.format(len(output_img_b_list)))

for output_img in input_img_a_list:
    img_b = io.imread(output_img)[..., :3]
    color_set = set(img_b.flat)
    print(color_set)
    _max = np.amax(img_b)
    _min = np.amin(img_b)
    if _min < min_value:
        min_value = _min
    if _max > max_value:
        max_value = _max
    if _min == 0:
        print(output_img, 0)
    if _max == 255:
        print(output_img, 255)
print('final max: {}'.format(max_value))
print('final min: {}'.format(min_value))
