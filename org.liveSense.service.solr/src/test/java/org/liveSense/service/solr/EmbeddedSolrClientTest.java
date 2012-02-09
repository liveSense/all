package org.liveSense.service.solr;

import junit.framework.Assert;

import org.apache.commons.io.FileUtils;
import org.apache.solr.core.CoreContainer;
import org.junit.Before;
import org.junit.Test;
import org.liveSense.service.solr.impl.EmbeddedSolrClient;
import org.liveSense.service.solr.impl.LiveSenseResourceLoader;
import org.liveSense.service.solr.impl.Utils;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.osgi.framework.BundleContext;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.framework.ServiceReference;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;
import org.osgi.service.component.ComponentContext;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Dictionary;
import java.util.Hashtable;
import java.util.List;

import javax.xml.parsers.ParserConfigurationException;

public class EmbeddedSolrClientTest {


  @Mock
  private ComponentContext componentContext1;
  @Mock
  private BundleContext bundleContext1;
  @Mock
  private ServiceReference loaderRef1;
  @Mock
  private ServiceReference corecontainerRef1;

  
  @Mock
  private ComponentContext componentContext2;
  @Mock
  private BundleContext bundleContext2;
  @Mock
  private ServiceReference loaderRef2;
  @Mock
  private ServiceReference corecontainerRef2;
  

  private LiveSenseResourceLoader loader = null;

  private CoreContainer coreContainer = null;
  /*
  @Mock
  private ConfigurationAdmin configurationAdmin;
  @Mock
  private Configuration configuration;
  */
  
  public EmbeddedSolrClientTest() {
   MockitoAnnotations.initMocks(this);
  }

  /*
  @Test
  public void testRemoteSolrClient() throws IOException, ParserConfigurationException, SAXException {
    EmbeddedSolrClient embeddedSolrClient = new EmbeddedSolrClient();
    Mockito.when(componentContext.getBundleContext()).thenReturn(bundleContext);
    FileUtils.deleteQuietly(new File("target/slingtest"));
    Mockito.when(bundleContext.getProperty("sling.home")).thenReturn("target/slingtest");
    Dictionary<String, Object> properties = new Hashtable<String, Object>();
    Mockito.when(componentContext.getProperties()).thenReturn(properties);
 */
    
    /*
    embeddedSolrClient.configurationAdmin = configurationAdmin;
    Mockito.when(configurationAdmin.getConfiguration(EmbeddedSolrClient.class.getName()))
        .thenReturn(null);
    Mockito.when(
        configurationAdmin.createFactoryConfiguration(
            "org.apache.sling.commons.log.LogManager.factory.config", null)).thenReturn(
        configuration);

    */
/*    
    embeddedSolrClient.activate(componentContext);
    embeddedSolrClient.enable(null);
    Assert.assertNotNull(embeddedSolrClient.getSolrHome());
    Assert.assertNotNull(embeddedSolrClient.getServer());
    embeddedSolrClient.deactivate(componentContext);
  }
*/
  
  private void setMockForIntstance1(Dictionary<String, Object> properties) throws InvalidSyntaxException, IOException {
    Mockito.when(componentContext1.getBundleContext())
    	.thenReturn(bundleContext1);
	  
    Mockito.when(bundleContext1.getProperty("sling.home"))
    	.thenReturn("target/slingtest");
    
    Mockito.when(bundleContext1.getServiceReferences(LiveSenseResourceLoader.class.getName(), "("+EmbeddedSolrClient.SOLR_EMBEDDED_SERVICE_KEY+"=true"))
    	.thenReturn(new ServiceReference[]{loaderRef1});

    Mockito.when(bundleContext1.getServiceReferences(CoreContainer.class.getName(), "("+EmbeddedSolrClient.SOLR_EMBEDDED_SERVICE_KEY+"=true"))
	.thenReturn(new ServiceReference[]{corecontainerRef1});

    final String solrHome = Utils.getSolrHome(bundleContext1);
    if (loader == null)
    	loader = new LiveSenseResourceLoader(solrHome, this.getClass().getClassLoader());
    if (coreContainer == null)
    	coreContainer = new CoreContainer(loader);
    
    Mockito.when(bundleContext1.getService(loaderRef1))
 	.thenReturn(loader);

    Mockito.when(bundleContext1.getService(corecontainerRef1))
	.thenReturn(coreContainer);

    Mockito.when(componentContext1.getProperties()).thenReturn(properties);

  }

