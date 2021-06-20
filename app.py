# Adapted from https://buildcoding.com/upload-and-download-file-using-flask-in-python/
import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hello world
@app.route('/')
def hello_world():
    return 'Hello this is sampler-flask'
    # Add a template with links to:
    # Upload a new file
    # Download an existing file--list the files in 

# Run sampler API
@app.route('/run', methods=['GET', 'POST'])
def run():
    #print('Running run')
    if request.method == 'POST':
        #print('request.files: {}'.format(request.files))
        #print('POST')
        # check if the post request has the file part
        if 'input_file' not in request.files:
            print('no file')
            return redirect(request.url)
        #print('A file was provided')
        file = request.files['input_file']
        #print('file = {}'.format(file))
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
            # Add code here to 
            #  1) compose output_file filepath (path/name)
            #  2) run Sampler, so output_file is written to appropriate place

            # Change filename to be the output_file
            # send file name as parameter to download
            return redirect('/downloadfile/' + filename)

    # If request.method is GET
    return render_template('run.html')

"""
# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print('request.files: {}'.format(request.files))
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
"""

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
