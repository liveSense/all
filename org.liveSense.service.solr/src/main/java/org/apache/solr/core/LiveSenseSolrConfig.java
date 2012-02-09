package  org.apache.solr.core;

import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;

public class LiveSenseSolrConfig extends SolrConfig {

  public LiveSenseSolrConfig(SolrResourceLoader loader, String name, InputSource is)
      throws ParserConfigurationException, IOException, SAXException {
    super(loader, name, is);
  }

}
