#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest

class MyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "setUpClass"

    def test_example(self):
        self.assertTrue(1==1)

    @classmethod
    def tearDownClass(cls):
        print "running teardown"

def test_single():
    suite = unittest.TestSuite()
    suite.addTest(MyTest('test_example'))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    unittest.main()
