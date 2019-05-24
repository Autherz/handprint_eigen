from flask import Flask, render_template, request, redirect, Response
import base64
import json
import os
from model import recogniser_str

app = Flask(__name__)
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/upload_image", methods=["POST"])
def upload():
    print("xxxx")
    if request.method == 'POST':
        print("ok, post")
        file = request.files['file']
        
        if 'image' in file.content_type:
            print('ok image')
            f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            img = os.path.join('static/images/', file.filename)
            file.save(img)
            index, similarity = recogniser_str(img)
            print(similarity)
            img2 = os.path.join('static/train/', str(index)+'.jpg')
            image_path = os.path.join('static/images/', file.filename)
            return json.dumps({'data':'true','img_path': image_path, 'img_path2':img2,'similarity':similarity, 'index': str(index)})

        else:
            print('not ok image')
            return json.dumps({'data': 'false', 'err':'NOT_IMG'})
    else:
        print('error')
        return json.dumps({'data':'false'})

if __name__ == '__main__':
    app.run('0.0.0.0', '5010')
