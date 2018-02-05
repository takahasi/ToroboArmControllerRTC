#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ToroboArmControllerRTC.py
 @brief ToroboArmController
 @date $Date$


"""
import sys

# Import RTM module
import RTC
import OpenRTM_aist

import ManipulatorCommonInterface_Common_idl
import ManipulatorCommonInterface_Middle_idl

# Import Service implementation class
# <rtc-template block="service_impl">
from ManipulatorCommonInterface_Common_idl_example import *
from ManipulatorCommonInterface_Middle_idl_example import *

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">

# </rtc-template>

import ToroboArmController
import ToroboArmMonitor
import ToroboArmControllerState


# This module's spesification
# <rtc-template block="module_spec">
toroboarmcontrollerrtc_spec = [
    "implementation_id", "ToroboArmControllerRTC",
    "type_name",         "ToroboArmControllerRTC",
    "description",       "ToroboArmController",
    "version",           "1.0.0",
    "vendor",            "Takahashi",
    "category",          "Controller",
    "activity_type",     "STATIC",
    "max_instance",      "1",
    "language",          "Python",
    "lang_type",         "SCRIPT",
    "conf.default.stub_mode", "off",

    "conf.__widget__.stub_mode", "radio",
    "conf.__constraints__.stub_mode", "(off, on)",

    "conf.__type__.stub_mode", "string",
    ""]
# </rtc-template>


##
# @class ToroboArmControllerRTC
# @brief ToroboArmController
#
#
class ToroboArmControllerRTC(OpenRTM_aist.DataFlowComponentBase):

    ##
    # @brief constructor
    # @param manager Maneger Object
    #
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_joints = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._jointsIn = OpenRTM_aist.InPort("joints", self._d_joints)

        self._d_mode = RTC.TimedOctet(RTC.Time(0, 0), 0)
        self._modeIn = OpenRTM_aist.InPort("mode", self._d_mode)

        self._d_status = RTC.TimedOctet(RTC.Time(0, 0), 0)
        self._statusOut = OpenRTM_aist.OutPort("status", self._d_status)

        self._d_out_joints = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._out_jointsOut = OpenRTM_aist.OutPort("out_joints",
                                                   self._d_out_joints)

        self._d_out_vel = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._out_velOut = OpenRTM_aist.OutPort("out_vel",
                                                self._d_out_vel)

        self._d_out_trq = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._out_trqOut = OpenRTM_aist.OutPort("out_trq",
                                                self._d_out_trq)

        self._d_out_cur = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._out_curOut = OpenRTM_aist.OutPort("out_cur",
                                                self._d_out_cur)

        self._d_out_tmp = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._out_tmpOut = OpenRTM_aist.OutPort("out_tmp",
                                                self._d_out_tmp)

        self._d_is_moving = RTC.TimedBoolean(RTC.Time(0, 0), False)
        self._is_movingOut = OpenRTM_aist.OutPort("is_moving",
                                                  self._d_is_moving)

        self._commonPort = OpenRTM_aist.CorbaPort("common")
        self._common = ManipulatorCommonInterface_Common_i()

        self._middlePort = OpenRTM_aist.CorbaPort("middle")
        self._middle = ManipulatorCommonInterface_Middle_i()

        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
        """
         - Name:  stub_mode
         - DefaultValue: off
        """
        self._stub_mode = ['off']

        # </rtc-template>

        self._controller = ToroboArmController.ToroboArmController()
        self._monitor = ToroboArmMonitor.ToroboArmMonitor()

        self._log = OpenRTM_aist.Manager.instance().getLogbuf("ToroboArmController")

    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # formaer rtc_init_entry()
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onInitialize(self):
        # Bind variables and configuration variable
        self.bindParameter("stub_mode", self._stub_mode, "off")

        # Set InPort buffers
        self.addInPort("joints", self._jointsIn)
        self.addInPort("mode", self._modeIn)

        # Set OutPort buffers
        self.addOutPort("status", self._statusOut)
        self.addOutPort("out_joints", self._out_jointsOut)
        self.addOutPort("out_vel", self._out_velOut)
        self.addOutPort("out_trq", self._out_trqOut)
        self.addOutPort("out_cur", self._out_curOut)
        self.addOutPort("out_tmp", self._out_tmpOut)
        self.addOutPort("is_moving", self._is_movingOut)

        # Set service provider to Ports
        self._commonPort.registerProvider("common",
                                          "JARA_ARM::ManipulatorCommonInterface_Common",
                                          self._common)
        self._middlePort.registerProvider("middle",
                                          "JARA_ARM::ManipulatorCommonInterface_Middle",
                                          self._middle)

        # Set service consumers to Ports

        # Set CORBA Service Ports
        self.addPort(self._commonPort)
        self.addPort(self._middlePort)

        return RTC.RTC_OK

    #   ##
    #   #
    #   # The finalize action (on ALIVE->END transition)
    #   # formaer rtc_exiting_entry()
    #   #
    #   # @return RTC::ReturnCode_t
    #
    #   #
    # def onFinalize(self):
    #
    #   return RTC.RTC_OK

    #   ##
    #   #
    #   # The startup action when ExecutionContext startup
    #   # former rtc_starting_entry()
    #   #
    #   # @param ec_id target ExecutionContext Id
    #   #
    #   # @return RTC::ReturnCode_t
    #   #
    #   #
    # def onStartup(self, ec_id):
    #
    #   return RTC.RTC_OK

    #   ##
    #   #
    #   # The shutdown action when ExecutionContext stop
    #   # former rtc_stopping_entry()
    #   #
    #   # @param ec_id target ExecutionContext Id
    #   #
    #   # @return RTC::ReturnCode_t
    #   #
    #   #
    def onShutdown(self, ec_id):

        self._controller.exit()
        self._monitor.exit()

        return RTC.RTC_OK

        ##
        #
        # The activated action (Active state entry action)
        # former rtc_active_entry()
        #
        # @param ec_id target ExecutionContext Id
        #
        # @return RTC::ReturnCode_t
        #
        #
    def onActivated(self, ec_id):

        self._target_joints = [0 for i in range(7)]
        self._target_mode = 0
        self._state = ToroboArmControllerState.ControllerState()

        if self._stub_mode == ['on']:
            self._controller.stub = True
            self._monitor.stub = True

        self._controller.start()
        self._monitor.start()

        return RTC.RTC_OK

        ##
        #
        # The deactivated action (Active state exit action)
        # former rtc_active_exit()
        #
        # @param ec_id target ExecutionContext Id
        #
        # @return RTC::ReturnCode_t
        #
        #
    def onDeactivated(self, ec_id):

        self._controller.stop()
        self._monitor.stop()
        del(self._state)

        return RTC.RTC_OK

        ##
        #
        # The execution action that is invoked periodically
        # former rtc_active_do()
        #
        # @param ec_id target ExecutionContext Id
        #
        # @return RTC::ReturnCode_t
        #
        #
    def onExecute(self, ec_id):
        # check controller exixts
        if not self._controller:
            self._log.RTC_ERROR("robot is not yet initialized")
            return RTC.RTC_ERROR

        # update mode
        self._update_mode()

        # move by joints
        self._move_by_joints()

        # output joints position
        self._output_joints()

        # output joints velocity
        self._output_velocity()

        # output joints torque
        self._output_force()

        # output joints current
        self._output_current()

        # output joints tempreture
        self._output_tempreture()

        # output joints moving
        self._output_moving()

        return RTC.RTC_OK

    #   ##
    #   #
    #   # The aborting action when main logic error occurred.
    #   # former rtc_aborting_entry()
    #   #
    #   # @param ec_id target ExecutionContext Id
    #   #
    #   # @return RTC::ReturnCode_t
    #   #
    #   #
    # def onAborting(self, ec_id):
    #
    #   return RTC.RTC_OK

    #   ##
    #   #
    #   # The error action in ERROR state
    #   # former rtc_error_do()
    #   #
    #   # @param ec_id target ExecutionContext Id
    #   #
    #   # @return RTC::ReturnCode_t
    #   #
    #   #
    # def onError(self, ec_id):
    #
    #   return RTC.RTC_OK

    #   ##
    #   #
    #   # The reset action that is invoked resetting
    #   # This is same but different the former rtc_init_entry()
    #   #
    #   # @param ec_id target ExecutionContext Id
    #   #
    #   # @return RTC::ReturnCode_t
    #   #
    #   #
    # def onReset(self, ec_id):
    #
    #   return RTC.RTC_OK

    #   ##
    #   #
    #   # The state update action that is invoked after onExecute() action
    #   # no corresponding operation exists in OpenRTm-aist-0.2.0
    #   #
    #   # @param ec_id target ExecutionContext Id
    #   #
    #   # @return RTC::ReturnCode_t
    #   #

    #   #
    # def onStateUpdate(self, ec_id):
    #
    #   return RTC.RTC_OK

    #   ##
    #   #
    #   # The action that is invoked when execution context's rate is changed
    #   # no corresponding operation exists in OpenRTm-aist-0.2.0
    #   #
    #   # @param ec_id target ExecutionContext Id
    #   #
    #   # @return RTC::ReturnCode_t
    #   #
    #   #
    # def onRateChanged(self, ec_id):
    #
    #   return RTC.RTC_OK

    def _update_mode(self):
        # update mode
        if self._modeIn.isNew():
            mode = self._modeIn.read()
            if self._target_mode != mode.data:
                if mode.data == 10:
                    self._log.RTC_INFO("teaching mode")
                    self._state.teaching = True
                    self._controller.mode_free()
                elif mode.data == 2:
                    self._log.RTC_INFO("slow mode")
                    self._state.status = "slow"
                elif mode.data == 3:
                    self._log.RTC_INFO("pause mode")
                    self._state.status = "pause"
                elif mode.data == 4:
                    self._log.RTC_INFO("stop mode")
                    self._state.status = "stop"
                else:
                    self._log.RTC_INFO("normal mode")
                    self._state.teaching = False
                    self._controller.mode_point()
                self._target_mode = mode.data
                self._d_status.data = self._state.status_id
                self._statusOut.write()

    def _move_by_joints(self):
        # move by joints
        if self._jointsIn.isNew():
            val = self._jointsIn.read()
            if len(val.data) == 7 and self._target_joints != val.data:
                self._log.RTC_INFO("goal_joints: " + str(val.data))
                self._controller.move(val.data, speed=self._state.speed)
                self._target_joints = val.data

    def _output_joints(self):
        # output joints information
        joints = self._monitor.joints
        self._log.RTC_DEBUG("out_joints: " + str(joints))
        self._d_out_joints.data = joints
        self._out_jointsOut.write()

    def _output_velocity(self):
        # output velocity information
        vel = self._monitor.vel
        self._log.RTC_DEBUG("out_vel: " + str(vel))
        self._d_out_vel.data = vel
        self._out_velOut.write()

    def _output_current(self):
        # output current information
        cur = self._monitor.cur
        self._log.RTC_DEBUG("out_cur: " + str(cur))
        self._d_out_cur.data = cur
        self._out_curOut.write()

    def _output_tempreture(self):
        # output tempreture information
        tmp = self._monitor.tmp
        self._log.RTC_DEBUG("out_tmp: " + str(tmp))
        self._d_out_tmp.data = tmp
        self._out_tmpOut.write()

    def _output_moving(self):
        # output moving information
        moving = self._monitor.moving
        self._log.RTC_DEBUG("is_moving: " + str(moving))
        self._d_is_moving.data = moving
        self._is_movingOut.write()

    def _output_force(self):
        # output force information
        force = self._monitor.trq
        self._log.RTC_DEBUG("force: " + str(force))
        self._d_out_trq.data = force
        self._out_trqOut.write()


def ToroboArmControllerRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=toroboarmcontrollerrtc_spec)
    manager.registerFactory(profile,
                            ToroboArmControllerRTC,
                            OpenRTM_aist.Delete)


def MyModuleInit(manager):
    ToroboArmControllerRTCInit(manager)

    # Create a component
    manager.createComponent("ToroboArmControllerRTC")


def main():
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()
