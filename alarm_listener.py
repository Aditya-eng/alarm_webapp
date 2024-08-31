import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
from gpiozero import LED

# Set up LED for visual alarm
led = LED(18)

# MQTT settings
MQTT_BROKER = "aftnrjs54yfev-ats.iot.eu-north-1.amazonaws.com"
MQTT_PORT = 8883
MQTT_TOPIC = "alarm/set"
CA_PATH = "/home/ados2405/certs/rootCA.pem"
CERT_PATH = "/home/ados2405/certs/device.pem.crt"
KEY_PATH = "/home/ados2405/certs/private.pem.key"
CLIENT_ID = "raspberry_ados"

# List to store multiple alarms
alarms = []

def connect_mqtt():
    client = mqtt.Client(client_id=CLIENT_ID)
    client.tls_set(ca_certs=CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH)
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    print("Connected to MQTT broker")
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic {MQTT_TOPIC}")
    return client

def on_message(client, userdata, message):
    global alarms
    try:
        payload = json.loads(message.payload.decode())
        alarm_time_str = payload['time']
        alarm_time = datetime.strptime(alarm_time_str, "%H:%M:%S").time()
        now = datetime.now().time()

        # If the alarm time is already in the past for today, add one day to schedule it for tomorrow
        if alarm_time <= now:
            alarm_datetime = datetime.combine(datetime.now() + timedelta(days=1), alarm_time)
        else:
            alarm_datetime = datetime.combine(datetime.now(), alarm_time)

        # Add the alarm to the list
        alarms.append(alarm_datetime)
        print(f"New alarm set for: {alarm_datetime}")

    except (KeyError, ValueError) as e:
        print(f"Error parsing message: {e}")

def trigger_alarm():
    global alarms
    now = datetime.now()
    triggered_alarms = [alarm for alarm in alarms if alarm <= now]

    for alarm in triggered_alarms:
        print(f"Alarm triggered at {alarm.time()}!")
        led.on()  # Turn on the LED as a visual indicator of the alarm
        time.sleep(10)  # Keep the alarm active for 10 seconds
        led.off()  # Turn off the LED after the alarm duration
        alarms.remove(alarm)  # Remove the triggered alarm from the list

        # Feedback to AWS IoT
        feedback = {
            "status": "triggered",
            "time": alarm.time().strftime("%H:%M:%S")
        }
        client.publish("alarm/feedback", json.dumps(feedback))
        print("Feedback sent to AWS IoT")

if __name__ == "__main__":
    client = connect_mqtt()
    client.subscribe(MQTT_TOPIC)
    client.on_message = on_message
    client.loop_start()

    try:
        while True:
            trigger_alarm()
            time.sleep(1)  # Check every second for triggered alarms

    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        client.loop_stop()
        client.disconnect()
