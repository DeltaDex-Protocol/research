from flask import request, Flask

from deltadex_calibration import get_IV

app = Flask(__name__)

@app.route('/my-route')
def my_route():
    model = request.args.get('model', default = 'sabr', type = str)
    underlying_price = request.args.get('underlying_price', default = 1, type = int)
    strike = request.args.get('strike', default = 1, type = int)
    expiry = request.args.get('expiry', default = 1, type = int)
    # filter = request.args.get('filter', default = '*', type = str)
    print(model, underlying_price, strike, expiry)
    print(type(model), type(underlying_price), type(strike), type(expiry))
    price, iv = get_IV(1270, 1325, 1)
    
    return f"{price, iv}"
    
app.run()


