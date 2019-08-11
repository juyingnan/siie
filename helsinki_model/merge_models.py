import os

root_dir = r'C:\Users\bunny\Desktop\Data'
batch_size = 10
file = open('command/step_5.bat', 'w')

dirs = os.listdir(root_dir)

for dir in dirs:
    dir_path = os.path.join(root_dir, dir)
    # print(dir_path)
    file_names = [file for file in os.listdir(dir_path) if file.endswith('obj')]
    assert len(file_names) >= 1
    if len(file_names) <= 1:
        continue
    default_line = r'START /W C:\Users\bunny\Desktop\CloudCompareStereo_v2.10.2_bin_x64\CloudCompare.exe ' \
                   r'-SILENT -NO_TIMESTAMP -M_EXPORT_FMT OBJ '
    line = '{}'.format(default_line)
    for file_name in file_names:
        file_path = os.path.join(dir_path, file_name)
        level = file_name.split('_')[3]
        assert level == 'L21'
        line += r'-O {} '.format(file_path)
        if len(line) >= 900:
            line += '-MERGE_MESHES'
            print(line)
            file.write(line + '\n')
            line = '{}'.format(default_line)
    if not line.endswith('FMT OBJ '):
        line += '-MERGE_MESHES'
        print(line)
        file.write(line + '\n')

    for file_name in file_names:
        file_path = os.path.join(dir_path, file_name)
        file.write('del {}'.format(file_path) + '\n')
        file.write('del {}'.format(file_path.replace('.obj', '.mtl')) + '\n')
file.close()
