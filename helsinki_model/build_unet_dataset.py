import os
import random
import numpy as np
from skimage import io, transform
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


root_dir = r'C:\Users\bunny\Desktop\data'
source_img_path = r"C:\Users\bunny\Desktop\merge.tif"
source_img = io.imread(source_img_path)
source_mask_path = r"C:\Users\bunny\Desktop\merge_db_mask_.tif"
source_mask = io.imread(source_mask_path)
split_func = ['train', 'test']
split_ratio = 0.8
img_count = 5000
crop_size = 512
functions = ['image', 'mask']

sp_line = int(source_img.shape[0] * split_ratio)
sp_info = {
    'train': {'img': {'image': source_img[:sp_line],
                      'mask': source_mask[:sp_line], },
              'count': int(img_count * split_ratio), },
    'test': {'img': {'image': source_img[sp_line:],
                     'mask': source_mask[sp_line:], },
             'count': int(img_count * (1 - split_ratio))},
}

for sp in sp_info:
    print(sp)
    for function in sp_info[sp]['img']:
        output_dir = os.path.join(root_dir, sp, function)
        make_dir(output_dir)
    image_count = 0

    x_max, y_max = sp_info[sp]['img']['image'].shape[:2]
    while image_count < sp_info[sp]['count']:
        startpoint = [random.randint(0, x_max - crop_size),
                      random.randint(0, y_max - crop_size)]
        end_point = [point + crop_size for point in startpoint]
        for function in sp_info[sp]['img']:
            output_img = sp_info[sp]['img'][function][startpoint[0]: end_point[0], startpoint[1]: end_point[1]]
            loc = '_'.join([str(point) for point in startpoint + end_point])
            output_path = os.path.join(root_dir, sp, function, loc + '.png')
            io.imsave(output_path, output_img, check_contrast=False)
        image_count += 1
        print('\rImage done: {}'.format(image_count), end='')
    print()
