# Adapted from https://buildcoding.com/upload-and-download-file-using-flask-in-python/
import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template
import shutil # for duplicating a file, to prototype Sampler output

#if __name__ == "__main__" and __package__ is None:
#    __package__ = "sampler.sample"
#from sampler.sample import Sampler
#import sampler.sample.sampler
#import sampler.sample # VSC recognizes
import sampler.sample.sampler # VSC recognizes
#import sampler

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
        # check if the post request has the file part
        if 'input_file' not in request.files:
            print('no file')
            return redirect(request.url)
        #print('A file was provided')
        input_file = request.files['input_file']
        #print('file = {}'.format(file))
        # if user does not select file, browser also
        # submit a empty part without filename
        if input_file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            # Handle input parameters output_file, n_results
            output_file = request.form.get('output_file')
            n_results = request.form.get('n_results')
            print('output_file, n_results= {}, {}'.format(output_file, n_results))

            # --- Upload inut_file ---
            # Ensure the upload folder exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            # ensure the filename is safe to use
            input_filename = secure_filename(input_file.filename)
            # compose file path: upload folder + filename
            input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
            # save file
            input_file.save(input_filepath)
            print("saved file successfully")
            # Add code here to 
            #  1) compose output_file filepath (path/name)
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_file)

            # Prototype Sampler by simply copying input file as output file
            #shutil.copy(input_filepath, output_filepath)

            #  2) run Sampler, so output_file is written to appropriate place
            #sampler.sample.debug.py
            sampler.sample.sampler.Sampler(input_filepath, output_filepath, n_results)

            # send output_file name as parameter to download
            return redirect('/downloadfile/' + output_file)

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
