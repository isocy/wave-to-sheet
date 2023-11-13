# mid 폴더 내의 확장자를 추가하거나 제거하는 코드.
# my_extension을 ''로 하면 확장자를 제거하고
# '.mid'를 붙이면 .mid확장자로 바꿔줌

my_extension = ''


import os

midi_folder = './midi'
file_list = os.listdir(midi_folder)

for file in file_list:
    file_path = os.path.join(midi_folder, file)
    try:
        file_name, file_extension = os.path.splitext(file_path)
        new_file_path = file_name + my_extension
        os.rename(file_path, new_file_path)
    except:
        pass

