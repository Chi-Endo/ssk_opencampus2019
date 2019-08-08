// -*- C++ -*-
/*!
 * @file  CognizeTouch.cpp
 * @brief CognizeTouch
 * @date $Date$
 *
 * $Id$
 */

#include "CognizeTouch.h"
long getAverage(vector<long> &data);

// Module specification
// <rtc-template block="module_spec">
static const char* cognizetouch_spec[] =
  {
    "implementation_id", "CognizeTouch",
    "type_name",         "CognizeTouch",
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
CognizeTouch::CognizeTouch(RTC::Manager* manager)
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
CognizeTouch::~CognizeTouch()
{
}



RTC::ReturnCode_t CognizeTouch::onInitialize()
{
  // Registration: InPort/OutPort/Service
  // <rtc-template block="registration">
  // Set InPort buffers
  addInPort("PosIn", m_PosInIn);
  
  // Set OutPort buffer
  addOutPort("PosOut", m_PosOutOut);
  
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
RTC::ReturnCode_t CognizeTouch::onFinalize()
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouch::onStartup(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouch::onShutdown(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/


RTC::ReturnCode_t CognizeTouch::onActivated(RTC::UniqueId ec_id)
{
	flag = 0;
	infinity_time = 0;
	xarray.clear();
	yarray.clear();

  return RTC::RTC_OK;
}

/*
RTC::ReturnCode_t CognizeTouch::onDeactivated(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/


RTC::ReturnCode_t CognizeTouch::onExecute(RTC::UniqueId ec_id)
{

	if (m_PosInIn.isNew()) {		//新しいデータが来たら

		m_PosInIn.read();

		if (flag == 0) {
			infinity_time = m_PosIn.tm.sec;		//データが入ってくる最初の時間を保存する
			flag = 1;								//フラグを立てる
		}
		xarray.push_back(m_PosIn.data[0]);
		yarray.push_back(m_PosIn.data[1]);

		if (m_PosIn.tm.sec > infinity_time + m_INTERVAL_TIME) {
			if (xarray.size() > 5) {
				m_PosOut.data.length(2);
				m_PosOut.data[0] = getAverage(xarray);
				m_PosOut.data[1] = getAverage(yarray);
				cout << "x =" << m_PosOut.data[0] << endl;
				cout << "y =" << m_PosOut.data[1] << endl;
				m_PosOutOut.write();
			}
			xarray.clear();
			yarray.clear();

			flag = 0;
		}
		
	}
  return RTC::RTC_OK;
}
long getAverage(vector<long> &data) {
	
	long sum = 0;
	for (int i = 0; i < data.size(); i++) {
		sum += data[i];
	}
	return sum / data.size();
}

/*
RTC::ReturnCode_t CognizeTouch::onAborting(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouch::onError(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouch::onReset(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouch::onStateUpdate(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t CognizeTouch::onRateChanged(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/



extern "C"
{
 
  void CognizeTouchInit(RTC::Manager* manager)
  {
    coil::Properties profile(cognizetouch_spec);
    manager->registerFactory(profile,
                             RTC::Create<CognizeTouch>,
                             RTC::Delete<CognizeTouch>);
  }
  
};


