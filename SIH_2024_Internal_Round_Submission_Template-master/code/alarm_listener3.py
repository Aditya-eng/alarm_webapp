import json
import time
from datetime import datetime, timedelta
from gpiozero import LED  # Use LED class for a buzzer, or adjust accordingly
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# GPIO setup
BUZZER_PIN = 18  # Change this to the GPIO pin you are using for the buzzer or LED

# Initialize LED (or Buzzer)
# Set the pin factory to use pigpio
# from gpiozero.pins.pigpio import PiGPIOFactory
# factory = PiGPIOFactory()
buzzer = LED(BUZZER_PIN)
# buzzer = LED(BUZZER_PIN, pin_factory=factory)

# Configure the AWS IoT Client
client = AWSIoTMQTTClient("raspberry_ados")
client.configureEndpoint("aftnrjs54yfev-ats.iot.eu-north-1.amazonaws.com", 8883)
client.configureCredentials("certs/rootCA.pem", "certs/private.pem.key", "certs/device.pem.crt")

# Configuration for AWS IoT
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

# Connect to AWS IoT
client.connect()

# Function to trigger an alarm
def trigger_alarm():
    print("Alarm ringing!")
    buzzer.on()  # Turn on the buzzer or LED
    time.sleep(10)  # Keep the buzzer or LED on for 10 seconds
    buzzer.off()  # Turn off the buzzer or LED

    # feedback_payload = {
    #     "status":"triggered",
    #     "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # }

    # client.publish("alarm/feeback",json.dumps(feedback_payload),1)
    # print("feedback sent to aws iot alarm successfully triggered.")

# Callback function to handle incoming messages
# def on_message(client, userdata, message):
#     print(f"Received message from topic {message.topic}: {message.payload}")
#     payload = json.loads(message.payload)
#     alarm_time_str = payload['time']
    
#     # Parse the alarm time
#     alarm_time = datetime.strptime(alarm_time_str, '%H:%M').time()
#     now = datetime.now()

#     # Combine today's date with the alarm time
#     alarm_datetime = datetime.combine(now.date(), alarm_time)

#     # If the alarm time has already passed today, set it for tomorrow
#     if alarm_datetime < now:
#         alarm_datetime = alarm_datetime + timedelta(days=1)

#     time_until_alarm = (alarm_datetime - now).total_seconds()

#     print(f"Alarm set for {alarm_datetime.strftime('%Y-%m-%d %H:%M:%S')}. Waiting {time_until_alarm} seconds...")
#     time.sleep(time_until_alarm)
#     trigger_alarm()

# ////////////////////////////////////
def on_message(client, userdata, message):
    print(f"Received message from topic {message.topic}: {message.payload}")
    payload = json.loads(message.payload)
    alarm_time_str = payload['time']
    
    # Parse the alarm time, expecting a 12-hour time format with AM/PM
    alarm_time = datetime.strptime(alarm_time_str, '%I:%M %p').time()
    now = datetime.now()

    # Combine today's date with the alarm time
    alarm_datetime = datetime.combine(now.date(), alarm_time)

    # If the alarm time has already passed today, set it for tomorrow
    if alarm_datetime < now:
        alarm_datetime = alarm_datetime + timedelta(days=1)

    time_until_alarm = (alarm_datetime - now).total_seconds()

    print(f"Alarm set for {alarm_datetime.strftime('%Y-%m-%d %H:%M:%S')}. Waiting {time_until_alarm} seconds...")
    time.sleep(time_until_alarm)
    trigger_alarm()





# //////////////////////
# Subscribe to the alarm/set topic
client.subscribe("alarm/set", 1, on_message)

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
