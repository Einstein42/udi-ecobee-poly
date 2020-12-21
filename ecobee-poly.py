#!/usr/bin/env python3

import sys
CLOUD = False
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
    CLOUD = True

from nodes import Controller

import logging
LOGGER = polyinterface.LOGGER
# I want this logging
#logging.Formatter('%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')
# Default Format is:         '%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s'
#                            '%(asctime)s %(threadName)-10s %(module)-13s %(levelname)-8s %(funcName)s: %(message)s [%(module)s:%(funcName)s]'
#polyinterface.set_log_format('%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(message)s [%(module)s:%(funcName)s]')

if __name__ == "__main__":
    if sys.version_info < (3, 5):
        LOGGER.error("ERROR: Python 3.5 or greater is required not {}.{}".format(sys.version_info[0],sys.version_info[1]))
        sys.exit(1)
    try:
        polyglot = polyinterface.Interface('Ecobee')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
