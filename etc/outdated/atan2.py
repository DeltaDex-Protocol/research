## @dev more precise way of calculating atan2

# https://dspguru.com/dsp/tricks/fixed-point-atan2-with-self-normalization/
def arctan2(y, x):
    coeff_1 = math.pi/4
    coeff_2 = 3*coeff_1
    abs_y = abs(y)+1e-10
    
    if x>=0:
        r = (x - abs_y) / (x + abs_y)
        # theta1
        angle =0.1963 * r**3 - 0.9817 * r + coeff_1
    else:
        r = (x + abs_y) / (abs_y - x)
        # theta2
        angle = 0.1963 * r**3 - 0.9817 * r + coeff_2
   
    if y < 0:
        return(-angle)
    else:
        return(angle)


PI = 3.1415926535897933e+18

def EffienctArctan2(y, x):
    coeff_1 = PI/4
    coeff_2 = 3*coeff_1
    abs_y = abs(y)+1e8
    
    if x>=0:
        r = (x - abs_y) * 1e18 / (x + abs_y)
        angle = (coeff_1 * 1e18 - coeff_1 * r) / 1e18
    else:
        r = (x + abs_y) * 1e18 / (abs_y - x)
        angle = (coeff_2 * 1e18 - coeff_1 * r) / 1e18
   
    if y < 0:
        return(-angle)
    else:
        return(angle)
    
EffienctArctan2(2e18,2e18)