# Copyright (C) 2016-Present Pivotal Software, Inc. All rights reserved.
#
# This program and the accompanying materials are made available under
# the terms of the under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
from zipfile import ZipFile

from Models import ScanItem, ScanResult, ScanStats

rulebase = []
scan_results = []


def load_rules(rules_csv):
    global rulebase
    rulebase = []
    with open(rules_csv, 'rU') as csvfile:
        rulereader = csv.DictReader(csvfile, delimiter=',')
        for row in rulereader:
            rulebase.append(ScanItem(app_type=row['app_type'],
                                     file_type=row['file_type'],
                                     file_category=row['file_category'],
                                     file_name=row['file_name'],
                                     refactor_rating=row['refactor_rating'],
                                     description=row['description'],
                                     text_pattern=row['text_pattern']
                                     ))


def config_scan(file_path_list):
    configrules = []
    global scan_results

    for rule in rulebase:
        if (rule.file_type == "config") and (rule.app_type == "java"):
            configrules.append(rule)

    for path in file_path_list:
        if path.endswith('/'):
            path = path[:-1]
        file_name = path.split('/')[-1]
        for configrule in configrules:
            if file_name == configrule.file_name:
                scan_results.append(ScanResult(scan_item=configrule, flagged_file_id=file_name))


def source_scan(zfile):
    for fname in zfile.namelist():
        fun_to_call = get_scan_func(fname)
        if fun_to_call is not None:
            fun_to_call(zfile.open(fname).readlines(), fname)


def get_scan_func(fname):
    if fname.endswith('.java'):
        return java_file_scan
    elif fname.endswith('.xml'):
        return xml_file_scan
    elif fname.endswith('.csproj'):
        return csproj_file_scan
    elif fname.endswith('.cs'):
        return cs_file_scan


def xml_file_scan(file_lines, filename):
    xmlrules = []
    global scan_results
    for rule in rulebase:
        if (rule.file_type == "config") and (rule.file_name == "*.xml") and (rule.text_pattern != "NONE"):
            xmlrules.append(rule)

    for line in file_lines:
        for rule in xmlrules:
            if rule.text_pattern in line:
                scan_results.append(ScanResult(scan_item=rule, flagged_file_id=filename))


def java_file_scan(file_lines, filename):
    javarules = []
    global scan_results
    for rule in rulebase:
        if (rule.file_type == "java") \
                and (rule.app_type == "java") \
                and (rule.file_name == "*.java") \
                and (rule.text_pattern != "NONE"):
            javarules.append(rule)
    for line in file_lines:
        for rule in javarules:
            if rule.text_pattern in line:
                scan_results.append(ScanResult(scan_item=rule, flagged_file_id=filename))


def csproj_file_scan(file_lines, filename):
    dotnetrules = []
    global scan_results
    for rule in rulebase:
        if (rule.file_type == "config") \
                and (rule.app_type == "dotnet") \
                and (rule.file_name == "*.csproj") \
                and (rule.text_pattern != "NONE"):
            dotnetrules.append(rule)
    for line in file_lines:
        for rule in dotnetrules:
            if rule.text_pattern in line:
                scan_results.append(ScanResult(scan_item=rule, flagged_file_id=filename))


def cs_file_scan(file_lines, filename):
    cs_file_rules = []
    global scan_results
    for rule in rulebase:
        if (rule.file_type == "csharp") \
                and (rule.app_type == "dotnet") \
                and (rule.file_name == "*.cs") \
                and (rule.text_pattern != "NONE"):
            cs_file_rules.append(rule)
    for line in file_lines:
        for rule in cs_file_rules:
            if rule.text_pattern in line:
                scan_results.append(ScanResult(scan_item=rule, flagged_file_id=filename))


def scan_archive(file_name):
    global scan_results
    scan_results = []
    with ZipFile(file_name, 'r') as zfile:
        config_scan(zfile.namelist())
        source_scan(zfile)

    return scan_results, ScanStats(scan_results)
