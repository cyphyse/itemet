# internal
# external
import sys
import os
# logging
import logging
logger = logging.getLogger("Triggerable")

# interface (full app as module fails)
# TODO: there must be an easier way to get 'Triggerable'
plugin_path = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "itemet", "app"
)
sys.path.append(os.path.abspath(plugin_path))
from plugin.triggerable import Triggerable


class Application(Triggerable):
    def __init__(self):
        super().__init__("Gantt")

    def run(self):
        p = self.args.get("path")
        d = self.args.get("dir")
        logger.info("PLUGIN WAS TRIGGERED (file: %s, out: %s)" % (p, d))


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    app = Application()
    app.run()
