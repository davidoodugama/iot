# Publisher which will send temperature sensor data to MQTT server
from datetime import *
import pytz
import paho.mqtt.client as paho
from paho import mqtt
import json
from const.const import MQTT_BROKER, PORT, LOCAL_TIME_ZONE, MONGO_TEMP_DB, MONGO_TEMP_COLLECTION
from DB.DB_config import MongoDB
from bson import json_util

class Publisher:
    def __init__(self, topic):

        # Get Sri Lankan current time
        tz_SRI_LANKA = pytz.timezone(LOCAL_TIME_ZONE) 
        datetime_SRI_LANKA = datetime.now(tz_SRI_LANKA)
        SL_time = datetime_SRI_LANKA.strftime("%H:%M:%S")

        # Temp Temperature
        self.real_time_temp = 0
        self.temp_tot = 0
        self.avg = 0

        # DB Connection
        self.db = MongoDB(MONGO_TEMP_DB, MONGO_TEMP_COLLECTION)

        # MQTT Connection
        self.topic = topic
        self.date = str(date.today())
        self.sl_time = SL_time
        self.mqtt_broker = MQTT_BROKER
        self.mqtt_port = PORT
        self.count = 0
        
        # Creating Connection from the MQTT brocker
        self.client = paho.Client(client_id = "", userdata = None, protocol = paho.MQTTv5)
    
    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self, client, userdata, flags, rc, properties = None):
        print("CONNACK received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self, client, userdata, mid, properties = None):
        print("Published mid: " + str(mid))

    def publish_msg(self, msg):
        
        # Connect Hive MQ
        self.client.on_connect = self.on_connect

        # Start the loop
        self.client.loop_start()

        # connect to HiveMQ
        try:
            self.client.connect(self.mqtt_broker, self.mqtt_port)
        except:
            print("Connecting can not be establish. Try again to connect or check host. Trying again........")
            self.client.connect(self.mqtt_broker, self.mqtt_port)

        self.client.on_publish = self.on_publish
        self.real_time_temp = int(msg)
        self.temp_tot += int(msg)
        self.count += 1
        self.avg =  self.temp_tot / self.count

        # Creating a dictionary to store in Mongo DB
        mongo_temperature = {
            "mqtt_topic": self.topic,
            "current_date": self.date,
            "current_time": self.sl_time,
            "temperature": self.real_time_temp,
            "avg_temperature": self.avg
        }

        # Creating a dictionary to pass the results
        read_temperature = {
            "mqtt_topic": self.topic,
            "temperature": self.real_time_temp,
        }

        print("temp values == " + str(self.real_time_temp))

        # Creat Json object 
        temperature_db = self.parse_json(mongo_temperature)

        # Insert values to DB
        # if self.db:
        #     res = self.db.insert_into(temperature_db)
        #     print("Insert values successful \n")
        # else:
        #     print("Can't insert values to DB \n")

        # res = self.db.get_records()
        
        # for records in res:
        #     print(records)
        
        self.client.publish(self.topic, payload = json.dumps(read_temperature, indent = 4), qos = 1)

        # loop_forever for simplicity, here you need to stop the loop manually
        # you can also use loop_start and loop_stop
        # time.sleep(10)
        self.client.loop_stop()

    def parse_json(self, data):
        return json.loads(json_util.dumps(data))
    
    
