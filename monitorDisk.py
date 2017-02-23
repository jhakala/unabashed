from commands import getoutput
from optparse import OptionParser
from time import sleep
from datetime import datetime

# John Hakala - Feb 13, 2017

def getRecipients() :
  # these are your @cern.ch email account names
  return ["john.charles.hakala"]  

def sendWarning(hostName, dir, percent, waitBeforeWarningAgain):
  timestamp =  datetime.now().strftime("%Y-%m-%d %H:%M")
  message = "%s : \n Warning! The machine %s has %i percent usage in %s!" % (timestamp, hostName, percent, dir)
  print message
  for recipient in getRecipients():
    print getoutput("/nfshome0/hcalpro/bin/mailOut.pl '%s' 'Disk usage warning -- %s:%s' '%s'" % (recipient, hostName, dir, message))
  sleep(waitBeforeWarningAgain)

if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-n", "--hostName" ,  dest="hostName" ,  default="hcalutca01"      ,
                    help = "the hostname of the machine to watch disk space on [default=hcalutca01]"     ) 
  parser.add_option("-d", "--dir"      ,  dest="dir"      ,  default="/tmp"            ,
                    help = "the dir to check on the specified host [default=/tmp]"                       ) 
  parser.add_option("-s", "--sleep"    ,  dest="sleep"    ,  default=10              , type=int , 
                    help = "the sleep time between polls of the disk usage [default=10]"                 ) 
  parser.add_option("-w", "--warnDelay",  dest="warnDelay",  default=60*10           , type=int , 
                    help = "the time to wait before sending another warning [default=600 (ten minutes)]" ) 
  parser.add_option("-p", "--percent"  ,  dest="percent"  ,  default=90              , type=int , 
                    help = "the max percentage before sending warnings [default=90]"                     ) 
  parser.add_option("-v", action="store_true"  ,  dest="verbose",  default=False  , 
                    help = "print out the usage percent to the command-line"                             ) 
  parser.add_option("-e", action="store_true"  ,  dest="email",  default=False  , 
                    help = "send emails on warnings"                                                     ) 
  (options, args) = parser.parse_args()
  
  incantation = "ssh %s 'df -h'" % options.hostName
  while True:
    response = getoutput(incantation)
    foundLine = False
    for line in response.splitlines():
      if options.dir in line:
        foundLine = True
        percent=int(line.split()[3].replace("%",""))
        if (options.verbose):
          print "percent usage of %s on %s: %i" % (options.dir, options.hostName, percent)
        if (percent > options.percent):
          sendWarning(options.hostName, options.dir, percent, options.warnDelay)
    if not foundLine:
      print "requested dir (%s) not found in response from df on %s. response: \n %s" % (
        options.dir, options.hostName, response
      )
      exit(1)
      
    sleep(options.sleep)
  
  
