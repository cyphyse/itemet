# -*- coding: <utf-8>
# intern
from .. import app
from . triggerable import EXIT_CODE
# external
import sys
import os
import subprocess
import time
import glob
import pandas as pd

# logging
import logging
logger = logging.getLogger(__file__)


PLUGIN_PATH = os.path.dirname(__file__)


class Trigger():
    """Triggers an application with arguments of a triggerable application."""

    def __init__(self):
        pass

    def init(self, apps, store):
        self.dir_with_apps = os.path.abspath(apps)
        self.dir_out = os.path.abspath(store)
        self.app_data_model = {}
        # search apps with app pattern
        for path in glob.glob(self.dir_with_apps):
            self.app_data_model.update({
                    os.path.abspath(path): {
                        "t0": time.time()
                    }
                }
            )
        logger.info("Found: " + str(self.app_data_model))
        paths = list(self.app_data_model.keys())
        names = [os.path.basename(os.path.dirname(p)) for p in paths]
        status = ["ok" for p in paths]
        data = {
            "name": names,
            "status": status
        }
        self.df = pd.DataFrame(data, index=paths)
        self.start()

    def update_status(self):
        """Writes status"""
        with open(os.path.join(self.dir_out, 'appstatus.html'), 'w') as fp:
            self.df.to_html(fp)

    def call(self, app_path, file_path, dt):
        """Executes triggerable application"""
        try:
            cmd = []
            # make interface findable
            cmd.append("PYTHONPATH='" + PLUGIN_PATH + "'")
            # run plugins in same python environment TODO: decide to remove
            cmd.append(sys.executable)
            # build app start command
            cmd.append(app_path)
            cmd.append("-d='" + self.dir_out + "'")
            cmd.append("-p='" + file_path + "'")
            cmd.append("-t='" + str(dt) + "'")
            logger.info("Call '" + str(cmd) + "' ...")
            proc = subprocess.Popen(" ".join(cmd), shell=True)
            proc.wait()
            if proc.returncode > 0:
                for s, v in EXIT_CODE.items():
                    if proc.returncode == v:
                        self.df.loc[app_path, "status"] = s
            else:
                self.df.loc[app_path, "status"] = "ok"
        except Exception as err:
            self.df.loc[app_path, "status"] = err

    def start(self):
        """Function which is called on program start"""
        t1 = time.time()
        for app_path, app_info in self.app_data_model.items():
            self.call(app_path, "", 0)
            self.app_data_model[app_path]["t0"] = t1
        self.update_status()
        return self

    def on_event(self, filepath):
        """Function which is called on data event"""
        for idx, row in self.df.iterrows():
            row.loc["status"] = "open"
        t1 = time.time()
        logger.info(filepath)
        for app_path, app_info in self.app_data_model.items():
            dt = t1 - app_info["t0"]
            self.call(app_path, filepath, dt)
            self.app_data_model[app_path]["t0"] = t1
        self.update_status()

    def stop(self):
        """[NOT USED] Function which is called on program stop"""
        self.observer.stop()
        for app_path, app_info in self.app_data_model.items():
            self.call(app_path, "", -1)
        self.update_status()



plugintrigger = Trigger()
