#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import unittest
sys.path.append(".")
sys.path.append("..")

import ToroboArm


class TestToroboArmBase(unittest.TestCase):
    def tearDown(self):
        self.assertIsNotNone(self.t)
        self.assertTrue(self.t.start())
        time.sleep(0.1)
        self.assertTrue(self.t.stop())
        time.sleep(0.1)
        self.assertTrue(self.t.exit())
        time.sleep(0.1)
        del(self.t)

    def test_normal(self):
        self.t = ToroboArm.ToroboArm('tcp://localhost:5555',
                                     ToroboArm.ToroboArm.REQ,
                                     False)

    def test_normal_debug(self):
        self.t = ToroboArm.ToroboArm('tcp://localhost:5555',
                                     ToroboArm.ToroboArm.REQ,
                                     True)

    def test_normal_subscriber(self):
        self.t = ToroboArm.ToroboArm('tcp://localhost:5554',
                                     ToroboArm.ToroboArm.SUB,
                                     True)

    def test_address_illegal(self):
        self.t = ToroboArm.ToroboArm('tcp://hoge',
                                     ToroboArm.ToroboArm.REQ,
                                     True)


class TestToroboArm(unittest.TestCase):
    def setUp(self):
        self.t = ToroboArm.ToroboArm('tcp://localhost:5555',
                                     ToroboArm.ToroboArm.REQ,
                                     True)
        self.t.start()

    def tearDown(self):
        self.t.stop()
        time.sleep(0.1)
        self.t.exit()
        time.sleep(0.1)
        del(self.t)

    def test_start_normal(self):
        self.assertTrue(self.t.start())

    def test_start_already(self):
        self.assertTrue(self.t.start())
        time.sleep(0.1)
        self.assertTrue(self.t.start())

    def test_stop_normal(self):
        self.assertTrue(self.t.stop())

    def test_stop_already(self):
        self.assertTrue(self.t.stop())
        time.sleep(0.1)
        self.assertTrue(self.t.stop())

    def test_exit_normal(self):
        self.assertTrue(self.t.exit())

    def test_exit_already(self):
        self.assertTrue(self.t.exit())
        time.sleep(0.1)
        self.assertTrue(self.t.exit())

    def test_stub_true(self):
        self.t.stub = True
        self.assertTrue(self.t.stub)

    def test_stub_false(self):
        self.t.stub = False
        self.assertFalse(self.t.stub)


def test():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    test()
