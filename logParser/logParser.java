import java.io.File;
import java.io.IOException;
import java.io.StringWriter;

import java.util.HashMap;
import java.util.Map;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
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
public class logParser {

  /**
   *   Scans a logcollector XML file and returns a JSON map 
   *   of apps types and how many logs they've posted
   */
  public logParser() {
    // TODO Auto-generated constructor stub
  }

  /**
   * @param args input logfile name
   */
  public static void main(String[] args) {
    if (args.length != 1) {
      System.out.println("Please supply one argument: the input logfile.");
      System.exit(1);
    }
    boolean debugFlag = true;
    File xmlFile = new File(args[0]);
    indexLogs(xmlFile, debugFlag);
  }
  public static void indexLogs(File xmlFile,  boolean debugFlag){
    // instantiate a map to keep tally of the number of logs from each type of app
    Map<String, Integer> logsMap = new HashMap<String, Integer>();
    
    // usual xml parsing stuff
    DocumentBuilder docBuilder;
    try {
      docBuilder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
      Document ledXML = docBuilder.parse(xmlFile);
      ledXML.getDocumentElement().normalize();

      // the event nodes correspond to a log message
      NodeList eventNodes = ledXML.getDocumentElement().getElementsByTagName("log4j:event");
      for (int iEventNode=0; iEventNode<eventNodes.getLength(); iEventNode++){
        // the "logger" attribute tells what has written that log message
        String loggerNodeValue = eventNodes.item(iEventNode).getAttributes().getNamedItem("logger").getNodeValue();
        String appType = "unknown";
        // the logger attribute has a name like 'cms.hcal.hcal::someapp.instance(0)'
        // we want to grab the type of app, in the example, 'hcal::someapp'
        String[] loggerNodeArray = loggerNodeValue.split("\\.");
        for (int iLoggerPart = 0; iLoggerPart < loggerNodeArray.length; iLoggerPart++) {
          // most apps say their name right before their instance number or lid number
          if (loggerNodeArray[iLoggerPart].contains("lid") || loggerNodeArray[iLoggerPart].contains("instance")){
            appType = loggerNodeArray[iLoggerPart - 1];
          }
        }
        if (appType == "unknown") {
          // others don't have an instance number, their name is at the end
          appType = loggerNodeArray[loggerNodeArray.length - 1];
          String[] parts = appType.split(":");
          if (parts[0].equals("p")){
            // some logs don't really say the name of the app writing them
            // instead they show up just as a port on a host
            // for some of these logs though though, CDATA section of the message has info
            appType = "unknown";
            if (nodeToString(eventNodes.item(iEventNode)).split("CDATA\\[")[1].contains("profile")) {
              // the messages about loading the profile don't identify themselves much at all
              appType = "xdaq profile loading message";
            }
            else {
              // most of the rest have the code's name at the beginning of the CDATA
              appType = "xdaq startup message: " + nodeToString(eventNodes.item(iEventNode)).split("CDATA\\[")[1].split(" ")[0].split("]]")[0];
            }
          }
        }
        // fill all the app types into a hashmap
        logsMap.putIfAbsent(appType, 1);
        // keep track of how many logs by that app type are found
        logsMap.put(appType, logsMap.get(appType) + 1);
      }
      // manually build a JSON map -- Gson doesn't come installed everywhere
      System.out.println("{");
      Boolean first = true;
      for (String appType : logsMap.keySet()) {
        if (!first) { System.out.print(",\n");}
        System.out.print('"' + appType + "\" : " + logsMap.get(appType).toString());
        first = false;
      }
      System.out.print("\n}");
      // sends the JSON to stdout
    }
    catch (DOMException | ParserConfigurationException | SAXException | IOException e) {
      e.printStackTrace();
    }
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
