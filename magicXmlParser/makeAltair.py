from os import path, makedirs
from glob import glob
from pandas import read_json
from altair import Row, Column, Chart, Text, load_dataset
import json 
from magicXMLsax import makeJSON
from magicXMLutils import *

# taken from https://altair-viz.github.io/recipes.html#plot-recipes/population
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
  
  from argparse import ArgumentParser
  argParser = ArgumentParser(description = "parses magic xmls and creates JSON representations")
  argParser.add_argument("--mode"  , dest="mode"   ,  
                         help = "either 'single' or 'diff"                   )
  argParser.add_argument("--inXML" , dest="inXML"  ,  
                         help = "for single mode: input filename"            )
  argParser.add_argument("--new"   , dest="new" ,  
                         help = "for diff mode: new input xml filename"      )
  argParser.add_argument("--old"   , dest="old" ,  
                         help = "for diff mode: old input xml filename"      )
  args = argParser.parse_args()

  if args.mode == "single":
    if not args.inXML or args.new or args.old:
      error("Please pick one and only one input file  with the --inXML option")
    else:
      inFileNames = [args.inXML]
  if args.mode == "diff":
      if  not (args.new and args.old) or args.inXML:
        error("Please pick one and only one new file and one and only one old file  with the --new and --old options")
      else:
        inFileNames = [args.old, args.new]
  outJSONnames = []
  outPlotsDir = "outputPlots"
  if not path.exists(outPlotsDir):
    makedirs(outPlotsDir)
  outPlotNames = []
  first = True
  for inFileName in inFileNames:
    if not path.isdir(inFileName):
      outJSONnames.append(path.basename(inFileName.replace(".xml", ".json")))
      outPlotNames.append("plot_{}".format(outJSONnames[-1].replace(".json", "")))
    else:
      # TODO HACK HACK
      for inFile in glob("{}/*.xml".format(inFileName)):
        outJSONnames.append("ledAmplitudes_" + path.basename(inFile).replace(".xml", ".json"))
    makeJSON(inFileName, outJSONnames[-1])
 
    if path.isdir(inFileName):
      fullList = []
      for outJSON in outJSONnames: 
        with open(path.join("outputJSONs", outJSON)) as partialListFile:
          partialList = json.load(partialListFile)
          for channel in partialList:
            channel["eta"] = str(int(channel["side"])*int(channel["eta"]))
          fullList.extend(partialList)
      with open(path.join("outputJSONs", "tmp_fullJSON.json"), "w") as outFullJSON:
        json.dump(fullList, outFullJSON)
        outJSONnames = [path.basename(outFullJSON.name)]
        outPlotNames = ["plot_{}".format(outFullJSON.name.replace(".json", ""))]

  if args.mode == "single":
    info("making visualization of " + inFileName)
    plotName = outJSONnames[0]

  elif args.mode == "diff":
    with open(path.join("outputJSONs", outJSONnames[0])) as inFile:
      old = json.load(inFile)
    with open(path.join("outputJSONs", outJSONnames[1])) as inFile:
      new = json.load(inFile)
    for channelNew in new: 
      for channelOld in old:
        if channelNew["ieta"] == channelOld["ieta"] and channelNew["iphi"] == channelOld ["iphi"] and channelNew["depth"] == channelOld["depth"]:
          channelNew["delay"] = str(int(channelNew["delay"]) - int(channelOld["delay"]))
    outDiffName = 'diff_{}_{}'.format(outJSONnames[0].replace(".json",""), outJSONnames[1])
    with open(path.join("outputJSONs", outDiffName), "w") as outFile:
      json.dump(new, outFile)
    plotName = outDiffName
  else:
    error("invalid mode '{0}': must be either 'diff' or 'single'".format(args.mode))
    exit(1)
    
  with open(path.join("outputJSONs", plotName)) as inFile:
    jsonDict = json.load(inFile)

  for depth in range(1,10):
    depthDict = [channel for channel in jsonDict if int(channel["depth"]) == depth]
    # TODO probably can have pandas directly read the dict instead of going back to JSON first
    depthData = read_json(json.dumps(depthDict))
    plot = heatmap(depthData, row="phi", column="eta", color="amplitude")
    plot.savechart(path.join(outPlotsDir, "{}_depth{}.json".format(plotName.replace(".json", ""), depth)), "json")
