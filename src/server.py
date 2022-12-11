import datetime
import logging
import threading
import time
import numpy as np

from flask import request, Flask, jsonify

from deltadex_calibration import calibrate_sabr
from sabr import SABR
from sabr_calibration import SABRCalibrator
from deribit_parser import GetOptionMeta




from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

sabrs = {}
underlying_price = None


# def get_sabr(sabr_params, r=0.0):
#     sabr_calib = SABRCalibrator(interest_rate=r)
#     sabr_calib.sabr_params = sabr_params
#     sabr_calib.sabr = SABR(interest_rate=r, sabr_params=sabr_params)
#     sabr = sabr_calib.get_model()
    
#     import json

    
#     return sabr


def thread_function(name):
    logging.info("Thread %s: starting", name)



    
    global sabrs, underlying_price
    
    format_str = '%d/%b/%Y' # The format
    
    while True:
        print('hi')

        try:
            OptionMeta = GetOptionMeta()['Expiry']
            expiries = list(map(lambda expiry: (expiry[:-5] + "/" + expiry[-5:-2] + "/" + expiry[-2:]), OptionMeta))
            print(expiries)
            print('---')
            for expiry in expiries:
                print(expiry)
                sabr, underlying_price = calibrate_sabr(SELECTED_EXPIRY = expiry)
                sabrs[expiry] = sabr
                time.sleep(1)
            # print(sabr.sabr_params)
            # print(sabr.sabr_params, underlying_price)
            time.sleep(10)
        except Exception as e:
            print('exception')

        
        
    # logging.info("Thread %s: finishing", name)






@app.route('/optionsdata/get-option-price')
@cross_origin()
def get_option_price():
    model = request.args.get('model', default = 'sabr', type = str)
    strike = request.args.get('strike', default = 1, type = int)
    expiry = request.args.get('expiry', default = '29SEP23', type = str)
    isCall = request.args.get('iscall', default = 1, type = int)
    OptionMeta = GetOptionMeta()['Expiry']
    
    
    print(model, strike, expiry, isCall)

    if expiry not in OptionMeta:
        return jsonify({'data':'wrong expiry'})
    
    if (isCall) != 0 and (isCall) != 1:
        return jsonify({'data':'wrong option type (isCall must be 0 or 1)'})

    
    upd_expiry = expiry[:-5] + "/" + expiry[-5:-2] + "/" + expiry[-2:]
    
    format_str = '%d/%b/%Y' # The format
    SELECTED_EXPIRY = datetime.datetime.strptime(expiry[:-5] + "/" + expiry[-5:-2] + "/20" + expiry[-2:], format_str)
    
    days = (SELECTED_EXPIRY - datetime.datetime.strptime((datetime.date.today().isoformat()), "%Y-%m-%d")).days
        
    # filter = request.args.get('filter', default = '*', type = str)
    # print(type(model), type(underlying_price), type(strike), type(expiry))
    # price, iv = get_IV(strike, isCall=True, SELECTED_EXPIRY=SELECTED_EXPIRY)
    
    # sabr = calibrate_sabr(SELECTED_EXPIRY=SELECTED_EXPIRY)
    
    # print(sabrs)
    
    global sabrs, underlying_price
    
    price, iv = (sabrs[upd_expiry](np.array([strike]), np.array([underlying_price]), np.array([days / 365.25]), isCall))
    
    print(sabrs)

    return jsonify({'data': {'underlying_price': underlying_price, 'expiry': expiry, 'strike': strike, 'price':price[0], 'implied_volatility':iv[0], 'isCall': isCall}})

    



@app.route('/optionsdata/expirations')
@cross_origin()
def expirations():
    format_str = '%d/%b/%Y' # The format

    OptionMeta = sorted(GetOptionMeta()['Expiry'], key=lambda expiry: datetime.datetime.strptime(expiry[:-5] + "/" + expiry[-5:-2] + "/20" + expiry[-2:], format_str))
    
    return jsonify(OptionMeta)



threading.Thread(target=lambda: app.run(host='0.0.0.0', use_reloader=False)).start()

x = threading.Thread(target=thread_function, args=(1,))
x.start()



