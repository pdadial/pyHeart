# webcamChannel_G
Turning your webcam into a simple Green light sensor
sampling at the framerate.

## Prerequisites

```
pip3 install opencv-contrib-python
pip3 install opencv-python
```

## How to use

### Import it

```
import webcamChannel_G
```

### Get an instance

```
camera = webcamChannel_G.WebcamChannel_G()
```

### Set up a callback function and create a VideoCapture object

```
cam = cv2.VideoCapture(0)
def hasData(data):
```

### Start continous acquisition

```
camera.start(cam, callback = hasData)
```
the callback is then called at the framerate of the camera


### Stop the acquisition

```
camera.stop()
```
