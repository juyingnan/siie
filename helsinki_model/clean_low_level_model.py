import os

clean_types = ['.obj', '.mtl', 'jpg']
root_dir = r'C:\Users\bunny\Desktop\Data'
to_delete_list = list()
for type in clean_types:
    for (dirpath, dirnames, filenames) in os.walk(root_dir):
        to_delete_list += [os.path.join(dirpath, file) for file in filenames if
                           (file.endswith(type) and 'L21' not in file)]

step = len(to_delete_list) // 100
count = 0
for delete_file in to_delete_list:
    if os.path.exists(delete_file):
        os.remove(delete_file)
    count += 1
    if count % step == 0:
        print(count // step)
