import os

root_dir = r'C:\Users\bunny\Desktop\iu_model'
rendering_txt_list = list()
for (dirpath, dirnames, filenames) in os.walk(root_dir):
    rendering_txt_list += [os.path.join(dirpath, file) for file in filenames if file.endswith('.txt')]

step = len(rendering_txt_list) // 100
count = 0
for txt_file in rendering_txt_list:
    lines = open(txt_file).read().splitlines()
    for i in range(len(lines)):
        numbers = lines[i].split(' ')
        num_4 = float(numbers[3])
        new_num_4 = num_4 * 0.57
        numbers[3] = str(new_num_4)
        new_line = ' '.join(numbers)
        lines[i] = new_line
    # lines[0] = '270.0' + lines[0][5:]
    # lines[1] = '180.0' + lines[1][5:]
    # lines[2] = '90.0' + lines[2][4:]
    # lines[3] = '0.0' + lines[3][5:]
    open(txt_file, 'w').write('\n'.join(lines))
    count += 1
    if count % step == 0:
        print(count // step)
