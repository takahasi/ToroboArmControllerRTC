ToroboArmControllerRTC
======================

This is RT-Component(RTC) for ToroboArm(Tokyo Robotics Inc.)

Preparation
-----------
Get & run `armmgr` from Tokyo Robotics.
`armmgr` is the daemon of comunnication to ToroboArm.

Usage
-----------
```
$ python ToroboArmControllerRTC.py
```

Unit Test (Use real robot)
-----------
```
$ python ToroboArmController.py
$ python ToroboArmMonitor.py
```

Unit Test (Use dummy server)
-----------
```
$ python tests/test_server.py
$ python ToroboArmController.py
$ python ToroboArmMonitor.py
```
