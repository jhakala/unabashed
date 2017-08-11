from pandas import read_json
from altair import Row, Column, Chart, Text, load_dataset
import json 
from magicXMLsax import makeJSON
from pprint import pprint

def heatmap(data, row, column, color, cellsize=(30, 15)):
   """Create an Altair Heat-Map

   Parameters
   ----------
   row, column, color : str
      Altair trait shorthands
   cellsize : tuple
      specify (width, height) of cells in pixels
   """
   return Chart(data).mark_text(
          applyColorToBackground=True,
        ).encode(
          row=row,
          column=column,
          text=Text(value=' '),
          color=color
        ).configure_scale(
          textBandWidth=cellsize[0],
          bandSize=cellsize[1]
        )

if __name__ == "__main__":
  from sys import argv
  makeJSON(argv[1])
  jsonName = "rbxDelays_tmp.json"
  with open(jsonName) as inFile:
    jsonDict = json.load(inFile)
  print jsonDict

  for depth in range(0,8):
    depthDict = [channel for channel in jsonDict if int(channel["depth"]) == depth]
    if depth == 1:
      pprint(depthDict)
    depthData = read_json(json.dumps(depthDict))
    plot = heatmap(depthData, row="iphi", column="ieta", color="delay")
    plot.savechart("testAltair_depth%i.html" % depth, "html")
  
 
