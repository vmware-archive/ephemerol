from __future__ import print_function
import os
import unittest

from ephemerol import Scanner

class test_Scanner(unittest.TestCase):
    def test_load_rules(self):
        Scanner.load_rules(os.path.join("ephemerol", "test", "rulebase.csv"))
        rb = Scanner.rulebase


        self.assertEqual(66, rb[(rb.app_type == "java")].shape[0])
        self.assertEqual(1, rb[(rb.file_id == "persistence.xml")].shape[0])
        self.assertEqual(6, rb[(rb.refactor_rating == 3)].shape[0])
        self.assertEqual(1, rb[(rb.description == "JPA based ORM")].shape[0])
        self.assertEqual(53, rb[(rb.file_type == "config")].shape[0])
        self.assertEqual(6, rb[(rb.file_category == "Web Profile")].shape[0])
        self.assertEqual(1, rb[(rb.text_pattern == "import javax.ejb.")].shape[0])

    def test_java_scan(self):
        Scanner.load_rules(os.path.join("ephemerol", "test", "rulebase.csv"))
        df = Scanner.scan_archive(os.path.join("ephemerol", "test", "SampleWebApp-master.zip"))
        #print(df)
        self.assertEqual(1, df[(df.refactor_rating == 3)].shape[0])
        self.assertEqual(5, df[(df.refactor_rating == 1)].shape[0])
        self.assertEqual(7, df[(df.refactor_rating == 0)].shape[0])
        self.assertEqual(92, 100 - df.refactor_rating.cumsum().tail(1).item())

    def test_config_scan(self):
        Scanner.load_rules(os.path.join("ephemerol", "test", "rulebase.csv"))
        file_path_list = ['persistence.xml', 'web.xml', 'bing.xml', 'dir/dir/dir/ra.xml', '/dir/dir/ejb-jar.xml',
                          'dir/dir/web.xml']
        Scanner.config_scan(file_path_list=file_path_list)
        results = Scanner.scan_results
        self.assertEqual(4, len(results))
        print(results)


if __name__ == '__main__':
    unittest.main()
