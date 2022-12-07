from flask import request, Flask, jsonify

import datetime
from deltadex_calibration import get_IV
from deribit_parser import GetOptionMeta

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'






@app.route('/optionsdata/get-option-price')
@cross_origin()
def get_option_price():
    model = request.args.get('model', default = 'sabr', type = str)
    strike = request.args.get('strike', default = 1, type = int)
    expiry = request.args.get('expiry', default = '29SEP23', type = str)
    OptionMeta = GetOptionMeta()['Expiry']
    
    if expiry not in OptionMeta:
        return jsonify({'data':'wrong expiry'})
    
    
    format_str = '%d/%b/%Y' # The format
    SELECTED_EXPIRY = datetime.datetime.strptime(expiry[:-5] + "/" + expiry[-5:-2] + "/20" + expiry[-2:], format_str)
        
    # filter = request.args.get('filter', default = '*', type = str)
    # print(type(model), type(underlying_price), type(strike), type(expiry))
    price, iv = get_IV(strike, isCall=True, SELECTED_EXPIRY=SELECTED_EXPIRY)
    
    return jsonify({'data': {'expiry': expiry, 'strike': strike, 'price':price[0], 'implied_volatility':iv[0]}})



@app.route('/optionsdata/expirations')
@cross_origin()
def expirations():
    format_str = '%d/%b/%Y' # The format

    OptionMeta = sorted(GetOptionMeta()['Expiry'], key=lambda expiry: datetime.datetime.strptime(expiry[:-5] + "/" + expiry[-5:-2] + "/20" + expiry[-2:], format_str))
    
    return jsonify(OptionMeta)

    
app.run(debug=False)


