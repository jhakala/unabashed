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
public class logParser extends DefaultHandler {

  /**
   *   Scans a logcollector XML file and returns a JSON map 
   *   of apps types and how many logs they've posted
   */
  // instantiate a map to keep tally of the number of logs from each type of app
  logEvent logEventTmp;
  private StringBuffer curCharValue = new StringBuffer(2048);
  Map<String, Integer> logsMap;
  String fileName;
  String loggerNodeValue;
  String appType;
  String[] loggerNodeArray;
  String[] parts;
  public logParser(String fileName) {
    this.logsMap = new HashMap<String, Integer>();
    this.fileName = fileName;
    parseLogFile();
    printMap();
  }

  // usual xml parsing stuff
  private void parseLogFile() {
    try {
      SAXParserFactory factory = SAXParserFactory.newInstance();
      SAXParser saxParser = factory.newSAXParser();
      saxParser.parse(fileName, this);
    }
    catch (DOMException | ParserConfigurationException | SAXException | IOException e) {
      e.printStackTrace();
    }
  }

  // the event nodes correspond to a log message
  @Override
    public void startElement(String s, String s1, String elementName, Attributes attributes) throws SAXException {
      if (elementName.equals("log4j:event")) {
        logEventTmp = new logEvent();
        logEventTmp.logger = attributes.getValue("logger");
      }
      if (elementName.equals("log4j:message")) {
        curCharValue.delete(0, curCharValue.length());
      }
    }

  @Override
    public void characters(char ch[], int start, int length) throws SAXException{
      curCharValue.append(ch, start, length);
    }

  @Override
    public void endElement(String s, String s1, String element) throws SAXException {
      if (element.equals("log4j:event")) {
        loggerNodeValue = logEventTmp.logger;
        appType = "unknown";
        // the logger attribute has a name like 'cms.hcal.hcal::someapp.instance(0)'
        // we want to grab the type of app, in the example, 'hcal::someapp'
        loggerNodeArray = loggerNodeValue.split("\\.");
        for (int iLoggerPart = 0; iLoggerPart < loggerNodeArray.length; iLoggerPart++) {

          // most apps say their name right before their instance number or lid number
          if (loggerNodeArray[iLoggerPart].contains("lid") || loggerNodeArray[iLoggerPart].contains("instance")){
            appType = loggerNodeArray[iLoggerPart - 1];
          }
        }
        if (appType == "unknown") {
          // others don't have an instance number, their name is at the end
          appType = loggerNodeArray[loggerNodeArray.length - 1];
          parts = appType.split(":");
          if (parts[0].equals("p")){
            // some logs don't really say the name of the app writing them
            // instead they show up just as a port on a host
            // for some of these logs though though, CDATA section of the message has info
            appType = "unknown";
            if (logEventTmp.message != null) {
              if (logEventTmp.message.split("CDATA\\[")[1].contains("profile")) {
                // the messages about loading the profile don't identify themselves much at all
                appType = "xdaq profile loading message";
              }
              else {
                // most of the rest have the code's name at the beginning of the CDATA
                appType = "xdaq startup message: " + logEventTmp.message.split("CDATA\\[")[1].split(" ")[0].split("]]")[0];
              }
            }
          }
        }
        // fill all the app types into a hashmap
        logsMap.putIfAbsent(appType, 0);
        // keep track of how many logs by that app type are found
        logsMap.put(appType, logsMap.get(appType) + 1);
      }
    }

  // manually build a JSON map -- Gson doesn't come installed everywhere
  public void printMap(){
    System.out.println("{");
    Boolean first = true;
    for (String appKey : logsMap.keySet()) {
      if (!first) { System.out.print(",\n");}
      System.out.print('"' + appKey + "\" : " + logsMap.get(appKey).toString());
      first = false;
    }
    System.out.print("\n}");
    // sends the JSON to stdout
  }

  public static void main(String[] args) {
    if (args.length != 1) {
      System.out.println("Please supply one argument: the input logfile.");
      System.exit(1);
    }
    boolean debugFlag = true;
    new logParser(args[0]);
  }

  private static String nodeToString(Node node) {
    // taken from 
    // https://stackoverflow.com/questions/6534182/java-geting-all-content-of-a-xml-node-as-string
    StringWriter sw = new StringWriter();
    try {
      Transformer t = TransformerFactory.newInstance().newTransformer();
      t.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
      t.transform(new DOMSource(node), new StreamResult(sw));
    } catch (TransformerException te) {
      System.out.println("nodeToString Transformer Exception");
    }
    return sw.toString();
  }
}
