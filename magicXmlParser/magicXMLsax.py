from xml.sax import saxutils, handler, make_parser
from copy import deepcopy

# John Hakala 8/10/17

# base class for defining the parser for any kind of magic xml
class CfgBrick():
  def __init__(self):
    self.elementType = "CFGBrick"
    self.tmpContent = ""
    self.tmpKind = "other"

  def clearContent(self):
    self.tmpContent = ""

  def setKind(self, kind):
    self.tmpKind = kind

  def resetKind(self):
    self.tmpKind = "other"

  def startElement(self, elementName, attributes):
    if (elementName == "Parameter"):
      self.setKind(attributes.getValue("name"))

  def contentFiller(self, innerText):
    self.tmpContent = innerText

  def endDocument(self):
    pass

# This class is a special implementation of a CfgBrick that specializes it to parsing RBX delay cfgBricks
# TODO a class like this will be needed for each kind of magicXML
class CfgBrickDelay(CfgBrick):
  def __init__(self):
    print "RBX Delays"
    CfgBrick.__init__(self)
    self.rbx = "test"
    self.qieDelays = {}
    self.tmpDict = {}
    self.tmpKinds = ["RBX", "Data"]

  def startElement(self, elementName, attributes):
    if elementName == "Parameter":
      if attributes.getValue("name") == "RBX":
        self.tmpKind = "RBX"
    if elementName == "Data":
      self.tmpKind = "Data"
      self.tmpDict = {"qie": attributes.getValue("qie"), "rm":attributes.getValue("rm")}
    

  def contentFiller(self, innerText):
    if self.tmpKind in self.tmpKinds:
      self.tmpContent = innerText
    
  def endElement(self, elementName):
    if self.tmpKind == "RBX":
      self.rbx = self.tmpContent
      self.qieDelays[self.rbx]=[]
      self.clearContent()

    elif self.tmpKind == "Data":
      self.tmpDict["delay"] = self.tmpContent
      self.clearContent()
      self.qieDelays[self.rbx].append(deepcopy(self.tmpDict))
      self.tmpDict = {}

  def endDocument(self):
    from john_emapParser import emapper
    # TODO make this settable via argument
    emap = emapper("HCALmapHBHEP17_J.txt")
    emap.parseEmap()

    # TODO this could be moved to a function that isn't specific for RBX delays
    # right now this is just where we stick the json formatting stuff
    for channel in emap.listAll():
      foundChannel = False
      if channel["RBX"] in self.qieDelays.keys():
        for qieDelay in self.qieDelays[channel["RBX"]]:
          if channel["RM"] == qieDelay["rm"] and int(channel["card"])*int(channel["QIE"]) == int(qieDelay["qie"]):
            channel["delay"] = qieDelay["delay"]
            foundChannel = True
      if not foundChannel:
        emap.emap.remove(channel)

    keepKeys = ["ieta", "iphi", "depth", "delay"]
    for channel in emap.emap:
      for key in channel.keys():
        if not key in keepKeys:
          del channel[key]
    import json
    # TODO make this configurable
    with open("rbxDelays_tmp.json", "w") as outFile:
      json.dump(emap.emap, outFile)
      
    
  
# this is meant to be a generic sax parser for all the different kind of magic xmls
# to parse different types of magic xmls, you endow its' "self.brick" member object
# which will direct it to pull the particular stuff of interest from the xml
class magicSAX(handler.ContentHandler):
  def __init__(self):
    self.brick = CfgBrick()
    handler.ContentHandler.__init__(self)
    self.outDict = {}

    ## TODO this will need to be changed for all different kinds of magicXMLs
    self.validInfoTypes = ["DELAY"]
  
  # this factory is used so that the handler can inherit specific 
  def CfgBrickFactory(self, infotype):
    if infotype in self.validInfoTypes:
      print "Parsing magicXML of type:",
    else:
      print "the infotype found was not valid:", infotype

    ## TODO this will need to be changed for all different kinds of magicXMLs
    if infotype == "DELAY":
      self.brick = CfgBrickDelay()

  def startElement(self, elementName, attributes):
    self.brick.startElement(elementName, attributes)

  def characters(self, innerText):
    self.brick.contentFiller(innerText)

  def endElement(self, elementName):
    # this infotype parameter should come first
    # based on it, we cast the magicSAX's member "brick" to a particular kind of brick
    # corresponding to a a given kind of magic xml
    # the different bricks it inherits from overload the handler's methods to grab only
    # the relevant chunks from the xml depending on the infotype parameter
    if self.brick.tmpKind == "INFOTYPE":
      self.CfgBrickFactory(self.brick.tmpContent)
      self.brick.clearContent()
    else:
      self.brick.endElement(elementName)
    self.brick.tmpKind = "other"

  def endDocument(self):
    self.brick.endDocument()

    
# function to call if you want to dump a json from another python script (e.g. makeAltair.py)
def makeJSON(inputName):
  from os.path import isfile, isdir
  if isfile(inputName):
    inFile = inputName
  elif isfile(inputName):
    inDir = inputName
    print "parsing directories of xmls is not yet supported"
    exit(1)
  else:
    print "the input specified does not seem to be a valid file or directory:", inputName
     
  saxParser = make_parser()
  saxParser.setContentHandler(magicSAX())
  saxParser.parse(inFile)

if __name__ == "__main__":
  
  from argparse import ArgumentParser
  argParser = ArgumentParser(description = "parses magic xmls and creates JSON representations")
  argParser.add_argument("--inXML" , dest="inXML" ,  help = "input filename"        )
  args = argParser.parse_args()

  if not args.inXML:
    print "Please pick one and only one input file or one input directory"
    exit(1)
  makeJSON(args.inXML)
