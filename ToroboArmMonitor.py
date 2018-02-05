#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import json

import ToroboArm


class ToroboArmMonitor(ToroboArm.ToroboArm):

    def __init__(self,
                 port='tcp://localhost:5554',
                 socktype=ToroboArm.ToroboArm.SUB,
                 debug=False):
        super(ToroboArmMonitor, self).__init__(port, socktype, debug)
        self._init_data()

    def _init_data(self):
        with self._lock:
            self._joints = [0 for i in range(7)]
            self._vel = [0 for i in range(7)]
            self._trq = [0 for i in range(7)]
            self._cur = [0 for i in range(7)]
            self._tmp = [0 for i in range(7)]
            self._mode = [0 for i in range(7)]
            self._error = [0 for i in range(7)]
            self._trjstatus = [0 for i in range(7)]
            self._moving = False

    def _init_communication(self):
        self._init_data()
        super(ToroboArmMonitor, self)._init_communication()

    def _exit_communication(self):
        self._init_data()
        super(ToroboArmMonitor, self)._exit_communication()

    def _inject_stub_data(self):
        with self._lock:
            for i in range(7):
                self._joints[i] = 0  # random.uniform(0, 180)
                self._vel[i] = 0  # random.uniform(0, 10)
                self._trq[i] = 0  # random.uniform(0, 10)
                self._cur[i] = 0  # random.uniform(0, 10)
                self._tmp[i] = 0  # random.uniform(0, 10)
                self._mode[i] = 0
                self._error[i] = 0
                self._trjstatus[i] = 0
            self._moving = False

    def _parse_contents(self, contents):
        state = json.loads(contents)
        with self._lock:
            for i in range(7):
                js = state["jointState"][i]
                try:
                    self._joints[i] = js["position"]
                    self._vel[i] = js["velocity"]
                    self._trq[i] = js["effort"]
                    self._cur[i] = js["current"]
                    self._tmp[i] = js["temperature"]
                    self._mode[i] = js["ctrlMode"]
                    self._error[i] = js["ewStatus"]
                    self._trjstatus[i] = js["trjStatus"]
                except KeyError:
                    logging.error("json KeyError:\n" + str(state))
                    continue
            # update moving status
            self._moving = self._check_moving()

    def _check_moving(self):
        # Check moving
        # mode:
        #   0x00: TrjCtrl
        #   0x05: ExtForceFollow
        # trjStatus:
        #   0x00: Stop
        #   0x01: Start -> moving
        #   0x02: Running -> moving
        #   0x03: NextPoint -> moving
        #   0x04: Complete
        #   0x05: Cancel
        #   0x65~: Error
        for i in range(7):
            if self._trjstatus[i] == 1:
                return True
            elif self._trjstatus[i] == 2:
                return True
            elif self._trjstatus[i] == 3:
                return True
            elif self._mode[i] == 5:
                # "external force mode" as moving
                return True
        # all joits are not moving
        return False

    def _process(self):
        # processing
        self._open_socket()
        if self._sock in dict(self._poll.poll(timeout=100)):
            try:
                [addr, cont] = self._sock.recv_multipart()
            except self.COMError:
                logging.error("Communication Error!")
            else:
                self._parse_contents(cont)
        self._close_socket()
        return 0

    def _process_stub(self):
        # processing
        self._inject_stub_data()
        return 0.1

    @property
    def joints(self):
        with self._lock:
            logging.debug("joints:" + str(self._joints))
            return self._joints

    @property
    def vel(self):
        with self._lock:
            logging.debug("vel:" + str(self._vel))
            return self._vel

    @property
    def trq(self):
        with self._lock:
            logging.debug("trq:" + str(self._trq))
            return self._trq

    @property
    def cur(self):
        with self._lock:
            logging.debug("cur:" + str(self._cur))
            return self._cur

    @property
    def tmp(self):
        with self._lock:
            logging.debug("tmp:" + str(self._tmp))
            return self._tmp

    @property
    def moving(self):
        with self._lock:
            logging.debug("moving:" + str(self._moving))
            return self._moving

    @property
    def mode(self):
        with self._lock:
            logging.debug("mode:" + str(self._mode))
            return self._mode

    @property
    def error(self):
        with self._lock:
            logging.debug("error:" + str(self._error))
            return self._error

    @property
    def trjstatus(self):
        with self._lock:
            logging.debug("trjstatus:" + str(self._trjstatus))
            return self._trjstatus


if __name__ == '__main__':
    # self test
    t = ToroboArmMonitor(debug=True)
    t.start()
    time.sleep(0.1)
    t.joints
    t.vel
    t.tmp
    t.trq
    t.moving
    t.mode
    t.error
    t.trjstatus
    time.sleep(1.0)
    t.joints
    t.vel
    t.tmp
    t.trq
    t.moving
    t.mode
    t.error
    t.trjstatus
    time.sleep(0.1)
    t.stop()
    time.sleep(0.1)
    t.exit()
