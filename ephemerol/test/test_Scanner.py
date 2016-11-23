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

import os
import unittest

from ephemerol import Scanner
from ephemerol.Models import ScanStats


class TestScanner(unittest.TestCase):
    TEST_RULE_FILE = "rulebase.csv"

    def __init__(self, *args, **kwargs):
        super(TestScanner, self).__init__(*args, **kwargs)
        if not os.path.isfile(TestScanner.TEST_RULE_FILE):
            TestScanner.TEST_RULE_FILE = os.path.join("ephemerol", "test", TestScanner.TEST_RULE_FILE)

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
        """Verify cloud readiness index for SampleWebApp-master.zip and rulebase.csv"""
        archive = "SampleWebApp-master.zip"
        if not os.path.isfile(archive):
            archive = os.path.join("ephemerol", "test", archive)
        results_stats = Scanner.scan_archive(archive)
        stats = results_stats[1]
        self.assertEqual(97.44, stats.cloud_readiness_index)

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

    def test_scan_for_oledb_use(self):
        """Found .cs file with \"using System.Data.OleDb\'"""
        Scanner.cs_file_scan(['using System.Data.OleDb;'], 'Repository.cs')
        results = Scanner.scan_results
        self.assertEqual(1, len(results))

    def test_scan_for_obdc_use(self):
        """Found .cs file with \"using System.Data.Obdc\'"""
        Scanner.cs_file_scan(['using System.Data.Odbc;'], 'Repository.cs')
        results = Scanner.scan_results
        self.assertEqual(1, len(results))

    def test_scan_for_ado_net_use(self):
        """Found .cs file with \"using System.Data\'"""
        Scanner.cs_file_scan(['using System.Data;'], 'Repository.cs')
        results = Scanner.scan_results
        self.assertEqual(1, len(results))

    def test_scan_double_hit_for_ado_net_and_odbc_use(self):
        """Found .cs file with \"using System.Data\'" and \"using System.Data.Odbc\'"""
        Scanner.cs_file_scan(['using System.Data;', 'using System.Data.Odbc;'], 'Repository.cs')
        results = Scanner.scan_results
        self.assertEqual(2, len(results))

    def test_scan_for_ef_use(self):
        """Found .cs file with \"using System.Data.Entity\'"""
        Scanner.cs_file_scan(['using System.Data;', 'using System.Data.Odbc;'], 'Repository.cs')
        results = Scanner.scan_results
        self.assertEqual(2, len(results))

    def test_scan_for_file_write(self):
        """Found .cs file with call to File.WriteAllText"""
        Scanner.cs_file_scan(['File.WriteAllText("foo.bar", "Some Text");'], 'FileWrite.cs')
        results = Scanner.scan_results
        self.assertEqual(1, len(results))

    def test_scan_for_file_open(self):
        """Found .cs file with call to File.Open"""
        Scanner.cs_file_scan(
            ['        using (FileStream fs = File.Open(path, FileMode.Open, FileAccess.Write, FileShare.None))'],
            'FileWrite.cs')
        results = Scanner.scan_results
        self.assertEqual(1, len(results))

    def test_scan_for_filesystem_watcher(self):
        """Found .cs file with call to File.WriteAllText"""
        Scanner.cs_file_scan(['        FileSystemWatcher watcher = new FileSystemWatcher();'], 'FileWrite.cs')
        results = Scanner.scan_results
        self.assertEqual(1, len(results))

    def test_cloud_readiness_index_algorithm(self):
        """make sure no scan results to 20 to 220 show consistent readiness index"""
        scan_stats = ScanStats(Scanner.scan_results)
        self.assertEqual(0, len(scan_stats.scan_result_list))
        self.assertEqual(100, scan_stats.cloud_readiness_index)

        for counter in range(0, 10):
            Scanner.java_file_scan(['import javax.ejb.'], 'BadPojo.java')
            Scanner.java_file_scan(['import org.springframework.'], 'GoodPojo.java')

        scan_stats = ScanStats(Scanner.scan_results)
        self.assertEqual(20, len(scan_stats.scan_result_list))
        self.assertEqual(85, scan_stats.cloud_readiness_index)

        for counter in range(0, 100):
            Scanner.java_file_scan(['import javax.ejb.'], 'BadPojo.java')
            Scanner.java_file_scan(['import org.springframework.'], 'GoodPojo.java')
            scan_stats = ScanStats(Scanner.scan_results)

        self.assertEqual(220, len(scan_stats.scan_result_list))
        self.assertEqual(85, scan_stats.cloud_readiness_index)

if __name__ == '__main__':
    unittest.main()
