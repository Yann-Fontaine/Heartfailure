import pandas as pd
import numpy as np
from flask import Flask, request
import flasgger
from flasgger import Swagger
import pickle as pkl
from db import createDb, addOneToDb, addManyToDb

app = Flask(__name__)
Swagger(app)

with open('model.pkl', 'rb') as f:
    model = pkl.load(f)

@app.route('/')
def home():
    return 'Welcome to the Thunderdome !'

@app.route('/predict', methods=['Get'])
def predict_case():

    """ Let's first give some informations to the machine
    ---
    parameters:
      - name: age
        in: query
        type: number
        required: true
      - name: anaemia
        in: query
        type: number
        required: true
      - name: creatinine_phosphokinase
        in: query
        type: number
        required: true
      - name: diabetes
        in: query
        type: number
        required: true
      - name: ejection_fraction
        in: query
        type: number
        required: true
      - name: high_blood_pressure
        in: query
        type: number
        required: true
      - name: platelets
        in: query
        type: number
        required: true
      - name: serum_creatinine
        in: query
        type: number
        required: true
      - name: serum_sodium
        in: query
        type: number
        required: true
      - name: sex
        in: query
        type: number
        required: true
      - name: smoking
        in: query
        type: number
        required: true
      - name: time
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output value

    """

    age = request.args.get('age')
    anaemia = request.args.get('anaemia')
    creatinine_phosphokinase = request.args.get('creatinine_phosphokinase')
    diabetes = request.args.get('diabetes')
    ejection_fraction = request.args.get('ejection_fraction')
    high_blood_pressure = request.args.get('high_blood_pressure')
    platelets = request.args.get('platelets')
    serum_creatinine = request.args.get('serum_creatinine')
    serum_sodium = request.args.get('serum_sodium')
    sex = request.args.get('sex')
    smoking = request.args.get('smoking')
    time = request.args.get('time')
    params = np.array([[age, anaemia, creatinine_phosphokinase, diabetes, ejection_fraction, high_blood_pressure, platelets, serum_creatinine, serum_sodium, sex, smoking, time]])
    diagnostic = model.predict_proba(params)
    createDb()
    addOneToDb(params, diagnostic)
    return f'The probabilities of you being at risk are {diagnostic[0][1]}'

@app.route('/predict_csv', methods=['POST'])
def predict_bunch():

    """ Let's give to the machine a whole bunch of informations
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true

    responses:
        200:
            description: The output values

    """

    df = pd.read_csv(request.files.get('file'))
    params = df.to_numpy()
    diagnostic = model.predict_proba(df)
    createDb()
    addManyToDb(params, diagnostic)
    return f'The probabilities of being at risk for each subject are {diagnostic[:, 1]}'


if __name__ == '__main__':
    app.run()