import logging
import os
import paho.mqtt.client as mqtt
import yaml

from yaml_lambda import *
from influx import Influx
import vault


class MQTT2InfluxDB():

    def __init__(self, config_path='config.yml'):
        with open(config_path) as cfg_file:
            self.config = yaml.safe_load(cfg_file)

        influx_config = vault.read_data('secret/mqtt2influx/influxdb')
        self.mqtt_config = vault.read_data('secret/mqtt2influx/mqtt')

        self.influx = Influx(
            influx_config['host'], influx_config['port'],
            influx_config['user'], influx_config['pass'],
            self.obj_get(self.config, 'influx_db', 'mqtt2influxdb'),
        )

    def obj_get(self, obj, key, default=None):
        if key in obj:
            return obj[key]
        return default

    def on_connect(self, client, userdata, flags, rc):
        topics = [(topic, 1) for topic in self.config['subscriptions'].keys()]
        result, _ = client.subscribe(topics)

        if result != mqtt.MQTT_ERR_SUCCESS:
            raise(Exception('MQTT subscribe failed: {}'.format(result)))

        logging.info('MQTT connected and subscribed to {n} topics'.format(
            n=len(topics),
        ))

    def on_message(self, client, userdata, msg):
        points = []

        for processor in self.obj_get(self.config['subscriptions'], msg.topic, []):
            tffn = self.obj_get(processor, 'transform',
                                YAMLLambda('x: float(x)'))
            value = tffn.run(msg.payload)

            points.append({
                'measurement': processor['metric'],
                'tags': self.obj_get(processor, 'tags', {}),
                'fields': {
                    'value': value,
                },
            })

            logging.debug(
                'MQTT Message received: topic={topic} metric={metric} value={value}'.format(
                    topic=msg.topic,
                    metric=processor['metric'],
                    value=value,
                ))

        if len(points) > 0:
            logging.info('Submitting {n} datapoints for topic {topic}'.format(
                n=len(points),
                topic=msg.topic,
            ))
            self.influx.submit(points)

    def run(self):
        client = mqtt.Client()
        client.enable_logger()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.username_pw_set(
            self.obj_get(os.environ, 'MQTT_USER', self.mqtt_config['user']),
            self.obj_get(os.environ, 'MQTT_PASS', self.mqtt_config['pass']),
        )

        logging.debug('Connecting to MQTT broker...')

        client.connect(
            self.obj_get(os.environ, 'MQTT_HOST', self.mqtt_config['host']),
            self.obj_get(os.environ, 'MQTT_PORT',
                         self.obj_get(self.mqtt_config, 'port', 1883)),
            keepalive=10,
        )

        client.loop_forever()


if __name__ == '__main__':
    loglevel = logging.INFO
    if 'LOG_LEVEL' in os.environ and os.environ['LOG_LEVEL'] == 'DEBUG':
        loglevel = logging.DEBUG

    configpath = 'config.yml'
    if 'CONFIG_PATH' in os.environ:
        configpath = os.environ['CONFIG_PATH']

    logging.basicConfig(
        datefmt='%m/%d/%Y %I:%M:%S %p',
        format='[%(asctime)s][%(levelname)s] %(message)s',
        level=loglevel,
    )

    inst = MQTT2InfluxDB(configpath)
    inst.run()
