# import the necessary packages
import os
import sys
import requests
import ssl
from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file
from flask import redirect, url_for
from flask import render_template
from werkzeug import secure_filename

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import json

import zipfile
from io import BytesIO

import time

from uuid import uuid4

from os import path
# import torch

# import fastai
# from fasterai.visualize import *
from pathlib import Path


# torch.backends.cudnn.benchmark=True

# image_colorizer = get_image_colorizer(artistic=True)
# video_colorizer = get_video_colorizer()

# os.environ['CUDA_VISIBLE_DEVICES']='0'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
TO_EMAIL = 'lazukav@gmail.com'

app = Flask(__name__, template_folder=".")

# app.config['SENDGRID_API_KEY'] = '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'
# app.config['SENDGRID_DEFAULT_FROM'] = 'customer@colorizer.com'
sg = SendGridAPIClient('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')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# define a predict function as an endpoint

@app.route("/process_image", methods=["POST", "GET"])
def process_image():
    if request.method == 'POST':
        memory_file = BytesIO()
        if request.files.getlist('photos')[0].filename == '':
            return redirect(url_for('index'))
        with zipfile.ZipFile(memory_file, 'w') as zf:
            # print(request.files.getlist('photos'))
            for f in request.files.getlist('photos'):
               #f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
                print("hi")
                if f and allowed_file(f.filename):
                    filename = secure_filename(f.filename)
                    data = zipfile.ZipInfo(filename)
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(data, f.read())
                    print(f)
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='capsule.zip', as_attachment=True)

            # return 'Upload completed.'
    return redirect(url_for('index'))
    # return "Kuku"


@app.route("/contact_us", methods=["POST", "GET"])
def contact_us():
    if request.method == 'POST':
        if request.form['email'] and request.form['note']:
            message = Mail(
                from_email='customer@colorizer.com',
                to_emails=TO_EMAIL,
                subject='Customer of colorizer',
                html_content='<strong>'+ request.form['name'] +'</strong> <br>' + request.form['note'])
            response = sg.send(message)
        # dataDict = json.loads(data)
    # print(data['name'])

    # message = Mail(
    #     from_email='customer@colorizer.com',
    #     to_emails='lazukav@gmail.com',
    #     subject='Sending with Twilio SendGrid is Fun',
    #     html_content='<strong>and easy to do anywhere, even with Python</strong>')
    # response = sg.send(message)
    return redirect(url_for('index'))

@app.route('/')
def hello_world():
    # message = Mail(
    #     from_email='customer@colorizer.com',
    #     to_emails='lazukav@gmail.com',
    #     subject='Sending with Twilio SendGrid is Fun',
    #     html_content='<strong>and easy to do anywhere, even with Python</strong>')
    # response = sg.send(message)
    return 'Hello, World!'


@app.route('/index')
def index():
    return render_template('index.html')





# @app.route("/process_image_api", methods=["POST"])
# def process_image_api():
#     source_url = request.json["source_url"]
#     render_factor = int(request.json["render_factor"])

#     upload_directory = 'upload'
#     if not os.path.exists(upload_directory):
#            os.mkdir(upload_directory)

#     random_filename = str(uuid4()) + '.png'
    
#     image_colorizer.plot_transformed_image_from_url(url=source_url, path=os.path.join(upload_directory, random_filename), figsize=(20,20),
#             render_factor=render_factor, display_render_factor=True, compare=False)

#     callback = send_file(os.path.join("result_images", random_filename), mimetype='image/jpeg')

#     os.remove(os.path.join("result_images", random_filename))
#     os.remove(os.path.join("upload", random_filename))

#     return callback


if __name__ == '__main__':
    port = 5005
    host = '127.0.0.1'
    app.run(host=host, port=port, threaded=True, debug=True)
