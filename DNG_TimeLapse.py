#!/usr/bin/python3

# Capture a DNG.

import time
from picamera2 import Picamera2, Preview
import os
from picamera2.controls import Controls

# Configuration
output_directory = "/home/solarpi/Pictures/TestImages/"  # Set your desired output directory
interval_seconds = 60  # Set the time interval between captures in seconds
num_images = 10  # Set the number of images to capture

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.create_preview_configuration()
capture_config = picam2.create_still_configuration(raw={})
picam2.configure(preview_config)

picam2.start()
picam2.set_controls({"AeEnable": False, "AwbEnable": False, "FrameRate": 10})
picam2.title_fields = ["ExposureTime", "AnalogueGain", "DigitalGain"]

with picam2.controls as ctrl:
    ctrl.AnalogueGain = 6.0
    ctrl.ExposureTime = 6000
print("analog gain of 6 and exposure of 60000")
    
#    ctrls = Controls(picam2)
#    ctrls.AnalogueGain = 1.0
#    ctrls.ExposureTime = 100
#    picam2.set_controls(ctrls)
time.sleep(2)

# test=input('Enter to start capture')

start_time = time.time()
for i in range(num_images):
    timestamp = time.strftime("%Y-%m-%d-%H:%M:%S")
#    dng_filename = f"{output_directory}/{timestamp}.dng"
    picam2.switch_mode_and_capture_file(capture_config, f"/home/solarpi/Pictures/TestImages/full_{timestamp}.dng", name="raw")
    print(f"saving captured image {i} of num_images at {time.time() - start_time:.2f}s")
    time.sleep(interval_seconds)


print("Capture complete.")