from fileinput import filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import  ImageDataGenerator
from flask import Flask,request,render_template,redirect,url_for,flash
from werkzeug.utils import secure_filename
import os

def predict():
    model=load_model('model.h5')
    datagen=ImageDataGenerator(rescale=1./255)
    test_generator=datagen.flow_from_directory('C:/Users/ritod/Programs/Cats_Dogs_Project/Classification/images',target_size=(180,180),class_mode=None)
    pred = model.predict(test_generator)
    return pred

UPLOAD_FOLDER ='C:/Users/ritod/Programs/Cats_Dogs_Project/Classification/images/test'
ALLOWED_EXTENSIONS={'jpg','jpeg','png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

@app.route('/')  
def upload():  
    return render_template("upload.html")  

@app.route('/result/<file_name>')
def result(file_name):
    pred=predict()
    os.remove(os.path.join("C:/Users/ritod/Programs/Cats_Dogs_Project/Classification/images/test",os.listdir('C:/Users/ritod/Programs/Cats_Dogs_Project/Classification/images/test')[0]))
    return render_template("result.html", pred=pred, acc=pred if pred>0.5 else 1-pred)
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        file_name=os.path.join(app.config['UPLOAD_FOLDER'],f.filename)
        f.save(file_name)
        return redirect(url_for('result',file_name="abc"))
 

if __name__ == '__main__':  
    app.run(debug = True)  