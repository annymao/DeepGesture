#ifndef MYTOUCHTASK_H
#define MYTOUCHTASK_H

#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <algorithm>
//#include <nlohmann/json.hpp>
#include "json.hpp"
using namespace std;
using json = nlohmann::json;

class MyTouchTask{
public:
	MyTouchTask();
	double GetSuccessRate(vector<string> *tasks, map<string, json*> *data);
	double GetSuccessRate2(vector<string> *tasks, map<string, json*> *data,int mode);

	double ClassificationTask(json *taskData,int taskIndex,int mode);
	double TapTask(json *taskData);
	//double TapTaskScrollView(json *taskData);
	double LongPressTask(json *taskData);
	double HorizontalScrollTask(json *taskData);
	double VerticalScrollTask(json *taskData);
	double SwipeTask(json *taskData);
	double PinchTask(json *taskData);
	double RotationTask(json *taskData);

	void SetScreenSize(double x, double y);
	void SetOutputStream(ofstream* _ofs);
private:
	double successRate;
	double TapMaximumDuration = 1.5;
	double TapAllowableMovement = 45;
	double LongPressMinimumPressDuration = 0.5;
	double LongPressAllowableMovement = 10;
	double PanHysteresis = 10;
	double PanMagicNumberX = 0.35;
	double PanMagicNumberY = 0.35;
	double SwipeMaximumDuration = 0.5;
	double SwipeMinimumMovement = 30;
	double SwipeMinimumVelocity = 200;
	double PinchHysteresis = 8;
	double RotationHysteresis = 10.0 / 180 * M_PI;
	double RotationMaximumAngleEachTimestamp = 0.785;

	double screenSizeX;
	double screenSizeY;

	ofstream* ofs;
};

#endif