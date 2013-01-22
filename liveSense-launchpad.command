#!/bin/bash
# Formatting constants
UNDERLINE_ON=`echo -e "\033[4m"`
UNDERLINE_OFF=`echo -e "\033[0m"`
BOLD_ON=`echo -e "\033[1m"`
BOLD_OFF=`echo -e "\033[0m"`
Black=`echo -e "\033[0;30m"`
BlackBG=`echo -e "\033[0;40m"`
DarkGrey=`echo -e "\033[1;30m"`
DarkGreyBG=`echo -e "\033[1;40m"`
LightGrey=`echo -e "\033[0;37m"`
LightGreyBG=`echo -e "\033[0;47m"`
White=`echo -e "\033[1;37m"`
WhiteBG=`echo -e "\033[1;47m"`
Red=`echo -e "\033[0;31m"`
RedBG=`echo -e "\033[0;41m"`
LightRed=`echo -e "\033[1;31m"`
LightRedBG=`echo -e "\033[1;41m"`
Green=`echo -e "\033[0;32m"`
GreenBG=`echo -e "\033[0;42m"`
LightGreen=`echo -e "\033[1;32m"`
LightGreenBG=`echo -e "\033[1;42m"`
Brown=`echo -e "\033[0;33m"`
BrownBG=`echo -e "\033[0;43m"`
Yellow=`echo -e "\033[1;33m"`
YellowBG=`echo -e "\033[1;43m"`
Blue=`echo -e "\033[0;34m"`
BlueBG=`echo -e "\033[0;44m"`
LightBlue=`echo -e "\033[1;34m"`
LightBlueBG=`echo -e "\033[1;44m"`
Purple=`echo -e "\033[0;35m"`
PurpleBG=`echo -e "\033[0;45m"`
Pink=`echo -e "\033[1;35m"`
PinkBG=`echo -e "\033[1;45m"`
Cyan=`echo -e "\033[0;36m"`
CyanBG=`echo -e "\033[0;46m"`
LightCyan=`echo -e "\033[1;36m"`
LightCyanBG=`echo -e "\033[1;46m"`

BASEDIR=$(dirname $0)

cd $BASEDIR/org.liveSense.launchpad/target
java -Xms128m -Xmx1024m -XX:MaxPermSize=256m -Dproject.root=$BASEDIR -jar org.liveSense.launchpad-1.0.2-SNAPSHOT-standalone.jar -p 8080 | sed  \
-e "s/\(^.\{24\}INFO..\)\(.*\)\(.\-.BundleEvent.\)\(.*\)/${BlackBG}${LightGray}\1${LightCyan}\2${LightGray}\3${RedBG}${Yellow}\4${BlackBG}${BOLD_OFF}/g" \
-e "s/\(^.\{24\}INFO  \)\(.*\)\( \- Service \)\(\[.*\]\) \([a-zA-Z0-9]*\) \([a-zA-Z0-9]*\)/${BlackBG}${LightGray}\1${LightCyan}\2${LightGray}\3${Yellow}\4 ${White}\5 ${RedBG}${Yellow}\6${BlackBG}${BOLD_OFF}/g" \
-e "s/\(^.\{24\}INFO..GWTREQUESTFACTORY.-.>>>*\)/${BlackBG}${Pink}\1${BlackBG}${BOLD_OFF}/g" \
-e "s/\(^.\{24\}INFO..GWTREQUESTFACTORY.-.<<<*\)/${BlackBG}${LightCyan}\1${BlackBG}${BOLD_OFF}/g" \
-e "s/\(^.\{24\}INFO..logs\/access.log*\)/${BlackBG}${LightGreen}\1${BlackBG}${BOLD_OFF}/g" \
-e "s/\(^.\{24\}INFO..logs\/request.log*\)/${BlackBG}${Green}\1${BlackBG}${BOLD_OFF}/g" \
-e "s/\(^.\{24\}ERROR.*\)/${LightRed}\1${BOLD_OFF}/g" \
-e "s/\(^.\{24\}WARN.*\)/${BlackBG}${Yellow}\1${BlackBG}${BOLD_OFF}/g" \
-e "s/\(^.\{24\}INFO.*\)/${BlackBG}${White}\1${BlackBG}${BOLD_OFF}/g" \
-e "s/\(^.*\)/${LightGray}${UNDERLINE_OFF}\1/g"

read -p "Press [Enter] key to close"