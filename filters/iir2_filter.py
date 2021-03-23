
class IIR2Filter:
    
    def __init__(self, b0, b1, b2, _, a1, a2): 
        """

        Initialises 2nd order iir filter coefficients, delay buffers and accumulators.
        Parameters
        ----------
        b0, b1, b2 : fir coefficients
        a1, a2 : iir coefficients
    
        """
        # 2nd order filter coefficients
        self.a1 = a1
        self.a2 = a2
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        
        # delay buffers
        self.buff1 = 0
        self.buff2 = 0
        
        # accumulators
        self.in_acc = 0
        self.out_acc = 0
     
        
    def dofilter(self, value):    
        """

        Performs filtering through a single 2nd order iir filter.
        Parameters
        ----------
        value : input sample value
        
        Returns
        -------
        out_acc : filtered sample value
        
        """
        self.in_acc = value

        self.in_acc = self.in_acc - (self.a1 * self.buff1) - (self.a2 * self.buff2)
        
        self.out_acc = self.in_acc * self.b0
        self.out_acc = self.out_acc + (self.b1 * self.buff1) + (self.b2 * self.buff2)
        
        self.buff2 = self.buff1
        self.buff1 = self.in_acc
        
        return self.out_acc
    