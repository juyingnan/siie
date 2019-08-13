# A simple script that uses blender to render views of a single object by rotation the camera around it.
# Also produces depth map at the same time.
#
# Example:
# blender --background --python mytest.py -- --views 10 /path/to/my.obj
#

import argparse
import sys
import os
from math import radians
import math

parser = argparse.ArgumentParser(description='Renders given obj file by rotation a camera around it.')
parser.add_argument('--views', type=int, default=1,
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
parser.add_argument('--move_and_save', type=bool, default=False,
                    help='Move to center and overwrite the original file.')
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

import bpy
from mathutils import Vector

# Set up rendering of depth map.
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

# Add passes for additionally dumping albedo and normals.
bpy.context.scene.render.layers["RenderLayer"].use_pass_normal = True
bpy.context.scene.render.layers["RenderLayer"].use_pass_color = True
bpy.context.scene.render.image_settings.file_format = args.format
bpy.context.scene.render.image_settings.color_depth = args.color_depth

# Clear default nodes
for n in tree.nodes:
    tree.nodes.remove(n)

# Create input render layer node.
render_layers = tree.nodes.new('CompositorNodeRLayers')

depth_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
depth_file_output.label = 'Depth Output'
if args.format == 'OPEN_EXR':
    links.new(render_layers.outputs['Depth'], depth_file_output.inputs[0])
else:
    # Remap as other types can not represent the full range of depth.
    map = tree.nodes.new(type="CompositorNodeMapValue")
    # Size is chosen kind of arbitrarily, try out until you're satisfied with resulting depth map.
    map.offset = [0]
    map.size = [args.depth_scale]
    map.use_min = True
    map.min = [0]
    map.use_max = True
    map.max = [255]
    links.new(render_layers.outputs['Depth'], map.inputs[0])

    links.new(map.outputs[0], depth_file_output.inputs[0])

scale_normal = tree.nodes.new(type="CompositorNodeMixRGB")
scale_normal.blend_type = 'MULTIPLY'
# scale_normal.use_alpha = True
scale_normal.inputs[2].default_value = (0.5, 0.5, 0.5, 1)
links.new(render_layers.outputs['Normal'], scale_normal.inputs[1])

bias_normal = tree.nodes.new(type="CompositorNodeMixRGB")
bias_normal.blend_type = 'ADD'
# bias_normal.use_alpha = True
bias_normal.inputs[2].default_value = (0.5, 0.5, 0.5, 0)
links.new(scale_normal.outputs[0], bias_normal.inputs[1])

normal_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
normal_file_output.label = 'Normal Output'
links.new(bias_normal.outputs[0], normal_file_output.inputs[0])

# albedo_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
# albedo_file_output.label = 'Albedo Output'
# links.new(render_layers.outputs['Color'], albedo_file_output.inputs[0])

# Delete default cube
bpy.data.objects['Cube'].select = True
bpy.ops.object.delete()

bpy.ops.import_scene.obj(filepath=args.obj)

obs = []
for ob in bpy.context.scene.objects:
    # whatever objects you want to join...
    if ob.type == 'MESH':
        obs.append(ob)
ctx = bpy.context.copy()
# one of the objects to join
ctx['active_object'] = obs[0]
ctx['selected_objects'] = obs
# we need the scene bases as well for joining
ctx['selected_editable_bases'] = [bpy.context.scene.object_bases[ob.name] for ob in obs]
bpy.ops.object.join(ctx)
ctx['name'] = 'combine'

obj_dimension = 0
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        print(ob.name, ob.location, ob.rotation_euler, ob.dimensions)
        obj_dimension = max(ob.dimensions)
print('Max dimension: {}'.format(obj_dimension))

for object in bpy.context.scene.objects:
    if object.name in ['Camera', 'Lamp']:
        continue
    bpy.context.scene.objects.active = object
    # if args.scale != 1:
    #     bpy.ops.transform.resize(value=(args.scale, args.scale, args.scale))
    #     bpy.ops.object.transform_apply(scale=True)
    if obj_dimension != 0:
        bpy.ops.transform.resize(value=(1 / obj_dimension, 1 / obj_dimension, 1 / obj_dimension))
        bpy.ops.object.transform_apply(scale=True)
    if args.remove_doubles:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')
    if args.edge_split:
        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].split_angle = 1.32645
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="EdgeSplit")

for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        ob.rotation_euler[0] = 0
        bpy.ops.object.transform_apply(rotation=True)
        print(ob.name, ob.location, ob.rotation_euler)
        print(ob.data)
        me = ob.data
        verts_sel = [v.co for v in me.vertices if v.select]
        min_x = min([vert[0] for vert in verts_sel])
        min_y = min([vert[1] for vert in verts_sel])
        max_x = max([vert[0] for vert in verts_sel])
        max_y = max([vert[1] for vert in verts_sel])
        # pivot = sum(verts_sel, Vector()) / len(verts_sel)
        # global_offset = ob.matrix_world * pivot
        # print("Local:", pivot)
        # print("Global:", global_offset)
        # pivot[2] = 0

        ob.location = ob.location - Vector(((min_x + max_x) / 2, (min_y + max_y) / 2, 0))
        # if args.move_and_save:
        #     bpy.ops.export_scene.obj(filepath=args.obj, use_selection=True)

