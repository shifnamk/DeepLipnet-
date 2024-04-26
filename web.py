# web.py
import tensorflow as tf
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from modelutil import load_model, load_data
from utils import num_to_char
import os

app = Flask(__name__)

# Define allowed file extensions and upload folder
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mpg'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load your model
model = load_model()  # Load the model without weights

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            frames, _ = load_data(filepath)  # Pass the file path directly
            if frames is None:
                # Handle unknown video (no alignment data available)
                return render_template('unknown_video.html', video_file=filename)
            else:
                yhat = model.predict(tf.expand_dims(frames, axis=0))
                decoder = tf.keras.backend.ctc_decode(yhat, [75], greedy=True)[0][0].numpy()
                converted_prediction = tf.strings.reduce_join(num_to_char(decoder)).numpy().decode('utf-8')
                return render_template('result.html', video_file=filename, prediction=converted_prediction)
    return render_template('index.html')

if __name__ == '__main__':
   app.run(port=8000)  # Only specifying the port
