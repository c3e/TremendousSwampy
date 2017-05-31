import argparse
import logging
import sys
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

from lib.swamp import Swamp
from time import sleep

from settings import PATTERNS


# all the cmdline foo
parser = argparse.ArgumentParser(
    description='Daemon for mqtt2influxdb mapping')

parser.add_argument('--test', action="store_true",
                    dest="test", help='runs all test for the module')
parser.add_argument('--run', action="store_true",
                    dest="run", help='runs the module as daemon')

parser.add_argument('--verbose', action="store_true", dest="debug", help="verbose console output")

parser.add_argument("--mqtthost", type=str, help="MQTT Host",
                    default="localhost")
parser.add_argument("--mqttport", type=int, help="MQTT Port", default=1883)


parser.add_argument("--influxhost", type=str,
                    help="influxdb Host", default="localhost")
parser.add_argument("--influxport", type=int, help="influxdb Port", default=8086)

parser.add_argument("--influxuser", type=str,
                    help="influxdb User")
parser.add_argument("--influxpass", type=str,
                    help="influxdb Pass")
parser.add_argument("--influxdb", type=str,
                    help="influxdb Database")
args = parser.parse_args()
if args.run:
    if args.debug:
        print("Show debug log on console")
        # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # mqtt client
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc) + " to mqtt broker")
        connected = True

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(args.mqtthost, args.mqttport, 60)

    sleep(5)

    # influx client
    influx_client = InfluxDBClient(
        args.influxhost, args.influxport, args.influxuser, args.influxpass, args.influxdb)
    # Swamp stuff
    swamp = Swamp(mqtt_client, influx_client, PATTERNS)
    swamp.subscribe()
    swamp.loop()
elif args.test:
    import pytest
    pytest.main([])
else:
    pass
    # print(args.accumulate(args.integers))
