#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
import json
import Queue

import ToroboArm


class ToroboArmController(ToroboArm.ToroboArm):

    def __init__(self,
                 port='tcp://localhost:5555',
                 socktype=ToroboArm.ToroboArm.REQ,
                 debug=False):
        super(ToroboArmController, self).__init__(port, socktype, debug)
        self._command_q = Queue.Queue()

    def _process(self):
        # processing
        if self._command_q.empty():
            return 0.1
        else:
            with self._lock:
                command = self._command_q.get()
            self._open_socket()
            try:
                self._sock.send(json.dumps(command))
                if self._sock in dict(self._poll.poll(timeout=1000)):
                    self._sock.recv(flags=self.NOBLOCK)
            except self.COMError:
                logging.error("Communication Error!")
            self._close_socket()
            self._command_q.task_done()
            logging.info(json.dumps(command))
            return 0

    def _process_stub(self):
        # processing
        if self._command_q.empty():
            return 0.1
        else:
            with self._lock:
                command = self._command_q.get()
            self._command_q.task_done()
            logging.info(json.dumps(command))
            return 0

    def start(self):
        super(ToroboArmController, self).start()
        self.reset()
        self.servo_on()
        self.mode_point()
        self.clear_command()
        self.move_home()

    def stop(self):
        super(ToroboArmController, self).stop()
        with self._lock:
            self._command_q.queue.clear()

    def send_command(self, command):
        with self._lock:
            self._command_q.put(command)

    def clear_command(self):
        logging.debug("clear command")
        c = {
            "command": "--tc",
            "joint_id": "all"
        }
        self.send_command(c)
        return

    def reset(self):
        logging.debug("reset")
        c = {
            "command": "--reset",
            "joint_id": "all",
        }
        self.send_command(c)
        return

    def servo_on(self):
        logging.debug("servo on")
        c = {
            "command": "--servo",
            "servo_state": "ON",
            "joint_id": "all",
        }
        self.send_command(c)
        return

    def servo_off(self):
        logging.debug("servo off")
        c = {
            "command": "--servo",
            "servo_state": "OFF",
            "joint_id": "all",
        }
        self.send_command(c)
        return

    def mode_point(self):
        logging.debug("mode point")
        c = {
            "command": "--mode",
            "mode_id": "0",
            "joint_id": "all"
        }
        self.send_command(c)
        return

    def mode_free(self):
        logging.debug("mode free")
        c = {
            "command": "--mode",
            "mode_id": "5",
            "joint_id": "all"
        }
        self.send_command(c)
        return

    def move_home(self, speed=3):
        logging.debug("move home")
        self.move([0, 0, 0, 0, 0, 0, 0], speed)
        return

    def move(self, j, speed=3):
        logging.debug("move")
        for i in range(7):
            c = {
                "command": "--tpts",
                "joint_id": str(i + 1),
                "pos": str(j[i]),
                "time": str(speed)
            }
            self.send_command(c)

        c = {
            "command": "--ts",
            "joint_id": "all",
        }
        self.send_command(c)
        return


if __name__ == '__main__':
    # self test
    t = ToroboArmController(debug=True)
    t.start()
    time.sleep(0.1)
    t.reset()
    t.servo_on()
    t.mode_point()
    t.clear_command()
    t.move_home()
    t.move([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    t.mode_free()
    t.servo_off()
    time.sleep(5)
    t.stop()
    time.sleep(0.1)
    t.exit()
