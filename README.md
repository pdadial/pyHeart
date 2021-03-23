# pyHeart
Measure heartrate using fingertip placed over webcam.

A real-time application of IIR filter to detect heart rate by placing index finger over the webcam. The webcam’s sampling rate is used to sample values from the green channel. These values are then filtered using a chain of two 2nd order bandpass IIR filters and the filtered samples are stored in a temporary ring buffer for detecting the peaks representing heartbeats, which are then used to calculate momentary heart rate.
![alt text](https://github.com/pdadial/pyHeart/blob/main/images/Figure.png)


## Prerequisites
```
pip3 install opencv-contrib-python
pip3 install opencv-python
```

## How to use
```
python hr_main.py
```
