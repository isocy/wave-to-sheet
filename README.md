# 실행 환경

- PyCharm IDE
- Anaconda virtual environment (Python 3.7)

# Magenta 모델 설치, 실행 방법

## 1. 개발 환경 설정

``` pip install magenta ```

``` pip install rtmidi ``` 

``` git clone https://github.com/tensorflow/magenta.git ```

``` pip install -e . ```

## 2. [checkpoint](https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/maestro_checkpoint.zip) 설치

## 3. 실행

onsets_frames_trascription_transcribe.py 파일의 Run Configuration을 아래의 파라미터로 작성하여 실행
```
--model_dir=<path to directory containing checkpoint>
<piano_recording1.wav, piano_recording2.wav, ...>
```
---
# 미디를 악보화하는 방법

## midi_to_sheets.py를 사용합니다

    # 미디 폴더를 지정
    midi_folder = "./Moon_test_folder/midi/"
    # 출력 폴더를 지정
    sheet_folder = "./Moon_test_folder/sheets"
    # MuseScore3.exe의 경로를 지정
    MuseScore3_exe_path = "C:/Program Files/MuseScore 3/bin/MuseScore3.exe"

파라미터를 수정하고 py를 실행하면 지정된 폴더의 midi 파일들이 MuseScore3에 의해 악보화 됩니다.
