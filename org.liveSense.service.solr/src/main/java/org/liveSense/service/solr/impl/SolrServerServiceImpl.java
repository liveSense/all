package org.liveSense.service.solr.impl;

import java.util.Map;

import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Reference;
import org.apache.felix.scr.annotations.ReferenceCardinality;
import org.apache.felix.scr.annotations.ReferencePolicy;
import org.apache.felix.scr.annotations.ReferenceStrategy;
import org.apache.felix.scr.annotations.References;
import org.apache.felix.scr.annotations.Service;
import org.apache.solr.client.solrj.SolrServer;
import org.liveSense.service.solr.api.SolrClient;
import org.liveSense.service.solr.api.SolrServerService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.collect.Maps;

@Component(immediate = true, metatype = false)
@Service(value = SolrServerService.class)
@References(
		value={
				@Reference(name="solrClients", cardinality=ReferenceCardinality.OPTIONAL_MULTIPLE,policy=ReferencePolicy.DYNAMIC,strategy=ReferenceStrategy.EVENT,bind="bind",unbind="unbind",referenceInterface=SolrClient.class)
		})
public class SolrServerServiceImpl implements SolrServerService {

	private static Logger log = LoggerFactory.getLogger(SolrServerServiceImpl.class);
	private Map<String, SolrClient> servers = Maps.newConcurrentMap();

	public SolrServer getServer(String serverName) {
		return servers.get(serverName).getServer();
	}

	public SolrServer getUpdateServer(String serverName) {
		return servers.get(serverName).getUpdateServer();
	}

	public String getSolrHome(String serverName) {
		return servers.get(serverName).getSolrHome();
	}
	
	public void bind(SolrClient client) {
		log.info("Binding solrCore - "+client.getName());
		servers.put(client.getName(), client);
	}

	public void unbind(SolrClient client) {
		log.info("Unbinding solrCore - "+client.getName());
		servers.remove(client.getName());
	}

}
