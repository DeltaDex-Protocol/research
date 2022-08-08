# BS root Call
def BS_root_call(x0, S, K, T, r, sigma):
    TV0 = 2 * x0
    z1 = (((-1 * (np.log(S/K) + (r - 0.5*sigma**2) * T)) / np.sqrt(T)) / sigma)
    first_part = (np.exp(-r*T) * TV0) * N(-z1)
    
    r = r/2
    sigma = sigma / 2
    z2 = z1 - sigma * np.sqrt(T)
    second_part = (np.exp(-r*T) * TV0 * np.sqrt(S/K)) * (np.exp(-0.5 * sigma**2 * T) * np.exp(r*T)) * N(-z2)

    C = (-1 * first_part) + second_part
    
    return C
    

def delta_BS_root_call(x0, S, K, T, r, sigma):
    z1 = (((-1 * (np.log(S/K) + (r - 0.5*sigma**2) * T)) / np.sqrt(T)) / sigma)
    r = r/2
    sigma = sigma / 2
    z2 = z1 - sigma * np.sqrt(T)

    delta = (np.exp(-r*T) * x0 / np.sqrt(K*S)) * (np.exp(-0.5 * sigma**2 * T)*np.exp(r*T)) * N(-z2)

    return delta


# BS root Put
def BS_root_put(x0, S, K, T, r, sigma):
    TV0 = 2 * x0
    z1 = (-1 * (np.log(S/K))) + (((r - 0.5*sigma**2) * T) / np.sqrt(T)) / sigma
    first_part = (np.exp(-r*T) * TV0) * N(z1)

    r = r/2
    sigma = sigma / 2
    z2 = z1 - sigma * np.sqrt(T)
    second_part = (np.exp(-r*T) * TV0 * np.sqrt(S/K)) * (np.exp(-0.5 * sigma**2 * T) * np.exp(r*T)) * N(z2)

    C = first_part - second_part

    return C


def delta_BS_root_put(x0, S, K, T, r, sigma):
    z1 = (-1 * (np.log(S/K))) + (((r - 0.5*sigma**2) * T) / np.sqrt(T)) / sigma
    r = r/2
    sigma = sigma / 2
    z2 = z1 - sigma * np.sqrt(T)

    delta = (-1 * (np.exp(-r*T) * x0 / np.sqrt(K*S))) * (np.exp(-0.5 * sigma**2 * T) * np.exp(r*T)) * N(z2)

    return delta


def aux(arr):
    print('input (solidity):', end=" ")
    print('[', end="")
    for i in range(len(arr)):
        if i != len(arr)-1:
            print(" %.0f" % arr[i], end=",")
        else:
            print(" %.0f" % arr[i], end='')
    print(']')
    
if __name__ == "__main__":
    import numpy as np
    from scipy.stats import norm
    N = norm.cdf
    option = {"x0": 250, "S": 1100, "K": 1000, "T": 0.5, "r": 0, "sigma": 0.7}

    arr = list(map(lambda x: (x*10**18) , [1100, 1000, 0.5, 0, 0.7]))
    aux(arr)

    print(BS_root_call(option["x0"], option["S"], option["K"], option["T"], option["r"], option["sigma"]))
    print(delta_BS_root_call(option["x0"], option["S"], option["K"], option["T"], option["r"], option["sigma"]))
    