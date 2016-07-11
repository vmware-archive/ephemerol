from __future__ import print_function

import os
import unittest

from ephemerol import Scanner


class TestScanner(unittest.TestCase):
    TEST_RULE_FILE = os.path.join("ephemerol", "test", "rulebase.csv")

    def setUp(self):
        Scanner.load_rules(self.TEST_RULE_FILE)
        Scanner.scan_results = []

    def test_load_rules(self):
        rulecount = -1  # start with -1 to exclude header row from count
        total_refactor = 0
        with open(self.TEST_RULE_FILE, 'rU') as f:
            for line in f:
                rulecount += 1
                if rulecount != 0:
                    total_refactor += int([field for field in line.split(',')][4])
        results = Scanner.rulebase
        self.assertEqual(rulecount, len(results))
        self.assertEqual(total_refactor, sum([int(entry.refactor_rating) for entry in results]))

    def test_archive_scan(self):
        results_stats = Scanner.scan_archive(os.path.join("ephemerol", "test", "SampleWebApp-master.zip"))
        stats = results_stats[1]
        self.assertEqual(90, stats.cloud_readiness_index)

    def test_config_scan(self):
        file_path_list = ['persistence.xml', 'web.xml', 'bing.xml', 'dir/dir/dir/ra.xml', '/dir/dir/ejb-jar.xml',
                          'dir/dir/web.xml']
        Scanner.scan_results = []
        Scanner.config_scan(file_path_list=file_path_list)
        results = Scanner.scan_results
        self.assertEqual(5, len(results))
        print(results)

    def test_has_scan_func_for_csproj(self):
        """Make sure files ending in csproj have a scan function"""
        scan_func = Scanner.get_scan_func("foobar.csproj")
        self.assertIsNotNone(scan_func)

    def dotnet_version_tester(self, sample_data, refactor_rating):
        Scanner.csproj_file_scan([sample_data], "testfile.csproj")
        results = Scanner.scan_results
        self.assertEqual(1, len(results))
        self.assertEqual(refactor_rating, results[0].scan_item.refactor_rating)

    def test_dotnet_version_3_0(self):
        """.NET framework version 3.0 is refactor of 1"""
        self.dotnet_version_tester('    <TargetFrameworkVersion>v3.0</TargetFrameworkVersion>', 1)

    def test_dotnet_version_3_5(self):
        """.NET framework version 3.5 is refactor of 0"""
        self.dotnet_version_tester('    <TargetFrameworkVersion>v3.5</TargetFrameworkVersion>', 0)

    def test_dotnet_version_4_0(self):
        """.NET framework version 4.0 is refactor of 0"""
        self.dotnet_version_tester('    <TargetFrameworkVersion>v4.0</TargetFrameworkVersion>', 0)

    def test_dotnet_version_4_5(self):
        """.NET framework version 4.5 is refactor of 0"""
        self.dotnet_version_tester('    <TargetFrameworkVersion>v4.5</TargetFrameworkVersion>', 0)

    def test_dotnet_version_4_6(self):
        """.NET framework version 4.6 is refactor of 0"""
        self.dotnet_version_tester('    <TargetFrameworkVersion>v4.6</TargetFrameworkVersion>', 0)

    def test_dotnet_version_2_0_refactor_1(self):
        """.NET framework version 2.0 is refactor of 3"""
        self.dotnet_version_tester('    <TargetFrameworkVersion>v2.0</TargetFrameworkVersion>', 3)

    def test_dotnet_version_1_0_refactor_1(self):
        """.NET framework version 1.0 is refactor of 3"""
        self.dotnet_version_tester('    <TargetFrameworkVersion>v1.0</TargetFrameworkVersion>', 3)

    def test_dotnet_version_not_present(self):
        """.NET framework version not in csproj file"""
        Scanner.csproj_file_scan(['    <NoFrameworkVersion></NoFrameworkVersion>'], "testfile.csproj")
        results = Scanner.scan_results
        self.assertEqual(0, len(results))

    def test_scan_for_servicebase_extension(self):
        """Found .cs file with class extending ServiceBase"""
        Scanner.cs_file_scan(['using System.ServiceProcess;',
                              'using System.Text;',
                              'using System.Threading.Tasks;',
                              'namespace WindowsService1',
                              '{',
                              '    public partial class Service1 : ServiceBase',
                              '    {'],
                             'Service1.cs')
        results = Scanner.scan_results
        self.assertEqual(1, len(results))
        self.assertEqual(20, results[0].scan_item.refactor_rating)

    def test_scan_for_no_extension(self):
        """Found .cs file with class not extending anything"""
        Scanner.cs_file_scan(['using System.ServiceProcess;',
                              'using System.Text;',
                              'using System.Threading.Tasks;',
                              'namespace WindowsService1',
                              '{',
                              '    public partial class Service1',
                              '    {'],
                             'Service1.cs')
        results = Scanner.scan_results
        self.assertEqual(0, len(results))

    def test_scan_for_extension_but_not_servicebase(self):
        """Found .cs file with class extending FooBar"""
        Scanner.cs_file_scan(['using System.ServiceProcess;',
                              'using System.Text;',
                              'using System.Threading.Tasks;',
                              'namespace WindowsService1',
                              '{',
                              '    public partial class Service1 : FooBar',
                              '    {'],
                             'Service1.cs')
        results = Scanner.scan_results
        self.assertEqual(0, len(results))


if __name__ == '__main__':
    unittest.main()
