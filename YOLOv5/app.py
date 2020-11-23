from flask import Flask, render_template, json, request
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from detect import detect
import torch
import torch.backends.cudnn as cudnn
import argparse
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords,
    xyxy2xywh, plot_one_box, strip_optimizer, set_logging)
from utils.torch_utils import select_device, load_classifier, time_synchronized


app = Flask(__name__)
UPLOAD_FOLDER = './uploded/fileuploaded'
OUTPUT_FOLDER = './uploded/fileoutput'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


ALLOWED_EXTENSIONS = set(['mp4', 'avi','gif'])

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def main():
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload',methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        print(request.headers)
        print(request.files)
        # check if the post request has the file part
        if 'data_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['data_file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html')

    

@app.route('/uploaded_file/<path:filename>')
def uploaded_file(filename):
    path_to_input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='last.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default=path_to_input_file, help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-dir', type=str, default='uploded/fileoutput', help='directory to save results')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    opt = parser.parse_args()

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                final_pred = detect(opt)
                strip_optimizer(opt.weights)
        else:
            final_pred = detect(opt)
    flash("This is a "+final_pred, "info")
    return redirect(url_for('show_file',filename=filename))
    
@app.route('/show_file/<path:filename>')
def show_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

@app.route('/successyolo', methods=['POST', 'GET'])
def goyolo():
    return render_template('success.html')
    
    

    
if __name__ == "__main__":
    app.run(port=5000)
