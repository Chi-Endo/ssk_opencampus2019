#!/usr/bin/env python
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

import cv2 as cv
import numpy as np
from PIL import Image
import random
import os
import glob

global deco
global image
global cv_background_image
global cv_overlay_image


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
		 "conf.default.OVERLAY_IMAGE_SIZE_H", "347",
		 "conf.default.OVERLAY_IMAGE_SIZE_W", "640",
		 "conf.default.GAP", "75",

		 "conf.__widget__.SCREEN_SIZE_W", "text",
		 "conf.__widget__.SCREEN_SIZE_H", "text",
		 "conf.__widget__.WINDOW_SIZE_W", "text",
		 "conf.__widget__.WINDOW_SIZE_H", "text",
		 "conf.__widget__.OVERLAY_IMAGE_SIZE_H", "text",
		 "conf.__widget__.OVERLAY_IMAGE_SIZE_W", "text",
		 "conf.__widget__.GAP", "text",

         "conf.__type__.SCREEN_SIZE_W", "int",
         "conf.__type__.SCREEN_SIZE_H", "int",
         "conf.__type__.WINDOW_SIZE_W", "int",
         "conf.__type__.WINDOW_SIZE_H", "int",
         "conf.__type__.OVERLAY_IMAGE_SIZE_H", "int",
         "conf.__type__.OVERLAY_IMAGE_SIZE_W", "int",
         "conf.__type__.GAP", "int",

		 ""]
