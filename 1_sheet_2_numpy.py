import glob
from PIL import Image
import numpy as np
import os
from tqdm import tqdm

path = './midi_and_sheet/'
sheet_files = glob.glob(path+'*.png')

sheets = []
size = 128
for sheet in tqdm(sheet_files):
    pixels = Image.open(sheet).convert('L')
    pixels = pixels.resize((size, size), Image.Resampling.LANCZOS)
    pixels = np.asarray(pixels)
    sheets.append(pixels)
sheets = np.asarray(sheets)
sheets = np.expand_dims(sheets, axis=3)
print(sheets.shape)

save_path = './data/'
if not os.path.isdir(save_path):
    os.mkdir(save_path)
file_name = 'sheet_{}.npy'.format(sheets.shape[1:3])
np.save(save_path+file_name, sheets)
