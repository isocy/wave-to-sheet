import subprocess

# MuseScore의 실행 파일 경로와 MIDI 경로, 악보 경로를 입력
musescore_executable_path = "C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe"
midi_file_path = "./midi/summer.mid"
output_file_path = "./sheets/summer.png"

# 명령 구성
command = f'"{musescore_executable_path}" -o "{output_file_path}" "{midi_file_path}"'