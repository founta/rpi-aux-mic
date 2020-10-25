import subprocess

from common import parse_args

args = parse_args()
host = args.host
pid_file = args.pid_file

subprocess.run(["ssh", "-q", "%s" % (host), 
                "pkill", "-F", "%s" % (pid_file), "--signal", "2"])
