import subprocess
import os
import signal
from time import sleep
from forcelink import force_symlink
# this is a hack to avoid complex log rotation and deal with the difficulty of circular-buffer-style logs
# basically it tail -f's the log into two copies,
# then, staggered by half a day, it clears a copy and restarts one copy process
# always pointing at copy that wasn't just cleared

# Start by making both processes... would be nicer to start proc2 later but it's not as easy
args1 = "./mkLog1.sh"
args2 = "./mkLog2.sh"
copyProc1 = subprocess.Popen(args1, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
copyProc2 = subprocess.Popen(args2, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
force_symlink("log1.xml", "log_copy.xml")
while True:
  # now wait half a day before moving to the second copy
  sleep(60*60*12)
  force_symlink("log2.xml", "log_copy.xml")
  # kill the first copy process, remove its log, and restart it
  # copyProc1.kill()
  os.killpg(os.getpgid(copyProc1.pid), signal.SIGTERM)
  copyProc1.wait()
  os.remove("log1.xml")
  copyProc1 = subprocess.Popen(args1, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
  # wait half the day before moving back to the first copy
  sleep(60*60*12)
  force_symlink("log1.xml", "log_copy.xml")
  # now kill the second process, remove its log, and restart it
  #copyProc2.kill()
  os.killpg(os.getpgid(copyProc2.pid), signal.SIGTERM)
  copyProc2.wait()
  os.remove("log2.xml")
  copyProc2 = subprocess.Popen(args2, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
  

  

