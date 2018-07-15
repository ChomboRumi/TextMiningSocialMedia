package flujoSimple;

import java.io.File;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import io.vertx.core.buffer.Buffer;
import io.vertx.core.json.JsonArray;
import io.vertx.core.json.JsonObject;

public class xmlJsonm {
	
	public static void main(String[] args) throws ParserConfigurationException, SAXException, IOException {
		List<String> folders = new ArrayList<>();
		folders.add("test");
		folders.add("training");		
		folders.stream().forEach(n -> {
		File xml= new File("/home/ramon/Escritorio/pan-ap17-bigdata/"+n);
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
		File[] files = xml.listFiles(
			    new FilenameFilter()
			    {
			        public boolean accept(final File a_directory,
			                              final String a_name)
			        {
			            return a_name.endsWith(".xml");
			            // Or could use a regular expression:
			            //
			            //     return a_name.toLowerCase().matches(".*\\.(gif|jpg|png)$");
			            //
			        };
			    });
		FileWriter fileWriter;
		try {
			fileWriter = new FileWriter("/home/ramon/Escritorio/frases_"+n+".json");

		PrintWriter printWriter = new PrintWriter(fileWriter);
		JsonObject obj = new JsonObject();
		for(File file:files) {
			DocumentBuilder dBuilder= dbFactory.newDocumentBuilder();
			Document doc = dBuilder.parse(file);
			Element root = doc.getDocumentElement();
			Node child1 = root.getChildNodes().item(1);
			NodeList list = child1.getChildNodes();
			JsonArray o = new JsonArray();
			for (int i =0; i<list.getLength(); i++) {
				String data = list.item(i).getTextContent();
				if(!data.equalsIgnoreCase("\n\t\t")) {
					o.add(list.item(i).getTextContent());
				}
				
			}
			obj.put(file.getName().replace(".xml", ""), o);
		}
		printWriter.println(obj.toString());
		printWriter.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ParserConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SAXException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		});
		
		
	}

}
