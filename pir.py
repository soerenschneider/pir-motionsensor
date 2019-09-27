#!/usr/bin/env python3

import RPi.GPIO as GPIO
import smbus
import time
import datetime
import logging

class PirSensor:
    prefix = 'sensors_pir'

    def __init__(self, args, callbacks=None):
        self._id = args.id

        if callbacks:
            self.callbacks = callbacks

        self._counter = Counter(f'{prefix}_motions_detected_total', 'Counter of detected motions', ['location'], registry=_registry)
        self._heartbeat = Gauge(f'{prefix}_timestamp_seconds', 'Timestamp of last detected motion', ['location'], registry=_registry)

    def triggered(self, channel):
        """ Callback when the sensor is triggered. """
        logging.debug("Detected motion")

        # set metrics
        self._counter.labels(location=self.id).inc()
        self._heartbeat.set_to_current_time()

        data = dict()
        data['client'] = self._id

        try:
            for callback in callbacks:
                callback.triggered(data)
        except Exception as e:
            logging.error("Error invoking callback: %s", e)

    def run(self, args):
        try:
            logging.info("Initializing GPIO...")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(args.gpio, GPIO.IN)
            while GPIO.input(args.gpio) != 0:
                time.sleep(0.1)
            logging.info("Successfully initialized GPIO!")

            # attach callback to GPIO
            GPIO.add_event_detect(args.gpio, GPIO.RISING, callback=triggered)
        except:
            self.cleanup()

    def cleanup(self):
        """ Cleans up current state nicely. """
        logging.warning("Received signal, cleaning up...")
        GPIO.cleanup()

