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
		global filelist
		global plist
		# global overlay_size_x
		# global overlay_size_y
		global image_list


		cv_background_image = cv.imread("srcImage\\base\\" + "toyosuC2.jpg",cv.IMREAD_UNCHANGED)
		#cv_background_image = cv.imread("srcImage\\base\\" + "ohmiyaC.jpg",cv.IMREAD_UNCHANGED)
		image = cv_background_image
		
		path = "srcImage\\deco\\"
		filelist = []
		for f in os.listdir(path):
			if os.path.isdir(os.path.join(path, f)):
				filelist.append(f)
		print(filelist)

		plist = []

		# overlay_size_x = 640
		# overlay_size_y = 347

		# 画像をimreadして配列に保存
		# cv_overlay_image = cv.resize(cv_overlay_image, dsize=(overlay_size, overlay_size))
		image_list = []
		for f_num in filelist:
			images = []
			i_path = "srcImage\\deco\\" + f_num + "\\*.png"
			for i_num in glob.glob(i_path):
				# print(i_num) # 読み込む画像のpath
				img = cv.imread(i_num, cv.IMREAD_UNCHANGED)
				# print(img)
				# img = cv.resize(img, dsize=(960, 540))
				# img = cv.resize(img, (overlay_size_x, overlay_size_y))
				img = cv.resize(img, (self._OVERLAY_IMAGE_SIZE_W[0], self._OVERLAY_IMAGE_SIZE_H[0]))
				images.append(img)
			image_list.append(images)
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
		global filelist
		global plist
		# global overlay_size_x
		# global overlay_size_y
		global image_list
		# width = 1920
		# height = 1080
		# width = 1280
		# height = 960
		# screen_width = 1640


		if self._PosIn.isNew():
			print("isNew")
			Pos = self._PosIn.read()
			x = int(self._WINDOW_SIZE_W[0] - (Pos.data[0] * (self._WINDOW_SIZE_W[0] / self._SCREEN_SIZE_W[0])))
			y = int((Pos.data[1] + self._GAP[0]) * (self._WINDOW_SIZE_H[0] / self._SCREEN_SIZE_H[0]))
			# if 0.5*self._OVERLAY_IMAGE_SIZE_W[0] < x < self._WINDOW_SIZE_W[0] - 0.5*self._OVERLAY_IMAGE_SIZE_W[0] and 0.5*self._OVERLAY_IMAGE_SIZE_H[0] < y < self._WINDOW_SIZE_H[0] - 0.5*self._OVERLAY_IMAGE_SIZE_H[0]:
			plist.append([x,y,random.randrange(len(filelist)),0])
		if not len(plist) == 0:
			print(plist)
			for flist in plist:
				point = (flist[0] - int(0.5 * self._OVERLAY_IMAGE_SIZE_W[0]),flist[1] - int(0.5 * self._OVERLAY_IMAGE_SIZE_H[0]))#座標が中心に来る
				cv_overlay_image = image_list[flist[2]][flist[3]]
				flist[3] += 1
				print(flist[3])
				image = CvOverlayImage.overlay(image, cv_overlay_image,point)
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

