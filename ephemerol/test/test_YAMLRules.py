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

from __future__ import print_function

import unittest
import os
from ephemerol import Scanner


class TestYAMLRules(unittest.TestCase):
    def setUp(self):
        Scanner.scan_results = []

    def test_simple_rule_load(self):
        rule = """
- category: "Web Profile"
  app_type: java
  file_type: config
  refactor_rating: 0
  description: "Web application config file"
  files: ["web.xml"]
"""

        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(1, len(Scanner.rulebase), "Should have loaded 1 rule")
        rule = Scanner.rulebase[0]
        self.assertEqual("Web Profile", rule.file_category, "Category should be mapped")
        self.assertEqual("java", rule.app_type, "App Type should be mapped")
        self.assertEqual("config", rule.file_type, "File Type should be mapped")
        self.assertEqual("0", rule.refactor_rating, "Refactor Rating should be mapped")
        self.assertEqual("Web application config file", rule.description, "Description should be mapped")
        self.assertEqual("web.xml", rule.file_name, "File Name should be mapped")

    def test_multiple_file_rule_load(self):
        rule = """
- category: "Web Profile"
  app_type: java
  file_type: config
  refactor_rating: 0
  description: "Web application config file"
  files:
    - "web.xml"
    - "foo.barml"
"""

        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(2, len(Scanner.rulebase))
        rule = Scanner.rulebase[0]
        self.assertEqual("Web Profile", rule.file_category, "Category should be mapped")
        self.assertEqual("java", rule.app_type, "App Type should be mapped")
        self.assertEqual("config", rule.file_type, "File Type should be mapped")
        self.assertEqual("0", rule.refactor_rating, "Refactor Rating should be mapped")
        self.assertEqual("Web application config file", rule.description, "Description should be mapped")
        self.assertEqual("web.xml", rule.file_name, "File Name should be mapped")
        rule = Scanner.rulebase[1]
        self.assertEqual("Web Profile", rule.file_category, "Category should be mapped")
        self.assertEqual("java", rule.app_type, "App Type should be mapped")
        self.assertEqual("config", rule.file_type, "File Type should be mapped")
        self.assertEqual("0", rule.refactor_rating, "Refactor Rating should be mapped")
        self.assertEqual("Web application config file", rule.description, "Description should be mapped")
        self.assertEqual("foo.barml", rule.file_name, "File Name should be mapped")

    def test_rule_load_with_replatform_advice(self):
        rule = """
- category: "JEE Config"
  app_type: java
  file_type: config
  refactor_rating: 1
  replatform_advice: "Convert to Spring based application configuration"
  description: "JEE specific config file"
  files:
    - "application.xml"
"""

        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(1, len(Scanner.rulebase))
        rule = Scanner.rulebase[0]
        self.assertEqual("JEE Config", rule.file_category, "Category should be mapped")
        self.assertEqual("java", rule.app_type, "App Type should be mapped")
        self.assertEqual("config", rule.file_type, "File Type should be mapped")
        self.assertEqual("1", rule.refactor_rating, "Refactor Rating should be mapped")
        self.assertEqual("Convert to Spring based application configuration", rule.replatform_advice,
                         "Replatform Advice should be mapped")
        self.assertEqual("JEE specific config file", rule.description, "Description should be mapped")
        self.assertEqual("application.xml", rule.file_name, "File Name should be mapped")

    def test_rule_load_with_overriden_description_replatform_advice_refactor_rating(self):
        rule = """
- category: "cat1"
  app_type: app1
  file_type: type1
  refactor_rating: 0
  replatform_advice: "foo"
  description: "desc1"
  files:
    - "file1": { description: "desc2", replatform_advice: "bar", refactor_rating: 2 }
    - "file2"
"""
        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(2, len(Scanner.rulebase))
        found1 = False
        found2 = False
        for rule in Scanner.rulebase:
            self.assertEqual("cat1", rule.file_category, "Category should be mapped")
            self.assertEqual("app1", rule.app_type, "App Type should be mapped")
            self.assertEqual("type1", rule.file_type, "File Type should be mapped")
            self.assertTrue(rule.file_name == "file1" or rule.file_name == "file2")
            if rule.file_name == "file1":
                found1 = True
                self.assertEqual("2", rule.refactor_rating, "Refactor Rating should be mapped")
                self.assertEqual("bar", rule.replatform_advice, "Replatform Advice should be mapped")
                self.assertEqual("desc2", rule.description, "Description should be mapped")
            elif rule.file_name == "file2":
                found2 = True
                self.assertEqual("0", rule.refactor_rating, "Refactor Rating should be mapped")
                self.assertEqual("foo", rule.replatform_advice, "Replatform Advice should be mapped")
                self.assertEqual("desc1", rule.description, "Description should be mapped")
                self.assertEqual("file2", rule.file_name, "File Name should be mapped")
        self.assertTrue(found1 and found2, "Should have found both file1 and file2")

    def test_rule_load_with_text_pattern(self):
        rule = """
- category: "cat1"
  app_type: app1
  file_type: type1
  refactor_rating: 1
  replatform_advice: "foo"
  description: "desc1"
  text_patterns: [ "pattern1" ]
  files: [ "file1" ]
"""
        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(1, len(Scanner.rulebase))
        rule = Scanner.rulebase[0]
        self.assertEqual("cat1", rule.file_category, "Category should be mapped")
        self.assertEqual("app1", rule.app_type, "App Type should be mapped")
        self.assertEqual("type1", rule.file_type, "File Type should be mapped")
        self.assertEqual("file1", rule.file_name, "File name should be mapped")
        self.assertEqual("1", rule.refactor_rating, "Refactor Rating should be mapped")
        self.assertEqual("foo", rule.replatform_advice, "Replatform Advice should be mapped")
        self.assertEqual("desc1", rule.description, "Description should be mapped")
        self.assertEqual("pattern1", rule.text_pattern, "Text pattern should be mapped")

    def test_rule_load_with_multiple_text_patterns(self):
        rule = """
- category: "cat1"
  app_type: app1
  file_type: type1
  refactor_rating: 1
  replatform_advice: "foo"
  description: "desc1"
  text_patterns: [ "pattern1", "pattern2" ]
  files: [ "file1" ]
"""
        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(2, len(Scanner.rulebase))
        found1 = False
        found2 = False
        for rule in Scanner.rulebase:
            self.assertEqual("cat1", rule.file_category, "Category should be mapped")
            self.assertEqual("app1", rule.app_type, "App Type should be mapped")
            self.assertEqual("type1", rule.file_type, "File Type should be mapped")
            self.assertEqual("file1", rule.file_name, "File name should be mapped")
            self.assertTrue(rule.text_pattern == "pattern1" or rule.text_pattern == "pattern2")
            if rule.text_pattern == "pattern1":
                found1 = True
            elif rule.text_pattern == "pattern2":
                found2 = True
        self.assertTrue(found1 and found2, "Should have found pattern1 and pattern2")

    def test_rule_load_with_multiple_text_patterns_with_override(self):
        rule = """
- category: "cat1"
  app_type: app1
  file_type: type1
  refactor_rating: 1
  replatform_advice: "foo"
  description: "desc1"
  text_patterns:
    - "pattern1"
    - "pattern2": { description: "desc2", replatform_advice: "bar", refactor_rating: 2 }
  files: [ "file1" ]
"""
        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(2, len(Scanner.rulebase))
        found1 = False
        found2 = False
        for rule in Scanner.rulebase:
            self.assertEqual("cat1", rule.file_category, "Category should be mapped")
            self.assertEqual("app1", rule.app_type, "App Type should be mapped")
            self.assertEqual("type1", rule.file_type, "File Type should be mapped")
            self.assertEqual("file1", rule.file_name, "File name should be mapped")
            self.assertTrue(rule.text_pattern == "pattern1" or rule.text_pattern == "pattern2")
            if rule.text_pattern == "pattern1":
                found1 = True
                self.assertEqual("desc1", rule.description, "Description should be mapped")
                self.assertEqual("foo", rule.replatform_advice, "Replatform advice should be mapped")
                self.assertEqual("1", rule.refactor_rating, "Refactor rating should be mapped")
            elif rule.text_pattern == "pattern2":
                found2 = True
                self.assertEqual("desc2", rule.description, "Description should be mapped")
                self.assertEqual("bar", rule.replatform_advice, "Replatform advice should be mapped")
                self.assertEqual("2", rule.refactor_rating, "Refactor rating should be mapped")
        self.assertTrue(found1 and found2, "Should have found pattern1 and pattern2")

    def test_rule_load_with_file_pattern(self):
        rule = """
- category: "cat1"
  app_type: app1
  file_type: type1
  refactor_rating: 1
  replatform_advice: "foo"
  description: "desc1"
  file_pattern: "*.file1"
"""
        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(1, len(Scanner.rulebase))
        rule = Scanner.rulebase[0]
        self.assertEqual("cat1", rule.file_category, "Category should be mapped")
        self.assertEqual("app1", rule.app_type, "App Type should be mapped")
        self.assertEqual("type1", rule.file_type, "File Type should be mapped")
        self.assertEqual("*.file1", rule.file_name, "File name should be mapped")
        self.assertEqual("1", rule.refactor_rating, "Refactor Rating should be mapped")
        self.assertEqual("foo", rule.replatform_advice, "Replatform Advice should be mapped")
        self.assertEqual("desc1", rule.description, "Description should be mapped")

    def test_rule_load_with_multiple_text_patterns_overrides_and_file_pattern(self):
        rule = """
- category: "cat1"
  app_type: app1
  file_type: type1
  refactor_rating: 1
  replatform_advice: "foo"
  description: "desc1"
  text_patterns:
    - "pattern1"
    - "pattern2": { description: "desc2", replatform_advice: "bar", refactor_rating: 2 }
  file_pattern: "*.file1"
"""
        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(2, len(Scanner.rulebase))
        found1 = False
        found2 = False
        for rule in Scanner.rulebase:
            self.assertEqual("cat1", rule.file_category, "Category should be mapped")
            self.assertEqual("app1", rule.app_type, "App Type should be mapped")
            self.assertEqual("type1", rule.file_type, "File Type should be mapped")
            self.assertEqual("*.file1", rule.file_name, "File name should be mapped")
            self.assertTrue(rule.text_pattern == "pattern1" or rule.text_pattern == "pattern2")
            if rule.text_pattern == "pattern1":
                found1 = True
                self.assertEqual("desc1", rule.description, "Description should be mapped")
                self.assertEqual("foo", rule.replatform_advice, "Replatform advice should be mapped")
                self.assertEqual("1", rule.refactor_rating, "Refactor rating should be mapped")
            elif rule.text_pattern == "pattern2":
                found2 = True
                self.assertEqual("desc2", rule.description, "Description should be mapped")
                self.assertEqual("bar", rule.replatform_advice, "Replatform advice should be mapped")
                self.assertEqual("2", rule.refactor_rating, "Refactor rating should be mapped")
        self.assertTrue(found1 and found2, "Should have found pattern1 and pattern2")

    def test_rule_load_with_text_pattern_overriding_files_overriding_rule(self):
        rule = """
- category: "cat1"
  app_type: app1
  file_type: type1
  refactor_rating: 1
  replatform_advice: "foo"
  description: "desc1"
  text_patterns:
    - "pattern1"
    - "pattern2": { description: "desc3", replatform_advice: "bap", refactor_rating: 3 }
  files:
    - "file1"
    - "file2": { description: "desc2", replatform_advice: "bar", refactor_rating: 2 }
"""
        Scanner.load_yaml_rules_stream(rule)
        self.assertEqual(4, len(Scanner.rulebase))
        found1and1 = False
        found1and2 = False
        found2and1 = False
        found2and2 = False
        for rule in Scanner.rulebase:
            self.assertEqual("cat1", rule.file_category, "Category should be mapped")
            self.assertEqual("app1", rule.app_type, "App Type should be mapped")
            self.assertEqual("type1", rule.file_type, "File Type should be mapped")
            self.assertTrue(rule.text_pattern == "pattern1" or rule.text_pattern == "pattern2")
            self.assertTrue(rule.file_name == "file1" or rule.file_name == "file2")
            if rule.file_name == "file1":
                if rule.text_pattern == "pattern1":
                    found1and1 = True
                    self.assertEqual("desc1", rule.description, "Description should be mapped")
                    self.assertEqual("foo", rule.replatform_advice, "Replatform advice should be mapped")
                    self.assertEqual("1", rule.refactor_rating, "Refactor rating should be mapped")
                elif rule.text_pattern == "pattern2":
                    found1and2 = True
                    self.assertEqual("desc3", rule.description, "Description should be mapped")
                    self.assertEqual("bap", rule.replatform_advice, "Replatform advice should be mapped")
                    self.assertEqual("3", rule.refactor_rating, "Refactor rating should be mapped")
            elif rule.file_name == "file2":
                if rule.text_pattern == "pattern1":
                    found2and1 = True
                    self.assertEqual("desc2", rule.description, "Description should be mapped")
                    self.assertEqual("bar", rule.replatform_advice, "Replatform advice should be mapped")
                    self.assertEqual("2", rule.refactor_rating, "Refactor rating should be mapped")
                elif rule.text_pattern == "pattern2":
                    found2and2 = True
                    self.assertEqual("desc3", rule.description, "Description should be mapped")
                    self.assertEqual("bap", rule.replatform_advice, "Replatform advice should be mapped")
                    self.assertEqual("3", rule.refactor_rating, "Refactor rating should be mapped")

        self.assertTrue(found1and1 and found1and2 and found2and1 and found2and2, "Should have found all 4 rule combos")

    def test_archive_scan_yaml(self):
        Scanner.load_yaml_rules(self.path_helper("rulebase.yml"))
        results_stats = Scanner.scan_archive(self.path_helper("SampleWebApp-master.zip"))
        self.assertEqual(97.44, results_stats.cloud_readiness_index)

    # Helps allow resources to be resolved if running via py.test or directly in IDE
    def path_helper(self, file_name):
        archive = os.path.join("ephemerol", "test", file_name)
        if not os.path.isfile(archive):
            archive = file_name
        return archive

if __name__ == '__main__':
    unittest.main()
