# flaskftp
# Upload and download files

## Instructions:
1. Clone this repo to a local folder, for example flaskftp
2. In your shell, change directory to that folder, for example cd flaskftp
3. If desired, create a virtual environment using
3.1. $ python3 -m venv venv
3.2. $ . venv/bin/activate
4. $ pip install -r requirements.txt
5. $ export FLASK_APP=__init__
6. $ flask run
7. Point your web browser to the URL in your shell followed by /uploadfile, typically 127.0.0.1:5000/uploadfile
8. Upload a file; it should appear in the uploads subfolder, for example flaskftp/uploads
9. Download that file; it should be downloaded, and probably be opened by your web browser in an appropriate application
