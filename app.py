from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
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
@app.route('/fileUpload',methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save('./uploads/'+filename)
            return render_template('complete.html')

    return render_template('fail.html')

@app.route('/list')
def list():
    uploaded_file = os.listdir('./uploads')
    return render_template('list.html',uploaded_file=uploaded_file)

if __name__ == '__main__':
    app.run(debug=True)