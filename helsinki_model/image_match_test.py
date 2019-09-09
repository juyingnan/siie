from scipy import signal
from scipy import misc
import numpy as np
from skimage import io

image_mask = io.imread(r'C:\Users\bunny\Desktop\mask_kalasatama_ss.png')[..., 0]
image_depth = io.imread(r'C:\Users\bunny\Desktop\depth_s.png')[..., 0]
corr = signal.correlate2d(image_mask, image_depth, boundary='fill', mode='same')
y, x = np.unravel_index(np.argmax(corr), corr.shape)
print(y, x)
