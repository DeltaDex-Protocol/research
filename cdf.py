
"""
   int a1 = 254829592000000000;
    int a2 = -284496736000000000;
    int a3 = 1421413741000000000;
    int a4 = -1453152027000000000;
    int a5 = 1061405429000000000;
    int p = 327591100000000000;

    int SQRT_2 = 1414213562373095100;


    function pdf(int x) internal pure returns (int y) {
        y = ((-1 * x.pow(2)) / 2).exp() / 2506628274631000200;
        return y;
    }
    

    function cdf(int x) internal view returns (int y) {
        y = (erf(x * 1e18 / SQRT_2) + 1e18) / 2;
        return y;
    }


    function erf(int x) internal view returns (int y) {

        // save the sign
        int sign = 1;
        if (x < 0) {
            sign = -1;
        }

        x = x.abs();

        int t = 1e36/ (1e18 + (p*x) / 1e18);
        y = 1e18 - ((((((a5*t/1e18 + a4)*t/1e18) + a3)*t/1e18 + a2)*t/1e18 + a1)*t/1e18) * ((-x*x)/1e18).exp() / 1e18;

        return sign*y; 
    }


"""

a1 = 254829592000000000
a2 = -284496736000000000
a3 = 1421413741000000000
a4 = -1453152027000000000
a5 = 1061405429000000000
p = 327591100000000000


def pdf(x): 
    y = 

