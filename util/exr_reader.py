import cv2
from skimage import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont

camera_height = 250

filename = f"{camera_height}.exr"

# input_path = rf"C:\Users\bunny\Desktop\open_exr\{filename}"
input_path = rf"C:\Users\bunny\Desktop\test\02_d.png0001.exr"

exr_info = cv2.imread(input_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

print(exr_info)

img = Image.fromarray((exr_info * 255).astype('uint8'), 'RGB')
real_image = io.imread(rf"C:\Users\bunny\Desktop\open_exr\250\00.png")
# img = Image.fromarray(real_image)
font_path = r"c:\windows\fonts\bahnschrift.ttf"

grid_h = len(exr_info) // 10
grid_w = len(exr_info[0]) // 10

h = grid_h // 2
w = grid_w // 2

for i in range(10):
    for j in range(10):
        w = grid_w // 2 + j * grid_w
        h = len(exr_info) - (grid_h // 2 + i * grid_h)
        value = exr_info[h][w][0]
        height = camera_height - value * 1000
        text = f'{"%.3f" % height} ({"%.3f" % value})'
        font = ImageFont.truetype(font_path, 12)
        ImageDraw.Draw(img).text((w + 3, h + 3), f'{text}', font=font)#, fill='black')
        ImageDraw.Draw(img).point((w, h), fill='red')

output_path = input_path[:-3] + 'tif'
img.save(output_path)
print(f"Image saved to {output_path}", 'TIFF')

# img = np.array(img)
# io.imsave(output_path, img.astype('uint8'))
