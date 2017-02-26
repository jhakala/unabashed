import subprocess
from time import sleep
from forcelink import force_symlink
import shlex
# this is a hack to avoid complex log rotation and deal with the difficulty of circular-buffer-style logs
# basically it tail -f's the log into two copies,
# then, staggered by half a day, it clears a copy and restarts one copy process
# always pointing at copy that wasn't just cleared

# Start by making both processes... would be nicer to start proc2 later but it's not as easy
copyProc1 = subprocess.Popen("./mkLog1.sh")
copyProc2 = subprocess.Popen("./mkLog2.sh")
force_symlink("log1.xml", "log_copy.xml")
while True:
  # now wait half a day before moving to the second copy
  sleep(60*60*12)
  force_symlink("log2.xml", "log_copy.xml")
  # kill the first copy process, remove its log, and restart it
  copyProc1.kill()
  os.remove("log1.xml")
  copyProc1 = subprocess.Popen(args1)
  # wait half the day before moving back to the first copy
  sleep(60*60*12)
  force_symlink("log2.xml", "log_copy.xml")
  # now kill the second process, remove its log, and restart it
  copyProc2.kill()
  os.remove("log2.xml")
  copyProc2 = subprocess.Popen(args2)
  

  

