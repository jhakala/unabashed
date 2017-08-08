/**
 * 
 */
//package logParser;

import java.io.File;
import java.io.FileNotFoundException;
//import java.io.FileWriter;
import java.io.IOException;
//import java.io.StringReader;
import java.io.StringWriter;
//import java.util.Scanner;

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
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

/**
 * @author John Hakala
 *
 */
public class logParser {

  /**
   * 
   */
  public logParser() {
    // TODO Auto-generated constructor stub
  }

  /**
   * @param args
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
    Map<String, Integer> logsMap = new HashMap<String, Integer>();
    DocumentBuilder docBuilder;
    try {

      docBuilder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
      Document ledXML = docBuilder.parse(xmlFile);
      ledXML.getDocumentElement().normalize();


      NodeList eventNodes = ledXML.getDocumentElement().getElementsByTagName("log4j:event");
      for (int iEventNode=0; iEventNode<eventNodes.getLength(); iEventNode++){
        String loggerNodeValue = eventNodes.item(iEventNode).getAttributes().getNamedItem("logger").getNodeValue();
        String appType = "unknown";
        String[] loggerNodeArray = loggerNodeValue.split("\\.");
        for (int iLoggerPart = 0; iLoggerPart < loggerNodeArray.length; iLoggerPart++) {
          if (loggerNodeArray[iLoggerPart].contains("lid") || loggerNodeArray[iLoggerPart].contains("instance")){
            appType = loggerNodeArray[iLoggerPart - 1];
          }
        }
        if (appType == "unknown") {
          appType = loggerNodeArray[loggerNodeArray.length - 1];
          String[] parts = appType.split(":");
          //for (String part : parts){ 
          //  System.out.println(part);
          //}
          if (parts[0].equals("p")){
            appType = "unknown";
            //System.out.println(nodeToString(eventNodes.item(iEventNode)));
            //System.out.println(nodeToString(eventNodes.item(iEventNode)).split("CDATA\\[")[1].split(" ")[0]);
            if (nodeToString(eventNodes.item(iEventNode)).split("CDATA\\[")[1].contains("profile")) {
              appType = "xdaq profile loading message";
            }
            else {
              appType = "xdaq startup message: " + nodeToString(eventNodes.item(iEventNode)).split("CDATA\\[")[1].split(" ")[0].split("]]")[0];
            }
          }
        }
        logsMap.putIfAbsent(appType, 1);
        logsMap.put(appType, logsMap.get(appType) + 1);
      }
      System.out.println("{");
      Boolean first = true;
      for (String appType : logsMap.keySet()) {
        if (!first) { System.out.print(",\n");}
        System.out.print('"' + appType + "\" : " + logsMap.get(appType).toString());
        first = false;
      }
      System.out.print("\n}");
      //if (dataElement.getAttribute("item").equals("amplitude")){
      //  System.out.println("\nScaling " + inputXMLfile + ":");
      //  int amplitudeValue = Integer.parseInt(dataElement.getTextContent());
      //  System.out.println("Old amplitude value is: " + amplitudeValue);
      //  double newAmplitudeValue = ((double) amplitudeValue) * scaleValue;
      //  int newAmplitudeInt = (int) newAmplitudeValue; 
      //  dataElement.setTextContent(Integer.toString(newAmplitudeInt));
      //  System.out.println("New amplitude value is: " + newAmplitudeInt);
      //}
    }
    catch (DOMException | ParserConfigurationException | SAXException | IOException e) {
      e.printStackTrace();
    }
  }


  private static String nodeToString(Node node) {
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
