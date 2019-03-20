# Rock, Paper, Scissors example experiment
A demonstration of the CREPE communication framwork utilizing hardware, sensor data and network communications. 



### Intention
This demonstration is a simple example use case of the CREPE framework, demonstrating how CREPE allows for seemless and effortless experimentation with biological neurons. 

The demo setup will capture the IR profile of a rock/paper/scissor and trasnmitt this in json format through wifi to CREPE. CREPE will communcate the data further to the biological neurons, interpretate the results and transmitt these back to the demo setup, which will display the result on a display. 


### Setup of demo, physical components and configuraton

**Components:**
- Arudino Uno       
  - [Datasheet](https://www.terraelectronica.ru/pdf/show?pdf_file=%2Fz%2FDatasheet%2FU%2FUNO_R3(CH340G).pdf&fbclid=IwAR2FrlMjTS1hMZOYdpzgNwjVe-th5LTBIL-3l3MgKYxddCArinXqffufGAc)
- ESP8266 SMT module (Wifi module)
  - [Datasheet](http://wiki.ai-thinker.com/_media/esp8266/docs/a001ps01a2_esp-01_product_specification_v1.2.pdf?fbclid=IwAR2E6Dpguf-HQLodjZ8DdVEVA4pAAcRWWhqb_sUmmcb46i1hmuMgdBjYaW4)
- Adafruit AMG8833   (IR-sensor)
  - [Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-amg8833-8x8-thermal-camera-sensor.pdf?timestamp=1552457921)
- Adafruit 1.44" Color TFT LCD Display 
  - [Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-1-44-color-tft-with-micro-sd-socket.pdf?timestamp=1552457427)

**Overveiw of complete setup:**
The harware is mounted inside a 3D printed container, powered by a power bank also mounted inside. A small LCD dislay is mounted on he exterior of the container. A IR-sensor is mounted on the interior of the box, capturing data througha slot in the box. The sensor is mounted at XX mm above table height. A adjustable plate is attached to the bottom of the container. This plate is equipped with a button connected to the arduino. The subject places its hand on the button to initate the capturing of its IR-profile. The button is spaced XX mm from the front of the container 

**Arduino: setup**
The Arduino Uno is through a PCB shield equipped with the IR-sensor, wifi module and the LCD Display. It captures the IR profile of a rock/paper/scissor and transmits this to CREPE in json format. Results recieved from CREPE are displayed on the display. Capturing of data is triggered by the button mounted on the adjustable plate. 



### Requisites 
- The Arduino Uno used is a un-officila arduino. It requires a special driver to connect to Windows. [Driver link]()


### Installation

Copy-paste the following into a terminal

```
git clone git@github.com:hjerner-i-team/SSP.git
cd SSP
git clone git@github.com:hjerner-i-team/CREPE.git
cd CREPE
git checkout structure
cd ..
python -m venv env
source env/bin/activate
pip install -r CREPE/requirements.txt
```

Then upload the [arduino code files](https://github.com/hjerner-i-team/SSP/tree/dev/ir_sensor) to the arduino.


## Versioning

Version 1.0.0. (04.2018). Will not be updated. 
