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

import yaml

from Models import ScanItem, ScanResult, ScanStats

rulebase = []
scan_results = []


def load_rules(rules_csv):

    rules = []
    with open(rules_csv, 'rU') as csvfile:
        rulereader = csv.DictReader(csvfile, delimiter=',')
        for row in rulereader:
            rules.append(ScanItem(app_type=row['app_type'],
                                     file_type=row['file_type'],
                                     file_category=row['file_category'],
                                     file_name=row['file_name'],
                                     refactor_rating=row['refactor_rating'],
                                     description=row['description'],
                                     text_pattern=row['text_pattern']
                                     ))
    set_rulebase(rules)

def load_yaml_rules(yaml_file):
    with open(yaml_file, 'rU') as yamlfile:
        load_yaml_rules_stream(yamlfile)

def load_yaml_rules_stream(yaml_stream):
    rules = []

    yaml_rules = yaml.load(yaml_stream)

    for rule in yaml_rules:
        app_type = rule.get('app_type')
        category = rule.get('category')
        file_type = rule.get('file_type')
        file_pattern = rule.get("file_pattern")
        refactor_rating = rule.get('refactor_rating')
        description = rule.get('description')
        replatform_advice = rule.get('replatform_advice')
        if file_pattern is not None:
            text_patterns = rule.get("text_patterns")
            if text_patterns is not None:
                for text_pattern in text_patterns:
                    # Text patterns can have overrides, so we have to account for that
                    override_refactor_rating = refactor_rating
                    override_description = description
                    override_replatform_advice = replatform_advice
                    text_pattern_key = text_pattern
                    if not isinstance(text_pattern, basestring):
                        text_pattern_key = text_pattern.keys()[0]
                        pattern_override_map = text_pattern[text_pattern.keys()[0]]
                        if 'refactor_rating' in pattern_override_map:
                            override_refactor_rating = pattern_override_map.get('refactor_rating')
                        if 'description' in pattern_override_map:
                            override_description = pattern_override_map.get('description')
                        if 'replatform_advice' in pattern_override_map:
                            override_replatform_advice = pattern_override_map.get('replatform_advice')

                    rules.append(
                        ScanItem(app_type, category, file_type, file_pattern, override_refactor_rating,
                                 override_description, text_pattern_key, override_replatform_advice)
                    )
            else:
                rules.append(
                    ScanItem(app_type, category, file_type, file_pattern, refactor_rating, description, None,
                             replatform_advice)
                )

        elif rule.get("files") is not None:
            text_patterns = rule.get("text_patterns")
            for file_item in rule.get("files"):
                # Files can have overrides, so we have to account for that
                file_override_refactor_rating = refactor_rating
                file_override_description = description
                file_override_replatform_advice = replatform_advice
                file_item_key = file_item
                if not isinstance(file_item, basestring):
                    file_item_key = file_item.keys()[0]
                    file_override_map = file_item[file_item.keys()[0]]
                    if 'refactor_rating' in file_override_map:
                        file_override_refactor_rating = file_override_map.get('refactor_rating')
                    if 'description' in file_override_map:
                        file_override_description = file_override_map.get('description')
                    if 'replatform_advice' in file_override_map:
                        file_override_replatform_advice = file_override_map.get('replatform_advice')

                if text_patterns is None:
                    rules.append(
                        ScanItem(app_type, category, file_type, file_item_key, file_override_refactor_rating,
                                 file_override_description, None, file_override_replatform_advice)
                    )

                else:
                    for text_pattern in text_patterns:
                        # Text patterns can have overrides, so we have to account for that
                        # We'll use the file_override data because at this point it will have
                        # either the overriden data from a file entry, or the original rule data
                        pattern_override_refactor_rating = file_override_refactor_rating
                        pattern_override_description = file_override_description
                        pattern_override_replatform_advice = file_override_replatform_advice
                        text_pattern_key = text_pattern
                        if not isinstance(text_pattern, basestring):
                            text_pattern_key = text_pattern.keys()[0]
                            pattern_override_map = text_pattern[text_pattern.keys()[0]]
                            if 'refactor_rating' in pattern_override_map:
                                pattern_override_refactor_rating = pattern_override_map.get('refactor_rating')
                            if 'description' in pattern_override_map:
                                pattern_override_description = pattern_override_map.get('description')
                            if 'replatform_advice' in pattern_override_map:
                                pattern_override_replatform_advice = pattern_override_map.get('replatform_advice')

                        rules.append(
                            ScanItem(app_type, category, file_type, file_item_key, pattern_override_refactor_rating,
                                     pattern_override_description, text_pattern_key, pattern_override_replatform_advice)
                        )

        else:
            raise RuntimeError("Error parsing rule.  No file_pattern value or files array specified.", rule)

    set_rulebase(rules)


def set_rulebase(rules):
    global rulebase
    rulebase = rules

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
