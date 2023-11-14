from PIL import Image
import os

def resize_image(file_path, output_path, size=(1024, 1024)):
    # 이미지 불러오기
    with Image.open(file_path) as img:
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(output_path)

if __name__ == '__main__':
    sheet_folder = "./binary_sheets"
    file_list = os.listdir(sheet_folder)

    for file in file_list:
        file_path = os.path.join(sheet_folder, file)
        output_path = './resize_sheets/' + file
        resize_image(file_path, output_path)


