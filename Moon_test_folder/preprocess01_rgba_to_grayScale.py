from PIL import Image, ImageOps
import os

sheet_folder = "./sheets"

file_list = os.listdir(sheet_folder)
for file in file_list:
    file_path = os.path.join(sheet_folder, file)
    image = Image.open(file_path)
    rgba_image = image.convert("RGBA")
    new_image = Image.new("RGB", rgba_image.size, "WHITE")  # 흰색 배경으로 새 이미지 생성
    for x in range(rgba_image.size[0]):
        for y in range(rgba_image.size[1]):
            r, g, b, a = rgba_image.getpixel((x, y))
            if a != 0:  # 알파 값이 0이 아니면, 즉 투명하지 않으면
                new_image.putpixel((x, y), (0, 0, 0))  # 해당 위치를 검은색으로 설정

    # 이미지를 이진 모드로 변환
    binary_image = new_image.convert('1')
    # 변환된 이미지 저장
    binary_image.save(f'./binary_sheets/binary_{file}')

