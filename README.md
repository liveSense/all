# liveSense project

liveSense reactor is a multimodule maven project helps to build all components of [liveSense](http://github.com/liveSense).

## ABOUT LIVESENSE

liveSense is a Java based web application framework designed for portals, web-based 'cloud' applications and various SAAS-solutions.
liveSense is built on the OSGi modell, which provides a modularized, dynamic runtime environment, where the modules are manageable at runtime.

## TECHNOLOGY

liveSense is based on Apache Sling, which is a content-driven CMS system programmable in several script languages (ESP, Scala, JSP, Freemarker, Groovy). liveSense can operate under any Java-enabled operation system - Windows, Linux, Mac OS X, Solaris - both standalone (it contains integrated web server) and web application - IBM WebSphere, Oracle Weblogic, Apache Tomcat, JBoss - mode. The CMS data can be stored in the file-system or in a relational database.


### GENERAL
* REST-based operation
* SOA-based operation
* ACL-based security model
* LDAP and ActiveDirectory support
* I18N support
* WebDav access of the CMS
* Job and Event handling system
* Virtual domains handling
* Database pooler
* Unified querying for MySQL, Oracle, Firebird, MSSQL
* Remote logging

### APACHE SLING

[Apache Sling](http://sling.apache.org/) is an open source Web framework for the Java platform designed to create content-centric applications on top of a JSR-170-compliant (aka JCR) content repository. Apache Sling allows developers to deploy their application components as OSGi bundles or as scripts and templates in the content repository. Supported scripting languages are JSP, server-side JavaScript, Ruby, Velocity.
The goal of Apache Sling is to expose content in the content repository as HTTP resources, fostering a RESTful style of application architecture.

[More on wikipedia...](http://en.wikipedia.org/wiki/Apache_Sling)

### APACHE JACKRABBIT

[Apache Jackrabbit](http://jackrabbit.apache.org/) is an open source content repository for the Java platform. Jackrabbit used as the reference implementation of JSR-170, specified within the Java Community Process.
Java Content Repository (JCR) specifies an API for application developers (and application frameworks) to use for interaction with modern content repositories that provide content services such as searching, versioning, transactions, etc

[More on wikipedia...](http://en.wikipedia.org/wiki/Apache_Jackrabbit)

### OSGI

The [OSGi framework (Open Services Gateway initiative)](http://www.osgi.org/) is a module system and service platform for the Java programming language that implements a complete and dynamic component model.
Applications or components (coming in the form of bundles for deployment) can be remotely installed, started, stopped, updated, and uninstalled without requiring a reboot; management of Java packages/classes is specified in great detail.
Application life cycle management (start, stop, install, etc.) is done via APIs that allow for remote downloading of management policies. The service registry allows bundles to detect the addition of new services, or the removal of services, and adapt accordingly.

[More on wikipedia...](http://en.wikipedia.org/wiki/OSGi)

### ACTIVITI

[Activiti](http://activiti.org/) is an open-source workflow engine written in Java that can execute business processes described in BPMN 2.0. The project is actually a suite of applications that work together:
* Modeler, a web-based graphical workflow authoring interface based on Signavio.
* Designer, an Eclipse plug-in for developing workflows.
* Engine, the core workflow processor.
* Explorer, a web tool to deploy process definitions, start new process instances and carry-out work on workflows.
* Cycle, a web app for collaboration between business users and software engineers.

[More on wikipedia...](http://en.wikipedia.org/wiki/Activiti_(software))

### APACHE SOLR

[Solr](http://lucene.apache.org/solr/) is an open source enterprise search platform from the Apache Lucene project. Its major features include powerful full-text search, hit highlighting, faceted search, dynamic clustering, database integration, and rich document (e.g., Word, PDF) handling. Providing distributed search and index replication, Solr is highly scalable.
Solr is written in Java and uses the Lucene Java search library at its core for full-text indexing and search, and has REST-like HTTP/XML and JSON APIs that make it easy to use from virtually any programming language. Solr's powerful external configuration allows it to be tailored to almost any type of application without Java coding, and it has an extensive plugin architecture when more advanced customization is required.

[More on wikipedia...](http://en.wikipedia.org/wiki/Apache_Solr)

### GWT

[Google Web Toolkit (GWT)](https://developers.google.com/web-toolkit/) is an open source set of tools that allows web developers to create and maintain complex JavaScript front-end applications in Java. Other than a few native libraries, everything is Java source that can be built on any supported platform with the included GWT Ant build files.
GWT emphasizes reusable, efficient solutions to recurring Ajax challenges, namely asynchronous remote procedure calls, history management, bookmarking, internationalization and cross-browser portability.

[More on wikipedia...](http://en.wikipedia.org/wiki/Google_Web_Toolkit)

### GXT

[GXT](http://www.sencha.com/products/gxt/), also known as Ext GWT is a dual-licensed component framework from Sencha. GXT is a fastest and powerful way to create rich web-based applications using Java.
GXT uses the Google Web Toolkit (GWT) compiler that allows developers to write applications in Java and compile code into highly optimized cross-browser HTML5 and JavaScript.

[See examples...](http://www.sencha.com/products/gxt/examples/)

### JASPER REPORTS

[JasperReports](http://community.jaspersoft.com/project/jasperreports-library) is an open source Java reporting tool that can write to a variety of targets, such as: screen, a printer, into PDF, HTML, Microsoft Excel, RTF, ODT, Comma-separated values or XML files.
It can be used in Java-enabled applications, including Java EE or web applications, to generate dynamic content. It reads its instructions from an XML or .jasper file. JasperReports is part of the Lisog open source stack initiative.

[More on wikipedia...](http://en.wikipedia.org/wiki/JasperReports)

### APACHE CXF

[Apache CXF](http://cxf.apache.org/) is an open-source, fully featured Web services framework. It originated as the combination of two open-source projects: Celtix developed by IONA Technologies and XFire developed by a team hosted at Codehaus. These two projects were combined by people working together at the Apache Software Foundation. The name CXF derives from combining the 'Celtix' and 'XFire' project names.

[More on wikipedia...](http://en.wikipedia.org/wiki/Apache_CXF)

## LICENSE

liveSense is licensed under [Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html), which means the source code is free to use even for developing commercial products.

# How can I start?

To build you have to download

* Sun Java SDK / openJDK 1.6/1.7
* [Maven 3.0.3](http://maven.apache.org/)
* [All modules of liveSense](http://github.com/liveSense/all)
* git 1.7 client

# How can I download source code?

	git clone https://github.com/liveSense/all.git

* Run the following git commands in the directory where the source is checked out

		git submodule init
		git submodule update
		git submodule foreach git pull origin master

* Install the parent project:

		cd parent
		mvn clean install
		cd ..
* Run reactor install

		mvn clean install

* Run the engine

		./liveSense-launchpad.command

* After you start, you can explore it in [http://localhost:8080](http://localhost:8080)