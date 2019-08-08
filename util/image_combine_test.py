from skimage import io, segmentation, color
from skimage.future import graph

image_normal = io.imread(
    r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151136.985298\output\40\scene_mesh_textured_rotated\scene_mesh_textured_rotated_-10_0_-10\00_n.png0001.png')
image_depth = io.imread(
    r'C:\Users\bunny\Desktop\iu_model\modelFriJun07151136.985298\output\40\scene_mesh_textured_rotated\scene_mesh_textured_rotated_-10_0_-10\00_d.png0001.png')
img = image_normal[..., :3]


labels1 = segmentation.slic(img, compactness=30, n_segments=400)

g = graph.rag_mean_color(img, labels1, mode='similarity')
labels2 = graph.cut_normalized(labels1, g)
out2 = color.label2rgb(labels2, img, kind='avg')

depth_layer = 255 - image_depth[..., 0] / 1.5
image_normal[..., :3] = out2
image_normal[..., 3] = depth_layer
io.imsave(r'C:\Users\bunny\Desktop\test.png', image_normal)
