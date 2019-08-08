import os
import numpy as np
from skimage import transform, io


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


resized_shape = (256, 512)

file_root_list = [r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151136.985298',
                  r'C:\Users\bunny\Desktop\iu_model\modelFriJun07150600.397829',
                  r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151356.571771',
                  # r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151814.953600',
                  r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151951.305606', ]

for img_root in file_root_list:
    root_postfix = img_root[-6:]

    input_img_a_list = list()
    for (dirpath, dirnames, filenames) in os.walk(img_root):
        input_img_a_list += [os.path.join(dirpath, file) for file in filenames if
                             (file.endswith('.png') and len(file) < 7)]

    for function in ['depth', 'normal']:
        output_dir = os.path.join(img_root, function)
        make_dir(output_dir)

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
            resized = transform.resize(merge, resized_shape, anti_aliasing=True)
            dims = os.path.dirname(input_img).split('_')[-3:]
            loc = '_'.join(dims)
            file_name = os.path.basename(input_img)
            output_path = os.path.join(output_dir, root_postfix + '_' + loc + '_' + file_name)
            io.imsave(output_path, resized)
            count += 1
            print(count, '/', total_count, '\r', end='')
