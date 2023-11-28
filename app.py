from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from music_to_sheet import wav_to_midi

import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

ALLOWED_EXTENSIONS={'wav'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS

@app.route('/view',methods=['GET','POST'])
def view():
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save('./uploads/'+filename)

            # 악보 생성
            wav_to_midi(filename)
            idx = filename.find('.wav')
            midi = 'midi/'+filename[:idx]+'.midi'

            while not os.path.isfile(midi):
                continue

            return render_template('view.html',filename=filename, midi=midi)
    return render_template('fail.html')



if __name__ == '__main__':
    app.run(debug=True)