# </rtc-template>
class CvOverlayImage(object):
	"""
	[summary]
		OpenCV形式の画像に指定画像を重ねる
	"""

	def __init__(self):
		pass

	@classmethod
	def overlay(
		cls,
		cv_background_image,
		cv_overlay_image,
		cv_mask_image,
		point,
		):
		"""
		[summary]
			OpenCV形式の画像に指定画像を重ねる
		Parameters
		----------
		cv_background_image : [OpenCV Image]
		cv_overlay_image : [OpenCV Image]
		cv_mask_image : [OpenCV Image]
		point : [(x, y)]
		Returns : [OpenCV Image]
		"""
		print("overlay")
		overlay_height, overlay_width = cv_overlay_image.shape[:2]
		background_height, background_width = cv_background_image.shape[:2]
		
		cv_bgr_result_image = cv_background_image.copy()

		# x座標がoverlay不可の範囲の時
		if point[0] < 0:
			point[0] = 0
		if point[0] > background_width - overlay_width:
			print("overlay12")
			point[0] = background_width - overlay_width
		# ｙ座標がoverlay不可の範囲の時
		if point[1] < 0:
			point[1] = 0
		if point[1] > background_height - overlay_height:
			print("overlay14")
			point[1] = background_height - overlay_height
		

		print("overlay2")
		cv_bgr_result_image[point[1]:overlay_height + point[1],point[0]:overlay_width + point[0]] *= 1 - cv_mask_image
		print("overlay3")
		cv_bgr_result_image[point[1]:overlay_height + point[1],point[0]:overlay_width + point[0]] += cv_overlay_image * cv_mask_image
		
		return cv_bgr_result_image

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
		 - DefaultValue: 347
		"""
		self._OVERLAY_IMAGE_SIZE_H = [347]
		"""
		
		 - Name:  OVERLAY_IMAGE_SIZE_W
		 - DefaultValue: 640
		"""
		self._OVERLAY_IMAGE_SIZE_W = [640]
		"""
		
		 - Name:  GAP
		 - DefaultValue: 75
		"""
		self._GAP = [75]
		
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
		self.bindParameter("OVERLAY_IMAGE_SIZE_H", self._OVERLAY_IMAGE_SIZE_H, "347")
		self.bindParameter("OVERLAY_IMAGE_SIZE_W", self._OVERLAY_IMAGE_SIZE_W, "640")
		self.bindParameter("GAP", self._GAP, "75")
		
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
		print("onActivated")
		global deco
		global image
		global cv_background_image
		global cv_overlay_image
		global dirlist_len
		global plist
		global image_list
		global mask_list


		cv_background_image = cv.imread("srcImage\\base\\" + "toyosuC2.jpg",cv.IMREAD_UNCHANGED)
		#cv_background_image = cv.imread("srcImage\\base\\" + "ohmiyaC.jpg",cv.IMREAD_UNCHANGED)
		image = cv_background_image
		
		path = "srcImage\\deco\\"
		dirlist = []
		for f in os.listdir(path):
			if os.path.isdir(os.path.join(path, f)):
				dirlist.append(f)
		print(dirlist)
		dirlist_len = len(dirlist)
		# dirlist_len は花火の種類の数

		plist = []

		# overlay_size_x = 640
		# overlay_size_y = 347

		# 画像をimreadして配列に保存
		# cv_overlay_image = cv.resize(cv_overlay_image, dsize=(overlay_size, overlay_size))
		image_list = []
		mask_list = []
		for f_num in dirlist:
			images = []
			masks = []
			i_path = "srcImage\\deco\\" + f_num + "\\*.png"
			for i_num in glob.glob(i_path):
				# print(i_num) # 読み込む画像のpath
				img = cv.imread(i_num, cv.IMREAD_UNCHANGED)
				img = cv.resize(img, (self._OVERLAY_IMAGE_SIZE_W[0], self._OVERLAY_IMAGE_SIZE_H[0]))				
				mask = img[:,:,3]
				mask = cv.cvtColor(mask,cv.COLOR_GRAY2BGR)
				mask = mask / 255
				mask = mask.astype('uint8')
				img = img[:,:,:3]
				images.append(img)
				masks.append(mask)
			image_list.append(images)
			mask_list.append(masks)
		print("complete image load")
		cv.namedWindow("decorate",cv.WINDOW_KEEPRATIO)
		cv.imshow("decorate", image)
		cv.waitKey(0)

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
		print("onDeactivated")
		cv.destroyAllWindows()
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
		global deco
		global image
		global cv_background_image
		global cv_overlay_image
		global dirlist_len
		global plist
		global image_list
		global mask_list


		if self._PosIn.isNew():
			print("isNew")
			Pos = self._PosIn.read()
			x = int(self._WINDOW_SIZE_W[0] - (Pos.data[0] * (self._WINDOW_SIZE_W[0] / self._SCREEN_SIZE_W[0])))
			y = int((Pos.data[1] + self._GAP[0]) * (self._WINDOW_SIZE_H[0] / self._SCREEN_SIZE_H[0]))
			# if 0.5*self._OVERLAY_IMAGE_SIZE_W[0] < x < self._WINDOW_SIZE_W[0] - 0.5*self._OVERLAY_IMAGE_SIZE_W[0] and 0.5*self._OVERLAY_IMAGE_SIZE_H[0] < y < self._WINDOW_SIZE_H[0] - 0.5*self._OVERLAY_IMAGE_SIZE_H[0]:
			plist.append([x,y,random.randrange(dirlist_len),0])
		if not len(plist) == 0:
			print(plist)
			for flist in plist:
				# point = (flist[0] - int(0.5 * self._OVERLAY_IMAGE_SIZE_W[0]),flist[1] - int(0.5 * self._OVERLAY_IMAGE_SIZE_H[0]))#座標が中心に来る
				point = [flist[0] - int(0.5 * self._OVERLAY_IMAGE_SIZE_W[0]),flist[1] - int(0.5 * self._OVERLAY_IMAGE_SIZE_H[0])]#座標が中心に来る				
				cv_overlay_image = image_list[flist[2]][flist[3]]
				cv_mask_image = mask_list[flist[2]][flist[3]]
				flist[3] += 1
				# print(flist[3])
				image = CvOverlayImage.overlay(image, cv_overlay_image, cv_mask_image, point)
			# cv.imshow("decorate", cv.resize(image, (1280, 960)))
			cv.imshow("decorate", image)
			# print("imshow")
			cv.waitKey(1)
			# print("waitkey")
			image = cv_background_image
			# print("background_image\n")
			print("end\n")

			if plist[0][3] >= 60:
				plist.remove(plist[0])
				print("remove")
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

