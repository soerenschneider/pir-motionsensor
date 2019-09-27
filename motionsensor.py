#!/usr/bin/env python3

import time
import configargparse
import logging

from prometheus_client import start_http_server

def parse():
    """ Argparse stuff happens here. """
    parser = configargparse.ArgumentParser(prog='motion-sensor')

    parser.add_argument('--id', action="store", env_var="PIR_ID", required=True)
    parser.add_argument('--gpio', action="store", type=int, default=4)
    #parser.add_argument('--host', action="store", env_var="PIR_HOST", required=True)
    #parser.add_argument('--user', action="store", env_var="PIR_USER")
    #parser.add_argument('--topic', action="store", default='house/sensors/{}/motion')
    parser.add_argument('--prom-listen-port', action='store', type=int, env_var='PROM_LISTEN_PORT', default=9191)
    parser.add_argument('--password', action="store", env_var="PIR_PASS")
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

if __name__ == '__main__':
    args = parse()
    setup_logging(args)
    print_config(args)
    setup_prometheus(args)
    time.sleep(600)
