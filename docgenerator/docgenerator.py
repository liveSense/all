#!/usr/bin/python
import json
from pprint import pprint
import sys
import re
import httplib
import base64
import string
import os.path
import StringIO
import urllib
import urllib2
import subprocess
import fileinput
import cookielib

# This module uses the poster library that can do multipart HTTP POSTs
# To install, use: easy_install poster
# http://atlee.ca/software/poster/
import poster
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

from xml.dom.minidom import parseString

#####################################
## PARAMETERS
#####################################
PROJECT='org.liveSense'
PROJECTDIR="../"

WIKISERVER = "http://localhost/"
WIKIINDEXPHP = "mediawiki/index.php"
WIKIAPI    = "mediawiki/api.php"
WIKIUSER="yourusername"
WIKIPASSWORD="yourpassword"
WIKIID=1
WIKITITLEPREFIX="liveSense";
WIKIPACKAGELISTPAGE="liveSensePackages"

WIKILINKS=[
{"symbolicNamePrefix" : "org.liveSense", "link":"[http://github.com/liveSense/%(symbolicName)s %(name)s - %(symbolicName)s (%(version)s)]"}
]

MARKDOWNLINKS=[
{"symbolicNamePrefix" : "org.liveSense", "link":"__[%(name)s - %(symbolicName)s (%(version)s)](http://github.com/liveSense/%(symbolicName)s)__"}
]

CONSOLEUSER = "admin"
CONSOLEPASSWORD = "admin"
CONSOLEHOST= "localhost"
CONSOLEPORT = 8080

colorModel= ["yellow", "green", "\"/blues3/3\"",  "\"/blues3/2\"", "\"/blues3/1\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\""]

###################################

def dictify(text):
	lst = text.split(" ")
	lst = filter(lambda x: "=" in x, lst)
	lkup = {}
	for l in lst:
		t1 = l.split("=")
		lkup[t1[0]]=t1[1].strip('"').strip("'")
	return lkup

def wikiLogin(opener,host,api,user,pw):
	reqdata = urllib.urlencode({"format":"xml","action":"login","lgname":user})
	req = urllib2.Request(host + api,reqdata)

	handle = opener.open(req)
	t = handle.read()
	lkup = dictify(t)
	print t

	reqdata = urllib.urlencode({"lgtoken":lkup["token"],"format":"xml","action":"login","lgname":user,"lgpassword":pw})
	req = urllib2.Request(host + api,reqdata)
	handle = opener.open(req)
	t = handle.read()
	print t

def wikiEditApiPhp(opener,host,api,title,text):
	reqdata = urllib.urlencode({"action":"tokens","type":"edit","format":"xml"})
	req = urllib2.Request(host + api,reqdata)
	t = opener.open(req).read()
	params = dictify(t)

	datagen, headers = multipart_encode([("action","edit"),("title",title),("text",text),("token",params["edittoken"]),("format","xml")])
	req = urllib2.Request(host + api,datagen,headers)
	t = opener.open(req).read()
#  print "Title '%s'  Result: %s" % (title,t)


def travelDependencies(bundles={}, id=0, root=True, recursion=0, parent=-1, nodes={}, connections={}, recursionStack=[], dotfileCache={}, nodeDefined={}):

	# Find id on recursion stack
	if (len(recursionStack)>0):
		for stack_id in recursionStack:
			if stack_id == id:
#				print "ID is already on stack! - Break iteration ID: "+str(id)
				return

	if root:
		dotfileCache.clear()
		nodeDefined.clear()
		recursionStack = []
		nodes.clear()
		nodes[0] = []
		nodes[0].append(bundles[id])
		nodeDefined[id] = True;

	recursionStack.append(id)

	if (len(bundles[id]['dependencies'])<=0 or id == 0):
		if (len(recursionStack)>0):
			recursionStack.pop()
		return
	else:
		dotfileToDisplay = []
		for dep_id in bundles[id]['dependencies']:
			if not id in dotfileCache:
				 dotfileCache[id] = {}
				 
			if not dep_id in dotfileCache[id] and dep_id != 0:
				dotfileCache[id][dep_id] = True;
				dotfileToDisplay.append(dep_id);

			for dep_id in dotfileToDisplay:
				if dep_id not in nodeDefined:
					nodeDefined[dep_id] = True;
					if not nodes.has_key(recursion+1):
						nodes[recursion+1] = []
					nodes[recursion+1].append(bundles[dep_id])

		for dep_id in dotfileToDisplay:
			if not connections.has_key(recursion):
				connections[recursion] = []
			connections[recursion].append({"from":bundles[id], "to": bundles[dep_id]})
