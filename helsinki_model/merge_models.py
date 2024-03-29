import os
import clean_low_level_model as clean

root_dir = r'X:\675499'
merge_level = 'L21'
file = open('command/merge_test.bat', 'w')

clean.clean_lower_levels(root_dir)
dirs = os.listdir(root_dir)

for dir in dirs:
    dir_path = os.path.join(root_dir, dir)
    if not os.path.isdir(dir_path):
        continue
    # print(dir_path)
    file_names = [file for file in os.listdir(dir_path) if file.endswith('obj')]
    # assert len(file_names) >= 1
    if len(file_names) <= 1:
        continue
    default_line = r'START /W "Merging" "C:\Program Files\CloudCompare\CloudCompare.exe" ' \
                   r'-SILENT -NO_TIMESTAMP -M_EXPORT_FMT OBJ '
    line = '{}'.format(default_line)
    parameter_count = 0
    for file_name in file_names:
        file_path = os.path.join(dir_path, file_name)
        level = file_name.split('_')[3]
        assert level == merge_level
        line += r'-O {} '.format(file_path)
        parameter_count += 1
        if len(line) >= 900:
            line += '-MERGE_MESHES'
            parameter_count = 0
            print(line)
            file.write(line + '\n')
            line = '{}'.format(default_line)
    if parameter_count > 1:
        line += '-MERGE_MESHES'
        print(line)
        file.write(line + '\n')
    if parameter_count == 1:
        file_names.pop()

    for file_name in file_names:
        file_path = os.path.join(dir_path, file_name)
        file.write('del {}'.format(file_path) + '\n')
        file.write('del {}'.format(file_path.replace('.obj', '.mtl')) + '\n')
file.close()
