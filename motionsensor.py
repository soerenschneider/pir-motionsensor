#!/usr/bin/env python3

import time
import configargparse
import logging

from prometheus_client import start_http_server
from pir import PirSensor
from mqttbackend import MqttBackend

def parse():
    """ Argparse stuff happens here. """
    parser = configargparse.ArgumentParser(prog='motion-sensor')

    parser.add_argument('--id', action="store", env_var="PIR_ID", required=True)
    parser.add_argument('--gpio', action="store", type=int, default=4)
    parser.add_argument('--prom-listen-port', action='store', type=int, env_var='PROM_LISTEN_PORT', default=9191)
    parser.add_argument('--mqtt-host', action='store', env_var='PIR_MQTT_HOST')
    parser.add_argument('--mqtt-topic', action='store', env_var='PIR_MQTT_TOPIC', default="/sensors/pir/{}")
    parser.add_argument('--verbose', action="store_true")
    
    return parser.parse_args()

def setup_logging(args):
    """ Sets up the logging. """
    loglevel = logging.INFO
    if args.verbose:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel, format='%(levelname)s\t %(asctime)s %(message)s')

def setup_prometheus(args):
    """ Starts the prometheus http server. """
    logging.info("Starting prometheus http server on port %s", args.prom_listen_port)
    start_http_server(args.prom_listen_port)
    logging.info("Successfully set up prometheus server!")

def print_config(args):
    logging.info("Started pir motion sensor")
    logging.info("Using id=%s", args.id)
    logging.info("Using gpio=%s", args.gpio)

def initialize_mqtt(args):
    if args.mqtt_host is None:
        return

    backend = MqttBackend(host=args.mqtt_host, location=args.id, topic=args.mqtt_topic)
    return backend

if __name__ == '__main__':
    args = parse()
    setup_logging(args)
    print_config(args)
    setup_prometheus(args)

    callbacks = list()
    mqtt_backend = initialize_mqtt(args)
    if mqtt_backend:
        callbacks.append(mqtt_backend)
    
    p = PirSensor(args, callbacks=callbacks)
    p.run()
