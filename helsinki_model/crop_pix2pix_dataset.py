import os
import random
import numpy as np
from skimage import io, transform
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


root_dir = r'C:\Users\bunny\Desktop\train'
# root_dir = r'C:\Users\bunny\Desktop\Test'
functions = ['3ch', '4ch']
left_img_name = 'left.png'
right_img_name = 'right.png'
resized_shape = (256, 512)

original_dim_range = [1024, 1024]

startpoint_list = list()
crop_dim_list = list()
for function in functions:
    print(function)
    input_dir = os.path.join(root_dir, function)
    output_dir = os.path.join(input_dir, 'output')
    make_dir(output_dir)
    left_img = io.imread(os.path.join(input_dir, left_img_name))
    right_img = io.imread(os.path.join(input_dir, right_img_name))
    assert left_img.shape == right_img.shape

    image_count = 5000
    while len(startpoint_list) < image_count:
        crop_dim = random.randint(original_dim_range[0], original_dim_range[1])
        startpoint = [random.randint(0, left_img.shape[0] - crop_dim), random.randint(0, left_img.shape[1] - crop_dim)]
        startpoint_list.append(startpoint)
        crop_dim_list.append(crop_dim)
    for i in range(len(startpoint_list)):
        startpoint = startpoint_list[i]
        crop_dim = crop_dim_list[i]
        end_point = [point + crop_dim for point in startpoint]
        cropped_left_img = left_img[startpoint[0]:end_point[0], startpoint[1]:end_point[1]]
        cropped_right_img = right_img[startpoint[0]:end_point[0], startpoint[1]:end_point[1]]
        merge = np.concatenate((cropped_left_img, cropped_right_img), axis=1)
        resized = (255 * transform.resize(merge, resized_shape, anti_aliasing=True)).astype(np.uint8)
        loc = '_'.join([str(point) for point in startpoint + end_point])
        output_path = os.path.join(output_dir, loc + '.png')
        io.imsave(output_path, resized)
        image_count -= 1
        print('\rImage left: {}'.format(image_count), end='')
    print()
