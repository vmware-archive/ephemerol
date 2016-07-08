from __future__ import print_function
import os
import unittest

from ephemerol import Scanner

class test_Scanner(unittest.TestCase):
    def setUp(self):
        Scanner.load_rules(os.path.join("ephemerol", "test", "rulebase.csv"))
        Scanner.scan_results = []

    def test_load_rules(self):
        rb = Scanner.rulebase

        self.assertEqual(66, rb[(rb.app_type == "java")].shape[0])
        self.assertEqual(1, rb[(rb.file_id == "persistence.xml")].shape[0])
        self.assertEqual(9, rb[(rb.refactor_rating == 3)].shape[0])
        self.assertEqual(1, rb[(rb.description == "JPA based ORM")].shape[0])
        self.assertEqual(65, rb[(rb.file_type == "config")].shape[0])
        self.assertEqual(6, rb[(rb.file_category == "Web Profile")].shape[0])
        self.assertEqual(1, rb[(rb.text_pattern == "import javax.ejb.")].shape[0])

    def test_java_scan(self):
        df = Scanner.scan_archive(os.path.join("ephemerol", "test", "SampleWebApp-master.zip"))
        print(df)
        self.assertEqual(1, df[(df.refactor_rating == 3)].shape[0])
        self.assertEqual(5, df[(df.refactor_rating == 1)].shape[0])
        self.assertEqual(11, df[(df.refactor_rating == 0)].shape[0])
        self.assertEqual(92, 100 - df.refactor_rating.cumsum().tail(1).item())

    def test_config_scan(self):
        file_path_list = ['persistence.xml', 'web.xml', 'bing.xml', 'dir/dir/dir/ra.xml', '/dir/dir/ejb-jar.xml',
                          'dir/dir/web.xml']
        Scanner.config_scan(file_path_list=file_path_list)
        results = Scanner.scan_results
        self.assertEqual(4, len(results))
        #print(results)

    def test_has_scan_func_for_csproj(self):
        """Make sure files ending in csproj have a scan function"""
        scan_func = Scanner.get_scan_func("foobar.csproj")
        self.assertIsNotNone(scan_func)

    def dotnet_version_tester(self, sample_data, refactor_rating):
        Scanner.csproj_file_scan([sample_data], "testfile.csproj")
        results = Scanner.scan_results
        self.assertEqual(1, len(results))
        self.assertEqual(refactor_rating, results[0].refactor_rating)

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

if __name__ == '__main__':
    unittest.main()
