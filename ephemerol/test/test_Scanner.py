from __future__ import print_function
import os
import unittest

from ephemerol import Scanner

class test_Scanner(unittest.TestCase):
    def test_load_rules(self):
        Scanner.load_rules(os.path.join("ephemerol", "test", "rulebase.csv"))
        results = Scanner.rulebase
        self.assertEqual(66, len(results))
        self.assertEqual(70, sum([int(entry.refactor_rating) for entry in results]))

    def test_archive_scan(self):
        Scanner.load_rules(os.path.join("ephemerol", "test", "rulebase.csv"))
        results_stats = Scanner.scan_archive(os.path.join("ephemerol", "test", "SampleWebApp-master.zip"))
        results = results_stats[0]
        stats = results_stats[1]
        #print(df)
        #self.assertEqual(1, df[(df.refactor_rating == 3)].shape[0])
        self.assertEqual(90, stats.cloud_readiness_index)

    def test_config_scan(self):
        Scanner.load_rules(os.path.join("ephemerol", "test", "rulebase.csv"))
        file_path_list = ['persistence.xml', 'web.xml', 'bing.xml', 'dir/dir/dir/ra.xml', '/dir/dir/ejb-jar.xml',
                          'dir/dir/web.xml']
        Scanner.scan_results = []
        Scanner.config_scan(file_path_list=file_path_list)
        results = Scanner.scan_results
        self.assertEqual(5, len(results))
        print(results)


if __name__ == '__main__':
    unittest.main()
