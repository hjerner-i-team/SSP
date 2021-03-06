### Setup description of the rock, paper, scissor hardware demo.
This page will describe the hardware demo used in this project such that it could be completely replicated solely based on the information found here. It will cover physical hardware components, how they interface the Raspberry Pi, and how the Raspberry Pi must be configured to replicate the demo.

**Components:**
- Raspberry Pi Model 3 B+
  - [Product Info](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
- Generic Powerbank (2A+ output)
- Adafruit AMG8833   (IR-sensor)
  - [Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-amg8833-8x8-thermal-camera-sensor.pdf?timestamp=1552457921)
- Adafruit 1.44" Color TFT LCD Display 
  - [Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-1-44-color-tft-with-micro-sd-socket.pdf?timestamp=1552457427)

**Deprecated Components:**
- Arduino Uno       
  - [Datasheet](https://www.terraelectronica.ru/pdf/show?pdf_file=%2Fz%2FDatasheet%2FU%2FUNO_R3(CH340G).pdf&fbclid=IwAR2FrlMjTS1hMZOYdpzgNwjVe-th5LTBIL-3l3MgKYxddCArinXqffufGAc)
- ESP8266 (ESP-01) module (Wifi module)
  - [Datasheet](http://wiki.ai-thinker.com/_media/esp8266/docs/a001ps01a2_esp-01_product_specification_v1.2.pdf?fbclid=IwAR2E6Dpguf-HQLodjZ8DdVEVA4pAAcRWWhqb_sUmmcb46i1hmuMgdBjYaW4)
  
**Initial Attempt:**

A system driving the AMG8833 and LCD display using an Arduino Uno + ESP8266 was initially attempted. 
The Arduino Uno was intended to interface, through a custom PCB shield, the AMG8833 IR-sensor, ESP8266 wifi module and the TFT LCD Display. The PCB shield was mainly needed for voltage regulation and level shifting between the 5V Arduino and 3.3V ESP8266.
Problems arose when most documentation surrounding usage of the ESP8266 ended after establishing a connection to an access point, leaving no proper documentation for how to send and receive data from servers. This configuration was then deprecated due to the difficulty of configuring the ESP8266 to establish an interface to the CREPE HTTP REST API. 
A Raspberry Pi was chosen as a substitute 

### Overview of complete setup
All hardware is mounted inside a 3D printed container, powered by a 2.1A power bank also mounted inside. The Raspberry Pi, 1.44" TFT LCD dislay and AMG8833 IR-sensor are mounted in the interior of the box. The AMG8833 can capture infrared data through a slit in the box, and a slit is made for the display as well. An adjustable plate is attached to the bottom of the container. This plate is equipped with a button, used for registering the presence of the hand of the user. The distance between the sensor and pushbutton to optimaly cover the users hand was found by trial and error. The sensor data was visualized by running main_with_visualization.py and the distance adjusted accordingly. The disctance used in this demo was **15cm**.
The display will inform the user of what state the system is currently in, and will iterate thorugh:
 - WAIT: The script is booting, loading necessary libraries and initializes the display, sensor and hardware interrupt for the pushbutton.
 - READY: The script is suspended and waiting for a hardware interrupt initiated by pressing down the pushbutton.
 - PROCESSING: The script is transmitting the IR sensor data to the CREPE HTTP REST API and wait for a valid response from the same server.
 - SERVER UNAVAILABLE: The script failed to contact the server, and is either due to lack of internet connectivity or an internal server failure. Will not be displayed if it succeeds to contact server.
 - GESTURE: Displays (for 5 seconds) the hand gesture the system predicts will beat the one played by the user.
 

### Physical Connections
This section will describe the physical connections between each hardware component as used in this project. Other configurations may work, but this will require you to do the appropriate changes in code. The pins on the Raspberry Pi are described in both physical pins and Broadcom GPIO numbers (BCM). 
It is very important to verify that there is good electrical conduction between all hardware components to ensure functional operation. A continuity test with a multimeter should suffice.

**Pushbutton**

This may vary depending on the type of pushbutton used, and it should be confirmed that the pins connected from the pushbutton are being shorted when pressed, as the script will react to a falling edge on the defined input pin.

| Pushbutton | Raspberry Pi 3B+ |
|------------|-----------------:|
| Any        |  Pin 12 (BCM 18) |
| Any        |     Pin 14 (GND) |

**AMG8833 IR Sensor**

| AMG8833 |   Raspberry Pi 3B+  |
|:-------:|:-------------------:|
| Vin     |        Pin 1 (3.3V) |
| GND     |         Pin 9 (GND) |
| SDA     | Pin 3 (BCM 2) (SDA) |
| SCL     | Pin 5 (BCM 3) (SCL) |

**TFT LCD Display**

| LCD Display | Raspberry Pi 3B+ |
|:-----------:|:----------------:|
| Vin         |    Pin 17 (3.3V) |
| GND         |     Pin 20 (GND) |
| SCK         |  Pin 23 (BCM 11) |
| SI          |  Pin 19 (BCM 10) |
| TCS         |  Pin 24 (BCM 8 ) |
| RST         |  Pin 22 (BCM 25) |
| D/C         |  Pin 18 (BCM 24) |

### Installation

To recreate this demonstration, download the repository and follow instructions given in comments on each source file. Clone to Raspberry Pi. All code in this repository is intended to use on the Raspberry Pi 3 B+ running Raspbian.

**Eduroam**

If you **DON'T** need the Raspberry Pi to be connected to an sduroam access point, skip this section. The following tutorial is confirmed on NTNU's eduroam network, and is not guaranteed to function properly on other eduroam networks. (It might though.)
To enable the Raspberry Pi to correctly communicate with eduroam's radius servers, the wpa_supplicant service must be configured:

```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
Add the following configuration:
```
network={
  ssid="eduroam"
  scan_ssid=1
  key_mgmt=WPA-EAP IEEE8021X
  eap=PEAP
  identity="username@ntnu.no" 
  password=hash:long_string_of_hashed_password
  phase1="peapver=0"
  phase2="MSCHAPV2"
}
```
Potentially username@your_institution.area_code if your institition is not NTNU.
To get a hashed string of your eduroam, open another terminal and type:
```
echo -n 'YOUR_PASSWORD' | iconv -t utf16le | openssl md4
```
This will return your password converted into a hashed string. Copy this into wpa_supplicant.conf.
Now reboot the Raspberry Pi, and verify that it connects to eduroam.

If it works, congratulations! You can skip to the next section.
If it doesn't, try to kill the wpa_supplicant process and reload wpa_supplicant.conf by: 
```
ps -aux | grep supplicant
```
Find process ID of wpa_supplicant process, and kill it.
```
kill process_ID
```
If it refuses to die, append parameter "-9" to kill it more firmly. (AT YOUR OWN RISK - might leave corrupted files etc.)
```
kill -9 process_ID
```
Next, run the newly configured wpa_supplicant.conf by:
```
sudo wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
```
This may have the Raspberry Pi connect to eduroam right away, but reboot it for good measure.
If you received an error message informing that a wpa_supplicant is already running, you either killed the wrong process, or didn't manage to kill wpa_supplicant successfully.

**Preparing for physical interfaces to AMG8833 and LCD Display**

Enter the Raspberry Pi configuration tool and enable SPI and I2C to enable use of the GPIO pins to communicate with the AMG8833 IR sensor and the LCD display. Enable SSH and/or VNC if you wish to remotely control the Raspberry Pi. 
```
sudo raspi-config --> enable SPI, I2C, SSH, VNC.
```

Copy the file main.py and the folder "graphics" from this repo onto the desktop of your Raspberry Pi. 
OPTIONAL: Copy the file main_with_visualization.py onto the desktop of your Raspberry Pi. This version is used for debugging, but will pause after gathering sensor data to display a (somewhat) human-interpretable, interpolated image of the IR data .

**Installing [Adafruit's Python library for the AMG8833 IR sensor](https://github.com/adafruit/Adafruit_CircuitPython_AMG88xx):**

```
sudo pip3 install adafruit-circuitpython-amg88xx
```

**Installing ["Adafruit" ST7735R Library](https://github.com/KYDronePilot/Adafruit_ST7735r).** 

This is an unofficial library derived from another official Adafruit LCD driver library. The motivation behind the use of this library is due to that the LCD display used in this project was originally intended for use with an Arduino, and thus the official Adafruit libraries are written for Arduino.  changed to enable use of the ST7735R LDC driver with Raspberry Pi. 

```
sudo apt-get install build-essential python-dev python-smbus python-pip python-imaging python-numpy
sudo pip3 install RPi.GPIO
clone https://github.com/KYDronePilot/Adafruit_ST7735r
sudo python3 setup.py install (in the cloned git repository)
```

**Run main.py automatically on boot**

Create systemd unit to enable the main python script to run on boot. This configuration will also restart the script in the event of a failure. This [tutorial](https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/) can be used as reference if something goes wrong, or if you want more details regarding this process.
```
sudo nano /lib/systemd/system/CREPE.service
```

```
[Unit]
Description=CREPE Hardware Example
[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
Environment=PYTHONUNBUFFERED=1
ExecStart=/bin/bash -c '/usr/bin/python3 /home/pi/Desktop/main.py > /home/pi/Desktop/CREPE.log 2>&1'
Restart=on-failure
RestartSec=5s
KillMode=process
TimeoutSec=infinity
[Install]
WantedBy=graphical.target
```

Now we need to register the service and enable it with systemctl such that it will run upon next boot.  **NOTE THAT ONLY ONE INSTANCE OF MAIN.PY CAN BE RUN AT ANY GIVEN TIME - ATTEMPTING TO MANUALLY RUN MAIN.PY WHILE THE SERVICE IS RUNNING WILL RESULT IN UNDEFINED BEHAVIOUR**
```
sudo chmod 644 /lib/systemd/system/CREPE.service
sudo systemctl daemon-reload
sudo systemctl enable CREPE.service
sudo reboot
```

Upon reboot, check that the service is running. (It can also be checked by confirming that the LCD display is updated with the "READY" status message)
```
sudo systemctl status CREPE.service
```

**NOTE:** To enable manual execution of main.py for debugging and/or changes to the code, you first need to disable the service and reboot. Also check status to verify that the service was stopped.
```
sudo systemctl stop CREPE.service
sudo systemctl disable CREPE.service
sudo systemctl status CREPE.service
sudo reboot
```

OPTIONAL: Instally numpy, scipy and matplotlib if you want to use main_with_visualization.py, which will display a human-interpretable, interpolated image of the IR data collected by the sensor.
libatlas-base-dev is needed to mitigate the error (ImportError: lib77blas.so.3 cannot open shared object file)
```
sudo apt-get install libatlas-base-dev 
pip3 install matplotlib scipy colour
```

End with an example of getting some data out of the system or using it for a little demo
