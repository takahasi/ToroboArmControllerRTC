#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ControllerState(object):

    def __init__(self, speed=3.0, status="normal", teach=False):
        self._teach = teach
        self._status = status
        self._speed = speed

    def dump(self):
        return ("slow: " + str(self.status) + "\n" +
                "teach: " + str(self.teaching) + "\n" +
                "speed: " + str(self.speed) + "\n" +
                "status_id: " + str(self.status_id) + "\n")

    @property
    def speed(self):
        if self.teaching:
            return 0.0
        elif self.status == "stop":
            return 0.0
        elif self.status == "pause":
            return 0.0
        elif self.status == "slow":
            return self._speed * 2
        else:
            return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val

    @property
    def teaching(self):
        return self._teach

    @teaching.setter
    def teaching(self, val):
        self._teach = val

    @property
    def status_id(self):
        if self.teaching:
            # teaching
            return 10
        elif self.status == "stop":
            # stop
            return 4
        elif self.status == "pause":
            # pause
            return 3
        elif self.status == "slow":
            # slow
            return 2
        else:
            # normal
            return 1


if __name__ == '__main__':
    s = ControllerState()
    print("dump-> \n" + str(s.dump()))
    s.status = "stop"
    s.teaching = True
    s.speed = 1.0
    print("dump-> \n" + str(s.dump()))
    s.status = "pause"
    s.teaching = False
    print("dump-> \n" + str(s.dump()))
    s.status = "normal"
    s.speed = 10.0
    print("dump-> \n" + str(s.dump()))
    del(s)
