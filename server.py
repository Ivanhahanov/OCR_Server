from flask import Flask, request, render_template, send_file, abort
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from gridfs import GridFS
from gridfs.errors import NoFile
from PIL import Image
from pytesseract import image_to_string

app = Flask(__name__)
Bootstrap(app)

app.config.update(
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=10,
    DROPZONE_MAX_FILES=120,
    DROPZONE_REDIRECT_VIEW='converted',
    DROPZONE_UPLOAD_MULTIPLE=True,
    DROPZONE_UPLOAD_ON_CLICK=True
)
dropzone = Dropzone(app)

DB = MongoClient(host=['mongodb:27017']).gridfs
FS = GridFS(DB)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/uploads', methods=['POST'])
def upload():
    i = 0
    for key, f in request.files.items():
        i += 1
        if key.startswith('file'):
            filename = secure_filename(f.filename).split('.')[0]
            filename += str(i)
            if FS.exists({"filename": f'{filename}.txt'}):
                continue
            text = image_to_string(Image.open(f), lang='rus')
            print(text)
            with open("zip/"+filename+'.txt', 'w') as f1:
                f1.write(text)
            FS.put(text.encode('utf-16'), content_type='text/plain', filename=f'{filename}.txt')
    return 'Upload complete'


@app.route('/download/<file>')
def download(file):
    try:
        file = FS.get_last_version(file)
        return send_file(file, mimetype=file.content_type)
    except NoFile:
        abort(404)


@app.route('/converted')
def converted():
    files = [FS.get_last_version(file) for file in FS.list()]
    return render_template('list_of_files.html', files=files)


@app.errorhandler(404)
def custom404(error):
    return render_template('error.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
