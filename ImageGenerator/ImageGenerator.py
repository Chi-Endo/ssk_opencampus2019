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
import glob

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
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_LRF_data = OpenRTM_aist.instantiateDataType(RTC.TimedLongSeq)
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
		global filelist
		global plist
		global overlay_size_x
		global overlay_size_y
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

		overlay_size_x = 640
		overlay_size_y = 347

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
				img = cv.resize(img, (overlay_size_x, overlay_size_y))
				images.append(img)
			image_list.append(images)
		print("complete image load")
		# image = cv.resize(image, (1280, 960)) endo0807
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
		global overlay_size_x
		global overlay_size_y
		global image_list
		# width = 1920
		# height = 1080
		width = 1280
		height = 960
		screen_width = 1640


		if self._LRF_dataIn.isNew():
			print("isNew")
			LRF_data = self._LRF_dataIn.read()
			# x = LRF_data.data[0] * (width/screen_width)
			# y = LRF_data.data[1] * (width/screen_width)
			x = int(LRF_data.data[0] * 0.78)
			y = int(LRF_data.data[1] * 0.78)
			# if overlay_size_x < x < width - overlay_size_x and overlay_size_y < y < height - overlay_size_y:
			# if 10 < x < width - 0.5*overlay_size_x and 10 < y < height - 0.5*overlay_size_y:
			if 0.5*overlay_size_x < x < width - 0.5*overlay_size_x and 0.5*overlay_size_y < y < height - 0.5*overlay_size_y:
				plist.append([x,y,random.randrange(len(filelist)),0])
				print("")
		if not len(plist) == 0:
			print(plist)
			for flist in plist:
				point = (flist[0] - int(0.5 * overlay_size_x),flist[1] - int(0.5 * overlay_size_y))#座標が中心に来る
				cv_overlay_image = image_list[flist[2]][flist[3]]
				flist[3] += 1
				print(flist[3])
				image = CvOverlayImage.overlay(image, cv_overlay_image,point)
			cv.imshow("decorate", cv.resize(image, (1280, 960)))
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

