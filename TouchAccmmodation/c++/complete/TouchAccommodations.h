#ifndef TOUCHACCOMMODATIONS_H
#define TOUCHACCOMMODATIONS_H

#include <iostream>
#include <algorithm>
#include <vector>
#include <map>
#include <iomanip>
#include <string>
//#include "../cget/include/nlohmann/json.hpp"
#include "../json.hpp"
#include "Utility.h"
#include "MyTouchTask.h"
//#include "GestureClassification.h"
using namespace std;
using json = nlohmann::json;

class TouchAccommodations{
public:
	TouchAccommodations(double _fromTime, double _toTime);
	void SimulationDefaultRecognizer(ofstream* ofs, vector<string> *tasks, json *data);
	void FindBestParameter(ofstream* ofs, vector<string> *tasks, json *data,int *Choose_HD_Index, int *Choose_IR_Index,int *Choose_TA_Index,float *Choose_holdDurationTimer,float *Choose_ignoreRepeatTimer,float *Choose_tapAssistanceTimer);
	void TestParameter(ofstream* ofs, vector<string> *tasks, json *data,int *Choose_HD_Index, int *Choose_IR_Index,int *Choose_TA_Index,float *Choose_holdDurationTimer,float *Choose_ignoreRepeatTimer,float *Choose_tapAssistanceTimer);
	void FilterOneTask(string taskName, json *taskData, HoldDuration holdDuration, double holdDurationTimer, IgnoreRepeat ignoreRepeat, double ignoreRepeatTimer, TapAssistance tapAssistance, double tapAssistanceTimer);
private:
	vector<TouchAccommodationsPara> bestParameter;
	MyTouchTask _MyTouchTask;
	//GestureClassification _GestureClassification;
	map<string, json*> dataMod;
	double fromTime;
	double toTime;
};

#endif