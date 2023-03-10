# Importing essential libraries
from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from PIL import Image
import cv2
import tensorflow as tf
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.secret_key = 'O.\x89\xcc\xa0>\x96\xf7\x871\xa2\xe6\x9a\xe4\x14\x91\x0e\xe5)\xd9'

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the Random Forest CLassifier model
filename = 'Models/diabetes-model.pkl'
filename1 = 'Models/cancer-model.pkl'
classifier = pickle.load(open(filename, 'rb'))
rf = pickle.load(open(filename1, 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    if request.method == 'POST':
        try:
            preg = int(request.form['pregnancies'])
            glucose = int(request.form['glucose'])
            bp = int(request.form['bloodpressure'])
            st = int(request.form['skinthickness'])
            insulin = int(request.form['insulin'])
            bmi = float(request.form['bmi'])
            dpf = float(request.form['dpf'])
            age = int(request.form['age'])

            data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
            my_prediction = classifier.predict(data)

            return render_template('d_result.html', prediction=my_prediction)
        except ValueError:
            flash(
                'Invalid input. Please fill in the form with appropriate values', 'info')
            return redirect(url_for('diabetes'))


@app.route('/cancer')
def cancer():
    return render_template('cancer.html')


@app.route('/predict_cancer', methods=['POST'])
def predict_cancer():
    if request.method == 'POST':
        rad = float(request.form['Radius_mean'])
        tex = float(request.form['Texture_mean'])
        par = float(request.form['Perimeter_mean'])
        area = float(request.form['Area_mean'])
        smooth = float(request.form['Smoothness_mean'])
        compact = float(request.form['Compactness_mean'])
        con = float(request.form['Concavity_mean'])
        concave = float(request.form['concave points_mean'])
        sym = float(request.form['symmetry_mean'])
        frac = float(request.form['fractal_dimension_mean'])
        rad_se = float(request.form['radius_se'])
        tex_se = float(request.form['texture_se'])
        par_se = float(request.form['perimeter_se'])
        area_se = float(request.form['area_se'])
        smooth_se = float(request.form['smoothness_se'])
        compact_se = float(request.form['compactness_se'])
        con_se = float(request.form['concavity_se'])
        concave_se = float(request.form['concave points_se'])
        sym_se = float(request.form['symmetry_se'])
        frac_se = float(request.form['fractal_dimension_se'])
        rad_worst = float(request.form['radius_worst'])
        tex_worst = float(request.form['texture_worst'])
        par_worst = float(request.form['perimeter_worst'])
        area_worst = float(request.form['area_worst'])
        smooth_worst = float(request.form['smoothness_worst'])
        compact_worst = float(request.form['compactness_worst'])
        con_worst = float(request.form['concavity_worst'])
        concave_worst = float(request.form['concave points_worst'])
        sym_worst = float(request.form['symmetry_worst'])
        frac_worst = float(request.form['fractal_dimension_worst'])

        data = np.array([[rad, tex, par, area, smooth, compact, con, concave, sym, frac, rad_se, tex_se, par_se, area_se, smooth_se, compact_se, con_se, concave_se,
                          sym_se, frac_se, rad_worst, tex_worst, par_worst, area_worst, smooth_worst, compact_worst, con_worst, concave_worst, sym_worst, frac_worst]])
        my_prediction = rf.predict(data)

        return render_template('c_result.html', prediction=my_prediction)


def ValuePredictor(to_predict_list, size):
    loaded_model = joblib.load('models/heart_model')
    to_predict = np.array(to_predict_list).reshape(1, size)
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/heart')
def heart():
    return render_template('heart.html')


@app.route('/predict_heart', methods=['POST'])
def predict_heart():

    if request.method == 'POST':
        try:
            to_predict_list = request.form.to_dict()
            to_predict_list = list(to_predict_list.values())
            to_predict_list = list(map(float, to_predict_list))
            result = ValuePredictor(to_predict_list, 11)

            if(int(result) == 1):
                prediction = 1
            else:
                prediction = 0

            return render_template('h_result.html', prediction=prediction)
        except ValueError:
            flash(
                'Invalid input. Please fill in the form with appropriate values', 'info')
            return redirect(url_for('heart'))


# this function use to predict the output for Fetal Health from given data
def fetal_health_value_predictor(data):
    try:
        # after get the data from html form then we collect the values and
        # converts into 2D numpy array for prediction
        data = list(data.values())
        data = list(map(float, data))
        data = np.array(data).reshape(1, -1)
        # load the saved pre-trained model for new prediction
        model_path = 'Models/fetal-health-model.pkl'
        model = pickle.load(open(model_path, 'rb'))
        result = model.predict(data)
        result = int(result[0])
        status = True
        # returns the predicted output value
        return (result, status)
    except Exception as e:
        result = str(e)
        status = False
        return (result, status)


# this route for prediction of Fetal Health
@app.route('/fetal_health', methods=['GET', 'POST'])
def fetal_health_prediction():
    if request.method == 'POST':
        # geting the form data by POST method
        data = request.form.to_dict()
        # passing form data to castome predict method to get the result
        result, status = fetal_health_value_predictor(data)
        if status:
            # if prediction happens successfully status=True and then pass uotput to html page
            return render_template('fetal_health.html', result=result)
        else:
            # if any error occured during prediction then the error msg will be displayed
            return f'<h2>Error : {result}</h2>'

    # if the user send a GET request to '/fetal_health' route then we just render the html page
    # which contains a form for prediction
    return render_template('fetal_health.html', result=None)


def strokeValuePredictor(s_predict_list):
    '''function to predict the output by data we get
    from the route'''

    model = joblib.load('Models/stroke_model.pkl')
    data = np.array(s_predict_list).reshape(1, -1)
    result = model.predict(data)
    return result[0]


@app.route('/stroke')
def stroke():
    return render_template('stroke.html')


@app.route('/predict_stroke', methods=['POST'])
# this route for predicting chances of stroke
def predict_stroke():

    if request.method == 'POST':
        s_predict_list = request.form.to_dict()
        s_predict_list = list(s_predict_list.values())
        # list to keep the values of the dictionary items of request.form field
        s_predict_list = list(map(float, s_predict_list))
        result = strokeValuePredictor(s_predict_list)

        if(int(result) == 1):
            prediction = 1
        else:
            prediction = 0
        return render_template('st_result.html', prediction=prediction)


def liverprediction(final_features):
    # Loading the pickle file
    model_path = 'Models/liver-disease_model.pkl'
    model = pickle.load(open(model_path, 'rb'))
    result = model.predict(final_features)
    return result[0]


@app.route('/liver')
def liver():
    return render_template('liver.html')


@app.route('/predict_liver', methods=['POST'])
# predicting
def predict_liver_disease():

    if request.method == 'POST':
        int_features = [float(x) for x in request.form.values()]
        final_features = [np.array(int_features)]
        output = liverprediction(final_features)
        pred = int(output)

        return render_template('liver_result.html', prediction=pred)


@app.route("/malaria", methods=['GET', 'POST'])
def malaria():
    return render_template('malaria.html')


@app.route("/malariapredict", methods=['POST', 'GET'])
def malariapredict():
    if request.method == 'POST':
        #try:
            if 'image' in request.files:
                file1 = request.files['image']
                
           
                #imageFileName = secure_filename(file1.filename)
                #print(imageFileName)
                #file1.save(os.path.join(app.config['UPLOAD_FOLDER'],imageFileName))
                #img = Image.open(file1)

                cov_predict = cv2.imread("static/uploads/imagecovid.jpg")
                imgs = cv2.cvtColor(cov_predict,cv2.COLOR_BGR2RGB)
                resized = cv2.resize(imgs,(224,224), interpolation = cv2.INTER_AREA)
                covid = np.array(resized) / 255.0
                predicting = covid.reshape((1,224,224,3))


                model_path = "Models/xray_covid.h5"
                model = tf.keras.models.load_model(model_path)
                predictMod = model.predict(predicting,batch_size=1)
                pred = np.argmax(predictMod, axis=1)
                #pred = 1
                
        #except:
            #message = "Please upload an Image"
            #return render_template('malaria.html', message=message)
    return render_template('malaria_predict.html', pred=pred)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
