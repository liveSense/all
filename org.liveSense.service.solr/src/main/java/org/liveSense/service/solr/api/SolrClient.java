package org.liveSense.service.solr.api;

import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;

import org.apache.solr.client.solrj.SolrServer;
import org.liveSense.service.solr.impl.SolrClientListener;
import org.xml.sax.SAXException;

public interface SolrClient {

	/**
	 * @return the name of the client.
	 */
	String getName();

	// this is not the same interface as SolrServerService to enable us to have
	// all solr clients active at the same time.
	/**
	 * @return the Current Solr Server, which might be embedded or might be
	 *         remote depending on the implementation of the service.
	 */
	SolrServer getServer();

	/**
	 * @return the Solr Server used to perform updates.
	 */
	SolrServer getUpdateServer();

	/**
	 * @return the location of the Solr Home.
	 */
	String getSolrHome();

	/**
	 * Enable the client and set the Solr listener.
	 * @param listener
	 * @throws IOException
	 * @throws ParserConfigurationException
	 * @throws SAXException
	 */
	void enable(SolrClientListener listener) throws IOException,
			ParserConfigurationException, SAXException;

	/**
	 * Disable the client.
	 */
	void disable();

}
