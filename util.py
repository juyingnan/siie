count = 72
ROOT_DIR = r'C:\Users\bunny\Desktop\models_google_poly'
FOLDER_NAME = 'models_google_poly'

for i in range(count):
    index = i + 1
    print(
        r'"c:\Program Files\Blender Foundation\Blender\blender.exe" '
        r'--background --python ./render_blender.py -- '
        r'--output_folder {0}\{1}\rendering\ '
        r'{0}\{1}\model.obj'.format(ROOT_DIR, index))
print()

for i in range(count):
    index = i + 1
    print(r'meshlabserver  -i {0}\{1}\model.obj '
          r'-o {0}\{1}\model.xyz '
          r'-s c:\Users\bunny\Desktop\upsample.mlx'.format(ROOT_DIR, index))
print()

for i in range(count):
    index = i + 1
    # print(r'python 2_generate_normal.py {}/{}/'.format(FOLDER_NAME, index))
    print(r'python 3_camera_transform.py {}/{}/'.format(FOLDER_NAME, index))
print()

# for i in range(count):
#     index = i + 1
#     for j in range(24):
#         print(r'Data/{}/{}/rendering/{:02d}.dat'.format(FOLDER_NAME, index, j))
# print()

# for i in range(count):
#     index = i + 1
#     for j in range(24):
#         print(r'python demo.py --image Data/{}/{}/rendering/{:02d}.png'.format(FOLDER_NAME, index, j))
# print()

for i in range(count):
    index = i+ 1
    print(r'"C:\Program Files\CloudCompare\CloudCompare.exe" -SILENT -AUTO_SAVE OFF '
          r'-O {0}\{1}\model.obj '
          r'-SAMPLE_MESH POINTS 10000 '
          r'-C_EXPORT_FMT ASC '
          r'-SAVE_CLOUDS FILE {0}\{1}\model_normal.xyz'.format(ROOT_DIR, index))

print()
for i in range(count):
    index = i+ 1
    print(r'del /S /Q {}\{}\rendering\*'.format(ROOT_DIR, index))