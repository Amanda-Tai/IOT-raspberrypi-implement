import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import random
import urllib.request
import requests
import threading
DHT_SENSOR = Adafruit_DHT.DHT22
LM386_PIN = 18
LED_PIN = 23
DHT_PIN = 21
BUZZER_PIN = 20
FAN_PIN = 14
DATA_SENDING_INTERVAL = 10
POOL_INTERVAL = 0.5
def init():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN,GPIO.out)
    GPIO.setup(LED_PIN,GPIO.out)
    GPIO.setup(BUZZER_PIN,GPIO.out)

def bell():
    C4 = 262 # Do
    E4 = 330 # Mi
    music = [C4, E4]
    M_1 = C4
    M_3 = E4
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    p = GPIO.PWM(BUZZER_PIN, 50)
    p.start(15) # 0 <= DV <= 100
    play(p, M_3, 1)
    play(p, M_1, 1)
    p.stop
def play(p, frequency, tempo):
    p.ChangeFrequency(frequency)
    time.sleep(0.5 * tempo)

def read_data_led():
    NEW_URL = 'https://api.thingspeak.com/channels/1625035/fields/5.json?api_key=HN7KQ6WSXMO4R23Q&results=2'
    get_data = requests.get(NEW_URL).json()
    channel_id = get_data['channel']['id']
    feild_l = get_data['feeds']
    t = []
    for x in feild_l:
        t.append(x['field5'])
    return(t[1])
def read_data_buzzer():
    NEW_URL = 'https://api.thingspeak.com/channels/1625035/fields/6.json?api_key=HN7KQ6WSXMO4R23Q&results=2'
    get_data = requests.get(NEW_URL).json()
    channel_id = get_data['channel']['id']
    feild_l = get_data['feeds']
    t = []
    for x in feild_l:
        t.append(x['field6'])
    return(t[1])
def read_data_fan():
    NEW_URL = 'https://api.thingspeak.com/channels/1625035/fields/7.json?api_key=HN7KQ6WSXMO4R23Q&results=2'
    get_data = requests.get(NEW_URL).json()
    channel_id = get_data['channel']['id']
    feild_l = get_data['feeds']
    t = []
    for x in feild_l:
        t.append(x['field7'])
    return(t[1])



def main():
    init()
    fan=read_data_fan()
    led=read_data_led()
    buzzer=read_data_buzzer()
    print(fan)
    print(led)
    print(buzzer)
    time.sleep(0.5)
    if fan ='1':
        GPIO.output(FAN_PIN,True)
        print('fan on')
    else:
        GPIO.output(FAN_PIN,False)
        print('fan off')
    if led ='1':
        GPIO.output(LED_PIN,True)
        print('led on')
    else:
        GPIO.output(LED_PIN,False)
        print('led off')
   if buzzer ='1':
        bell()
        print('buzzer on')
    else:
        print('buzzer off')
while True:
    main()
    time.sleep(5)
    
