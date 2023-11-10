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
