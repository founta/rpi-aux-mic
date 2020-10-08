import subprocess

import argparse
import json

#load config file
with open("config.json",'r') as f:
  config = json.loads(f.read())

host_default = config['host']

parser = argparse.ArgumentParser()
parser.add_argument("--host", default=host_default, nargs="?", type=str, 
                    help="Host that rpi-aux-mic is installed on")

args = parser.parse_args()
host = args.host

subprocess.check_output(["ssh", "-q", "%s" % (host), "python3", "~/rpi-aux-mic/host/echo.py"])
