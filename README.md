# 실행 환경

- PyCharm IDE
- Anaconda virtual environment (Python 3.7)

# Magenta 모델 설치, 실행 방법

## 1. 개발 환경 설정

``` pip install magenta ```

``` pip install rtmidi ``` 

``` git clone https://github.com/tensorflow/magenta.git ```

``` pip install -e . ```

## 2. checkpoint 설치
- [piano model checkpoint](https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/maestro_checkpoint.zip) which is trained on the MAESTRO dataset
- [drum model checkpoint](https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/e-gmd_checkpoint.zip) which is trained on the E-GMD dataset

## 3. 실행

[0_1_args.py](0_1_args.py)

midi file로 변환할 .wav 파일이 저장되어 있는 경로를 텍스트 파일로 저장 

[0_model_test.py](0_model_test.py)
- FLAGS config 값을 'onesets_frames' 또는 'drums'로 변경
- .wav 파일의 경로가 저장되어 있는 텍스트 파일의 경로 지정 
```python
FLAGS.config = 'drums' #'onsets_frames' : piano, 'drums' : drum
.
.
.
argv_path = './drum_Test.txt' # piano_Train, piano_Test, drum_Train, drum_Test
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

---

# Web APPLICATION

Flask 웹 프레임워크를 사용하여 Web 어플리케이션 제작

- [app.py](./app.py): 어플리케이션 실행 파일
    - 로컬 호스트에서 실행(127.0.0.1:5000)


- [index.html](./templates/index.html): 어플리케이션 첫 페이지
    - 파일 업로드: .wav 파일을 업로드
    - 파일 목록: 업로드한 파일을 리스트로 화면에 보여줌

---
# CycleGAN (실패)

## 1. Numpy Array Format으로 저장

[1_sheet_2_numpy.py](1_sheet_2_numpy.py)

- 악보 이미지를 grayscale 한 후 128x128 크기로 resize
- numpy 배열로 변환하여 .npy 파일로 저장

[1_1_midi_2_numpy.py](1_1_midi_2_numpy.py)

- midi 파일을 numpy 배열로 변환
- 악보 파일과 크기를 같게 resize하여 .npy 파일로 저장


[2_model_train.py](./2_model_train.py)

- cycleGAN 모델을 이용한 학습
    - generator_AtoB -> midi 파일을 악보 파일로 생성하는 것을 학습
    - generator_BtoA -> 악보 파일을 midi 파일로 생성하는 것을 학습
  