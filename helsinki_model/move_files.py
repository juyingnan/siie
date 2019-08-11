import os
import shutil

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


root_dir = r'C:\Users\bunny\Desktop\Data'
folder_name = 'combine'
output_path = os.path.join(root_dir, folder_name)
make_dir(output_path)

dirs = os.listdir(root_dir)
for dir in dirs:
    dir_path = os.path.join(root_dir, dir)
    # print(dir_path)
    file_names = [file for file in os.listdir(dir_path)]
    for file_name in file_names:
        file_path = os.path.join(dir_path, file_name)
        target_path = os.path.join(output_path, file_name)
        shutil.move(file_path, target_path)