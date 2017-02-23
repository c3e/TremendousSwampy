from paho.mqtt.client import MQTTMessage
from lib.swamp import  set_value, set_measurement, set_tags

def test_set_measurement():
    split_topic = ["some", "odd", "topic", "measurement"]
    pattern = {'MEASUREMENT': "leinwand"}
    assert set_measurement(pattern, split_topic) == "leinwand"

    pattern = {'MEASUREMENT': -1}
    assert set_measurement(pattern, split_topic) == split_topic[-1]

def test_set_value():
    pattern = {'TYPE': int}
    msg = MQTTMessage()
    msg.payload = b'-3'
    assert set_value(pattern, msg) == -3

    pattern = {'TYPE': float}
    assert set_value(pattern, msg) == -3.0

    pattern = {'TYPE': str}
    assert set_value(pattern, msg) == "-3"

    pattern = {'TYPE': bool}
    assert set_value(pattern, msg) is True

    msg.payload = "off"
    assert set_value(pattern, msg) is False

    pattern = {'TYPE': "FIXED VALUE"}
    assert set_value(pattern, msg) == "FIXED VALUE"

def test_set_tags():
    pattern = {'TAGS': {'TOPIC': 'TOPIC', 'ROOM': -2, 'ACTION': "fixed"}}
    msg = MQTTMessage()
    msg.topic = "some/odd/topic/test/measurement"
    msg.payload = "some payload"
    split_topic = msg.topic.split("/")
    assert set_tags(pattern, msg, split_topic) == {'topic': msg.topic, 'room': 'test', 'action': 'fixed'}