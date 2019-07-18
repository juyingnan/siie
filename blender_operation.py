# A simple script that uses blender to render views of a single object by rotation the camera around it.
# Also produces depth map at the same time.
#
# Example:
# blender --background --python mytest.py -- --views 10 /path/to/my.obj
#

import argparse
import sys
import os
import bpy
from math import radians
from mathutils import Vector
import math

parser = argparse.ArgumentParser(description='Renders given obj file by rotation a camera around it.')
parser.add_argument('--views', type=int, default=4,
                    help='number of views to be rendered')
parser.add_argument('obj', type=str,
                    help='Path to the obj file to be rendered.')
parser.add_argument('--output_folder', type=str, default='/tmp',
                    help='The path the output will be dumped to.')
parser.add_argument('--scale', type=float, default=1,
                    help='Scaling factor applied to model. Depends on size of mesh.')
parser.add_argument('--remove_doubles', type=bool, default=True,
                    help='Remove double vertices to improve mesh quality.')
parser.add_argument('--edge_split', type=bool, default=True,
                    help='Adds edge split filter.')
parser.add_argument('--depth_scale', type=float, default=1.4,
                    help='Scaling that is applied to depth. Depends on size of mesh. '
                         'Try out various values until you get a good result. '
                         'Ignored if format is OPEN_EXR.')
parser.add_argument('--color_depth', type=str, default='8',
                    help='Number of bit per channel used for output. Either 8 or 16.')
parser.add_argument('--format', type=str, default='PNG',
                    help='Format of files generated. Either PNG or OPEN_EXR')

argv = sys.argv[sys.argv.index("--") + 1:]
args = parser.parse_args(argv)

# Delete default cube
bpy.data.objects['Cube'].select = True
bpy.ops.object.delete()

bpy.ops.import_scene.obj(filepath=r'C:\Users\bunny\Desktop\test.obj')
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        ob.rotation_euler[0] += radians(-90)
        print(ob.name, ob.location, ob.rotation_euler)
        print(ob.data)
        me = ob.data
        verts_sel = [v.co for v in me.vertices if v.select]
        pivot = sum(verts_sel, Vector()) / len(verts_sel)
        print("Local:", pivot)
        print("Global:", ob.matrix_world * pivot)

        ob.location = ob.location - pivot

        bpy.ops.export_scene.obj(filepath=r'C:\Users\bunny\Desktop\test_2.obj', use_selection=True)