  private void setMockForIntstance2(Dictionary<String, Object> properties) throws InvalidSyntaxException, IOException {
	    Mockito.when(componentContext2.getBundleContext())
    	.thenReturn(bundleContext2);
	  
	    Mockito.when(bundleContext2.getProperty("sling.home"))
	    	.thenReturn("target/slingtest");
	    
	    Mockito.when(bundleContext2.getServiceReferences(LiveSenseResourceLoader.class.getName(), "("+EmbeddedSolrClient.SOLR_EMBEDDED_SERVICE_KEY+"=true"))
	    	.thenReturn(new ServiceReference[]{loaderRef2});
	
	    Mockito.when(bundleContext2.getServiceReferences(CoreContainer.class.getName(), "("+EmbeddedSolrClient.SOLR_EMBEDDED_SERVICE_KEY+"=true"))
		.thenReturn(new ServiceReference[]{corecontainerRef2});
	
	    final String solrHome = Utils.getSolrHome(bundleContext2);
	    if (loader == null)
	    	loader = new LiveSenseResourceLoader(solrHome, this.getClass().getClassLoader());
	    if (coreContainer == null)
	    	coreContainer = new CoreContainer(loader);
	    
	    Mockito.when(bundleContext2.getService(loaderRef2))
	 	.thenReturn(loader);
	
	    Mockito.when(bundleContext2.getService(corecontainerRef2))
		.thenReturn(coreContainer);
	
	    Mockito.when(componentContext2.getProperties()).thenReturn(properties);
  }

  
  @Before
  public void before() {
	  coreContainer = null;
	  loader = null;
  }

  @Test
  public void testEmbedSolrClient_SingleInstance() throws IOException, ParserConfigurationException, SAXException, InvalidSyntaxException {

    FileUtils.deleteQuietly(new File("target/slingtest"));
    
    /* default */

    EmbeddedSolrClient embeddedSolrClient1 = new EmbeddedSolrClient();
    Dictionary<String, Object> properties1 = new Hashtable<String, Object>();

    File fileList = new File("target/test-classes/default");
    properties1.put(EmbeddedSolrClient.PROP_SOLR_IMPORT_ROOT, fileList.getAbsolutePath());
    properties1.put(EmbeddedSolrClient.PROP_SOLR_IMPORT_FILES, getEntries(getFileListing(fileList), fileList));
    properties1.put(EmbeddedSolrClient.PROP_SOLR_CONFIG_FILENAME, EmbeddedSolrClient.DEFAULT_SOLR_CONFIG_FILENAME);
    properties1.put(EmbeddedSolrClient.PROP_SOLR_SCHEMA_FIlNAME, EmbeddedSolrClient.DEFAULT_SOLR_SCHEMA_FILENAME);
    properties1.put(EmbeddedSolrClient.PROP_SOLR_SERVER_NAME, "default");
    
    setMockForIntstance1(properties1);

    /* locations */

    EmbeddedSolrClient embeddedSolrClient2 = new EmbeddedSolrClient();
    Dictionary<String, Object> properties2 = new Hashtable<String, Object>();

    File fileList2 = new File("target/test-classes/locations");
    properties2.put(EmbeddedSolrClient.PROP_SOLR_IMPORT_ROOT, fileList2.getAbsolutePath());
    properties2.put(EmbeddedSolrClient.PROP_SOLR_IMPORT_FILES, getEntries(getFileListing(fileList2), fileList2));
    properties2.put(EmbeddedSolrClient.PROP_SOLR_CONFIG_FILENAME, EmbeddedSolrClient.DEFAULT_SOLR_CONFIG_FILENAME);
    properties2.put(EmbeddedSolrClient.PROP_SOLR_SCHEMA_FIlNAME, EmbeddedSolrClient.DEFAULT_SOLR_SCHEMA_FILENAME);
    properties2.put(EmbeddedSolrClient.PROP_SOLR_SERVER_NAME, "locations");
    
    setMockForIntstance2(properties2);

    /* locations */
    //EmbeddedSolrClient embeddedSolrClient2 = new EmbeddedSolrClient();
    //Mockito.when(componentContext2.getBundleContext()).thenReturn(bundleContext2);

    
    
    /*
    Mockito.when(bundleContext2.getProperty("sling.home")).thenReturn("target/slingtest");
    Dictionary<String, Object> properties2 = new Hashtable<String, Object>();
    properties2.put(EmbeddedSolrClient.PROP_SOLR_SERVER_NAME, "locations");
    
    File fileList2 = new File("target/test-classes/locations");
    properties2.put(EmbeddedSolrClient.PROP_SOLR_IMPORT_ROOT, fileList2.getAbsolutePath());
    properties2.put(EmbeddedSolrClient.PROP_SOLR_IMPORT_FILES, getEntries(getFileListing(fileList2), fileList2));

    Mockito.when(componentContext2.getProperties()).thenReturn(properties2);
    */
    /* */
    /*
    embeddedSolrClient.configurationAdmin = configurationAdmin;
    embeddedSolrClient2.configurationAdmin = configurationAdmin;

    Mockito.when(configurationAdmin.getConfiguration(EmbeddedSolrClient.class.getName()))
        .thenReturn(null);
    
    Mockito.when(
        configurationAdmin.createFactoryConfiguration(
            "org.apache.sling.commons.log.LogManager.factory.config", null)).thenReturn(
        configuration);
    
    */
    embeddedSolrClient1.activate(componentContext1);
    embeddedSolrClient1.enable(null);
    Assert.assertNotNull(embeddedSolrClient1.getSolrHome());
    Assert.assertNotNull(embeddedSolrClient1.getServer());

    embeddedSolrClient2.activate(componentContext2);
    embeddedSolrClient2.enable(null);
    Assert.assertNotNull(embeddedSolrClient2.getSolrHome());
    Assert.assertNotNull(embeddedSolrClient2.getServer());
    
    embeddedSolrClient1.deactivate(componentContext1);
    embeddedSolrClient2.deactivate(componentContext2);
    
  }

  
	/**
	 * Recursively walk a directory tree and return a List of all
	 * Files found; the List is sorted using File.compareTo().
	 *
	 * @param aStartingDir is a valid directory, which can be read.
	 */
	static public List<File> getFileListing(File aStartingDir) throws FileNotFoundException {
		validateDirectory(aStartingDir);
		List<File> result = getFileListingNoSort(aStartingDir);
		Collections.sort(result);
		return result;
	}

