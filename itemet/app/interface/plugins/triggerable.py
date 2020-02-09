# -*- coding: <utf-8>
# extern
import json
import argparse
# logging
import logging
logger = logging.getLogger(__file__)


EXIT_CODE = {
    "ok": 0,
    "errors detected": 100,
    "consistency": 200
}


class Triggerable(object):
    """Universal interface for all triggerable applications"""

    def __init__(self, name):
        self.name = name
        # parse arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--dir")
        parser.add_argument("-p", "--path")
        parser.add_argument("-t", "--time")
        self.args = vars(parser.parse_args())
        self.is_begin = self.args.get('time') == str(0)
        self.is_end = self.args.get('time') == str(-1)
        logger.debug(
            "Started '" + self.name + "'" + \
            " with args: \n" + json.dumps(self.args, indent=2))
