from datetime import datetime
import json
from paho.mqtt.client import topic_matches_sub
import logging

PATTERN_RULES = """
{
    'SUB': '#',
    'TAGS': {TAGNAME': 'TOPIC'|INDEX for TOPIC.split("/")|any fixed value except integer or 'TOPIC', ...},
    'MEASUREMENT': INDEX for TOPIC.split("/")|any fixed value,
    'TYPE': bool|int|float|str|any fixed value
    }
"""


def set_measurement(pattern, split_topic):
    # set measurement to either string or part of topic
    if type(pattern["MEASUREMENT"]) is int:
        measurement = split_topic[pattern["MEASUREMENT"]]
    else:
        measurement = pattern["MEASUREMENT"]
    return measurement


def set_value(pattern, message):
    # set value to defined type or fixed value
    if pattern['TYPE'] is int:
        value = int(float(message.payload))
    elif pattern['TYPE'] is float:
        value = float(message.payload)
    elif pattern['TYPE'] is str:
        value = message.payload.decode('UTF-8')
    elif pattern['TYPE'] is bool:
        if message.payload.lower() in (b"false", b"0", b"-1", b"off", b"none", b"not", b""):
            value = False
        else:
            value = True
    else:
        value = pattern['TYPE']
    return value


def set_tags(pattern, message, split_topic):
    # collect tag data
    tags = {}
    for key, value in pattern['TAGS'].items():
        key = key.lower()
        if value == "TOPIC":
            tags[key] =  message.topic
        elif isinstance(value, int):
            tags[key] = split_topic[value]
        else:
            tags[key] = value
    return tags



class Swamp(object):

    """Takes a mqtt-client, a influxdb-client and a list of patterns
    Subscribes to all patterns and push them into influxdb accordingly"""

    def __init__(self, mqttclient, influxdbclient, patterns, debug=True):
        super(Swamp, self).__init__()
        self.mqtt = mqttclient
        self.influx = influxdbclient
        self.patterns = patterns
        self.debug = debug

        if debug:
            import sys
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,format='%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

        # subscribe all topics

    def on_message(self, client, userdata, message):
        if self.debug:
            logging.debug('MQTT MSG received on topic: %s' % message.topic)
        for pattern in self.patterns:
            if topic_matches_sub(pattern['SUB'], message.topic):
                split_topic = message.topic.split("/")
                json_data = {}
                json_data['measurement'] = set_measurement(pattern, split_topic)
                json_data['fields'] = {'value': set_value(pattern, message), }
                json_data['tags'] = set_tags(pattern, message, split_topic)
                self.influx.write_points([json_data,])
                if self.debug:
                    logging.debug('saved to influx measurement %s: %s' % (json_data['measurement'], json_data['fields']))

    def subscribe(self):
        self.mqtt.subscribe([(pat['SUB'], 0) for pat in self.patterns])
        self.mqtt.on_message = self.on_message

    def loop(self):
        if self.debug:
            logging.debug('start mqtt loop')
        self.mqtt.loop_forever()
