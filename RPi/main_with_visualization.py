# DISCLAIMER: This script is older than main.py, and still contains some unneccessary bits of code used for development and debugging.
# If the visualization capabilities are wanted integrated into main.py, simply copy the necessary bits of code to make it work.

import numpy as np
from scipy.interpolate import griddata
from colour import Color
import math

# low range of the sensor (this will be blue on the screen)
MINTEMP = 26.
# high range of the sensor (this will be red on the screen)
MAXTEMP = 29.
# how many color values we can have
COLORDEPTH = 1024 # 1024

points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

# sensor is an 8x8 grid so lets do a square
height = 240
width = 240

# the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

# create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

displayPixelWidth = width / 30
displayPixelHeight = height / 30

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import matplotlib.pylab as plt

import time
import busio
import board
import json
import requests
import adafruit_amg88xx
import RPi.GPIO as GPIO

from PIL import Image
import ST7735 as TFT
import Adafruit_GPIO.SPI as SPI

## Init button interrupts - GPIO 18 set up as input, a pull-up resistor to be drawn low.
CAPTURE_BTN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(CAPTURE_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

## Init Sensor
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)
data = dict()

## Init HTTP REST API comms
URL = 'http://inca.ed.ntnu.no:8000'
_GET_RESPONSE = '/hw-api/output/'
_POST = '/hw-api/input/'
TIMEOUT = 5000

## Init TFT LCD Screen
WIDTH = 128
HEIGHT = 128
SPEED_HZ = 4000000

# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

# Create TFT LCD display class.
disp = TFT.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(
        SPI_PORT,
        SPI_DEVICE,
        max_speed_hz=SPEED_HZ))

# Initialize display.
disp.begin()

# Load status messages
gfx_wait               = Image.open('/home/pi/Desktop/graphics/wait.jpg'); disp.display(gfx_wait)
gfx_ready              = Image.open('/home/pi/Desktop/graphics/ready.jpg')
gfx_processing         = Image.open('/home/pi/Desktop/graphics/processing.jpg')
gfx_server_unavailable = Image.open('/home/pi/Desktop/graphics/server_unavailable.jpg')

# Load response images.
print('Loading images...')
gfx_scissors = Image.open('/home/pi/Desktop/graphics/scissors.jpg')
gfx_paper    = Image.open('/home/pi/Desktop/graphics/paper.jpg')
gfx_rock     = Image.open('/home/pi/Desktop/graphics/rock.jpg')

gfx_response = dict()
gfx_response["rock"]     = gfx_rock
gfx_response["paper"]    = gfx_paper
gfx_response["scissors"] = gfx_scissors

r = [gfx_rock, gfx_paper, gfx_scissors]
i = 0

while True:
    # Wait for button press:
    print("Waiting for user input...")
    disp.display(gfx_ready)
    try:  
        GPIO.wait_for_edge(CAPTURE_BTN, GPIO.FALLING)  
        print("\nFalling edge detected. Capturing sensor data.")  
    except KeyboardInterrupt:
        print("Exception error.")
        
    #Read sensor data:
    data["temps"] = amg.pixels
    for row in amg.pixels:
        # Pad to 1 decimal place
        print(['{0:.1f}'.format(temp) for temp in row])
        print("")
    print("\n")
    
    ### VISUALISATION
    pixels = []
    for row in amg.pixels:
        pixels = pixels + row

    normalized_pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
    #perform interpolation
    bicubic_pixels = griddata(points, normalized_pixels, (grid_x, grid_y), method='cubic')
    print(bicubic_pixels)
    plt.imshow(amg.pixels, cmap='jet')
    plt.show()
    
    ###
    
    # Convert data to json and send to HTTP REST API
    json_data = json.dumps(data)
    
    try:
        response = requests.post(URL + _POST, data = json_data, timeout=10.0)
        print(response.text)
    except:
        print("Server unavailable! (POST)")
        disp.display(gfx_server_unavailable)
        time.sleep(5)
        continue # Restart loop
    
    # Wait for response from HTTP REST API
    disp.display(gfx_processing)
    while(1):
        try:
            response = requests.get(URL + _GET_RESPONSE, timeout=10.0)
            print(response.text)
        except:
            print("Server unavailable! (GET)")
            disp.display(gfx_server_unavailable)
            time.sleep(5)
            
        if response.text in ["rock", "paper", "scissors"]: # CHANGE THIS!!!!
            print("Server response is", response.text)
            disp.display(gfx_response[response.text])
            break
        else:
            #break # Change this!
            print("Server not ready...")
            time.sleep(0.1)
            continue
    
    ###

    
    # Draw the image on the display hardware. DEBUG
    print(response.text)
    disp.display(r[i])
    
    # End loop
    time.sleep(5)
    i += 1
    i %= 3
    
    














