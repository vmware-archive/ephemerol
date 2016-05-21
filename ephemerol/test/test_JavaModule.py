from __future__ import print_function
import os
import unittest
import pandas as pd

from ephemerol import JavaModule

class test_JavaModule(unittest.TestCase):

    def test_java_module(self):
        results = JavaModule.scan_archive(os.path.join("ephemerol", "test", "SampleWebApp-master.zip"))
        df = pd.DataFrame(results)
        print(df)
        self.assertEqual(1, df[(df.refactor_rating == 3)].shape[0])
        self.assertEqual(6, df[(df.refactor_rating == 1)].shape[0])
        self.assertEqual(31, df[(df.refactor_rating == 0)].shape[0])

if __name__ == '__main__':
    unittest.main()