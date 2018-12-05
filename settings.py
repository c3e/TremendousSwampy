"""
PATTERN RULES
{
    'SUB': '#',
    'TAGS': {TAGNAME': 'TOPIC'|INDEX for TOPIC.split("/")|any fixed value except integer or 'TOPIC', ...},
    'MEASUREMENT': INDEX for TOPIC.split("/")|any fixed value,
    'TYPE': bool|int|float|str|any fixed value
}
"""

PATTERNS = [
    {'SUB': 'foobar/oben/lounge/leinwand/action',
     'TAGS': {'TOPIC': 'TOPIC', 'ROOM': -3},
     'MEASUREMENT': "leinwand", 'TYPE': str
     },
    {'SUB': 'foobar/+/tuer',
     'TAGS': {'location': -2},
     'MEASUREMENT': "door_status", 'TYPE': int
     },
    {'SUB': '/hq/og/baellebad/sensoren/temperatur',
     'TAGS': {'location': -3},
     'MEASUREMENT': "temperature", 'TYPE': float
     },
        {'SUB': '$SYS/#',
     'TAGS': {'TOPIC': 'TOPIC', 'format': -1},
     'MEASUREMENT': "mqtt_statistic", 'TYPE': float
     }
]
