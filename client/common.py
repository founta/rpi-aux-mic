import argparse
import json

def parse_args():
  #load config file
  with open("config.json",'r') as f:
    config = json.loads(f.read())

  host_default = config['host']
  pid_file_default = config['pid_file']

  parser = argparse.ArgumentParser()
  parser.add_argument("--host", default=host_default, nargs="?", type=str, 
                      help="Host that rpi-aux-mic is installed on")
  parser.add_argument("--pid_file", default=pid_file_default, nargs="?", type=str, 
                      help="The file to save the PID in")

  args = parser.parse_args()
  
  return args
