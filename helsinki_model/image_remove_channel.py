import os
from skimage import io

file_root_dir = r'C:\Users\bunny\Desktop\4ch2normal\val_3ch'
file_names = [file for file in os.listdir(file_root_dir) if file.endswith('.png')]
for file_name in file_names:
    file_path = os.path.join(file_root_dir, file_name)
    img = io.imread(file_path)[..., :3]
    io.imsave(file_path.replace('.png', '_3ch.png'), img)
