import paho.mqtt.client as mqtt
import time
import logging

from prometheus_client import Counter

class MqttBackend:
    def __init__(self, host, location, topic, port=1883):
        logging.info("Initializing MQTT backend...")
        if not host or not location or not topic:
            raise ValueError("host, location and topic must be set.")

        self._host = host
        self._location = location
        self._port = port
        self._topic = topic.format(location)

        self._prom_msg_error_cnt = Counter('iot_sensors_pir_backend_mqtt_msg_send_errors_total', 'Errors while publishing messages', ['location'])
        self._prom_reconnects = Counter('iot_sensors_pir_backend_mqtt_reconnects_total', 'Client reconnects', ['location'])
        
        self.connect()

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code %s", str(rc))
        self._prom_reconnects.labels(self._location).inc()

    def trigger(self, data):
        self.publish("ON")

    def publish(self, data):
        logging.debug("Publishing '%s' to %s", data, self._topic)
        try:
            self._client.publish(self._topic, data)
        except Exception as e:
            logging.error("Error while publishing message to topic %s: %s", self._topic, e)
            self._prom_msg_error_cnt.labels(self._location).inc()

    def connect(self):
        self._client = mqtt.Client()
        self._client.on_connect = self.on_connect

        self._client.connect_async(self._host, self._port, 60)
        self._client.loop_start()
        logging.info("Async connecting to %s", self._host)
