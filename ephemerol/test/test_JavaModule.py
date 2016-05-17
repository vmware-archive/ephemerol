# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import unittest
import pandas as pd
from ephemerol import ScanRecord

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
        df = pd.DataFrame(results)
        print(df)
        self.assertEqual(1, df[(df.refactor_rating == 3)].shape[0])
        self.assertEqual(6, df[(df.refactor_rating == 1)].shape[0])
        self.assertEqual(31, df[(df.refactor_rating == 0)].shape[0])


if __name__ == '__main__':
    unittest.main()