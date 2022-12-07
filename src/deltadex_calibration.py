import pandas as pd
import numpy as np
import requests
import scipy.stats as si
import datetime

from sabr import SABR
from sabr_calibration import SABRCalibrator

from deribit_parser import GetOptionBook, GetOptionMeta



def tuning_dataset(options_data, selected_expiry):
    DAYS_IN_YEAR = 365.25
    # options_data['expiry'] = options_data['underlying_index'].apply(lambda x: x.split('-')[-1])
    # options_data['strike'] = options_data['instrument_name'].apply(lambda x: x.split('-')[-2])
    # options_data['type'] = options_data['instrument_name'].apply(lambda x: 'call' if x.split('-')[-1] == 'C' else 'put')
    
    options_data_on_day = options_data[options_data['expiry'] == selected_expiry].reset_index(drop=True)
    
    # return options_data_on_day

    options_data_on_day.replace(to_replace=[None], value=np.nan, inplace=True)
    options_data_on_day['strike'] = options_data_on_day['strike'].apply(lambda x: float(x))

    options_data_on_day['bid_IV'] = options_data_on_day['bid_IV'].apply(lambda x: float(x))
    options_data_on_day['ask_IV'] = options_data_on_day['ask_IV'].apply(lambda x: float(x))

    options_data_on_day = options_data_on_day.drop(options_data_on_day[abs(options_data_on_day['bid_IV']) > 10].index).dropna().reset_index(drop=True)
    options_data_on_day = options_data_on_day.drop(options_data_on_day[abs(options_data_on_day['ask_IV']) > 10].index).dropna().reset_index(drop=True)
    
    puts = options_data_on_day[options_data_on_day['type']=='put'].dropna().reset_index(drop=True)
    calls = options_data_on_day[options_data_on_day['type']=='call'].dropna().reset_index(drop=True)
    puts = puts.drop(puts[abs(puts['bid_IV']) > 10].index).reset_index(drop=True)
    puts = puts.drop(puts[abs(puts['ask_IV']) > 10].index).reset_index(drop=True)

    calls = calls.drop(calls[abs(calls['bid_IV']) > 10].index).reset_index(drop=True)

    calls = calls.drop(calls[abs(calls['ask_IV']) > 10].index).reset_index(drop=True)
    
    return calls, puts



def get_data_from_df(day, df : pd.DataFrame):
    """
        This function extracts out the money data from given dataframe
        
        Args:
            df(pd.DataFrame): dataframe of market data
            
        Returns:
            c(np.ndarray): option prices 
            iv(np.ndarray): implied vols
            K(np.ndarray): strikes
            F(np.ndarray): underlying prices
            T(np.ndarray): expiration times
            weights(np.ndarray): weights
    """
    
#     #choose only out of the money options
#     ind = (df.payoff == 0.0) & (~np.isnan(df.mid_price).values)
#     df_ = df[ind].copy().reset_index(drop=True)

    df_ = df.copy().reset_index(drop=True)
    
    #future price
    F = df_.underlying_price.values
    #strike
    K = df_.strike.values
    #time to exp
    T = np.arange(len(K), dtype='float64')
    T.fill(day / 365.25)
    
    # iv = 0.5 * ( df_['ask_IV'].values + df_['bid_IV'].values ) / 100.0
    iv = 0.5 * ( df_['ask_IV'].values + df_['bid_IV'].values )
    
    c = df_.mid_price.values * F
    #weigths are propotional to open interest
    interest = df_.open_interest.values
    #weights
    weights = interest
    weights = weights / np.sum(weights)
    
    return c, iv, K, F, T, weights


def get_data_from_dfs(day, put:pd.DataFrame, call:pd.DataFrame):
    """
        This function extracts data from two dataframes for calls and puts and concatenates it
        
        Args:
            put(pd.DataFrame): dataframe with market data
            call(pd.DataFrame): dataframe with market data      
        
        Returns:
            c(np.ndarray): option prices 
            iv(np.ndarray): implied vols
            K(np.ndarray): strikes
            F(np.ndarray): underlying prices
            T(np.ndarray): expiration times
            weights(np.ndarray): weights
            typ(np.ndarray): list of types of an option, if True -- call option, else Put option
    """
    data_call = np.stack(get_data_from_df(day, call))
    data_put = np.stack(get_data_from_df(day, put))
    
    data = np.concatenate( (data_call, data_put), axis=-1)
    
    c, iv, K, F, T, weights = data
    
    typ = np.asarray([True] * data_call.shape[1] + [False] * data_put.shape[1])
    
    return c, iv, K, F, T, weights, typ