#
			travelDependencies(bundles, dep_id, False, recursion+1, id, nodes, connections, recursionStack, dotfileCache, nodeDefined);

	if (len(recursionStack)>0):
		recursionStack.pop()
	return
	

def readBundlesFromConsole(host, port, user, passwd):
	# Reading all bundles and parsing it
	headers = {'Authorization' : 'Basic ' + string.strip(base64.encodestring(user + ':' + passwd))}

	bundles = {};
	conn = httplib.HTTPConnection(host, 8080)
	conn.request("GET", "/system/console/bundles.json", "", headers)
	res = conn.getresponse()

	if res.status == 200 :
		json_data = res.read()
		data = json.loads(json_data)
		for obj in data['data'] :
			bundles[obj['id']] = obj;
	
	# Reading the sub package info
	for id in bundles.keys() : 
		conn = httplib.HTTPConnection(host, 8080)
		conn.request("GET", "/system/console/bundles/"+str(id)+".json", "", headers)
		res = conn.getresponse()
		if res.status == 200 :
			json_data = res.read()

			data = json.loads(json_data)

			importBundleId = set([])
			importBundleData = []
			exportBundleData = []
			embedJars = []
			for obj in data['data'][0]['props'] :
				if (obj['key'] == 'Imported Packages') :
					for v in obj['value'] :
						if 	v != 'None' :
							m = re.match(r'(?P<package>.*),version\=(?P<version>.*) from <a href=\'.*\'>(?P<bundle>.*) \((?P<id>.*)\)', v)
							importBundleId.add(int(m.group('id')))
							importBundleData.append({'id' : int(m.group('id')), 'package' : m.group('package'), 'bundle' : m.group('bundle'), 'version' : m.group('version')})
				if (obj['key'] == 'Exported Packages') :
					for v in obj['value'] :
						if 	v != '-' :
							m = re.match(r'(?P<package>.*),version\=(?P<version>.*)', v)
							exportBundleData.append({'package' : m.group('package'), 'version' : m.group('version')})
				if (obj['key'] == 'Bundle Classpath') :
					for v in obj['value'].split(",") :
						if v != '.' :
							embedJars.append(v)
							
			bundles[id]['dependencies'] = importBundleId
			bundles[id]['importpackages'] = importBundleData
			bundles[id]['exportpackages'] = exportBundleData
			bundles[id]['embedjars'] = embedJars
		else:
			pprint("Error: "+str(res.status))
	return bundles	

def umlName(bundle):
	return bundle['symbolicName'].replace(".","_").replace("-","_")

def writeDot(bundles, projectdesc, dot=StringIO.StringIO(), colorModel= ["yellow", "green", "\"/blues3/3\"",  "\"/blues3/2\"", "\"/blues3/1\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\"", "\"/greys3/2\""]):
	dot.write("digraph {\n\tnode[shape=record, fontname=\"Arial\", fontsize=8]")

	# Write Nodes
	for key in dotnodes.keys():
		for obj in dotnodes[key]:
			dot.write("node [style=filled, fillcolor="+colorModel[key]+", label= "+"\"{"+obj['name']+" | "+obj['symbolicName']+"("+obj['version']+")}\"] "+umlName(obj)+";\n")

	# Write connections
	for key in dotconnections.keys():
		for obj in dotconnections[key]:
			dot.write(umlName(obj['from'])+" -> "+umlName(obj['to'])+" [color="+colorModel[key]+"];\n")

	# Ranking level1 connections to same level
	for i in range(1,2):
		if dotnodes.has_key(i):
			dot.write("{rank=same;")
			for obj in dotnodes[i]:
				dot.write(umlName(obj)+";");
			dot.write("};")
				
	dot.write("}\n\n")
	return dot


