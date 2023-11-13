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
