import paho.mqtt.client as mqtt
import time
import logging

class MqttBackend:
    def __init__(self, host, location, topic="/sensors/pir/{}", port=1883):
        self._host = host
        self._location = location
        self._port = port
        self._topic = topic.format(location)

        self._client = mqtt.Client()
        self._client.on_connect = self.on_connect

        self._prom_msg_error_cnt = Counter('iot_sensors_pir_backend_mqtt_msg_send_errors_total', 'Errors while publishing messages', ['location'])
        self._prom_reconnects = Counter('iot_sensors_pir_backend_mqtt_reconnects_total', 'Client reconnects', ['location'])
        
        self.connect()

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code ", str(rc))
        self._prom_reconnects.labels(self._location).inc()

    def trigger(self, data):
        self.publish(data)

    def publish(self, data):
        logging.debug(f"Publishing '{data}' to {self._topic}")
        try:
            self._client.publish(self._topic, data)
        except Exception as e:
            logging.error("Error while publishing message to topic", self._topic)
            self._prom_msg_error_cnt.labels(self._location).inc()

    def connect(self):
        self._client.connect_async(self._host, self._port, 60)
        self._client.loop_start()