/**
 * 
 */
package xmlParser;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.Scanner;

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
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

/**
 * @author John Hakala
 *
 */
public class xmlParser {

  /**
   * 
   */
  public xmlParser() {
    // TODO Auto-generated constructor stub
  }

  /**
   * @param args
   */
  public static void main(String[] args) {
    if (args.length != 3) {
      System.out.println("Please supply three arguments to scaleLEDamps: the scale value, the input directory, and the output directory.");
      System.exit(1);
    }
    boolean debugFlag = false;
    double scaleValue = Double.parseDouble(args[0]);
    File inputDir = new File(args[1]);
    String outputDir = args[2];
    File[] listOfXMLs = inputDir.listFiles();
    for (File xml : listOfXMLs){
      scaleAmplitudes(scaleValue, inputDir.getAbsolutePath()+"/"+xml.getName(), outputDir, debugFlag);
    }
  }
  public static void scaleAmplitudes(double scaleValue, String inputXMLfile, String outputDirName, boolean debugFlag){
    String ledXMLstring = null;
    try {
      ledXMLstring = new Scanner( new File(inputXMLfile) ).useDelimiter("\\A").next();
    } catch (FileNotFoundException e1) {
      // TODO Auto-generated catch block
      e1.printStackTrace();
    }
    DocumentBuilder docBuilder;
    try {

      docBuilder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
      InputSource inputSource = new InputSource();
      inputSource.setCharacterStream(new StringReader(ledXMLstring));
      Document ledXML = docBuilder.parse(inputSource);
      ledXML.getDocumentElement().normalize();


      NodeList dataNodes = ledXML.getDocumentElement().getElementsByTagName("Data");
      for (int iDataNode=0; iDataNode<dataNodes.getLength(); iDataNode++){
        Element dataElement = (Element) dataNodes.item(iDataNode);
        if (dataElement.getAttribute("item").equals("amplitude")){
          System.out.println("\nScaling " + inputXMLfile + ":");
          int amplitudeValue = Integer.parseInt(dataElement.getTextContent());
          System.out.println("Old amplitude value is: " + amplitudeValue);
          double newAmplitudeValue = ((double) amplitudeValue) * scaleValue;
          int newAmplitudeInt = (int) newAmplitudeValue; 
          dataElement.setTextContent(Integer.toString(newAmplitudeInt));
          System.out.println("New amplitude value is: " + newAmplitudeInt);
        }
      }
      
      DOMSource domSource = new DOMSource(ledXML);
      StringWriter writer = new StringWriter();
      StreamResult result = new StreamResult(writer);
      TransformerFactory tf = TransformerFactory.newInstance();
      Transformer transformer = tf.newTransformer();
      transformer.setOutputProperty(OutputKeys.INDENT, "yes");
      transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
      transformer.transform(domSource, result);
      String newLedXMLstring = writer.toString();
      newLedXMLstring = newLedXMLstring.replaceAll("(?m)^[ \t]*\r?\n", "");
      if (debugFlag){
        System.out.println("led XML in file " + inputXMLfile + " is now:");
        System.out.println("---------------------------");
        System.out.println(newLedXMLstring);
        System.out.println("---------------------------");
      }
      
      String[] outputFilePath = inputXMLfile.split("/");
      String outputFileName = outputFilePath[outputFilePath.length-1].replace(".xml", "_scaled"+scaleValue+".xml"); 
      //File outputDir = new File("/Users/johnhakala/output_LED_scaled"+scaleValue);
      File outputDir = new File(outputDirName+scaleValue);
      outputDir.mkdir();
      File outputFile = new File(outputDir+"/"+outputFileName); 
      outputFile.createNewFile();
      FileWriter filewriter = new FileWriter(outputFile);
      filewriter.write(newLedXMLstring);
      filewriter.close();
    }
    catch (DOMException | ParserConfigurationException | SAXException | IOException | TransformerException e) {
      e.printStackTrace();
    }
  }
}
