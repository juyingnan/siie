import os
import shutil


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


root_dir = [r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151136.985298\depth']

split_line = 30
img_width = 40
low_line = split_line - img_width / 2
high_line = split_line + img_width / 2
split_axis = 2  # 0-x, 1-y, 2-z

for img_root in root_dir:
    input_img_a_list = list()
    output_train_dir = os.path.join(img_root, 'train/')
    output_val_dir = os.path.join(img_root, 'val/')
    output_test_dir = os.path.join(img_root, 'test/')
    make_dir(output_train_dir)
    make_dir(output_val_dir)
    make_dir(output_test_dir)
    input_img_list = list()
    for (dirpath, dirnames, filenames) in os.walk(img_root):
        input_img_list += [file for file in filenames if file.endswith('.png')]
    for img_name in input_img_list:
        cor_x = int(img_name.split('_')[split_axis])
        current_file_path = os.path.join(img_root, img_name)
        if cor_x <= low_line:
            shutil.move(current_file_path, os.path.join(output_train_dir, img_name))
        elif cor_x >= high_line:
            shutil.move(current_file_path, os.path.join(output_test_dir, img_name))
        else:
            shutil.move(current_file_path, os.path.join(output_val_dir, img_name))
