import json
import time
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

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
    # Example: Add code here to ring a buzzer, flash an LED, or play a sound

# Callback function to handle incoming messages
# def on_message(client, userdata, message):
#     print(f"Received message from topic {message.topic}: {message.payload}")
#     payload = json.loads(message.payload)
#     alarm_time = payload['time']

#     # Calculate the time until the alarm
#     alarm_datetime = datetime.strptime(alarm_time, '%H:%M')
#     now = datetime.now()
#     time_until_alarm = (alarm_datetime - now).total_seconds()

#     if time_until_alarm > 0:
#         print(f"Alarm set for {alarm_time}. Waiting...")
#         time.sleep(time_until_alarm)
#         trigger_alarm()
#     else:
#         print("Alarm time is in the past!")

def on_message(client, userdata, message):
    print(f"Received message from topic {message.topic}: {message.payload}")
    payload = json.loads(message.payload)
    alarm_time_str = payload['time']
    
    # Parse the alarm time
    alarm_time = datetime.strptime(alarm_time_str, '%H:%M').time()
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


# Subscribe to the alarm/set topic
client.subscribe("alarm/set", 1, on_message)

# Keep the script running
while True:
    time.sleep(1)
