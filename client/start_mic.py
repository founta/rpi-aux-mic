import subprocess

from common import parse_args

args = parse_args()
pid_file = args.pid_file
host = args.host

#start the mic program in the background and save the PID
subprocess.run(["ssh", "%s" % (host), 
                "nohup", "python3", "~/rpi-aux-mic/host/audio_main.py", "&>", "/dev/null", "&",
                "echo", "$!", ">", "%s" % (pid_file)])
