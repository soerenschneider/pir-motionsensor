#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import datetime
import logging

from prometheus_client import Counter, Gauge

class PirSensor:
    def __init__(self, args, callbacks=None):
        self._gpio = args.gpio
        self._id = args.id

        if not callbacks:
            callbacks = list()
        self.callbacks = callbacks

        self._counter = Counter('sensor_pir_motions_detected_total', 'Counter of detected motions', ['location'])
        self._heartbeat = Gauge('sensor_pir_timestamp_seconds', 'Timestamp of last detected motion', ['location'])

    def triggered(self, channel):
        """ Callback when the sensor is triggered. """
        logging.debug("Detected motion")

        # set metrics
        self._counter.labels(location=self._id).inc()
        self._heartbeat.labels(location=self._id).set_to_current_time()

        data = dict()
        data['client'] = self._id

        try:
            for callback in self.callbacks:
                callback.trigger(data)
        except Exception as e:
            logging.error("Error invoking callback: %s", e)

    def run(self):
        try:
            logging.info("Initializing GPIO...")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self._gpio, GPIO.IN)
            while GPIO.input(self._gpio) != 0:
                time.sleep(0.1)
            logging.info("Successfully initialized GPIO!")

            # attach callback to GPIO
            GPIO.add_event_detect(self._gpio, GPIO.RISING, callback=self.triggered)

            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            self.cleanup()
        except Exception as e:
            logging.info("Caught error", e)
            self.cleanup()

    def cleanup(self):
        """ Cleans up current state nicely. """
        logging.warning("Received signal, cleaning up...")
        GPIO.cleanup()

