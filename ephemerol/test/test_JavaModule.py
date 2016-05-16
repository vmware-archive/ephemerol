# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import unittest
from pprint import pprint

from ephemerol import JavaModule

class test_JavaModule(unittest.TestCase):

    def test_accepts_files_with_zip_suffix(self):
        assert JavaModule.handles("foo.zip")
        assert JavaModule.handles(".zip")
        assert JavaModule.handles(u'ファイル.zip')


    def test_rejects_files_without_zip_suffix(self):
        assert not JavaModule.handles(".doc")
        assert not JavaModule.handles("Jar.doc")
        assert not JavaModule.handles("foo.jar.doc")


    def test_java_module(self):
        results = JavaModule.do_handle(os.path.join("ephemerol", "test", "SampleWebApp-master.zip"))
        assert results is not None

        self.assertEqual(36, len(results)) #Analyze 36 files exactly
        self.assertEqual(7,sum([entry['REFACTOR_RATING'] for entry in results])) #Confirm total value of all refactor ratings is 7
        self.assertEqual(1, results[0]['REFACTOR_RATING']) #Confirm the first entry, ibm-web-ext.xmi, is 1
        self.assertEqual(0, results[4]['REFACTOR_RATING']) # Confirm the 5th entry, css, is 0




if __name__ == '__main__':
    unittest.main()