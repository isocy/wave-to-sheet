import glob

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from wav_to_midi import wav_to_midi
from midi_to_sheet import midi_to_sheet

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
    filename = request.args.get('filename')
    sheets = request.args.getlist('sheets')
    if filename is None and len(sheets)==0:
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save('./static/audio/'+filename)

                return redirect(url_for('loading', filename=filename))

        return render_template('fail.html')

    print(filename)
    print(sheets)

    return render_template('view.html', filename=filename, sheets=sheets, sheet_idx=0)

@app.route('/loading/<filename>')
def loading(filename):
    # 악보 생성
    wav_to_midi(filename)
    idx = filename.find('.wav')
    midi = 'midi/' + filename[:idx] + '.midi'

    while not os.path.isfile(midi):
        continue

    musescore_exe_path = 'C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe'
    sheet = 'static/images/'

    midi_to_sheet(midi, sheet, musescore_exe_path)

    sheet += filename[:idx] + '*.png'
    sheets = glob.glob(sheet)
    for i in range(len(sheets)):
        sheets[i] = 'images/' + sheets[i].split('\\')[-1]

    return redirect(url_for('view', filename=filename, sheets=sheets))

@app.route('/view/<string:name>/<int:idx>')
def view_sheet(name, idx):

    name_idx = name.find('.wav')

    sheet = 'static/images/'
    sheet += name[:name_idx] + '*.png'

    sheets = glob.glob(sheet)
    for i in range(len(sheets)):
        sheets[i] = 'images/' + sheets[i].split('\\')[-1]

    return render_template('view.html', filename=name, sheets=sheets, sheet_idx=idx)

if __name__ == '__main__':
    app.run(debug=True)