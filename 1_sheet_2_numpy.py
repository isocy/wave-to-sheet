import glob
from PIL import Image
import numpy as np


path = './midi_and_sheet/'
sheet_files = glob.glob(path+'*.png')

sheets = []
for sheet in sheet_files:
    pixels = Image.open(sheet).convert('L')
    pixels = np.asarray(pixels)
    sheets.append(pixels)
sheets = np.asarray(sheets)
sheets = np.expand_dims(sheets, axis=3)

save_path = './data/'
file_name = 'sheet.npy'
np.save(save_path+file_name, sheets)
