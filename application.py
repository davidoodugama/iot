from const.const import TOPIC
from flask import Flask, abort, request, jsonify, Response
# from flask_restful import Api, Resource, request
import prometheus_client
import pymysql
from prometheus_client import Summary, Counter, Histogram, Gauge, CollectorRegistry, push_to_gateway
import time

application = Flask(__name__)
_INF = float("inf")
graphs = {}
registry = CollectorRegistry()
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed request in publisher')
graphs['g'] = Gauge('python_request_temperature', 'The temperature')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets = (1,2,5,6,60,_INF))

#creating the database connection

HOST = "localhost"
USER = "user"
PASS = "user"
PORT = 3306
db = pymysql.connect(host = HOST, port = PORT, user = USER, password = PASS)

cursor = db.cursor()

sql = '''use temp_db'''
cursor.execute(sql)
prometheus_client.start_http_server(8000)
@application.route("/")
async def extract_temp():
    counter = 0
    while True:
        start = time.time()
        # temperature = temp_obj.getTempReadings()
        graphs['c'].inc() # increment counter
        temperature = 20 + counter *2
        print(temperature)
        sql = '''insert into temp_tb(temp) values(%i)
        ''' % (temperature)

        cursor.execute(sql)
        db.commit()

        # publisher.publish_msg(temperature)
        counter = counter + 1
        
        end = time.time()
        graphs['g'].set(temperature)
        graphs['h'].observe(end-start)
        push_to_gateway('localhost:8000', job='python', registry=registry)

if __name__ == '__main__':
    application.run(debug=True, port=5000)