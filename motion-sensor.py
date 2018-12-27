#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import datetime
import json
import argparse
import logging
import paho.mqtt.client as mqtt


client = None
args = None


def connect(args):
    """ Connect to the MQTT broker. """
    global client
    client = mqtt.Client(args.id)

    if args.user:
        client.username_pw_set(username=args.user, password=args.password)

    client.connect(args.host)


def triggered(channel):
    """ Callback when the sensor is triggered. """
    data = dict()
    data['client'] = args.id
    data['timestamp'] = datetime.datetime.now().isoformat()

    logging.debug("Detected motion")
    client.publish(args.topic, json.dumps(data), qos=1)


def parse():
    """ Argparse stuff happens here. """
    parser = argparse.ArgumentParser(prog='pir-sensor-reader')

    parser.add_argument('--id', action="store", required=True)
    parser.add_argument('--gpio', action="store", type=int, default=4)
    parser.add_argument('--host', action="store", required=True)
    parser.add_argument('--user', action="store")
    parser.add_argument('--password', action="store")
    parser.add_argument('--topic', action="store", default='house/sensors/{}/motion')
    parser.add_argument('--verbose', action="store_true")
    
    return parser.parse_args()


def cleanup():
    """ Cleans up current state nicely. """
    logging.warning("Bye...")
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()


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
        client.loop_forever()
    except:
        cleanup()


if __name__ == '__main__':
    args = parse()
    connect(args)
    run(args)
