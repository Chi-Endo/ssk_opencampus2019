﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file FireworksGenerator.py
 @brief FireworksGenerator
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
fireworksgenerator_spec = ["implementation_id", "FireworksGenerator", 
		 "type_name",         "FireworksGenerator", 
		 "description",       "FireworksGenerator", 
		 "version",           "1.0.0", 
		 "vendor",            "chi", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.SCREEN_SIZE_W", "1640",
		 "conf.default.SCREEN_SIZE_H", "1200",
		 "conf.default.WINDOW_SIZE_W", "1280",
		 "conf.default.WINDOW_SIZE_H", "960",
		 "conf.default.OVERLAY_IMAGE_SIZE_H", "640",
		 "conf.default.OVERLAY_IMAGE_SIZE_W", "347",

		 "conf.__widget__.SCREEN_SIZE_W", "text",
		 "conf.__widget__.SCREEN_SIZE_H", "text",
		 "conf.__widget__.WINDOW_SIZE_W", "text",
		 "conf.__widget__.WINDOW_SIZE_H", "text",
		 "conf.__widget__.OVERLAY_IMAGE_SIZE_H", "text",
		 "conf.__widget__.OVERLAY_IMAGE_SIZE_W", "text",

         "conf.__type__.SCREEN_SIZE_W", "int",
         "conf.__type__.SCREEN_SIZE_H", "int",
         "conf.__type__.WINDOW_SIZE_W", "int",
         "conf.__type__.WINDOW_SIZE_H", "int",
         "conf.__type__.OVERLAY_IMAGE_SIZE_H", "int",
         "conf.__type__.OVERLAY_IMAGE_SIZE_W", "int",

		 ""]
# </rtc-template>

##
# @class FireworksGenerator
# @brief FireworksGenerator
# 
# 
class FireworksGenerator(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_Pos = OpenRTM_aist.instantiateDataType(RTC.TimedLongSeq)
		"""
		"""
		self._PosIn = OpenRTM_aist.InPort("Pos", self._d_Pos)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  SCREEN_SIZE_W
		 - DefaultValue: 1640
		"""
		self._SCREEN_SIZE_W = [1640]
		"""
		
		 - Name:  SCREEN_SIZE_H
		 - DefaultValue: 1200
		"""
		self._SCREEN_SIZE_H = [1200]
		"""
		
		 - Name:  WINDOW_SIZE_W
		 - DefaultValue: 1280
		"""
		self._WINDOW_SIZE_W = [1280]
		"""
		
		 - Name:  WINDOW_SIZE_H
		 - DefaultValue: 960
		"""
		self._WINDOW_SIZE_H = [960]
		"""
		
		 - Name:  OVERLAY_IMAGE_SIZE_H
		 - DefaultValue: 640
		"""
		self._OVERLAY_IMAGE_SIZE_H = [640]
		"""
		
		 - Name:  OVERLAY_IMAGE_SIZE_W
		 - DefaultValue: 347
		"""
		self._OVERLAY_IMAGE_SIZE_W = [347]
		
		# </rtc-template>


		 
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
		self.bindParameter("SCREEN_SIZE_W", self._SCREEN_SIZE_W, "1640")
		self.bindParameter("SCREEN_SIZE_H", self._SCREEN_SIZE_H, "1200")
		self.bindParameter("WINDOW_SIZE_W", self._WINDOW_SIZE_W, "1280")
		self.bindParameter("WINDOW_SIZE_H", self._WINDOW_SIZE_H, "960")
		self.bindParameter("OVERLAY_IMAGE_SIZE_H", self._OVERLAY_IMAGE_SIZE_H, "640")
		self.bindParameter("OVERLAY_IMAGE_SIZE_W", self._OVERLAY_IMAGE_SIZE_W, "347")
		
		# Set InPort buffers
		self.addInPort("Pos",self._PosIn)
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	###
	## 
	## The finalize action (on ALIVE->END transition)
	## formaer rtc_exiting_entry()
	## 
	## @return RTC::ReturnCode_t
	#
	## 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The startup action when ExecutionContext startup
	## former rtc_starting_entry()
	## 
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The shutdown action when ExecutionContext stop
	## former rtc_stopping_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
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
	
		return RTC.RTC_OK
	
	###
	##
	## The aborting action when main logic error occurred.
	## former rtc_aborting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The error action in ERROR state
	## former rtc_error_do()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The reset action that is invoked resetting
	## This is same but different the former rtc_init_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The state update action that is invoked after onExecute() action
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##

	##
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The action that is invoked when execution context's rate is changed
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def FireworksGeneratorInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=fireworksgenerator_spec)
    manager.registerFactory(profile,
                            FireworksGenerator,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    FireworksGeneratorInit(manager)

    # Create a component
    comp = manager.createComponent("FireworksGenerator")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

