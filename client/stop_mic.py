import subprocess

from common import parse_args

args = parse_args()
pid_file = args.pid_file
host = args.host

#kill the process and remove the pid file
subprocess.check_output(["ssh", "-q", "%s" % (host), 
                        "pkill", "-F", pid_file, "--signal", "2", ";",
                        "rm", "-f", pid_file])
