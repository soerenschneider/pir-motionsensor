#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import datetime
import json
import logging
from prometheus_client import Counter


class PirSensor:
    def __init__(self):
        self._movements = Counter('sensor')
        c = Counter('my_failures', 'Description of counter')
c.inc()     # Increment by 1
c.inc(1.6)  # Increment by given value

    def triggered(channel):
        """ Callback when the sensor is triggered. """
        data = dict()
        data['client'] = args.id
        data['timestamp'] = datetime.datetime.now().isoformat()

        logging.debug("Detected motion")
        _client.publish(args.topic, json.dumps(data), qos=1)


    def cleanup():
        """ Cleans up current state nicely. """
        logging.warning("Bye...")
        GPIO.cleanup()
        _client.loop_stop()
        _client.disconnect()


    def setup_logging(args):
        """ Sets up the logging. """
        loglevel = logging.INFO
        if args.verbose:
            loglevel = logging.DEBUG
        logging.basicConfig(level=loglevel, format='%(levelname)s\t %(asctime)s %(message)s')


    def run(args):
        try:
            setup_logging(args)

            args.topic = args.topic.format(args.id)

            logging.info("Initializing GPIO")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(args.gpio, GPIO.IN)
            while GPIO.input(args.gpio) != 0:
                time.sleep(0.1)
            logging.info("Done!")

            # attach callback to GPIO
            GPIO.add_event_detect(args.gpio, GPIO.RISING, callback=triggered)

            # loop
            _client.loop_forever()
        except:
            cleanup()


if __name__ == '__main__':
    args = parse()
    connect(args)
    run(args)
