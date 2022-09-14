from urllib import response
from flask import Flask, jsonify, request, Markup
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS, cross_origin


app = Flask(__name__)

cors = CORS(app, resources={
            r"/crop-predict": {"origins": "*"},
            r"/fertilizer-predict" : {"origins": "*"}})

# Importing the machine learning model

crop_recommendation_model_path = 'models/recommendationModel.pkl'

crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():


    if request.method == 'POST':
        N = int(request.json['nitrogen'])
        P = int(request.json['phosphorous'])
        K = int(request.json['pottasium'])
        ph = float(request.json['ph'])
        rainfall = float(request.json['rainfall'])
        temperature = float(request.json['temperature'])
        humidity = float(request.json['humidity'])

        print("                  ")
        print(type(request.json))
        print("                 ")

        response = {
            'message': "Succesfully parsed",
            'status_code': 200
        }

        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        my_prediction = crop_recommendation_model.predict(data)
        final_prediction = my_prediction[0]

        response['result'] = final_prediction
        response = jsonify(response)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

        


@ app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():

    req = request.json

    if request.method == 'POST':
        crop_name = str(req['cropname'])
        N = int(req['nitrogen'])
        P = int(req['phosphorous'])
        K = int(req['pottasium'])

        df = pd.read_csv('fertilizer.csv')

        response = {
            'message': 'Data successfully parsed',
            'status_code': 200
        }

        nr = df[df['Crop'] == crop_name]['N'].iloc[0]
        pr = df[df['Crop'] == crop_name]['P'].iloc[0]
        kr = df[df['Crop'] == crop_name]['K'].iloc[0]

        n = nr - N
        p = pr - P
        k = kr - K
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        if max_value == "N":
            if n < 0:
                key = 'NHigh'
            else:
                key = "Nlow"
        elif max_value == "P":
            if p < 0:
                key = 'PHigh'
            else:
                key = "Plow"
        else:
            if k < 0:
                key = 'KHigh'
            else:
                key = "Klow"

        response['result'] = key
        response = jsonify(response)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


if __name__ == '__main__':
    app.run(debug=True)