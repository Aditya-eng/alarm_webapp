import time
import paho.mqtt.client as mqtt
import ssl
import json
import thread
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem', certfile='./device.pem.crt', keyfile='./private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("aftnrjs54yfev-ats.iot.eu-north-1.amazonaws.com", 8883, 60)
#Taken from REST API endpoint - Use your own. 


def intrusionDetector(Dummy):
    while (1): 
        x=GPIO.input(21)
        if (x==0): 
            print ("Just Awesome") 
            client.publish("device/data", payload="Ravi raj, Aditya Mohan!!" , qos=0, retain=False)
        time.sleep(5)

#thread.start_new_thread(intrusionDetector,("Create intrusion Thread",))
threading.Thread(target=intrusionDetector, args=("Create intrusion Thread",)).start()
    
client.loop_forever()

