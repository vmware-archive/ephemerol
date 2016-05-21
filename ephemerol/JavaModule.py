from zipfile import ZipFile
from ScanRecord import ScanRecord

# good file groups
web_profile_config_group = ['persistence.xml',
                            'web.xml',
                            'applicationContext.xml',
                            'WEB-INF',
                            'css']

cloudnative_build_group = ['pom.xml',
                           'build.gradle',
                           'ant.xml']

# bad file groups
jee_config_group = ['application.xml',
                    'application-client.xml',
                    'ejb-jar.xml',
                    'ra.xml',
                    'webservices.xml'
                    ]

weblogic_config_group = ['weblogic.xml',
                         'weblogic.xml',
                         'weblogic-cmp-rdbms-jar.xml',
                         'weblogic-ejb-jar.xml',
                         'weblogic-ra.xml',
                         'persistence-configuration.xml',
                         'weblogic-webservices.xml',
                         'weblogic-wsee-clientHandlerChain.xml',
                         'webservice-policy-ref.xml',
                         'weblogic-wsee-standaloneclient.xml',
                         'weblogic-application.xml'
                         ]

websphere_config_group = ['client-resource.xmi',
                          'ibm-application-bnd.xmi',
                          'ibm-application-bnd.xml',
                          'ibm-application-client-bnd.xmi',
                          'ibm-application-client-bnd.xml',
                          'ibm-application-client-ext.xmi',
                          'ibm-application-client-ext.xml',
                          'ibm-application-ext.xmi',
                          'ibm-application-ext.xml',
                          'ibm-ejb-access-bean.xml',
                          'ibm-ejb-jar-bnd.xmi',
                          'ibm-ejb-jar-bnd.xml',
                          'ibm-ejb-jar-ext.xmi',
                          'ibm-ejb-jar-ext.xml',
                          'ibm-ejb-jar-ext-pme.xmi',
                          'ibm-ejb-jar-ext-pme.xml',
                          'ibm-webservices-bnd.xmi',
                          'ibm-webservices-ext.xmi',
                          'ibm-web-bnd.xmi',
                          'ibm-web-bnd.xml',
                          'ibm-web-ext.xmi',
                          'ibm-web-ext.xml',
                          'ibm-web-ext-pme.xmi',
                          'ibm-web-ext-pme.xml',
                          'j2c_plugin.xml']

jboss_config_group = ['jaws.xml',
                      'jboss.xml',
                      'jbosscmp-jdbc.xml',
                      'jboss-service.xml',
                      'jboss-web.xml']

def config_scan(file_path_list, results):
    for path in file_path_list:
        if path.endswith('/'):
            path = path[:-1]
        file_name = path.split('/')[-1]
        if file_name in web_profile_config_group:
            results.append(ScanRecord(file_name=path,
                                     file_category="Web Profile",
                                     file_type="configuration",
                                     refactor_rating=0))
        elif file_name in jee_config_group:
            results.append(ScanRecord(file_name=path,
                                     file_category="JEE",
                                     file_type="configuration",
                                     refactor_rating=1))
        elif file_name in weblogic_config_group:
            results.append(ScanRecord(file_name=path,
                                     file_category="Weblogic",
                                     file_type="configuration",
                                     refactor_rating=1))
        elif file_name in websphere_config_group:
            results.append(ScanRecord(file_name=path,
                                     file_category="Websphere",
                                     file_type="configuration",
                                     refactor_rating=1))
        elif file_name in jboss_config_group:
            results.append(ScanRecord(file_name=path,
                                 file_category="JBoss",
                                 file_type="configuration",
                                 refactor_rating=1))


def source_scan(zfile, results):
    for file in zfile.namelist():
        if file.endswith('.java'):
            java_file_scan(zfile.open(file).readlines(), file, results)
        elif file.endswith('.xml'):
            xml_file_scan(zfile.open(file).readlines(), file, results)

def xml_file_scan(file_lines, file, results):
    for line in file_lines:
        if "port=" in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="Port Hard-Code",
                                      file_type="configuration",
                                      refactor_rating=1))

def java_file_scan(file_lines, file, results):
    for line in file_lines:
        if "import javax.ejb." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="EJB",
                                      file_type="java",
                                      refactor_rating=3))
        elif "import org.jboss." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="JBoss",
                                      file_type="java",
                                      refactor_rating=3))
        elif "import javax.resource." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="JCA",
                                      file_type="java",
                                      refactor_rating=3))
        elif "import javax.jms." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="JMS",
                                      file_type="java",
                                      refactor_rating=2))
        elif "import javax.naming." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="JNDI",
                                      file_type="java",
                                      refactor_rating=1))
        elif "import javax.persistence." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="JPA",
                                      file_type="java",
                                      refactor_rating=0))
        elif "import javax.transaction." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="JTA",
                                      file_type="java",
                                      refactor_rating=0))
        elif "import org.springframework.jndi." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="Spring/JNDI",
                                      file_type="java",
                                      refactor_rating=1))
        elif "import weblogic." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="Weblogic",
                                      file_type="java",
                                      refactor_rating=3))
        elif "import ibm.websphere." in line or "import ibm.wsspi." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="WebSphere",
                                      file_type="java",
                                      refactor_rating=3))
        elif "import org.springframework." in line:
            results.append(ScanRecord(file_name=file,
                                      file_category="Spring",
                                      file_type="java",
                                      refactor_rating=0))

def scan_archive(file_name):
    results = []
    with ZipFile(file_name, 'r') as zfile:
        config_scan(zfile.namelist(), results)
        source_scan(zfile, results)

    return results