def calibrate_sabr(SELECTED_EXPIRY = '29/SEP/23'):
    OptionMeta = GetOptionMeta()
    OptionBook = GetOptionBook()
    
    EXPIRIES = OptionMeta['Expiry'][::-1]
    
    
    col_names = ['full_name', 'type', 'open_interest', 'expiry', 'strike', 'bid_price', 'bid_IV', 'ask_price', 'ask_IV', 'mid_price', 'mid_IV', 'underlying_price']

    options_data = pd.DataFrame([], columns=col_names)

    for thisExpiry in (EXPIRIES):
        fullNames = ["ETH-"+thisExpiry+"-"+str(int(i)) for i in sorted(OptionMeta[thisExpiry])]
        strikes = [str(int(i)) for i in sorted(OptionMeta[thisExpiry])]

        for i in (range(len(fullNames))):
    #         print(fullNames[i])
            thisPut = [item for item in OptionBook if item.get('instrument_name')==fullNames[i]+"-P"][0]
    #         print(thisPut)
            thisCall = [item for item in OptionBook if item.get('instrument_name')==fullNames[i]+"-C"][0]
    #         print([fullNames[i], thisExpiry, strikes[i], thisPut['bid_IV'], thisCall['bid_IV'], thisPut['ask_IV'], thisCall['ask_IV']])
            row1 = pd.DataFrame([[fullNames[i], 'put', thisPut['open_interest'], thisExpiry, strikes[i], 
                                  thisPut['bid_price'], thisPut['bid_IV'], thisPut['ask_price'], thisPut['ask_IV'], 
                                  thisPut['mid_price'], thisPut['mid_IV'], thisPut['underlying_price']]], columns=col_names)
            row2 = pd.DataFrame([[fullNames[i], 'call', thisCall['open_interest'], thisExpiry, strikes[i], 
                                  thisCall['bid_price'], thisCall['bid_IV'], thisCall['ask_price'], thisCall['ask_IV'], 
                                  thisCall['mid_price'], thisCall['mid_IV'], thisCall['underlying_price']]], columns=col_names)

            options_data = pd.concat([options_data, row1], ignore_index=True)
            options_data = pd.concat([options_data, row2], ignore_index=True)

    # date_str = '29/DEC/2017' # The date - 29 Dec 2017
    format_str = '%d/%b/%Y' # The format
    options_data['expiry'] = options_data['expiry'].apply(lambda x: datetime.datetime.strptime(x[:-5] + "/" + x[-5:-2] + "/20" + x[-2:], format_str))

    
    calls, puts = tuning_dataset(options_data=options_data, selected_expiry=SELECTED_EXPIRY)
    
    
    day = (calls['expiry'][0] - datetime.datetime.strptime((datetime.date.today().isoformat()), "%Y-%m-%d")).days
    
    
    def calib():
        #extract data corresponding to day_before_exp = 120
        X, iv, K, F, T, weights, typ = get_data_from_dfs(day, puts, calls)
        weights = np.ones_like(X)
        # weights = 1.0 / np.sqrt(1.0 + (K - F) ** 2 )

        weights = weights / np.sum(weights)

        #create sabr calibrator object
        sabr_calib = SABRCalibrator(interest_rate=0.0)
        #call fit function
        result = sabr_calib.fit_iv(iv, K, F, T, Niter=500, weights=weights, fit_beta=True)
        #save fitted model
        sabr = sabr_calib.get_model()
        
        return result, sabr
    
    result, sabr = calib()
    
    
    names = ["alpha ", "v ", "beta  ", "rho"]
    
    print("optimized parameters:", *zip(names, (sabr.sabr_params).round(5)), sep='\n' )
    
    
    

    # def get_calibrated_IV(K, T, isCall=True):
    #     S = calls['underlying_price'][0]
    #     return sabr(K, S, T, isCall)

    return sabr, calls['underlying_price'][0]
    
    # return get_calibrated_IV(np.array([K]), np.array([day / 365.25]), isCall = True)



# def get_IV_by_sabr_params(K, T, isCall=True):
    
#     sabr_calib = SABRCalibrator(interest_rate=0.0)
#     sabr = sabr_calib.get_model()
#     sabr.sabr_params = ...
    
    
    
    
