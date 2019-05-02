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
import numpy as np

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

## Init Sensor interface over I2C protocol
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)
TEMP_THRESHOLD = 19.9

## HTTP REST API communication specifications
#URL = 'http://inca.ed.ntnu.no:8000'
URL = 'http://129.241.209.138:5000'
_GET_RESPONSE = '/hw-api/output/'
_POST = '/hw-api/input/'
TIMEOUT = 5000

## Init TFT LCD Screen
WIDTH = 128
HEIGHT = 128
SPEED_HZ = 4000000

# Raspberry Pi pinout configuration.
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

## Load status messages and gesture responses, display "WAIT" status as soon as possible
print('Loading images...')
gfx_wait               = Image.open('/home/pi/Desktop/graphics/wait.jpg'); disp.display(gfx_wait)
gfx_ready              = Image.open('/home/pi/Desktop/graphics/ready.jpg')
gfx_processing         = Image.open('/home/pi/Desktop/graphics/processing.jpg')
gfx_server_unavailable = Image.open('/home/pi/Desktop/graphics/server_unavailable.jpg')

gfx_scissors = Image.open('/home/pi/Desktop/graphics/scissors.jpg')
gfx_paper    = Image.open('/home/pi/Desktop/graphics/paper.jpg')
gfx_rock     = Image.open('/home/pi/Desktop/graphics/rock.jpg')

gfx_response = dict()
gfx_response["Rock"]     = gfx_paper
gfx_response["Paper"]    = gfx_scissors
gfx_response["Scissor"]  = gfx_rock
gfx_response["None"]     = gfx_server_unavailable

r = [gfx_rock, gfx_paper, gfx_scissors] # DEBUG ONLY - REMOVE BEFORE DELIVERY
i = 0 # DEBUG ONLY - REMOVE BEFORE DELIVERY

while True:
    # Wait for button press:
    print("Waiting for user input...")
    disp.display(gfx_ready)
    try:  
        GPIO.wait_for_edge(CAPTURE_BTN, GPIO.FALLING)  
        print("\nFalling edge detected. Capturing sensor data.")  
    except KeyboardInterrupt:
        print("Exception error. (GPIO)")
        
    #Read sensor data:
    num_pixels_over_threshold = 0
    for row in amg.pixels:
        # Pad to 1 decimal place
        num_pixels_over_threshold += sum(temp > TEMP_THRESHOLD for temp in row)
        print(['{0:.1f}'.format(temp) for temp in row])
        print("")
    print("\n")
    
    # Convert data to json and send to HTTP REST API
    print("\"Active\" pixels:", num_pixels_over_threshold)
    json_data = json.dumps(amg.pixels)
    
    try:
        response = requests.post(URL + _POST, data = json_data, timeout=10.0)
        #print(response.text) # UNCOMMENT
    except:
        print("Server unavailable! (POST command)")
        disp.display(gfx_server_unavailable) # UNCOMMENT
        time.sleep(5) # UNCOMMENT
        continue # Restart loop
    
    # Wait for response from HTTP REST API
    disp.display(gfx_processing)
    time.sleep(2)
    while(1):
        try:
            #break # REMOVE
            response = requests.get(URL + _GET_RESPONSE, timeout=10.0)
            
        except:
            print("Server unavailable! (GET)")
            disp.display(gfx_server_unavailable)
            time.sleep(5)
            break
            
            
        if response.text in ["Rock", "Paper", "Scissor", "None"]:
            print("Server response is", response.text)
            disp.display(gfx_response[response.text])
            time.sleep(5)
            break
        else:
            print("Server not ready... Response was", response.text)
            time.sleep(0.2)
            continue
    
    ###

    
    # Draw the image on the display hardware. DEBUG
    #disp.display(r[i])
    
    # End loop
    #time.sleep(5) # DEBUG
    i += 1 # DEBUG
    i %= 3 # DEBUG
    
    














