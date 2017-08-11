from os import path, makedirs
from pandas import read_json
from altair import Row, Column, Chart, Text, load_dataset
import json 
from magicXMLsax import makeJSON
from pprint import pprint

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
  argParser.add_argument("--new"   , dest="newXML" ,  
                         help = "for diff mode: new input xml filename"      )
  argParser.add_argument("--old"   , dest="oldXML" ,  
                         help = "for diff mode: old input xml filename"      )
  args = argParser.parse_args()

  if args.mode == "single" or args.new or args.old:
    if not args.inXML:
      print "Please pick one and only one input file  with the --inXML option"
      exit(1)
    else:
      inFileNames = [args.inXML]
  if args.mode == "diff":
      if  not (args.new and args.old) or args.inXML:
        print "Please pick one and only one new file and one and only one old file  with the --new and --old options"
        exit(1)
      else:
        inFileNames = [args.old, args.new]
  print inFileNames
  outJSONnames = []
  outPlotsDir = "outputPlots"
  if not path.exists(outPlotsDir):
    makedirs(outPlotsDir)
  outPlotNames = []
  first = False
  for inFileName in inFileNames:
    outJSONnames.append("rbxDelays_%s"%path.basename(args.inXML.replace(".xml", ".json")))
    outPlotNames.append("plot_{}".format(outJSONnames[-1].replace(".json", "")))
    makeJSON(args.inXML, outJSONnames[-1])

    if args.mode == "single":
      print "making visualization of", inFileName
      with open(path.join("outputJSONs", outJSONnames[0])) as inFile:
        jsonDict = json.load(inFile)

      for depth in range(1,10):
        depthDict = [channel for channel in jsonDict if int(channel["depth"]) == depth]
        if depth == 1:
          pprint(depthDict)
        # TODO probably can have pandas directly read the dict instead of going back to JSON first
        depthData = read_json(json.dumps(depthDict))
        plot = heatmap(depthData, row="iphi", column="ieta", color="delay")
        plot.savechart(path.join(outPlotsDir, "{}_depth{}.json".format(outPlotNames[-1], depth)), "json")

    elif args.mode == "diff":
      if first:
        print "making visualization diff between {0} and {1}".format(inFileNames[0], inFileNames[1])
        first = False
    else:
      print "invalid mode '{0}': must be either 'diff' or 'single'".format(args.mode)
      exit(1)