def writeWiki(bundles, projectdesc, project = "", wiki = StringIO.StringIO(), links = []):
	wiki.write("= ["+projectdesc['name']+" - "+projectdesc['symbolicName']+"] =\n")
	wiki.write("== Description ==\n");
	wiki.write(projectdesc['description']+"\n")

	if projectdesc.has_key('exportpackages'):
		wiki.write("== OSGi Exported packages ==\n");
		for exp in projectdesc['exportpackages'] :
			wiki.write("* "+exp['package']+"("+exp['version']+")\n");

	if projectdesc.has_key('dependencies'):
		wiki.write("== OSGi Dependencies ==\n");
		for dep_id in projectdesc['dependencies'] :
			# Documentation is here
#			if bundles[dep_id]['symbolicName'].find(project) == 0 :
#				wiki.write("*[["+bundles[dep_id]['wikiname']+"|"+bundles[dep_id]['name']+" - "+bundles[dep_id]['symbolicName']+" ("+bundles[dep_id]['version']+")]]\n")
#			else: 
			foundLink = False
			for link in links:
				if not foundLink and bundles[dep_id]['symbolicName'].find(link["symbolicNamePrefix"]) == 0:
					foundLink = True
					wiki.write("*"+link["link"]%bundles[dep_id]+"\n")
			if not foundLink:
				wiki.write("*"+bundles[dep_id]['name']+" - "+bundles[dep_id]['symbolicName']+" ("+bundles[dep_id]['version']+")\n")
			for imp in projectdesc['importpackages'] :
				if imp['id'] == dep_id :
					wiki.write("** "+imp['package']+"\n");

	if projectdesc.has_key('embedjars'):
		wiki.write("== OSGi Embedded JARs ==\n");
		for exp in projectdesc['embedjars'] :
			wiki.write("* "+exp+"\n");
	return wiki

def writeGithubMarkdown(bundles, projectdesc, project = "", markdown = StringIO.StringIO(), links = []):
	markdown.write("# ["+projectdesc['name']+" - "+projectdesc['symbolicName']+"](http://github.com/liveSense/"+projectdesc['symbolicName']+")\n")

	markdown.write("\n## Description\n");
	markdown.write(projectdesc['description']+"\n")

	if projectdesc.has_key('exportpackages'):
		markdown.write("\n## OSGi Exported packages\n");
		for exp in projectdesc['exportpackages'] :
			markdown.write("* "+exp['package']+"("+exp['version']+")\n");

	if projectdesc.has_key('exportpackages'):
		markdown.write("\n## OSGi Dependencies\n");
		for dep_id in projectdesc['dependencies'] :
			foundLink = False
			for link in links:
				if not foundLink and bundles[dep_id]['symbolicName'].find(link["symbolicNamePrefix"]) == 0:
					foundLink = True
					markdown.write("* "+link["link"]%bundles[dep_id]+"\n")
			if not foundLink:
				markdown.write("* __"+bundles[dep_id]['name']+" - "+bundles[dep_id]['symbolicName']+" ("+bundles[dep_id]['version']+")__\n")

			for imp in projectdesc['importpackages'] :
				if imp['id'] == dep_id :
					markdown.write("	* "+imp['package']+"\n");

	if projectdesc.has_key('embedjars'):
		markdown.write("\n## OSGi Embedded JARs\n");
		for exp in projectdesc['embedjars'] :
			markdown.write("* "+exp+"\n");
	return markdown;

# ===================================================
#  Main processor
# ===================================================

# Helpers
def getXmlText(nodelist):
	rc = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	st = ''.join(rc).strip().expandtabs(1).strip().replace('\n', ' ')
	while st.find('  ')>=0:
		st = st.replace('  ', ' ')
	return st

def getDomSingleElement(name, default):
	if (dom.getElementsByTagName(name) != None) and len(dom.getElementsByTagName(name))>0 and (dom.getElementsByTagName(name)[0] != None) :
		return getXmlText(dom.getElementsByTagName(name)[0].childNodes)
	return default

subprojectlist = []
subprojectlistnames = []

bundles = readBundlesFromConsole(CONSOLEHOST, CONSOLEPORT, CONSOLEUSER, CONSOLEPASSWORD)

# Collecting projects in bundles
for id in bundles.keys():
	if os.path.exists(PROJECTDIR+bundles[id]['symbolicName']) :
		projectdesc = bundles[id]
		projectdesc['osgiid'] = id;
		subprojectlist.append(projectdesc)
		subprojectlistnames.append(bundles[id]['symbolicName'])

