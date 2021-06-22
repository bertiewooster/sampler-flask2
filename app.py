# Adapted from https://buildcoding.com/upload-and-download-file-using-flask-in-python/
import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template
import pathlib

#import shutil # for duplicating a file, to prototype Sampler output
import sampler.sample.sampler # Works A. VSC recognizes

# For /yield--stream to web page
import flask
import subprocess
import time          #You don't need this. Just included it so you can see the output stream.

import secrets

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__, template_folder='templates')

secret = secrets.token_urlsafe(32)
app.secret_key = secret

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hello world
@app.route('/')
def hello_world():
    return 'Hello this is sampler-flask'
    # Add a template with links to:
    #   Run a new sampler
    #   Download an existing file--list the files in UPLOAD_FOLDER

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
            # --- Upload input_file ---
            # Ensure the upload folder exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            # ensure the filename is safe to use
            input_filename = secure_filename(input_file.filename)
            # compose file path: upload folder + filename
            input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
            # save file
            input_file.save(input_filepath)
            print("Uploaded file successfully")

            # Handle input parameters output_file, n_results
            output_file = request.form.get('output_file')
            if output_file and not output_file.isspace():
                output_filename = output_file
            else:
                # the string is non-empty
                output_identifier = pathlib.Path(input_filename).stem
                #print('output_identifier={}'.format(output_identifier))
                output_suffix = "_out"
                output_extension = os.path.splitext(input_filename)[1]
                #print('output_extension={}'.format(output_extension))
                output_filename = output_identifier + output_suffix + output_extension
            #print("output_filename = {}".format(output_filename))

            n_results = request.form.get('n_results')
            #print('output_file, n_results= {}, {}'.format(output_file, n_results))

            # Add code here to 
            #  1) compose output_file filepath (path/name)
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

            #print('input_filepath = {}'.format(input_filepath))
            #print('output_filepath = {}'.format(output_filepath))

            # Prototype Sampler by simply copying input file as output file
            #shutil.copy(input_filepath, output_filepath)

            #  2) run Sampler, so output_file is written to appropriate place
            try:
                sampler.sample.sampler.Sampler(input_filepath, output_filepath, n_results) # Works A.
            except sampler.sample.sampler.SamplerError as e:
                error_str = str(e)
                flash(error_str)
                flash("Input file: {}".format(input_filename))
                flash("Output file: {}".format(output_filename))
                flash("Number of results to find: {}".format(n_results))
                return redirect('/error')
                #return flask.Response("SamplerError", mimetype='text/html')  # text/html is required for most browsers to show this

            # send output_file name as parameter to download
            return redirect('/downloadfile/' + output_filename)

    # If request.method is GET
    return render_template('run.html')

# Error page
@app.route("/error", methods = ['GET'])
def show_error():
    return render_template('error.html')

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

@app.route('/yield')
def index():
    def inner():
        mylist = list(range(10))

        for number in mylist:
            time.sleep(1)                           # Don't need this just shows the text streaming
            yield str(number) + '<br/>\n'

    return flask.Response(inner(), mimetype='text/html')  # text/html is required for most browsers to show th$

app.run(debug=True, port=5000, host='0.0.0.0')