import paho.mqtt.client as paho
from paho import mqtt
import json
import time
import sys
# sys.path.insert(0, '../const')
# from const.const import MQTT_BROKER, PORT, TOPIC

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
broker = "broker.hivemq.com"
port = 1883
topic = "DS18B20_temperature/temperature"

    # setting callbacks for different events to see if it works, print the message etc.
def on_connect( client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# print which topic was subscribed to
def on_subscribe( client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message( client, userdata, msg):
    response = json.loads(msg.payload)
    print("temperature Value is: " + str(response['temperature']))

#----------------------------------------------------------------------------------------------

print("Sub is running ..............................................................")
client.on_connect = on_connect

# connect to HiveMQ
client.connect(broker, port)

# Start the loop
client.loop_start()

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message

#----------------------------------------------------------------------------------------------

# subscribe to all topics of testsensortopic by using the wildcard "#"
#client.subscribe("testsensortopic/#", qos=1)
client.subscribe(topic, qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
time.sleep(100)
client.loop_stop()