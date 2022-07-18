option = {"T": 0.5, "x0": 250, "K": 1000, "r": 0, "sigma": 0.7}

def BS_root_put(x0, S, K, T, r, sigma):
    TV0 = 2 * x0
    z1 = -(np.log(S/K) + (r - 0.5*sigma**2)*T)/np.sqrt(T)/sigma

    
    first_part = (np.exp(-r*T) * TV0) * N(z1)
    _r = r/2
    _sigma = sigma / 2
    z2 = z1 - _sigma * np.sqrt(T)
    second_part = (np.exp(-r*T) * TV0*np.sqrt(S/K)) * (np.exp(-0.5 * _sigma**2 * T)*np.exp(_r*T)) * N(z2)
    
    return first_part - second_part
    

def new_way_BS_delta_root_put(x0, S, K, T, r, sigma):
    z1 = -(np.log(S/K) + (r - 0.5*sigma**2)*T)/np.sqrt(T)/sigma
    _r = r/2
    _sigma = sigma / 2
    z2 = z1 - _sigma * np.sqrt(T)
    return -(np.exp(-r*T) * x0 / np.sqrt(K*S)) * (np.exp(-0.5 * _sigma**2 * T)*np.exp(_r*T)) * N(z2)


# BS root call

def BS_root_call(x0, S, K, T, r, sigma):
    TV0 = 2 * x0
    z1 = -(np.log(S/K) + (r - 0.5*sigma**2)*T)/np.sqrt(T)/sigma

    
    first_part = (np.exp(-r*T) * TV0) * N(-z1)
    _r = r/2
    _sigma = sigma / 2
    z2 = z1 - _sigma * np.sqrt(T)
    second_part = (np.exp(-r*T) * TV0*np.sqrt(S/K)) * (np.exp(-0.5 * _sigma**2 * T)*np.exp(_r*T)) * N(-z2)
    
    return -first_part + second_part
    

    

def delta_BS_root_call(x0, S, K, T, r, sigma):
    z1 = -(np.log(S/K) + (r - 0.5*sigma**2)*T)/np.sqrt(T)/sigma
    _r = r/2
    _sigma = sigma / 2
    z2 = z1 - _sigma * np.sqrt(T)
    
    return (np.exp(-r*T) * x0 / np.sqrt(K*S)) * (np.exp(-0.5 * _sigma**2 * T)*np.exp(_r*T)) * N(-z2)
    
    
    
    
    
    
    
    
    
    