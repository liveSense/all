#!/usr/bin/python
import os
import re
import subprocess
import sys
import getopt


def loginTravis(project, token):
    traviscmd = ["travis", "login", "--github-token", token]
    travisprocess = subprocess.Popen(traviscmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./'+project)
    travisout, traviserr = travisprocess.communicate()
    
    if traviserr:
        print "ERROR ON LOGIN ("+project+"): "+traviserr
        return False;
    return True;


def createTravisSecure(project = "", purge = False, keyName="ciDeployUserName", keyValue="robson"):
    purgeParam = "";
    if (purge):
        purgeParam = "-x"
    traviscmd = ["travis", "encrypt", "-r", "liveSense/"+project, purgeParam, "-a", "env.global", keyName+"="+keyValue]
    travisprocess = subprocess.Popen(traviscmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./'+project)
    travisout, traviserr = travisprocess.communicate()
    
    if traviserr:
        print "ERROR ON ENCRYPT ("+project+"): "+traviserr
    return

def processDirectories(ciDeployUserName, ciDeployPassword, githubToken):
    for project in os.listdir('.'):
        if os.path.isfile(project) or project == '.git' or project == 'docgenerator': pass
        else:
            if (not os.path.isfile(project+'/.travis.yml')):
                print("Updating travis secret: "+project+" "+ciDeployUserName+" "+ciDeployPassword+" "+githubToken)
                if (loginTravis(project, githubToken)):
                    f = open(project+'/.travis.yml', 'w')
                    f.truncate();
                    f.write("language: java\n")
                    f.write("before_install:\n")
                    f.write("- curl https://raw.github.com/liveSense/all/master/travis-settings.xml --create-dirs -o target/travis/settings.xml\n")
                    f.write("jdk:\n")
                    f.write("- openjdk6\n")
                    f.write("script:\n")
                    f.write("- mvn deploy --settings target/travis/settings.xml\n")
                    f.close()
                    createTravisSecure(project, True, "CI_DEPLOY_USERNAME", ciDeployUserName)
                    createTravisSecure(project, False, "CI_DEPLOY_PASSWORD", ciDeployPassword)

def printHelp():
    print 'Usage: \ngenerate-travis.py -t <github token> -u <maven deploy user> -p <maven deploy password>'
    return

def main(argv):
    githubToken = None
    ciDeployUserName = None
    ciDeployPassword = None

    try:
        opts, args = getopt.getopt(argv,"ht:u:p:",["github-token=","user=","password="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt in ("-t", "--github-token"):
            githubToken = arg
        elif opt in ("-u", "--user"):
            ciDeployUserName = arg
        elif opt in ("-p", "--password"):
            ciDeployPassword = arg

    if (githubToken is None):
        print('ERROR: You must specify GitHub authentication token\n');
        printHelp()
        sys.exit(2)

    if (githubToken is None):
        print('ERROR: You must specify Maven deploy username\n');
        printHelp()
        sys.exit(2)

    if (githubToken is None):
        print('ERROR: You must specify Maven deploy password\n');
        printHelp()
        sys.exit(2)

    processDirectories(ciDeployUserName, ciDeployPassword, githubToken)

if __name__ == "__main__":
    main(sys.argv[1:])