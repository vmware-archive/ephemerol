from zipfile import ZipFile
#import pandas as pd

# good file groups
cloudnative_config_group = ['persistence.xml',
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


def handles(file_name):
    return (
        file_name.endswith(".zip")
    )


def config_scan(file_path_list, results):
    for path in file_path_list:
        if path.endswith('/'):
            path = path[:-1]
        file_name = path.split('/')[-1]
        if file_name in cloudnative_config_group:
            results.append({'SCAN_GROUP': 'Cloud Native Config Files',
                            'FILE_NAME': file_name,
                            'REFACTOR_RATING': 0})
        elif file_name in jee_config_group:
            results.append({'SCAN_GROUP': 'JEE Config Files',
                            'FILE_NAME': file_name,
                            'REFACTOR_RATING': 1})
        elif file_name in weblogic_config_group:
            results.append({'SCAN_GROUP': 'Weblogic Config Files',
                            'FILE_NAME': file_name,
                            'REFACTOR_RATING': 1})
        elif file_name in websphere_config_group:
            results.append({'SCAN_GROUP': 'Websphere Config Files',
                            'FILE_NAME': file_name,
                            'REFACTOR_RATING': 1})
        elif file_name in jboss_config_group:
            results.append({'SCAN_GROUP': 'JBoss Config Files',
                            'FILE_NAME': file_name,
                            'REFACTOR_RATING': 1})


def source_scan(zfile, results):
    for file in zfile.namelist():
        if file.endswith('.java'):
            java_file_scan(zfile.open(file).readlines(), file, results)

def java_file_scan(file_lines, file, results):
    for line in file_lines:
        if "javax.ejb." in line:
            results.append({'SCAN_GROUP': 'Java Source Scan - EJB',
                            'FILE_NAME': file.split('/')[-1],
                            'REFACTOR_RATING': 3})
        if "org.springframework." in line:
            results.append({'SCAN_GROUP': 'Java Source Scan - Spring',
                            'FILE_NAME': file.split('/')[-1],
                            'REFACTOR_RATING': 0})

def do_handle(file_name):
    results = []
    with ZipFile(file_name, 'r') as zfile:
        config_scan(zfile.namelist(), results)
        source_scan(zfile, results)


    return results
