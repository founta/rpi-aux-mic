import subprocess

from common import parse_args

args = parse_args
pid_file = args.pid_file
host = args.host

#start the mic program in the background and save the PID
subprocess.check_output(["ssh", "-q", "%s" % (host), 
                        "python3", "~/rpi-aux-mic/host/echo.py", "&", ";",
                        "echo", "$!", ">", "~/rpi-aux-mic/host/MICPID_FILE"])