	// PRIVATE //
	static private List<File> getFileListingNoSort(File aStartingDir) throws FileNotFoundException {
		List<File> result = new ArrayList<File>();
		File[] filesAndDirs = aStartingDir.listFiles();
		List<File> filesDirs = Arrays.asList(filesAndDirs);
		for (File file : filesDirs) {
			result.add(file); // always add, even if directory
			if (!file.isFile()) {
				// must be a directory
				// recursive call!
				List<File> deeperList = getFileListingNoSort(file);
				result.addAll(deeperList);
			}
		}
		return result;
	}

	/**
	* Directory is valid if it exists, does not represent a file, and can be read.
	*/
	static private void validateDirectory(File aDirectory) throws FileNotFoundException {
		if (aDirectory == null) {
			throw new IllegalArgumentException("Directory should not be null.");
		}
		if (!aDirectory.exists()) {
			throw new FileNotFoundException("Directory does not exist: " + aDirectory);
		}
		if (!aDirectory.isDirectory()) {
			throw new IllegalArgumentException("Is not a directory: " + aDirectory);
		}
		if (!aDirectory.canRead()) {
			throw new IllegalArgumentException("Directory cannot be read: " + aDirectory);
		}
	}
  
  
	private String getEntries(List<File> files, File root) {
		StringBuffer sb = new StringBuffer();

		boolean firstEntry = true;
		for (File file : files) {
			if (!file.isDirectory() && !file.getAbsolutePath().endsWith("solrconfig.xml")
					&& !file.getAbsolutePath().endsWith("schema.xml")) {
				if (firstEntry) {
					firstEntry = false;
				} else {
					sb.append(",");
				}
				// Make the path realative
				sb.append(file.getAbsolutePath().substring(root.getAbsolutePath().length()));
			}
		}
		return sb.toString();

	}
	

}
