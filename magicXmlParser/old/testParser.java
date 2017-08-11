import java.io.File;
import java.io.IOException;
import java.io.StringWriter;

import java.lang.StringBuffer;

import java.util.HashMap;
import java.util.Map;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.DOMException;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.xml.sax.SAXException;

/**
 * @author John Hakala
 */
public class testParser extends DefaultHandler {

  /**
   *   Scans a logcollector XML file and returns a JSON map 
   *   of apps types and how many logs they've posted
   */
  // instantiate a map to keep tally of the number of logs from each type of app
  ledBrick ledBrickTmp;
  private StringBuffer curAmpValue = new StringBuffer(2048);
  private StringBuffer curRbxName = new StringBuffer(2048);
  String curKind;
  Map<String, Integer> ampsMap;
  File inDir;
  String fileName;
  public testParser(String inDirName) {
    this.ampsMap = new HashMap<String, Integer>();
    this.inDir = new File(inDirName);
    
    File[] listOfXMLs = this.inDir.listFiles();
    for (File xml : listOfXMLs){
      this.fileName = this.inDir.getAbsolutePath()+"/"+xml.getName();
      parseXmlFile();
    }
    printMap();
  }

  // usual xml parsing stuff
  private void parseXmlFile() {
    try {
      SAXParserFactory factory = SAXParserFactory.newInstance();
      SAXParser saxParser = factory.newSAXParser();
      saxParser.parse(fileName, this);
    }
    catch (DOMException | ParserConfigurationException | SAXException | IOException e) {
      e.printStackTrace();
    }
  }

  // the event nodes correspond to a log amplitude
  @Override
    public void startElement(String s, String s1, String elementName, Attributes attributes) throws SAXException {
      if (elementName.equals("CFGBrick")) {
        ledBrickTmp = new ledBrick();
      }
      if (elementName.equals("Parameter")) {
        if (attributes.getValue("name").equals("RBX")) {
          curKind = "rbx";
        }
        else {
          curKind = "other";
        }
      }
      if (elementName.equals("Data")) {
        if (attributes.getValue("item").equals("amplitude")) {
          curKind = "amplitude";
        }
      }
    }

  @Override
    public void characters(char ch[], int start, int length) throws SAXException{
      if (curKind == "rbx") {
        curRbxName.append(ch, start, length);
      }
      else if (curKind == "amplitude") {
        curAmpValue.append(ch, start, length);
      }
    }

  @Override
    public void endElement(String s, String s1, String element) throws SAXException {
      if (element.equals("Data")) {
          curKind = "other";
      }
      if (element.equals("Parameter")) {
          curKind = "other";
      }
      if (element == "CFGBrick"){
        ledBrickTmp.rbx = curRbxName.toString();
        ledBrickTmp.amplitude = curAmpValue.toString();
        ampsMap.putIfAbsent(ledBrickTmp.rbx, Integer.parseInt(ledBrickTmp.amplitude));
        curAmpValue.delete(0, curAmpValue.length());
        curRbxName.delete(0, curRbxName.length());
      }
    }

  // manually build a JSON map -- Gson doesn't come installed everywhere
  public void printMap(){
    System.out.println("{");
    Boolean first = true;
    for (String rbxKey : ampsMap.keySet()) {
      if (!first) { System.out.print(",\n");}
      System.out.print('"' + rbxKey + "\" : " + ampsMap.get(rbxKey));
      first = false;
    }
    System.out.print("\n}");
    // sends the JSON to stdout
  }

  public static void main(String[] args) {
    if (args.length != 1) {
      System.out.println("Please supply one argument: the input directory.");
      System.exit(1);
    }
    boolean debugFlag = true;
    new testParser(args[0]);
  }
}
