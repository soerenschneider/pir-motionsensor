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
    client.connect(args.host)

    if args.user:
        client.username_pw_set(username=args.user, password=args.password)

    client.loop_start()


def triggered():
    """ Callback when the sensor is triggered. """
    data = dict()
    data['client'] = args.id
    data['timestamp'] = datetime.datetime.now().isoformat()

    if args.verbose:
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
    parser.add_argument('--topic', action="store", default='house/sensors/motion')
    parser.add_argument('--verbose', action="store_true")
    
    return parser.parse_args()


def cleanup():
    """ Cleans up current state nicely. """
    logging.info("Bye...")
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()


def run(args):
    try:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s\t %(asctime)s %(message)s')

        GPIO.setmode(GPIO.BCM)
        gpio = args.gpio

        # Set pin as input
        GPIO.setup(gpio, GPIO.IN)

        logging.info("Initializing GPIO")
        while GPIO.input(gpio) != 0:
            time.sleep(0.1)
        logging.info("Done!")

        # attach callback to GPIO
        GPIO.add_event_detect(gpio, GPIO.RISING, callback=triggered)
        while True:
            time.sleep(60)

    except:
        cleanup()



if __name__ == '__main__':
    args = parse()
    connect(args)
    run(args)
