#!/usr/bin/python3
# Start camera with fixed exposure and gain.

import time, os, math, subprocess
from time import sleep
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from datetime import datetime
from libcamera import Transform
from PIL import Image
os.environ["LIBCAMERA_LOG_LEVELS"] = "4"
# "0" DEBUG, "1" INFO, "2" WARN, "3" ERROR, "4" FATAL

Exposures=100
LuminTarget=16
LuminTol=.025
ExposureTime=60

picam2 = Picamera2(0)


picam2.start_preview(Preview.QTGL, x = 960, y=10, width=860, height=680)
picam2.set_controls({"AeEnable": False, "ExposureTime": ExposureTime, "AwbEnable": False, "ColourGains": (3.1, 1.5), "FrameRate": 5})
picam2.title_fields = ["ExposureTime","AnalogueGain", "ColourGains"]
picam2.start()

while True:
    ctrls = Controls(picam2)
    ctrls.AnalogueGain = 1
    Frame=int(1000000/ExposureTime)
    ctrls.FrameRate=Frame+1
    ctrls.ExposureTime = ExposureTime
    ctrls.ColourGains = (3.1 , 1.5)
    picam2.set_controls(ctrls)

    request = picam2.capture_request()
    array  = request.make_array('main')
    metadata = request.get_metadata()
    request.release()
    lux= metadata['Lux']
    Exp = metadata['ExposureTime']
    Lumin=round(Exp/lux,2)
    print("exposure:",Exp,"usec ","Lux value:",(round(lux,1)),"Lumin ",Lumin,"framerate",(round(Frame,1)))
    picam2.stop()
    
    if (Lumin > LuminTarget * (1/(1-LuminTol))) :
        ExposureTime = int(.8 * ExposureTime)
        
    if (Lumin < LuminTarget * (1-LuminTol)) :
        ExposureTime = int(1.2 * ExposureTime)
        
    ctrls = Controls(picam2)
    ctrls.ExposureTime = ExposureTime
    picam2.set_controls(ctrls)
    
    picam2.start()

print("Done")

picam2.stop()
picam2.stop_preview()

#img = Image.open('/media/solarpi/SolarPi_512/images/AutoLongExposure_(date_time).jpg')
#new_image = img.resize((1000, 1000))
#new_image.show()
