import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hello world
@app.route('/')
def hello_world():
    return 'Hello this is flaskftp3'
    # Add a template with links to:
    # Upload a new file
    # Download an existing file--list the files in 

# Run sampler API
@app.route('/run', methods=['GET', 'POST'])
def run():
    print('Running run')
    if request.method == 'POST':
        #print('POST')
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        #print('A file was provided')
        file = request.files['file']
        #print('file.filename = {}'.format(file.filename))
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            # ensure the filename is safe to use
            filename = secure_filename(file.filename)
            # compose file path: upload folder + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # save file
            file.save(filepath)
            print("saved file successfully")
            # send file name as parameter to download
            return redirect('/downloadfile/' + filename)

    return render_template('run.html')

# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            # ensure the filename is safe to use
            filename = secure_filename(file.filename)
            # compose file path: upload folder + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # save file
            file.save(filepath)
            print("saved file successfully")
            # send file name as parameter to download
            return redirect('/downloadfile/' + filename)

    return render_template('upload_file.html')

# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
