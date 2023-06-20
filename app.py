from flask import Flask,jsonify,request
import json
from bs4 import BeautifulSoup
from flask_cors import CORS
from time import sleep
import requests
import datetime
import numpy as np 
import pandas as pd 
from statsmodels.tsa.arima.model import ARIMA
app = Flask(__name__)
CORS(app)
from markupsafe import escape
@app.route("/stock/<stock>/<int:a>")
def helper_func(stock,a): 
    ss=requests.get(f"https://scrap-29ek.onrender.com/stock/{stock}/{1825}")
    ss=ss.json()
    datetime=[]
    open=[]
    high=[]
    low=[]
    close=[]
    volume=[]
    for i in ss['data']:
        list=[]
        for j in i : 
            list.append(j)
        datetime.append(list[0])
        open.append(list[2])
        high.append(list[3])
        low.append(list[4])
        close.append(list[5])
        volume.append(list[6])
    dic={'datetime':datetime,'Open':open,'High':high,'Low':low,'Close':close,'Volume':volume}
    data=pd.DataFrame(dic)
    data['datetime'] = pd.to_datetime(data['datetime'])
    data = data.set_index('datetime')
    X = data['Close'].values
    history = [x for x in X]
    predictions = []
    # walk-forward validation
    import statsmodels.api as sm
    model = ARIMA(history, order=((6,2,8)))
    model_fit = model.fit()
    output = model_fit.forecast(steps=a)
    res=[]
    for i in output:
         res.append(i)
    return res
@app.route("/")
def home():
    data = {'page':'home page','message':'ok'}
    return jsonify(data)
###########################
app.run(debug=False,host='0.0.0.0')
