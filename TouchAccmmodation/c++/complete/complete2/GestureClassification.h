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

class GestureClassification{
public:
	GestureClassification();
	double GestureClassify(vector<string> *tasks, map<string, json*> *data);
	double Classify(json *taskData);
	double TapTask(json *taskData);
	//double TapTaskScrollView(json *taskData);
	double LongPressTask(json *taskData);
	double HorizontalScrollTask(json *taskData);
	double VerticalScrollTask(json *taskData);
	double SwipeTask(json *taskData);
private:
	double successRate;
	double TapMaximumDuration = 1.5;
	double TapAllowableMovement = 10;
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