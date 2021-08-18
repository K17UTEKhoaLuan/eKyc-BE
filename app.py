import flask
from flask import send_file, render_template, request
import os
import convert
import documentScanner
UPLOAD_FOLDER = './cmnd'


app = flask.Flask(__name__, template_folder=".")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def home():
    return "hello"


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], "a.jpg")
        file1.save(path)
        return path


@app.route("/frontside", methods=['POST'])
def frontside():
    data = request.json
    convert.convert_base64_to_image(data, "frontside")
    print("frontside/{}_frontside.jpg".format(data["name"]))
    documentScanner.valid_front_side_identity("frontside/{}_frontside.jpg".format(data["name"]))
    return "done"


if __name__ == '__main__':
    app.run()
