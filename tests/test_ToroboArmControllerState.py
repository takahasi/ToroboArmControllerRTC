#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import unittest
sys.path.append(".")
sys.path.append("..")

import ToroboArmControllerState as torobo


class TestToroboArmControllerState(unittest.TestCase):
    def setUp(self):
        self.s = torobo.ControllerState()

    def tearDown(self):
        del(self.s)

    def test_teaching(self):
        self.s.status = "stop"
        self.s.teaching = True
        self.s.speed = 1.0
        self.s.dump()
        self.assertTrue(self.s.teaching)
        self.assertEqual(self.s.speed, 0.0)
        self.assertEqual(self.s.status_id, 10)

    def test_stop(self):
        self.s.status = "stop"
        self.s.teaching = False
        self.s.speed = 2.0
        self.s.dump()
        self.assertFalse(self.s.teaching)
        self.assertEqual(self.s.speed, 0.0)
        self.assertEqual(self.s.status_id, 4)

    def test_pause(self):
        self.s.status = "pause"
        self.s.teaching = False
        self.s.speed = 3.0
        self.s.dump()
        self.assertFalse(self.s.teaching)
        self.assertEqual(self.s.speed, 0.0)
        self.assertEqual(self.s.status_id, 3)

    def test_slow(self):
        self.s.status = "slow"
        self.s.teaching = False
        self.s.speed = 4.0
        self.s.dump()
        self.assertFalse(self.s.teaching)
        self.assertEqual(self.s.speed, 8.0)
        self.assertEqual(self.s.status_id, 2)

    def test_normal(self):
        self.s.status = "normal"
        self.s.teaching = False
        self.s.speed = 10.0
        self.s.dump()
        self.assertFalse(self.s.teaching)
        self.assertEqual(self.s.speed, 10.0)
        self.assertEqual(self.s.status_id, 1.0)


def test():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    test()
