
import numpy as np
from filters import iir2_filter

class IIRFilter:
    
    def __init__(self, sos):
        """

        Initialises sos coefficients and chain of instances of 2nd order iir filter.
        Parameters
        ----------
        sos : array of coefficients from the butter command
    
        """
        self.sos = sos # array of sos coefficients
        self.num = len(sos)
        
        # chain of instances of 2nd order iir filter
        self.filters = [iir2_filter.IIR2Filter(*self.sos[i]) for i in range(self.num)]
       
        
    def dofilter(self, value):
        """

        Performs filtering through a chain of 2nd order iir filters.
        Parameters
        ----------
        value : input sample value
        
        Returns
        -------
        y : filtered sample value
        
        """        
        x = value
        y=0      
        for i in range(self.num):
            y = self.filters[i].dofilter(x)
            x = y          
        return y
    
def unittest(coefficients):
    """

        A unit test function for the iir filter.
        Parameters
        ----------
        coefficients : pre-defined coefficient array
        
        Returns
        -------
        PASS or FAIL
        
        """ 
    iir = IIRFilter(coefficients)

    # define a unit impulse as an input
    input_array = np.array([1,0,0,0,0])
    
    result = np.zeros(len(input_array))
    
    # filter ECG, sample-by-sample
    for i in range(len(input_array)):
        result[i] = iir.dofilter(input_array[i])

    # test the condition:
    # if result equals the expected value calculated manually
    assert np.all(result == np.array([1,0,2,0,1])), 'FAIL' 
    print('PASS')
    print('Result: ')
    print(result)
    
if __name__=='__main__':
    coeff = np.array([[1,0,1,1,0,0], [1,0,1,1,0,0]]) # filter coefficients
    unittest(coeff)