import subprocess

from common import parse_args

args = parse_args()
host = args.host

subprocess.check_output(["ssh", "-q", "%s" % (host), 
                         "pkill", "-f", "echo.py", "--signal", "2"])
