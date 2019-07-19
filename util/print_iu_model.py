import os

# step 0: use Blender to rotate and transfer the basic models
# no split
# rotation -> 0
# move to x/y 0, z proper

# C:\Users\bunny\Desktop\iu_model\modelFriJun07150600.397829\scene_mesh_textured_rotated.obj
# C:\Users\bunny\Desktop\iu_model\modelFriJun07151136.985298\scene_mesh_textured_rotated.obj
# C:\Users\bunny\Desktop\iu_model\modelFriJun07151356.571771\scene_mesh_textured_rotated.obj
# C:\Users\bunny\Desktop\iu_model\modelFriJun07151814.953600\scene_mesh_textured_rotated.obj
# C:\Users\bunny\Desktop\iu_model\modelFriJun07151951.305606\scene_mesh_textured_rotated.obj

# step 1:
# cross section
# Sample: "C:\Program Files\CloudCompare\CloudCompare.exe" -SILENT -AUTO_SAVE OFF
# -NO_TIMESTAMP -O C:\Users\bunny\Desktop\iu_model\modelFriJun07150600.397829\scene_mesh_textured_rotated.obj
# -M_EXPORT_FMT OBJ -CROSS_SECTION C:\Users\bunny\PycharmProjects\siie\iu_model\xml\cross_section_params_10_5.xml

# generate xml / lan le, copy
# xml path
# iu_model/xml/cross_section_params_30_10.xml
# iu_model/xml/cross_section_params_40_10.xml
# iu_model/xml/cross_section_params_50_20.xml
# iu_model/xml/cross_section_params_60_20.xml
# iu_model/xml/cross_section_params_70_20.xml

# generate command
obj_file_root_list = [r'C:\Users\bunny\Desktop\iu_model\modelFriJun07150600.397829',
                      r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151136.985298',
                      r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151356.571771',
                      r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151814.953600',
                      r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151951.305606', ]
obj_file_name = 'scene_mesh_textured_rotated.obj'
xml_file_list = list()

xml_root_dir = r"C:\Users\bunny\PycharmProjects\siie\iu_model\xml"
for file in os.listdir(xml_root_dir):
    if file.endswith(".xml"):
        xml_file_list.append(os.path.join(xml_root_dir, file))

file = open('../iu_model/command/step_1.txt', 'w')

for obj_root in obj_file_root_list:
    obj_file = os.path.join(obj_root, obj_file_name)
    line = r'"C:\Users\bunny\Desktop\CloudCompareStereo_v2.10.2_bin_x64\CloudCompare.exe" -AUTO_SAVE OFF ' \
           r'-NO_TIMESTAMP ' \
           r'-O {0} ' \
           r'-M_EXPORT_FMT OBJ'.format(obj_file)
    for xml_file in xml_file_list:
        line = line + r' -CROSS_SECTION {0}'.format(xml_file)
    print(line)
    file.write(line + '\n')
    print()
    file.write('\n')
print()
file.close()

# step 2:
# move obj to center
file = open('../iu_model/command/step_2.txt', 'w')

output_obj_list = list()
for obj_root in obj_file_root_list:
    output_dir = os.path.join(obj_root, 'output')
    for (dirpath, dirnames, filenames) in os.walk(output_dir):
        output_obj_list += [os.path.join(dirpath, file) for file in filenames if file.endswith('.obj')]
# print(output_obj_list)

for output_obj_file in output_obj_list:
    line = r'"c:\Program Files\Blender Foundation\Blender\blender.exe" ' \
           r'--background --python util/blender_operation.py -- ' \
           r'{0}'.format(output_obj_file)
    print(line)
    file.write(line + '\n')
print()
file.close()

# step 3
# generate thumb image
file = open('../iu_model/command/step_3.txt', 'w')

for output_obj_file in output_obj_list:
    filename, file_extension = os.path.splitext(os.path.basename(output_obj_file))
    line = r'"c:\Program Files\Blender Foundation\Blender\blender.exe" ' \
           r'--background --python iu_model/render_blender_iu.py -- ' \
           r'--output_folder {0} ' \
           r'{1}'.format(os.path.join(os.path.dirname(output_obj_file), filename), output_obj_file)
    print(line)
    file.write(line + '\n')
print()
file.close()
