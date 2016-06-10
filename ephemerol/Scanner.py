from zipfile import ZipFile
import pandas as pd
from Models import ScanItem

rulebase = pd.DataFrame.empty
scan_results = []

def load_rules(rules_csv):
    global rulebase
    rulebase = pd.read_csv(rules_csv)

def config_scan(file_path_list):
    configrules = rulebase.loc[(rulebase['file_type'] == "config") & (rulebase['app_type'] == "java")]
    global scan_results

    file_names = []
    for path in file_path_list:
        if path.endswith('/'):
            path = path[:-1]
        file_names.append(path.split('/')[-1])

    config_matches = configrules.loc[configrules['file_id'].isin(file_names)]

    for index, row in config_matches.iterrows():
        scan_results.append(ScanItem(file_name=row['file_id'],
                                     file_category=row['file_category'],
                                     file_type=row['file_type'],
                                     refactor_rating=row['refactor_rating']))
def source_scan(zfile):
    for fname in zfile.namelist():
        if fname.endswith('.java'):
            java_file_scan(zfile.open(fname).readlines(), fname)
        elif fname.endswith('.xml'):
            xml_file_scan(zfile.open(fname).readlines(), fname)


def xml_file_scan(file_lines, filename):
    xmlrules = rulebase.loc[
        (rulebase['file_type'] == "config") & (rulebase['file_id'] == "*.xml") & (
            rulebase['text_pattern'] != "NONE")]
    global scan_results
    xml_matches = xmlrules.loc[xmlrules['text_pattern'].isin(file_lines)]

    for index, row in xml_matches.iterrows():
        scan_results.append(ScanItem(file_name=file,
                                     file_category=row['file_category'],
                                     file_type=row['file_type'],
                                     refactor_rating=row['refactor_rating']))

def java_file_scan(file_lines, filename):
    javarules = rulebase.loc[
        (rulebase['file_type'] == "java") & (rulebase['app_type'] == "java") & (rulebase['file_id'] == "*.java") & (
            rulebase['text_pattern'] != "NONE")]
    javarules.apply(text_pattern_search,axis=1, args=(filename,tuple(file_lines)))


def c_sharp_file_scan(file_lines, filename):
    #TODO
    print(scan_results)

def text_pattern_search(row, *args):
    for line in args[1]:
       if row.text_pattern in line:
           scan_results.append(ScanItem(file_name=args[0],
                                        file_category=row.file_category,
                                        file_type=row.file_type,
                                        refactor_rating=row.refactor_rating))

def scan_archive(file_name):
    global scan_results
    scan_results = []
    with ZipFile(file_name, 'r') as zfile:
        config_scan(zfile.namelist())
        source_scan(zfile)

    resultsSet = set(scan_results)
    resultsDictList = []
    for sr in resultsSet:
        resultsDictList.append(sr.__dict__)
    pd.set_option('display.max_colwidth', -1)
    return pd.DataFrame(resultsDictList)
