import os
import numpy as np
from skimage import io
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


root_dir = r'D:\Projects\SIIE\helsinki\kalatasama_train_raw'
base_img_name = 'normal.png'
# alpha_img_name = None
alpha_img_name = 'mask.png'
output_img_name = base_img_name.replace('.png', '_3ch.png')
output_path = os.path.join(root_dir, output_img_name)

base_img = io.imread(os.path.join(root_dir, base_img_name))
print(base_img.shape)
alpha_layer = None
if alpha_img_name is None:
    layer_shape = [dim for dim in base_img.shape]
    layer_shape[-1] = 1
    alpha_layer = 1 - np.zeros(layer_shape, dtype=np.uint8)
else:
    alpha_layer = 255 - io.imread(os.path.join(root_dir, alpha_img_name))  # [..., :1]
print(alpha_layer.shape)
final_img = np.multiply(base_img, alpha_layer.reshape(alpha_layer.shape[0], alpha_layer.shape[1], 1) / 255)
print(final_img.shape)

io.imsave(output_path, final_img)
