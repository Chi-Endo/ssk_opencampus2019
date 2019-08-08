// -*- C++ -*-
/*!
 * @file  CognizeTouchTest.cpp
 * @brief CognizeTouch
 * @date $Date$
 *
 * $Id$
 */

#include "CognizeTouchTest.h"

// Module specification
// <rtc-template block="module_spec">
static const char* cognizetouch_spec[] =
  {
    "implementation_id", "CognizeTouchTest",
    "type_name",         "CognizeTouchTest",
    "description",       "CognizeTouch",
    "version",           "1.0.0",
    "vendor",            "chi",
    "category",          "Category",
    "activity_type",     "PERIODIC",
    "kind",              "DataFlowComponent",
    "max_instance",      "1",
    "language",          "C++",
    "lang_type",         "compile",
    // Configuration variables
    "conf.default.INTERVAL_TIME", "1.0",

    // Widget
    "conf.__widget__.INTERVAL_TIME", "text",
    // Constraints

    "conf.__type__.INTERVAL_TIME", "float",

    ""
  };
// </rtc-template>

/*!
 * @brief constructor
 * @param manager Maneger Object
 */
CognizeTouchTest::CognizeTouchTest(RTC::Manager* manager)
    // <rtc-template block="initializer">
  : RTC::DataFlowComponentBase(manager),
    m_PosInIn("PosIn", m_PosIn),
    m_PosOutOut("PosOut", m_PosOut)

    // </rtc-template>
{
}

/*!
 * @brief destructor
 */
CognizeTouchTest::~CognizeTouchTest()
{
}



RTC::ReturnCode_t CognizeTouchTest::onInitialize()
{
  // Registration: InPort/OutPort/Service
  // <rtc-template block="registration">
  // Set InPort buffers
  addInPort("PosOut", m_PosOutIn);
  
  // Set OutPort buffer
  addOutPort("PosIn", m_PosInOut);
  
  // Set service provider to Ports
  
  // Set service consumers to Ports
  
  // Set CORBA Service Ports
  
  // </rtc-template>

  // <rtc-template block="bind_config">
  // Bind variables and configuration variable
  bindParameter("INTERVAL_TIME", m_INTERVAL_TIME, "1.0");
  // </rtc-template>
  
  return RTC::RTC_OK;
}

/*
RTC::ReturnCode_t CognizeTouchTest::onFinalize()
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouchTest::onStartup(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouchTest::onShutdown(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/


RTC::ReturnCode_t CognizeTouchTest::onActivated(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}

/*
RTC::ReturnCode_t CognizeTouchTest::onDeactivated(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/


RTC::ReturnCode_t CognizeTouchTest::onExecute(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}

/*
RTC::ReturnCode_t CognizeTouchTest::onAborting(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouchTest::onError(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouchTest::onReset(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouchTest::onStateUpdate(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouchTest::onRateChanged(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/



extern "C"
{
 
  void CognizeTouchTestInit(RTC::Manager* manager)
  {
    coil::Properties profile(cognizetouch_spec);
    manager->registerFactory(profile,
                             RTC::Create<CognizeTouchTest>,
                             RTC::Delete<CognizeTouchTest>);
  }
  
};


