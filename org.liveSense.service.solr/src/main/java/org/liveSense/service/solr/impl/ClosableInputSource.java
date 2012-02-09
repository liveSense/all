package org.liveSense.service.solr.impl;

import java.io.IOException;
import java.io.InputStream;

import org.xml.sax.InputSource;

public class ClosableInputSource extends InputSource {
	private InputStream in;

	public ClosableInputSource(InputStream in) {
		super(in);
		this.in = in;
	}
	public void close() throws IOException {
		in.close();
	}
	
}
