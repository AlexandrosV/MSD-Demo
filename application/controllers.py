import os
import time
import math
import requests
import datetime
from flask import jsonify
from dateutil.relativedelta import relativedelta 

def get_price():
    COINGECKO_BASE_URL = os.environ.get('COINGECKO_BASE_URL')
    params = {  
        'ids': 'bitcoin',
        'vs_currencies': 'EUR,CZK'
        }
    response = requests.get(f"{COINGECKO_BASE_URL}/price", params = params)

    expiration_date = datetime.datetime.now() + relativedelta(years=1)

    coin_data = {
        'eur': response.json()['bitcoin']['eur'],
        'czk': response.json()['bitcoin']['czk'],
        'date': round(time.time() * 1000),
        'pk': datetime.datetime.now().strftime("%Y-%m-%d"),
        'expirationDate': math.trunc(expiration_date.timestamp()),
        'month': datetime.datetime.now().strftime("%Y-%m"),
    }
    return coin_data