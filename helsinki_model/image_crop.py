from skimage import io
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

original = io.imread(r'C:\Users\bunny\Desktop\models_test\00_d.png0001.png')

flipped = np.flip(original, 0)

start_x, start_y = 453,577
height, width = 2750 * 5, 1750 * 5

# start_x, start_y = 453,14328
# height, width = 5000, 3750

cropped = original[start_y:start_y + height, start_x:start_x + width]
# flipped = np.flip(cropped, 0)

io.imsave(r'C:\Users\bunny\Desktop\models_test\mask_kalasatama_cropped.png', cropped)
