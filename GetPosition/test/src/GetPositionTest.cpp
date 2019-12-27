﻿// -*- C++ -*-
/*!
 * @file  GetPositionTest.cpp
 * @brief GetPosition
 * @date $Date$
 *
 * $Id$
 */

#include "GetPositionTest.h"

// Module specification
// <rtc-template block="module_spec">
static const char* getposition_spec[] =
  {
    "implementation_id", "GetPositionTest",
    "type_name",         "GetPositionTest",
    "description",       "GetPosition",
    "version",           "1.0.0",
    "vendor",            "chi",
    "category",          "Category",
    "activity_type",     "PERIODIC",
    "kind",              "DataFlowComponent",
    "max_instance",      "1",
    "language",          "C++",
    "lang_type",         "compile",
    // Configuration variables
    "conf.default.DEVICE_NUM", "4",
    "conf.default.SCREEN_SIZE_W", "1640",
    "conf.default.SCREEN_SIZE_H", "1200",
    "conf.default.STANDARD_SD", "30",

    // Widget
    "conf.__widget__.DEVICE_NUM", "text",
    "conf.__widget__.SCREEN_SIZE_W", "text",
    "conf.__widget__.SCREEN_SIZE_H", "text",
    "conf.__widget__.STANDARD_SD", "text",
    // Constraints

    "conf.__type__.DEVICE_NUM", "int",
    "conf.__type__.SCREEN_SIZE_W", "int",
    "conf.__type__.SCREEN_SIZE_H", "int",
    "conf.__type__.STANDARD_SD", "int",

    ""
  };
// </rtc-template>

/*!
 * @brief constructor
 * @param manager Maneger Object
 */
GetPositionTest::GetPositionTest(RTC::Manager* manager)
    // <rtc-template block="initializer">
  : RTC::DataFlowComponentBase(manager),
    m_PosOut("Pos", m_Pos)

    // </rtc-template>
{
}

/*!
 * @brief destructor
 */
GetPositionTest::~GetPositionTest()
{
}



RTC::ReturnCode_t GetPositionTest::onInitialize()
{
  // Registration: InPort/OutPort/Service
  // <rtc-template block="registration">
  // Set InPort buffers
  addInPort("Pos", m_PosIn);
  
  // Set OutPort buffer
  
  // Set service provider to Ports
  
  // Set service consumers to Ports
  
  // Set CORBA Service Ports
  
  // </rtc-template>

  // <rtc-template block="bind_config">
  // Bind variables and configuration variable
  bindParameter("DEVICE_NUM", m_DEVICE_NUM, "4");
  bindParameter("SCREEN_SIZE_W", m_SCREEN_SIZE_W, "1640");
  bindParameter("SCREEN_SIZE_H", m_SCREEN_SIZE_H, "1200");
  bindParameter("STANDARD_SD", m_STANDARD_SD, "30");
  // </rtc-template>
  
  return RTC::RTC_OK;
}

/*
RTC::ReturnCode_t GetPositionTest::onFinalize()
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t GetPositionTest::onStartup(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t GetPositionTest::onShutdown(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/


RTC::ReturnCode_t GetPositionTest::onActivated(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}


RTC::ReturnCode_t GetPositionTest::onDeactivated(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}


RTC::ReturnCode_t GetPositionTest::onExecute(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}

/*
RTC::ReturnCode_t GetPositionTest::onAborting(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/


RTC::ReturnCode_t GetPositionTest::onError(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}

/*
RTC::ReturnCode_t GetPositionTest::onReset(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t GetPositionTest::onStateUpdate(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t GetPositionTest::onRateChanged(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/



extern "C"
{
 
  void GetPositionTestInit(RTC::Manager* manager)
  {
    coil::Properties profile(getposition_spec);
    manager->registerFactory(profile,
                             RTC::Create<GetPositionTest>,
                             RTC::Delete<GetPositionTest>);
  }
  
};


