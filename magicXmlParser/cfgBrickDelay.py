from copy import deepcopy
from magicXMLsax import CfgBrick
from magicXMLutils import *

# This class is a special implementation of a CfgBrick that specializes it to parsing RBX delay cfgBricks
# TODO a class like this will be needed for each kind of magicXML
class CfgBrickDelay(CfgBrick):
  def __init__(self, outFileName):
    info("Parsing magic xml of type: RBX Delays")
    CfgBrick.__init__(self)
    self.rbx = "test"
    self.qieDelays = {}
    self.tmpDict = {}
    self.tmpKinds = ["RBX", "Data"]
    self.resultName = "rbxDelays"
    self.outFileName = self.resultName + "_" + outFileName

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

    for channel in emap.listAll():
      foundChannel = False
      if channel["RBX"] in self.qieDelays.keys():
        for qieDelay in self.qieDelays[channel["RBX"]]:
          if channel["RM"] == qieDelay["rm"] and int(channel["card"])*int(channel["QIE"]) == int(qieDelay["qie"]):
            channel["delay"] = qieDelay["delay"]
            foundChannel = True
      if not foundChannel:
        emap.emap.remove(channel)

    keepKey = "delay"
    self.formatJson(keepKey, emap.emap)
