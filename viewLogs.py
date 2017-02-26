#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from commands import getoutput
from ansi2html import ansi2html

# John Hakala, 2/25/17

def getLastLogMessages(lines):
  #dirName = "~johakala/testLogDir"
  #incantation = "tail -%i %s/Logs_hcalpro.xml | ~hcalpro/scripts/Handsaw.pl" % (lines, dirName)
  incantation = "tail -%i /nfshome0/elaird/errors.txt" % lines
  return getoutput(incantation)
  

def formatMessages(messages):
  formattedMessages = "<br><br><tt>"
  # do colors here?
  for line in messages.splitlines():
    formattedMessages += ansi2html(line)
    formattedMessages+="<br>"
  formattedMessages += "</tt>"
  return formattedMessages

form = cgi.FieldStorage()
numberOfLines =  form.getvalue('numberOfLines')

html =  "<html><body>"

try: 
  nLines = int(numberOfLines)
  if nLines > 0:
    html += "Showing last %i lines of logcollector logs" % nLines
    html += formatMessages(getLastLogMessages(nLines))
  else:
    html += "the numberOfLines submitted seems to be a weird number: <tt> %s </tt>" % str(numberOfLines)
except ValueError:
    html += "the numberOfLines submitted does not seem to be a number <tt> %s </tt>" % str(numberOfLines)


html += "</body></html>"

print "Content-type: text/html"
print
print html
