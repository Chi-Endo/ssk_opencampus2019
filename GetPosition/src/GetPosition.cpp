// -*- C++ -*-
/*!
 * @file  GetPosition.cpp
 * @brief GetPositon
 * @date $Date$
 *
 * $Id$
 */

#include "GetPosition.h"

int getPoint(urg_t &urg, long *data, int data_num, long min_distance, long max_distance, long width, long height, long *result);
long getAverage(vector<long> &data, int standard_sd);

// Module specification
// <rtc-template block="module_spec">
static const char* getposition_spec[] =
{
  "implementation_id", "GetPosition",
  "type_name",         "GetPosition",
  "description",       "GetPositon",
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
GetPosition::GetPosition(RTC::Manager* manager)
// <rtc-template block="initializer">
	: RTC::DataFlowComponentBase(manager),
	m_PosOut("Pos", m_Pos)

	// </rtc-template>
{
}

/*!
 * @brief destructor
 */
GetPosition::~GetPosition()
{
}



RTC::ReturnCode_t GetPosition::onInitialize()
{
	// Registration: InPort/OutPort/Service
	// <rtc-template block="registration">
	// Set InPort buffers

	// Set OutPort buffer
	addOutPort("Pos", m_PosOut);

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
RTC::ReturnCode_t GetPosition::onFinalize()
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t GetPosition::onStartup(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t GetPosition::onShutdown(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/


RTC::ReturnCode_t GetPosition::onActivated(RTC::UniqueId ec_id)
{
	length_data = NULL;
	data_size = 0;
	min_distance = 0;
	max_distance = 0;

	//connect_device[]をコンフィグで定義
	ostringstream oss;
	oss << "COM" << m_DEVICE_NUM;
	const long connect_baudrate = 115200;

	// センサに対して接続を行う。
	//connect_deviceをossに変えた
	urg_open(&urg, URG_SERIAL, oss.str().c_str(), connect_baudrate);
	// データ受信のための領域を確保する
	length_data = (long *)malloc(sizeof(long) * urg_max_data_size(&urg));

	urg_set_scanning_parameter(&urg, urg_deg2step(&urg, -90), urg_deg2step(&urg, 90), 0);
	urg_distance_min_max(&urg, &min_distance, &max_distance);

	return RTC::RTC_OK;
}


RTC::ReturnCode_t GetPosition::onDeactivated(RTC::UniqueId ec_id)
{
	urg_stop_measurement(&urg);

	//  センサとの接続を閉じる。
	urg_close(&urg);
	free(length_data);

	return RTC::RTC_OK;
}


RTC::ReturnCode_t GetPosition::onExecute(RTC::UniqueId ec_id)
{
	int scan_time = 500;
	//vector<long> p;

	long result[2];
	vector<long> p_x;
	vector<long> p_y;
	int j = 0;

	urg_start_measurement(&urg, URG_DISTANCE, scan_time, 0);//500回データを取った
	data_size = urg_get_distance(&urg, length_data, NULL);//データ（距離+角度）を読み込む

	

	for (int i = 0; i < data_size; i++) {
		
		//if ((length > min_distance) && (length < max_distance))
		//if((length_data[i] > min_distance) && (length_data[i] < max_distance))
		
		int a = getPoint(urg,length_data, i, min_distance, max_distance, m_SCREEN_SIZE_W, m_SCREEN_SIZE_H,result);
		if (a != -1) {
			p_x.push_back(result[0]);
			p_y.push_back(result[1]);
		}
	}
	m_Pos.data.length(2);
	if (p_x.size() > 3) {

		long x_bar = getAverage(p_x, m_STANDARD_SD);
		if (x_bar != -1) {
			long y_bar = getAverage(p_y, m_STANDARD_SD);
			if (y_bar != -1){
				m_Pos.data[0] = x_bar;
				m_Pos.data[1] = y_bar;
				cout << "x =" << m_Pos.data[0] << endl;
				cout << "y =" << m_Pos.data[1] << endl;
				setTimestamp(m_Pos);
				m_PosOut.write();

			}
		}
	}
	return RTC::RTC_OK;
}

//スクリーン内の座標を取得
int getPoint(urg_t &urg,long *data, int data_num,long min_distance,long max_distance, long width, long height,long *result) {

	double radian = urg_index2rad(&urg, data_num);
	long length = data[data_num];
	if ((length > min_distance)&& (length < max_distance)) {	//センサが測れる距離データのみ
		long urg_x = (long)(length * cos(radian));
		long urg_y = (long)(length * sin(radian));
		result[0] = urg_y + (width / 2);
		result[1] = -urg_x + height;

		if ((0 <= result[0] && result[0] <= width) && (0 <= result[1] && result[1] <= height)) return 0;
		else return -1;
	}
	else return -1;
}
inline long sqr(long v) {

	return v * v;

}
//指定の標準偏差より、データの標準偏差が小さいとき、平均値を返す
long getAverage(vector<long> &data, int standard_sd) {
	int len = data.size();
	int i;
	long sum = 0;
	for (i = 0; i < len; i++) {
		sum += data[i];
	}
	long mean = sum / len;
	sum = 0;

	for (i = 0; i < len; i++) {
		sum += sqr(data[i] - mean);
	}
	long variance = sum / len;
	long sd = sqrt(variance);

	if (sd < standard_sd) return mean;
	else return -1;

}


/*
RTC::ReturnCode_t GetPosition::onAborting(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/


RTC::ReturnCode_t GetPosition::onError(RTC::UniqueId ec_id)
{
	return RTC::RTC_OK;
}

/*
RTC::ReturnCode_t GetPosition::onReset(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t GetPosition::onStateUpdate(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/

/*
RTC::ReturnCode_t GetPosition::onRateChanged(RTC::UniqueId ec_id)
{
  return RTC::RTC_OK;
}
*/



extern "C"
{

	void GetPositionInit(RTC::Manager* manager)
	{
		coil::Properties profile(getposition_spec);
		manager->registerFactory(profile,
			RTC::Create<GetPosition>,
			RTC::Delete<GetPosition>);
	}

};