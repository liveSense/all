: <<'END'
"org.liveSense.launchpad"
"org.liveSense.dist"
END

projects=(
"org.liveSense.auth.ldap"
"org.liveSense.content.initial"
"org.liveSense.core"
"org.liveSense.fragment.com.sun.image.codec.jpeg"
"org.liveSense.fragment.customloginpage"
"org.liveSense.fragment.jackrabbit.server.jaybird.ddl"
"org.liveSense.fragment.javax.activation-jre-1.6"
"org.liveSense.fragment.javax.jws-jre-1.6"
"org.liveSense.fragment.javax.xml-jre-1.6"
"org.liveSense.fragment.sun.misc"
"org.liveSense.fragment.sun.security"
"org.liveSense.framework.apacheds"
"org.liveSense.framework.cxf"
"org.liveSense.framework.docx4j"
"org.liveSense.framework.dom4j"
"org.liveSense.framework.fitnesse"
"org.liveSense.framework.gwt"
"org.liveSense.framework.gxt"
"org.liveSense.framework.itext"
"org.liveSense.framework.jasperreports"
"org.liveSense.framework.jodconverter"
"org.liveSense.framework.jodreports"
"org.liveSense.framework.lucene"
"org.liveSense.framework.odfdom"
"org.liveSense.framework.poi"
"org.liveSense.framework.solr"
"org.liveSense.framework.wro4j"
"org.liveSense.framework.xdocreport"
"org.liveSense.jdbc.h2"
"org.liveSense.jdbc.jaybird"
"org.liveSense.jdbc.mysql"
"org.liveSense.misc.configurationLoader"
"org.liveSense.misc.gwt.jsr303"
"org.liveSense.misc.i18n"
"org.liveSense.misc.javax.persistence"
"org.liveSense.misc.jcrom"
"org.liveSense.misc.jsr303"
"org.liveSense.misc.log.config.default"
"org.liveSense.misc.log.lilith.core"
"org.liveSense.misc.queryBuilder"
"org.liveSense.misc.queryBuilder.gwt"
"org.liveSense.scripting.jsp.taglib.jsonatg"
"org.liveSense.scripting.jsp.taglib.jstl"
"org.liveSense.service.securityManager"
"org.liveSense.service.activation"
"org.liveSense.service.apacheds"
"org.liveSense.service.apacheds.configurationLoader"
"org.liveSense.service.captcha"
"org.liveSense.service.cxf"
"org.liveSense.service.dataSourceProvider"
"org.liveSense.service.email"
"org.liveSense.service.guacamole"
"org.liveSense.service.gwt"
"org.liveSense.service.jcr.importexport"
"org.liveSense.service.languageSelector"
"org.liveSense.service.markdown"
"org.liveSense.service.report.jasper"
"org.liveSense.service.solr"
"org.liveSense.service.solr.configurationLoader"
"org.liveSense.service.thumbnailGenerator"
"org.liveSense.service.xssRemove"
"org.liveSense.jcr.explorer"
"org.liveSense.jcr.restexplorer"
"org.liveSense.webconsole.branding"
"org.liveSense.sample.configurationLoad"
"org.liveSense.sample.gwt.notes"
"org.liveSense.sample.gwt.notesRequestFactory"
"org.liveSense.sample.markdown"
"org.liveSense.sample.simplePortal"
"org.liveSense.sample.solr"
"org.liveSense.sample.webServiceServlet"
"org.liveSense.karaf"
)

#mvn versions:update-child-modules -DgenerateBackupPoms=false

for p in ${!projects[*]}
do
    cd "${projects[$p]}"

    #git add .
    #OUT=$?
    #if [ $OUT -ne 0 ];then
    #    echo "ERROR ON GIT ADD: ${PWD##*/}"
    #    exit 1;
    #fi

    #git diff-index --quiet HEAD ||  git commit --allow-empty -m "Update parent version"
    #OUT= $?
    #if [ $OUT -ne 0 ];then
    #    echo "ERROR ON GIT COMMIT: ${PWD##*/}"
    #    exit 1;
    #fi
    mvn versions:update-parent -DgenerateBackupPoms=false
    OUT=$?
    if [ $OUT -ne 0 ];then
        echo "ERROR ON UPDATE PARENT: ${PWD##*/}"
        exit 1;
    fi

    git add .
    OUT=$?
    if [ $OUT -ne 0 ];then
        echo "ERROR ON GIT ADD: ${PWD##*/}"
        exit 1;
    fi

    git diff-index --quiet HEAD ||  git commit --allow-empty -m "Update parent version"
    OUT= $?
    if [ $OUT -ne 0 ];then
        echo "ERROR ON GIT COMMIT: ${PWD##*/}"
        exit 1;
    fi
    
    /usr/local/bin/mvn -B release:clean
    /usr/local/bin/mvn -B release:prepare -DdryRun=true
    OUT=$?
    if [ $OUT -eq 0 ];then
        /usr/local/bin/mvn -B release:clean
        /usr/local/bin/mvn -B release:prepare
    else
        echo "ERROR ON RELEASE: ${PWD##*/}"
        /usr/local/bin/mvn -B release:clean
        exit 1;
    fi

    /usr/local/bin/mvn release:perform
    OUT=$?
    if [ $OUT -eq 0 ];then
        echo "RELEASE OK";
    else
        echo "ERROR ON RELEASE: ${PWD##*/}"
        /usr/local/bin/mvn -B release:rollback
        exit 1;
    fi

    cd ..
done