# Make light just directional, disable shadows.
lamp = bpy.data.lamps['Lamp']
lamp.type = 'SUN'
lamp.shadow_method = 'NOSHADOW'
# Possibly disable specular shading:
lamp.use_specular = False

# Add another light source so stuff facing away from light is not completely dark
bpy.ops.object.lamp_add(type='SUN')
lamp2 = bpy.data.lamps['Sun']
lamp2.shadow_method = 'NOSHADOW'
lamp2.use_specular = False
lamp2.energy = 0.2
bpy.data.objects['Sun'].rotation_euler = bpy.data.objects['Lamp'].rotation_euler
bpy.data.objects['Sun'].rotation_euler[0] += 180


def parent_obj_to_camera(b_camera):
    origin = (0, 0, 0)
    b_empty = bpy.data.objects.new("Empty", None)
    b_empty.location = origin
    b_camera.parent = b_empty  # setup parenting

    scn = bpy.context.scene
    scn.objects.link(b_empty)
    scn.objects.active = b_empty
    return b_empty


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    # else:
    #     shutil.rmtree(path)
    #     os.makedirs(path)

scene = bpy.context.scene
scene.render.resolution_x = obj_dimension * 10
scene.render.resolution_y = obj_dimension * 10
scene.render.resolution_percentage = 100
scene.render.alpha_mode = 'TRANSPARENT'
scene.camera.data.clip_end = 5000
cam = scene.objects['Camera']
bpy.data.cameras['Camera'].type = 'ORTHO'
bpy.data.cameras['Camera'].ortho_scale = 1
image_id = 0
cam_offset_base = [0, 0, 0]
# cam_offset_base = (11.65, -4.58, -51.47)
# cam_distance = 40 if obj_dimension == 0 else obj_dimension * 1.0
cam_distance = 0.5
small_distance = 0 # 1e-5
cam_location_base_list = [(small_distance, small_distance, cam_distance)]
# (small_distance, cam_distance, small_distance),
# (cam_distance, small_distance, small_distance)]
# cam_location_base_list = [(0, 0.0001, 2), (0, 2, 0), (0, 1.5, 1.5)]
make_dir(args.output_folder)
render_list_file_path = fp = os.path.join(args.output_folder, 'rendering_metadata.txt')
f = open(render_list_file_path, "w")

for cam_location_base in cam_location_base_list:
    cam.location = [(loc - offset) for loc, offset in zip(cam_location_base, cam_offset_base)]
    print(cam.location)
    phi = 0
    # phi = math.degrees(math.atan(cam_location_base[2] / cam_location_base[1]))
    cam_constraint = cam.constraints.new(type='TRACK_TO')
    cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    cam_constraint.up_axis = 'UP_Y'
    b_empty = parent_obj_to_camera(cam)
    cam_constraint.target = b_empty

    model_identifier = os.path.split(os.path.split(args.obj)[0])[1]
    fp = os.path.join(args.output_folder, model_identifier, model_identifier)
    scene.render.image_settings.file_format = 'PNG'  # set output format to .png

    stepsize = 360.0 / args.views
    rotation_mode = 'XYZ'

    for output_node in [depth_file_output, normal_file_output]:  # , albedo_file_output]:
        output_node.base_path = ''

    base_angle = 270
    print(b_empty.rotation_euler)
    b_empty.rotation_euler[2] += radians(45)

    for i in range(0, args.views):
        print("Rotation {}, {}".format((stepsize * i), radians(stepsize * i)))
        scene.render.filepath = os.path.join(args.output_folder, '{0:02d}'.format(image_id))
        depth_file_output.file_slots[0].path = os.path.join(args.output_folder, '{0:02d}_d.png'.format(image_id))
        # depth_file_output.file_slots[0].path = scene.render.filepath + "_depth.png"
        normal_file_output.file_slots[0].path = os.path.join(args.output_folder, '{0:02d}_n.png'.format(image_id))
        # albedo_file_output.file_slots[0].path = scene.render.filepath + "_albedo.png"

        bpy.ops.render.render(write_still=True)  # render still

        b_empty.rotation_euler[2] += radians(stepsize)
        image_id += 1

        # output rendering file
        angle = (base_angle - stepsize * i + 360) % 360
        distance = math.sqrt(sum([item * item for item in cam.location])) * 0.57
        f.write('{} {} 0 {} 25\n'.format(angle, phi, distance))

f.close()
print(cam_distance)