# Collecting not osgi projects
for filename in os.listdir(PROJECTDIR):
	if filename.startswith(PROJECT) and not filename in subprojectlistnames:
		projectdesc = {}
		projectdesc['symbolicName'] = filename;
		projectdesc['osgiid'] = None;
		subprojectlist.append(projectdesc)
		subprojectlistnames.append(filename)

# Login WikiMedia and store login token in cookie
cj = cookielib.LWPCookieJar()
opener = poster.streaminghttp.register_openers()
opener.add_handler(urllib2.HTTPCookieProcessor(cj))
wikiLogin(opener,WIKISERVER, WIKIAPI,WIKIUSER,WIKIPASSWORD)

# Adding metadatas
for projectdesc in subprojectlist : 
	# Reading POM.XML-s description
	if not os.path.exists(PROJECTDIR+projectdesc['symbolicName']+"/pom.xml"):
		projectdesc['description'] = '<UNDEFINED>'
		projectdesc['name'] = '<UNDEFINED>'
		projectdesc['version'] = '<UNDEFINED>'
		projectdesc['wikiname'] = (WIKITITLEPREFIX+projectdesc['symbolicName']+projectdesc['version']).replace(".","").replace("-","").replace("_","")
		continue
			
	file = open(PROJECTDIR+projectdesc['symbolicName']+'/pom.xml','r')
	data = file.read()
	file.close()

	dom = parseString(data)
	projectdesc['description'] = getDomSingleElement('description','<UNDEFINED>')
	projectdesc['name'] = getDomSingleElement('name','<UNDEFINED>')
	projectdesc['version'] = getDomSingleElement('version','<UNDEFINED>')
	projectdesc['wikiname'] = (WIKITITLEPREFIX+projectdesc['symbolicName']+projectdesc['version']).replace(".","").replace("-","").replace("_","")


for projectdesc in subprojectlist : 
	# Travel dependeny graph
	print "Processing "+projectdesc['symbolicName']

	dotnodes = {}
	dotconnections = {}
	if projectdesc['osgiid']:
		travelDependencies(bundles=bundles, id=projectdesc['osgiid'], nodes=dotnodes, connections=dotconnections)
	
	# Generate wiki
	wiki = writeWiki(bundles=bundles, projectdesc=projectdesc, links=WIKILINKS, wiki = StringIO.StringIO())
	markdown = writeGithubMarkdown(bundles=bundles, projectdesc=projectdesc, links=MARKDOWNLINKS, markdown = StringIO.StringIO())

	if projectdesc.has_key('dependencies') and len(projectdesc['dependencies'])>0:
		dot = writeDot(bundles=bundles, projectdesc=projectdesc, dot=StringIO.StringIO())

		# Generate DOT descriptor to file
		dotfile = open(PROJECTDIR+projectdesc['symbolicName']+"/osgidependencies.dot","w")
		dotfile.write(dot.getvalue())
		dotfile.close

		# Generate SVG output from dot
		dotcmd = ["dot", "-Tsvg"]
		dotprocess = subprocess.Popen(dotcmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		dotprocess.stdin.write(dot.getvalue())
		dotout, doterr = dotprocess.communicate()
		dotprocess.stdin.close

		if doterr:
			print "ERROR ("+projectdesc['symbolicName']+"): "+doterr
			
		if dotout:
			svgfile = open(PROJECTDIR+projectdesc['symbolicName']+"/osgidependencies.svg","w")
			svgfile.write(dotout)
			svgfile.close

			markdown.write("\n## Dependency Graph\n");
			markdown.write("![alt text](http://raw.github.com.everydayimmirror.in/liveSense/"+projectdesc[u'symbolicName']+"/master/osgidependencies.svg \"\")")
		else:
			print "No SVG out: "+projectdesc['symbolicName']

		wiki.write("== OSGI Dependency graph ==\n");
		wiki.write("<graphviz format='svg'>"+dot.getvalue()+"</graphwiz>")	
		dot.close
			

	readmefile = open(PROJECTDIR+projectdesc[u'symbolicName']+"/README.md","w")
	readmefile.write(markdown.getvalue())
	readmefile.close

	# Post Wiki
	wikiEditApiPhp(opener, WIKISERVER, WIKIAPI, projectdesc['wikiname'] , wiki.getvalue())
	markdown.close
	wiki.close
