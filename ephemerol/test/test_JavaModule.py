# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import unittest
import pandas as pd

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
        print(results)
        self.assertEqual(1, results[(results.REFACTOR_RATING == 3)].shape[0])
        self.assertEqual(4, results[(results.REFACTOR_RATING == 1)].shape[0])
        self.assertEqual(31, results[(results.REFACTOR_RATING == 0)].shape[0])


if __name__ == '__main__':
    unittest.main()