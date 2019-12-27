#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
@file ImageGenerator.py
@brief ModuleDescription
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
# import glob #追記
# import threading #追記

global deco
global image
global cv_background_image#解像度は3280*2800
global cv_overlay_image

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
imagegenerator_spec = ["implementation_id", "ImageGenerator", 
		 "type_name",         "ImageGenerator", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "AidaRena", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
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
		point,
		):
		"""
		[summary]
			OpenCV形式の画像に指定画像を重ねる
		Parameters
		----------
		cv_background_image : [OpenCV Image]
		cv_overlay_image : [OpenCV Image]
		point : [(x, y)]
		Returns : [OpenCV Image]
		"""
		overlay_height, overlay_width = cv_overlay_image.shape[:2]

		# OpenCV形式の画像をPIL形式に変換(α値含む)
		# 背景画像
		cv_rgb_bg_image = cv.cvtColor(cv_background_image, cv.COLOR_BGR2RGB)
		pil_rgb_bg_image = Image.fromarray(cv_rgb_bg_image)
		pil_rgba_bg_image = pil_rgb_bg_image.convert('RGBA')
		# オーバーレイ画像
		cv_rgb_ol_image = cv.cvtColor(cv_overlay_image, cv.COLOR_BGRA2RGBA)
		pil_rgb_ol_image = Image.fromarray(cv_rgb_ol_image)
		pil_rgba_ol_image = pil_rgb_ol_image.convert('RGBA')

		# composite()は同サイズ画像同士が必須のため、合成用画像を用意
		pil_rgba_bg_temp = Image.new('RGBA', pil_rgba_bg_image.size,
										(255, 255, 255, 0))
		# 座標を指定し重ね合わせる
		pil_rgba_bg_temp.paste(pil_rgba_ol_image, point, pil_rgba_ol_image)
		result_image = \
			Image.alpha_composite(pil_rgba_bg_image, pil_rgba_bg_temp)

		# OpenCV形式画像へ変換
		cv_bgr_result_image = cv.cvtColor(np.asarray(result_image), cv.COLOR_RGBA2BGRA)

		return cv_bgr_result_image
##
# @class ImageGenerator
# @brief ModuleDescription
# 
# 
class ImageGenerator(OpenRTM_aist.DataFlowComponentBase):
	deco = None
	image = None
	cv_background_image = None#解像度は3280*2800
	cv_overlay_image = None
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_LRF_data = OpenRTM_aist.RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._LRF_dataIn = OpenRTM_aist.InPort("LRF_data", self._d_LRF_data)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
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
		
		# Set InPort buffers
		self.addInPort("LRF_data",self._LRF_dataIn)
		
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
		global cv_background_image#解像度は3280*2800
		global cv_overlay_image
		cv.namedWindow("decorate",cv.WINDOW_KEEPRATIO)
		cv_background_image = cv.imread("srcImage\\base\\" + "base01.jpg",cv.IMREAD_UNCHANGED)
		image = cv_background_image
		cv.imshow("decorate", image)
		print("wait")
		cv.waitKey(10)#画面をスクリーンのサイズに合わせるための待ち
		print("onActivated end")

		path = "srcImage\\deco\\"
		filelist = []
		for f in os.listdir(path):
			if os.path.isdir(os.path.join(path, f)):
				filelist.append(f)
		print(filelist)
		return RTC.RTC_OK
	
	###
	##
	## The deactivated action (Active state exit action)
	## former rtc_active_exit()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
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
		global plist
		overlay_size = 300
		# width = 3280
		# height = 2400
		#座標を取得したら
		print("onExecuted")
		if self._LRF_dataIn.isNew():
			print("isNew")
			# LRF_dataIn.read()
			LRF_data = self._LRF_dataIn.read()
			print("read")
			# self._LRF_dataIn.read()
			# print(LRF_data.data)
			# point = (x - int(0.5 * overlay_size),y - int(0.5 * overlay_size))
			plist.append([LRF_data.data[0]*2,LRF_data.data[1]*2,random.randrange(len(filelist)),1])
			# plist.append([_d_LRF_data.data[0]*2,_d_LRF_data.data[1]*2,random.randrange(len(filelist)),1])
	# count += 1

		if len(plist) > 0:
			print("infor")
			# 4飛ばし
			for flist in plist:
				point (flist[0]- int(0.5 * overlay_size),flist[1]- int(0.5 * overlay_size))#座標が中心に来る
				# cv_overlay_image = cv.imread("srcImage\\deco\\" + filelist[flist[2] + "\\fireworks(" + str(flist[3])+ ").png", cv.IMREAD_UNCHANGED)
				cv_overlay_image = cv.imread("srcImage\\deco\\" + filelist[flist[2]] + "\\fireworks(" + str(filelist[3]) + ").png", cv.IMREAD_UNCHANGED)
				flist[3] += 1
				cv_overlay_image = cv.resize(cv_overlay_image, (1920, 1080))
				image = CvOverlayImage.overlay(image, cv_overlay_image,point) 
			cv.imshow("decorate", image)
			cv.waitKey(10)
			image = cv_background_image

			if plist[0][3] >= 61:
				plist.remove(plist[0]);
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
	



def ImageGeneratorInit(manager):
	profile = OpenRTM_aist.Properties(defaults_str=imagegenerator_spec)
	manager.registerFactory(profile,
							ImageGenerator,
							OpenRTM_aist.Delete)

def MyModuleInit(manager):
	ImageGeneratorInit(manager)

	# Create a component
	comp = manager.createComponent("ImageGenerator")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

