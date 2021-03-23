"""
 Copyright 2020 Bernd Porr. This source code file is part of webcam2rgb and is
 licensed under the GNU General Public License v3.0. For the full license text, 
 please see the file LICENSE.
 
 23 March 2020 - Modified by Prateek Dadial.
 
 Samples green channel of webcam.

"""


import cv2
import threading

class WebcamChannel_G():

    def start(self, cam, callback): 
        """

        Starts the thread.
        Parameters
        ----------
        cam : video capture object
        callback : a callback function
        
        """
        self.callback = callback
        self.cam = cam
        try:                
            self.running = True
            self.thread = threading.Thread(target = self.calc_mean)
            self.thread.start()
            self.ret_val = True           
        except:
            self.running = False
            self.ret_val = False


    def stop(self):  
        """

        Stops the thread.
        
        """
        self.running = False
        self.thread.join()


    def calc_mean(self):
        """

        Calculates mean value of the channel_G of webcam and passes 
        to the callback function.
        
        """   
        while self.running:
            try:
                self.ret_val = False
                self.ret_val, img = self.cam.read()                
                sample = cv2.mean(img)[1]
                self.callback(sample)                
            except:
                self.running = False
