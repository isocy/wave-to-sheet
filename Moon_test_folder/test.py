import numpy as np
from PIL import Image


image = "./binary_sheets/binary_029500_morning-rain-piano-65875-1.png"
with Image.open(image) as img:
    img_array = np.array(img)

print(img_array)
print(img_array.shape)
