
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.Parser;
import org.apache.tika.sax.BodyContentHandler;
import org.xml.sax.SAXException;
public class ParserExtraction {
public static void main(final String[] args) throws
IOException,TikaException, SAXException {
//Assume boy.jpg is n your current directory
File file=new File(args[0]);
//Parser method parameters
File file2= new File("buffer.txt");
FileOutputStream fop = new FileOutputStream(file2) ;

	// if file doesn't exists, then create it
	if (!file2.exists()) {
		file2.createNewFile();
	}

Parser parser = new AutoDetectParser();
BodyContentHandler handler = new BodyContentHandler(fop);
Metadata metadata = new Metadata();
FileInputStream inputstream = new FileInputStream(file);
ParseContext context = new ParseContext();
parser.parse(inputstream, handler, metadata, context);
//System.out.println(handler.toString());
//getting the list of all meta data elements
//System.out.println("hi");
/*String[] metadataNames = metadata.names();
for(String name : metadataNames){
System.out.println(name + ": " + metadata.get(name));

}*/
	// get the content in bytes
	
	//fop.flush();
	fop.close();

	System.out.println("Done");


}
}
