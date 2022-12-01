import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import sys
import random
import urllib.request
import requests
import threading
#import lineTool
DEVICE_TOKEN = "7aLP5TWE2gwfDn16Zyzo6fGdK"
DHT_SENSOR = Adafruit_DHT.DHT22
waterlevel = None
DHT_PIN = 17
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
LM386_PIN=26
PIN=20
# photoresistor connected to adc #0
photo_ch = 0
writekey='B7N0T7Q0YC1P8NAS'
readkey='HN7KQ6WSXMO4R23Q'
def thingspeak_post_humd(humidity,distance,temp,soundd):
    URl='https://api.thingspeak.com/update?api_key='
    KEY= writekey
    HEADER='&field1={}&field2={}&field3={}&field4={}'.format(humidity,distance,temp,soundd)
    NEW_URL=URl+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)
    print(data)

#port init
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()			#clean up at the end of your script
         GPIO.setmode(GPIO.BCM)		#to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS, GPIO.OUT)
         GPIO.setup(LM386_PIN, GPIO.IN)

#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def SwitchOnLight(PIN):
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, True)
    
def SwitchOffLight(PIN):
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, False)



def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)	
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
def get_temp():
    temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temp

def get__sound():
    return 1

def get_distance():
    TRIG = 18
    ECHO = 24
    i=0
    PIN=20
    GPIO.setup(TRIG ,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)
    print("Starting.....")
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()
    while GPIO.input(ECHO)==1:
      pulse_stop = time.time()
    pulse_time = pulse_stop - pulse_start
    distance = pulse_time * 17150
    return distance

def sound(channel):
    print('noise')
    time.sleep(0.5)
    return 1

def get_sound():
    GPIO.add_event_detect(LM386_PIN, GPIO.RISING,callback=sound,bouncetime=10)
    return 1

def main():
         init()
         print("will start detec water level\n")
         j=0
         while True:
                  adc_value=readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
                  useless,temperature=get_temp()#get_temp
                  distance=get_distance()
                  soundd=get__sound()
                  print(adc_value)
                  print(temperature)
                  print(distance)
                  print(soundd)
                  thingspeak_post_humd(adc_value,distance,temperature,soundd)
                  time.sleep(20)
         
        
        
        
if __name__ == '__main__':
         try:
                  main()
                 
         except KeyboardInterrupt:
                  pass
GPIO.cleanup()

