import os
import numpy as np
from skimage import transform, io


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


resized_shape = (256, 512)

file_root_dir = r'C:\Users\bunny\Desktop\Data'

functions = ['depth', 'normal']
for function in functions:
    output_dir = os.path.join(file_root_dir, function)
    make_dir(output_dir)

for img_root in os.listdir(file_root_dir):

    if img_root in functions:
        continue
    root_postfix = img_root[-8:]

    input_img_a_list = list()
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(file_root_dir, img_root)):
        input_img_a_list += [os.path.join(dirpath, file) for file in filenames if
                             (file.endswith('.png') and len(file) < 7)]

    for function in functions:
        output_dir = os.path.join(file_root_dir, function)
        output_img_b_list = list()
        for input_img in input_img_a_list:
            output_img = input_img.replace('.png', '_{}.png0001.png'.format(function[0]))
            assert os.path.exists(output_img)
            output_img_b_list.append(output_img)

        assert len(input_img_a_list) == len(output_img_b_list)
        total_count = len(input_img_a_list)
        count = 0

        for input_img, output_img in zip(input_img_a_list, output_img_b_list):
            img_a = io.imread(input_img)[..., :3]
            img_b = io.imread(output_img)[..., :3]
            merge = np.concatenate((img_a, img_b), axis=1)
            # resized = transform.resize(merge, resized_shape, anti_aliasing=True)
            # dims = os.path.dirname(input_img).split('_')[-3:]
            # loc = '_'.join(dims)
            loc = os.path.dirname(input_img).split('_')[-1]
            file_name = os.path.basename(input_img)
            output_path = os.path.join(output_dir, root_postfix + '_' + loc + '_' + file_name)
            io.imsave(output_path, merge)
            count += 1
            print(count, '/', total_count)  # , '\r', end='')
