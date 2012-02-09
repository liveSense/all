package org.liveSense.service.solr.api;

import org.apache.solr.client.solrj.SolrServer;

/**
 * A service to manage the SolrServer implementation.
 */
public interface SolrServerService {

  
	
  /**
   * @return the Current Solr Server, which might be embedded or might be remote depending
   *         on the implementation of the service.
   */
  SolrServer getServer(String serverName);

  /**
   * @return the Solr Server used to perform updates.
   */
  SolrServer getUpdateServer(String serverName);

  /**
   * @return the location of the Solr Home.
   */
  String getSolrHome(String serverName);


}
