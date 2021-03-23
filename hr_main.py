
# Place your fingertip over the camera and keep it as steady as possible.
# There will be a slight delay due to filtering.



import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
import cv2
import realtime_plot
from sensor import webcamChannel_G
from filters import iir_filter

class DetectHR:
    
    def __init__(self, fs):
        
        # initialize real-time plot windows
        self.fig, self.ax = plt.subplots(3,1, figsize=(6,10))
        self.rplt1 = realtime_plot.RealtimePlotWindow("Channel G", self.fig, self.ax[0])
        self.rplt2 = realtime_plot.RealtimePlotWindow("Filtered Channel G", self.fig, self.ax[1])
        self.rplt3 = realtime_plot.RealtimePlotWindow("", self.fig, self.ax[2], txt=True)
        
        # k1 and k2 are the cutoff values 50bpm and 250bpm converted to samples per sec
        self.k1 = int(np.round(50/60))
        self.k2 = int(np.round(250/60))
        self.fs = fs # sampling rate
    
        self.sos = self.createBandpassFilter(self.fs, self.k1, self.k2)
        self.iir = iir_filter.IIRFilter(self.sos)

        self.threshold_low = 0.05 # low threshold value for detecting peaks
        self.threshold_high = 2 # high threshold value for detecting peaks
        self.diff_min = 18 # minimum number of samples between two peaks
        self.diff_max = 25 # maximum number of samples between two peaks
        self.curr_peak = 0 # points to the current peak
        self.prev_peak = 0 # points to the previous peak
        self.rate = np.zeros(10) # a ring buffer to store momentary heartrate
        self.rate_idx = 0
        self.buff = np.zeros(100) # a ring buffer to store previous filtered values for detection
        self.buff_idx = 0
        self.flag = 0 # variable to denote that a possible peak is detected


    def createBandpassFilter(self, fs, lowcut, highcut):
        """

        Creates bandpass filter coefficients.
        Parameters
        ----------
        fs : sampling rate
        lowcut : low cutoff frequency
        highcut : high cutoff frequency
        
        Returns
        -------
        sos : array containing the sos coefficient
    
        """
        order = 4
        low = lowcut / fs # normalised low cutoff frequency
        high = highcut / fs # normalised high cutoff frequency
        sos = sp.butter(order, [low, high]*2, btype='band', output='sos')
        
        return sos
    
    
    def iirFiltering(self, x):
        """

        Filters and plots realtime sample values using iir filter.
        Parameters
        ----------
        x : input sample value (mean value of channel_G of webcam)
            
        """
        self.rplt1.addData(x)
        y = self.iir.dofilter(x)
        self.rplt2.addData(y)
        self.detectHeartrate(y)
        
    def calc_avg(self, x):
        """

        Calculates average value.
        Parameters
        ----------
        x : input numpy array
        
        Returns
        -------
        avg : average value
    
        """
        count = np.count_nonzero(x) # count non zero elements
        if count == 0: # if all elements in the array are 0
            count = len(x)
        if count >= 7: # if there are more than 7 non zero elements
            avg = np.sum(x)/count
        else:
            avg = 0
        return avg
    
    def insertValue(self, x, idx, v):
        """

        Inserts value in the ring buffer.
        Parameters
        ----------
        x : input numpy array
        idx : index value before insertaion
        v : value to be inserted
        
        Returns
        -------
        x : numpy array containing value v
        idx : index value after insertaion
    
        """
        size = len(x)
        idx = (idx + 1) % size
        x[idx] = v
        return x, idx

    def detectHeartrate(self, data):
        """

        Detects and displays momentary heartrate.
        Parameters
        ----------
        data : filtered sample value
    
        """
        # insert data into the buffer
        self.buff, self.buff_idx = self.insertValue(self.buff, self.buff_idx, data)
        
        # check if the new sample is between threshold values
        # if TRUE then set flag to mark a possible peak
        if self.buff[self.buff_idx] > self.threshold_low and self.buff[self.buff_idx] < self.threshold_high and self.buff_idx >= self.diff_min and self.buff_idx <= self.diff_max:        
            self.flag = 1
        
        # check if the flagged peak is greater than the one at previous index
        #if TRUE then reset flag and calculate momentary heartrate
        if  self.buff[self.buff_idx-1] > self.buff[self.buff_idx] and self.flag == 1:        
            self.flag = 0
            self.curr_peak = self.buff_idx - 1 # set current peak to index value
            self.buff_idx = 0 # reset buffer index
            
            # momentary heart rate
            temp = (self.fs/(self.curr_peak))*60
            self.rate, self.rate_idx = self.insertValue(self.rate, self.rate_idx, temp)
        
        bpm = int(self.calc_avg(self.rate)) # update average value of the rate buffer
        self.rplt3.addData(bpm)   
        
        if self.buff_idx >= len(self.buff)/2 and self.flag == 0: # reset rate buffer if no peaks have been flagged
            self.rate, self.rate_idx = self.insertValue(self.rate, self.rate_idx, 0)
            
                  
if __name__=='__main__' :
    
    camera = webcamChannel_G.WebcamChannel_G()
    cam = cv2.VideoCapture(0)
    fs = cam.get(cv2.CAP_PROP_FPS) # get frame rate (FPS)
    
    hr = DetectHR(fs)
    
    #start the thread and stop it when we close the plot windows
    camera.start(cam, callback = hr.iirFiltering)
        
    plt.show()
    camera.stop()
   