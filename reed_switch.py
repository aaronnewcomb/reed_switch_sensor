#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Change these as needed
mqtt_username = "???????"
mqtt_password =  "????????"
mqtt_host = "192.168.0.3"
mqtt_port = 1883

# Define pin
switchPin = 4

# Pin Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Pin State Setup
prevState = "Unknown"
state = "Unknown"

client.username_pw_set(mqtt_username, mqtt_password)
my_topic = "toggle/garage_door/state"
try:
    while True:
        prevState = state

        if GPIO.input(switchPin): # Switch is released
            state = "Opened"
        else: # Switch is connected
            state = "Closed"

        if prevState!=state:
            print(state)
            client.connect(mqtt_host, mqtt_port)
            if state == "Opened":
                # Publish Open
                client.publish(topic=my_topic, payload="ON", qos=0, retain=False)
            elif state == "Closed":
                # Publish Closed
                client.publish(topic=my_topic, payload="OFF", qos=0, retain=False)
            client.disconnect()

        time.sleep(0.1)
except KeyboardInterrupt: # Clean Exit
    GPIO.cleanup() # Cleanup all GPIO

except Exception as e: # Catch Errors
    print(e)