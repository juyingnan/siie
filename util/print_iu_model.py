import os

STEP_1 = True  # CROSS SECTION
STEP_2 = True  # 2 + 3: move to the center and generate thumb images
STEP_3 = True  # empty
STEP_4 = True  # generate point cloud
STEP_5 = True  # use 3_camera_transform.py to generate point cloud (pickle -> dat) for each image
STEP_6 = True  # generate train and test list
STEP_7 = True  # check if numbers of folder and point cloud are same

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
# Sample: "C:\Users\bunny\Desktop\CloudCompareStereo_v2.10.2_bin_x64\CloudCompare.exe" -SILENT -AUTO_SAVE OFF
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
obj_file_root_list = [r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151136.985298',
                      r'C:\Users\bunny\Desktop\iu_model\modelFriJun07150600.397829',
                      r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151356.571771',
                      # r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151814.953600',
                      r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151951.305606', ]
obj_file_name = 'scene_mesh_textured_rotated.obj'

# generate xml
# SAMPLE
# <?xml version="1.0" encoding="UTF-8"?>
# <CloudCompare>
#   <BoxThickness x="30" y="60" z="30"/>
# 	<BoxCenter x="0" y="0" z="0"/>
#   <RepeatDim>0</RepeatDim>
#   <RepeatDim>2</RepeatDim>
# 	<RepeatGap>-20</RepeatGap>
# 	<OutputFilePath>C:\Users\bunny\Desktop\output\30</OutputFilePath> #
# </CloudCompare>

if STEP_1:
    file = open('../iu_model/command/step_1.bat', 'w')

    default_height = 60
    repeat_dim_list = [0, 2]
    for obj_root in obj_file_root_list:
        xml_file_list = list()
        for dimension, gap in zip([40], [5]):
            xml_file_name = 'cross_section_params_{:02d}_{:02d}.xml'.format(dimension, gap)
            xml_path = os.path.join(obj_root, xml_file_name)
            xml_file = open(xml_path, 'w')
            xml_file.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n')
            xml_file.write('<CloudCompare>' + '\n')
            xml_file.write('\t<BoxThickness x="{0}" y="{1}" z="{0}"/>'.format(dimension, default_height) + '\n')
            xml_file.write('\t<BoxCenter x="0" y="0" z="0"/>' + '\n')
            for repeat_dim in repeat_dim_list:
                xml_file.write('\t<RepeatDim>{}</RepeatDim>'.format(repeat_dim) + '\n')
            xml_file.write('\t<RepeatGap>{}</RepeatGap>'.format(gap - dimension) + '\n')
            output_path = os.path.join(obj_root, 'output/{}'.format(dimension))
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            xml_file.write('\t<OutputFilePath>{}</OutputFilePath>'.format(output_path) + '\n')
            xml_file.write('<CloudCompare>' + '\n')
            xml_file.close()
            xml_file_list.append(xml_path)

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

# step 2 + 3
# move obj to center and generate thumb image
# SAMPLE: "c:\Program Files\Blender Foundation\Blender\blender.exe"
# --background --python iu_model/render_blender_iu.py --
# --output_folder C:\Users\bunny\Desktop\iu_model\modelFriJun07150600.397829\output\50\
# scene_mesh_textured_rotated\scene_mesh_textured_rotated_75_0_-75 --move_and_save True
# C:\Users\bunny\Desktop\iu_model\modelFriJun07150600.397829\output\50\scene_mesh_textured_rotated\scene_mesh_textured_rotated_75_0_-75.obj
output_obj_list = list()
for obj_root in obj_file_root_list:
    output_dir = os.path.join(obj_root, 'output')
    for (dirpath, dirnames, filenames) in os.walk(output_dir):
        output_obj_list += [os.path.join(dirpath, file) for file in filenames if file.endswith('.obj')]

if STEP_2:
    file = open('../iu_model/command/step_2.bat', 'w')

    for output_obj_file in output_obj_list:
        filename, file_extension = os.path.splitext(os.path.basename(output_obj_file))
        line = r'"c:\Program Files\Blender Foundation\Blender\blender.exe" ' \
               r'--background --python iu_model/render_blender_iu.py -- ' \
               r'--move_and_save True ' \
               r'--output_folder {0} ' \
               r'{1}'.format(os.path.join(os.path.dirname(output_obj_file), filename), output_obj_file)
        print(line)
        file.write(line + '\n')
    print()
    file.close()

# step 4:
# generate point cloud
# SAMPLE: "C:\Users\bunny\Desktop\CloudCompareStereo_v2.10.2_bin_x64\CloudCompare.exe" -SILENT -AUTO_SAVE OFF
# -O C:\Users\bunny\Desktop\models_google_poly\1\model.obj
# -SAMPLE_MESH POINTS 2000 -C_EXPORT_FMT ASC
# -SAVE_CLOUDS FILE C:\Users\bunny\Desktop\models_google_poly\1\model_normal.xyz
if STEP_4:
    file = open('../iu_model/command/step_4.bat', 'w')
    points = 20000

    for output_obj_file in output_obj_list:
        line = r'START /W C:\Users\bunny\Desktop\CloudCompareStereo_v2.10.2_bin_x64\CloudCompare.exe ' \
               r'-SILENT -AUTO_SAVE OFF ' \
               r'-O {0} ' \
               r'-SAMPLE_MESH POINTS {1} -C_EXPORT_FMT ASC ' \
               r'-SAVE_CLOUDS FILE {2}'.format(output_obj_file, points, output_obj_file.replace('obj', 'xyz'))
        print(line)
        file.write(line + '\n')
    print()
    file.close()

# step 5
# use 3_camera_transform.py to generate point cloud (pickle -> dat) for each image
if STEP_5:
    file = open('../iu_model/command/step_5.sh', 'w')
    file.write('#!/bin/bash\n')
    output_xyz_list = list()
    for obj_root in obj_file_root_list:
        output_dir = os.path.join(obj_root, 'output')
        for (dirpath, dirnames, filenames) in os.walk(output_dir):
            output_xyz_list += [os.path.join(dirpath, file) for file in filenames if file.endswith('.xyz')]

    for output_xyz_file in output_xyz_list:
        line = r'python 3_camera_transform.py {} {}'.format(
            output_xyz_file[output_xyz_file.find('iu_model'):].replace('\\', '/'), '/rendering_metadata.txt')
        print(line)
        file.write(line + '\n')
    print()
    file.close()

# step 6
# generate train and test list
if STEP_6:
    output_dat_list = list()
    for obj_root in obj_file_root_list[1:]:
        output_dir = os.path.join(obj_root, 'output')
        for (dirpath, dirnames, filenames) in os.walk(output_dir):
            output_dat_list += [os.path.join(dirpath, file.replace('.png', '.dat')) for file in filenames if
                                file.endswith('.png')]

    file = open('../iu_model/command/train_list_iu.txt', 'w')
    for output_dat_file in output_dat_list:
        line = r'{}'.format('Data/' + output_dat_file[output_dat_file.find('iu_model'):].replace('\\', '/'))
        print(line)
        file.write(line + '\n')
    print()
    file.close()

    output_dat_list = list()
    for obj_root in obj_file_root_list[:1]:
        output_dir = os.path.join(obj_root, 'output')
        for (dirpath, dirnames, filenames) in os.walk(output_dir):
            output_dat_list += [os.path.join(dirpath, file.replace('.png', '.dat')) for file in filenames if
                                file.endswith('.png')]

    file = open('../iu_model/command/test_list_iu.txt', 'w')
    for output_dat_file in output_dat_list:
        line = r'{}'.format('Data/' + output_dat_file[output_dat_file.find('iu_model'):].replace('\\', '/'))
        print(line)
        file.write(line + '\n')
    print()
    file.close()

# step 7
# check if numbers of folder and point cloud are same
if STEP_7:
    for obj_root in obj_file_root_list:
        output_dir = os.path.join(obj_root, 'output')
        for (dirpath, dirnames, filenames) in os.walk(output_dir):
            if len(filenames) > 10 and len(filenames) != len(dirnames):
                print(dirpath)
                for dirname in dirnames:
                    if (dirname + '.xyz') not in filenames:
                        print(dirname)
