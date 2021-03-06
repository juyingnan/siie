import os
import numpy as np
from skimage import io
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


root_dir = r'C:\Users\bunny\Desktop\helsinki_train_raw'
base_img_name = 'rgb.png'
# alpha_img_name = None
alpha_img_name = 'depth.png'
output_img_name = base_img_name.replace('.png', '_4ch.png')
output_path = os.path.join(root_dir, output_img_name)

base_img = io.imread(os.path.join(root_dir, base_img_name))
print(base_img.shape)
alpha_layer = None
if alpha_img_name is None:
    layer_shape = [dim for dim in base_img.shape]
    layer_shape[-1] = 1
    alpha_layer = 255 - np.zeros(layer_shape, dtype=np.uint8)
else:
    alpha_layer = 255 - io.imread(os.path.join(root_dir, alpha_img_name))[..., :1]
print(alpha_layer.shape)
final_img = np.dstack((base_img, alpha_layer))
print(final_img.shape)

io.imsave(output_path, final_img)
