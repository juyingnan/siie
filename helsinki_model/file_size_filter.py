import os
import numpy as np
from skimage import transform, io


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


file_root_dir = r'C:\Users\bunny\Desktop\helsinki\lod2_4ch_train_result\images\output'
output_dir = os.path.join(file_root_dir, '3ch')
make_dir(output_dir)
_4ch_names = [file for file in os.listdir(file_root_dir) if file.endswith('.png')]
# print(img_max_seg_name)
# for _4ch_name in _4ch_names:
#     _3ch_name = _4ch_name
#     _4ch_file_path = os.path.join(file_root_dir, _4ch_name)
#     img = io.imread(_4ch_file_path)  # [..., :1]
#     alpha_layer = img[..., 3]
#     final_img = np.multiply(img[..., :3], alpha_layer.reshape(alpha_layer.shape[0], alpha_layer.shape[1], 1) / 255)
#     print(final_img.shape)
#     io.imsave(os.path.join(output_dir, _4ch_name), final_img)

_3ch_names = [file for file in os.listdir(output_dir) if file.endswith('.png')]
for _4ch_name in _4ch_names:
    if _4ch_name not in _3ch_names:
        _4ch_file_path = os.path.join(file_root_dir, _4ch_name)
        os.remove(_4ch_file_path)
