# liveSense project

liveSense reactor is a multimodule maven project helps to build all components of [liveSense](http://github.com/liveSense).


# What is liveSense?
liveSense is a Java based portal engine utilizes the most recent Java portal technologies, like [Apache Sling](http://sling.apache.org), [Google Widget Tookit](https://developers.google.com/web-toolkit/) and the amazing [OSGi](http://www.osgi.org/) modell. liveSense is a glue, because Sling is a portal API that doesn't contain toolsets that need to build complete portals easy. The goal of liveSense, every developer able to develop web application easy without to spend a lot of time to integrate these technologies. liveSense is a JCR 2.0 compliant CMS (based on Apache Sling and [Apache Jackrabbit](http://jackrabbit.apache.org))

liveSense is a web framework that uses Apache Sling, a Java Content Repository, such as Apache Jackrabbit to store and manage content.

liveSense portal is an extended version of [Apache Sling](http://sling.apache.org), adding some portal functions, as registration framework, email framework, activation framework, thumbnail, captcha.

Sling applications use either scripts or Java servlets, selected based on simple name conventions, to process HTTP requests in a RESTful way.

# How can I start?

To build you have to download 
* Java SDK 1.6
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