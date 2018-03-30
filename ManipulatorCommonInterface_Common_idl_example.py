#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ManipulatorCommonInterface_Common_idl_examplefile.py
 @brief Python example implementations generated from ManipulatorCommonInterface_Common.idl
 @date $Date$


"""

import omniORB
from omniORB import CORBA, PortableServer
import JARA_ARM, JARA_ARM__POA


import ManipulatorCommonInterface_DataTypes_idl as DATATYPES_IDL
import ManipulatorCommonInterface_Common_idl as COMMON_IDL
import math

class ManipulatorCommonInterface_Common_i (JARA_ARM__POA.ManipulatorCommonInterface_Common):
    """
    @class ManipulatorCommonInterface_Common_i
    Example class implementing IDL interface JARA_ARM.ManipulatorCommonInterface_Common
    """

    def __init__(self):
        """
        @brief standard constructor
        Initialise member variables here
        """
        self._SYSTEMMODE_RUN = 2
        
        self._TRJSTATUS_START = 1
        self._TRJSTATUS_RUNNING = 2
        self._TRJSTATUS_NEXTPOINT = 3
        
        self._TRJREMAIN_BUFFER_MAX = 1000
        
        self._controller = None
        self._monitor = None
        self._middle = None
    
        self._axisnum = 7
        self._limit_joint_deg = [[160,-160],[105,-45],[160,-160],[105,-45],[160,-160],[90,-90],[160,-160]]
        
        
    def set_controller(self, controller):
        self._controller = controller

    def unset_controller(self, controller):
        self._controller = None

    def set_monitor(self, monitor):
        self._monitor = monitor

    def unset_monitor(self, monitor):
        self._monitor = None

    def set_middle(self, middle):
        self._middle = middle

    def unset_middle(self, middle):
        self._middle = None

    def _create_activealarm(self, error):
        alarm_list = []
        
        for i, joint_warning in enumerate(error):
            alarm_list.append(COMMON_IDL._0_JARA_ARM.Alarm(0xFFFFFFFF,COMMON_IDL._0_JARA_ARM.WARNING,'{:X}'.format(joint_warning)))
            
        return alarm_list    

    # RETURN_ID clearAlarms()
    def clearAlarms(self):
        if self._controller:
            self._controller.reset()
            msg = 'the Error is not clear if you do not remove the error factor.'
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, msg)
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG,'')

    # RETURN_ID getActiveAlarm(out AlarmSeq alarms)
    def getActiveAlarm(self):
        if self._monitor:
            msg = 'error status store description.'
            return  DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, msg),  self._create_activealarm(self._monitor.error)
        else:
            return  DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, ''),  []

    # RETURN_ID getFeedbackPosJoint(out JointPos pos)
    def getFeedbackPosJoint(self):
        if self._monitor:
            return  DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK,''),  self._monitor.joints
        else:
            return  DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG,''),  []

    # RETURN_ID getManipInfo(out ManipInfo mInfo)
    def getManipInfo(self):
        return  DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK,''), \
            COMMON_IDL._0_JARA_ARM.ManipInfo('Tokyo Robotics Inc.', 'ToroboArm', self._axisnum, 1, False)

    # RETURN_ID getSoftLimitJoint(out LimitSeq softLimit)
    def getSoftLimitJoint(self):
        limit_joint = []
        
        for i in range(self._axisnum):
            limit_joint.append(DATATYPES_IDL._0_JARA_ARM.LimitValue(\
                                                                    math.radians(self._limit_joint_deg[i][0]),\
                                                                    math.radians(self._limit_joint_deg[i][1])))

        return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK,''), limit_joint

    # RETURN_ID getState(out ULONG state)
    def getState(self):

        if not self._monitor or not self._middle:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG,'')
        
        self._state = 0
        counter = 0

        #check servo
        tmp = self._monitor._sysmode
        for val in tmp:
            if val == self._SYSTEMMODE_RUN:
                counter = counter + 1

        if counter == self._axisnum:
            self._state = self._state | 0x01

        #check moving
        tmp = self._monitor._trjstatus
        for val in tmp:
            if val == self._TRJSTATUS_START or val == self._TRJSTATUS_RUNNING or val == self._TRJSTATUS_NEXTPOINT:
                self._state = self._state | 0x02
                break

        #check alarm
        tmp = self._monitor.error
        for val in tmp:
            if val > 0:
                self._state = self._state | 0x04
                break

        #check buffer full
        tmp = self._monitor.trjremain
        for val in tmp:
            if val >= self._TRJREMAIN_BUFFER_MAX:
                self._state = self._state | 0x08
                break

        if self._middle._middle_idl_state == self._middle.MIDDLE_IDL_STATE_PAUSE:
            self._state = self._state | 0x10
            
        return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK,''), self._state
        

    # RETURN_ID servoOFF()
    def servoOFF(self):
        if self._controller:
            self._controller.servo_off()
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK,'')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG,'')
    
    # RETURN_ID servoON()
    def servoON(self):
        if self._controller:
            self._controller.servo_on()
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK,'')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG,'')

    # RETURN_ID setSoftLimitJoint(in LimitSeq softLimit)
    def setSoftLimitJoint(self, softLimit):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result


if __name__ == "__main__":
    import sys
    
    # Initialise the ORB
    orb = CORBA.ORB_init(sys.argv)
    
    # As an example, we activate an object in the Root POA
    poa = orb.resolve_initial_references("RootPOA")

    # Create an instance of a servant class
    servant = ManipulatorCommonInterface_Common_i()

    # Activate it in the Root POA
    poa.activate_object(servant)

    # Get the object reference to the object
    objref = servant._this()
    
    # Print a stringified IOR for it
    print orb.object_to_string(objref)

    # Activate the Root POA's manager
    poa._get_the_POAManager().activate()

    # Run the ORB, blocking this thread
    orb.run()

