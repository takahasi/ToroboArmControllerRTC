#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import unittest
sys.path.append(".")
sys.path.append("..")

import ToroboArmController as torobo


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
        self.t = torobo.ToroboArmController('tcp://localhost:5555',
                                            torobo.ToroboArmController.REQ,
                                            False)

    def test_normal_debug(self):
        self.t = torobo.ToroboArmController('tcp://localhost:5555',
                                            torobo.ToroboArmController.REQ,
                                            True)

    def test_normal_subscriber(self):
        self.t = torobo.ToroboArmController('tcp://localhost:5554',
                                            torobo.ToroboArmController.SUB,
                                            True)

    def test_address_illegal(self):
        self.t = torobo.ToroboArmController('tcp://hoge',
                                            torobo.ToroboArmController.REQ,
                                            True)


class TestToroboArm(unittest.TestCase):
    def setUp(self):
        self.t = torobo.ToroboArmController('tcp://localhost:5555',
                                            torobo.ToroboArmController.REQ,
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

    def test_move_home(self):
        self.assertTrue(self.t.move_home())
        time.sleep(3)

    def test_move_normal(self):
        self.assertTrue(self.t.move([1, 2, 3, 4, 5, 6, 7]))
        time.sleep(3)

    def test_move_illegal_short(self):
        self.assertFalse(self.t.move([1, 2, 3, 4, 5, 6]))

    def test_move_illegal_long(self):
        self.assertFalse(self.t.move([1, 2, 3, 4, 5, 6, 7, 8]))

    def test_reset(self):
        self.assertTrue(self.t.reset())
        time.sleep(0.1)

    def test_servo_on(self):
        self.assertTrue(self.t.servo_on())
        time.sleep(0.1)

    def test_servo_off(self):
        self.assertTrue(self.t.servo_off())
        time.sleep(0.1)

    def test_mode_point(self):
        self.assertTrue(self.t.mode_point())
        time.sleep(0.1)

    def test_mode_free(self):
        self.assertTrue(self.t.mode_free())
        time.sleep(0.1)

    def test_clear_command(self):
        self.assertTrue(self.t.clear_command())
        time.sleep(0.1)

    def test_command_full(self):
        for i in range(100):
            self.assertTrue(self.t.move_home())


def test():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    test()
