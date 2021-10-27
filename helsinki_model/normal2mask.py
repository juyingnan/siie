import os
import random
import numpy as np
from skimage import io, transform
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

image_path = r"C:\Users\bunny\Desktop\model_n0001.tif"
img = io.imread(image_path)

color_dict = {
    'r+': {
        "direction": "EAST",
        "color": (127 + 64, 0, 0),
        "mask": 1,
    },
    'r-': {
        "direction": "WEST",
        "color": (127 - 64, 0, 0),
        "mask": 2
    },
    'g+': {
        "direction": "EAST",
        "color": (0, 127 + 64, 0),
        "mask": 3
    },
    'g-': {
        "direction": "EAST",
        "color": (0, 127 - 64, 0),
        "mask": 4
    },
    'r+g+': {
        "direction": "EAST",
        "color": (127 + 64, 127 + 64, 0),
        "mask": 5
    },
    'r-g+': {
        "direction": "EAST",
        "color": (127 - 64, 127 + 64, 0),
        "mask": 6
    },
    'r+g-': {
        "direction": "EAST",
        "color": (127 + 64, 127 - 64, 0),
        "mask": 7
    },
    'r-g-': {
        "direction": "EAST",
        "color": (127 - 64, 127 - 64, 0),
        "mask": 8
    },
    'flat': {
        "direction": "EAST",
        "color": (127, 127, 0),
        "mask": 9
    },
    'ground': {
        "direction": "EAST",
        "color": (0, 0, 0),
        "mask": 0
    },

}

start = 0
end = 999999

ground = 188
threshold = 7
img_mask_rgb = img[start:end, start:end, :3]
img_mask = np.zeros((img_mask_rgb.shape[0], img_mask_rgb.shape[1]), dtype=np.uint8)
for i in range(len(img_mask_rgb)):
    for j in range(len(img_mask_rgb[i])):
        code = ""
        x, y, z = img_mask_rgb[i][j]
        x, y, z = x - ground, y - ground, z - ground
        if z == 0:
            code = 'ground'
        elif -threshold <= x <= threshold and -threshold <= y <= threshold:
            code = 'flat'
        else:
            if x < -threshold:
                code += 'r-'
            elif x > threshold:
                code += 'r+'
            if y < -threshold:
                code += 'g-'
            elif y > threshold:
                code += 'g+'
        img_mask_rgb[i][j] = color_dict[code]["color"]
        img_mask[i][j] = color_dict[code]["mask"]
    print(f"\r{i + 1} done", end='')

file_type = '.' + image_path.split('.')[-1]
rgb_mask_path = image_path.replace(file_type, '_rgbmask_' + file_type)
mask_path = image_path.replace(file_type, '_mask_' + file_type)
io.imsave(rgb_mask_path, img_mask_rgb)
io.imsave(mask_path, img_mask)
