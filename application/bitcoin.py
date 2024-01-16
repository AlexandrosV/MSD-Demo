import threading
import time
import btc
import os
from flask import Flask, jsonify
from datetime import datetime
from controllers import get_price
from dynamo import put_item, get_day_data, get_month_data

# Initializing the core application
def init_app():
    app = Flask(__name__)
    # This should be the "propper" way to handle app configurations
    # app.config.from_envvar('APPLICATION_SETTINGS') 
    COINGECKO_BASE_URL = os.environ.get('COINGECKO_BASE_URL')
    FETCH_FREQUENCY = int(os.environ.get('FETCH_FREQUENCY'))
    
    with app.app_context():
        # I would have use am AWS lambda function for this. 
        # Nevertheless, I'm following the instructions of the task.
        def feed_price():
            while True:
                data = get_price()
                put_item(data)
                time.sleep(FETCH_FREQUENCY)
        thread = threading.Thread(target=feed_price)
        thread.start()
     
    
    @app.route("/")
    # Root URL & Welcome message
    def home():
        return f"MSD - Alejandro V. - Fecth frequency: {FETCH_FREQUENCY} seconds - Price provider: {COINGECKO_BASE_URL}"


    @app.route('/bitcoinday/', methods=['GET'])
    @app.route('/bitcoinday/<date>', methods=['GET'])
    def calculate_price_day(date=None):
        # here validate date - todo
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')
        data = get_day_data(date)
        total_eur, total_czk = btc.average_price(data)        
        coin_data = {
            'eur': total_eur,
            'czk': total_czk,
            'day': date,
            'request_date': time.ctime()
        }
        return jsonify({'data': coin_data}), 200 if coin_data else 204
    
    
    @app.route('/bitcoinmonth/', methods=['GET'])
    @app.route('/bitcoinmonth/<date>', methods=['GET'])
    def calculate_price_month(date=None):
        # here validate date - todo
        if not date:
            date = datetime.today().strftime('%Y-%m')
        data = get_month_data(date)
        total_eur, total_czk = btc.average_price(data)        
        coin_data = {
            'eur': total_eur,
            'czk': total_czk,
            'day': date,
            'request_date': time.ctime()
        }
        return jsonify({'data': coin_data}), 200 if coin_data else 204
    
    return app  

app = init_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
