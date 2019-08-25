import os
import random
import numpy as np
from skimage import io, transform
from PIL import Image

left_dir = r'C:\Users\bunny\Desktop\4ch2normal_result\images'
right_dir = r'C:\Users\bunny\Desktop\4ch2normal_result_3ch\images'
left_base = False

file_names = [file for file in os.listdir(left_dir) if file.endswith('-outputs.png')]
for file_name in file_names:
    left_path = os.path.join(left_dir, file_name)
    left_img = io.imread(left_path)[..., :3]
    right_path = os.path.join(right_dir, file_name).replace('-outputs.png', '_3ch-outputs.png')
    right_img = io.imread(right_path)[..., :3]

    assert left_img.shape == right_img.shape

    merge = np.concatenate((right_img, left_img), axis=1)
    if left_base:
        io.imsave(left_path, merge)
    else:
        io.imsave(right_path, merge)
