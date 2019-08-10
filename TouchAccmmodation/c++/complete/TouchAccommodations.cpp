#include "TouchAccommodations.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
TouchAccommodations::TouchAccommodations(double _fromTime, double _toTime){
	fromTime = _fromTime;
	toTime = _toTime;
	_MyTouchTask = MyTouchTask();
	//_GestureClassification=GestureClassification();
}


void TouchAccommodations::SimulationDefaultRecognizer(ofstream* ofs, vector<string> *tasks, json *data){

	

	_MyTouchTask.SetScreenSize(double((*data)["deviceInfo"]["screenSize"][0]), double((*data)["deviceInfo"]["screenSize"][1]));
	_MyTouchTask.SetOutputStream(ofs);

	vector<string>::iterator iterString;

	bestParameter.clear();
	// Hold Duration (range = 0.10 - 4.00, delta = 0.05)
	HoldDuration holdDuration[2] = {holdDurationOff, holdDurationOn};
	// Ignore Repeat (range = 0.10 - 4.00, delta = 0.05)
	IgnoreRepeat ignoreRepeat[2] = {ignoreRepeatOff, ignoreRepeatOn};
	// Tap Assistance (range = 0.10 - 4.00, delta = 0.05)
	TapAssistance tapAssistance[3] = {tapAssistanceOff, tapAssistanceInit, tapAssistanceFinal};

	double successRateMax = -1.0;
	double successRate;
	dataMod.clear();
	for (iterString = (*tasks).begin() ; iterString != (*tasks).end() ; iterString++){
								dataMod[(*iterString)] = &((*data)[(*iterString)]);
								// FilterOneTask((*iterString), &((*data)[(*iterString)]), 
								// 	holdDuration[HD_Index], holdDurationTimer, 
								// 	ignoreRepeat[IR_Index], ignoreRepeatTimer, 
								// 	tapAssistance[TA_Index], tapAssistanceTimer
								// );
							}
	// dataMod=data;
	// cout << *data <<" " << endl;
	successRate = _MyTouchTask.GetSuccessRate2(tasks, &dataMod,0);
	//printf("GoClassify");
	//successRate = _GestureClassification.GestureClassify(tasks, &dataMod);
	//cout << successRate << endl;
	//return;

							
}


void TouchAccommodations::TestParameter(ofstream* ofs, vector<string> *tasks, json *data,int *Choose_HD_Index, int *Choose_IR_Index,int *Choose_TA_Index,float *Choose_holdDurationTimer,float *Choose_ignoreRepeatTimer,float *Choose_tapAssistanceTimer){

	printf("GoFindBest\n");

	//_MyTouchTask.SetScreenSize(double((*data)["deviceInfo"]["screenSize"][0]), double((*data)["deviceInfo"]["screenSize"][1]));
	_MyTouchTask.SetOutputStream(ofs);

	vector<string>::iterator iterString;

	bestParameter.clear();
	// Hold Duration (range = 0.10 - 4.00, delta = 0.05)
	HoldDuration holdDuration[2] = {holdDurationOff, holdDurationOn};
	// Ignore Repeat (range = 0.10 - 4.00, delta = 0.05)
	IgnoreRepeat ignoreRepeat[2] = {ignoreRepeatOff, ignoreRepeatOn};
	// Tap Assistance (range = 0.10 - 4.00, delta = 0.05)
	TapAssistance tapAssistance[3] = {tapAssistanceOff, tapAssistanceInit, tapAssistanceFinal};

	double successRateMax = -1.0;
	double successRate;
	
	int Choose_HD_Index_temp=*Choose_HD_Index;
	int Choose_IR_Index_temp=*Choose_IR_Index;
	int Choose_TA_Index_temp=*Choose_TA_Index;
	float Choose_holdDurationTimer_temp=*Choose_holdDurationTimer;
	float Choose_ignoreRepeatTimer_temp=*Choose_ignoreRepeatTimer;
	float Choose_tapAssistanceTimer_temp=*Choose_tapAssistanceTimer;
	dataMod.clear();
	//cout<<"Begin To Filter data in " <<" " <<HD_Index  <<" " <<IR_Index <<" " << TA_Index <<" "<< holdDurationTimer <<" "<< ignoreRepeatTimer <<" " << tapAssistanceTimer<<endl;
	for (iterString = (*tasks).begin() ; iterString != (*tasks).end() ; iterString++){
		dataMod[(*iterString)] = new json();
		FilterOneTask((*iterString), &((*data)[(*iterString)]), 
			holdDuration[Choose_HD_Index_temp], Choose_holdDurationTimer_temp, 
			ignoreRepeat[Choose_IR_Index_temp], Choose_ignoreRepeatTimer_temp, 
			tapAssistance[Choose_TA_Index_temp], Choose_tapAssistanceTimer_temp
		);
	}

	cout<<" Filter End in " <<Choose_HD_Index_temp<<" " <<Choose_IR_Index_temp<<" " <<Choose_TA_Index_temp<<" " <<Choose_holdDurationTimer_temp<<" " <<Choose_ignoreRepeatTimer_temp<<" " <<Choose_tapAssistanceTimer_temp<<" "<<endl;
	successRate = _MyTouchTask.GetSuccessRate2(tasks, &dataMod,1);
	

	for (iterString = (*tasks).begin() ; iterString != (*tasks).end() ; iterString++){
		delete dataMod[(*iterString)];
	}

	

	//successRate = _GestureClassification.GestureClassify(tasks, &dataMod);
	cout << successRate << endl;

	// for (int HD_Index = 0 ; HD_Index < 1 ; HD_Index++){
	// 	for (int IR_Index = 0 ; IR_Index < 1 ; IR_Index++){
	// 		for (int TA_Index = 0 ; TA_Index < 1 ; TA_Index++){
	// 			//cout << HD_Index << " " << IR_Index << " " << TA_Index << endl;
	// 			//cout << holdDuration[HD_Index] << " " << ignoreRepeat[IR_Index] << " " << tapAssistance[TA_Index] << endl;
	// 			for (float holdDurationTimer = 0.0 ; holdDurationTimer <= 0.3 ; holdDurationTimer = holdDurationTimer + 0.05){
	// 				for (float ignoreRepeatTimer = 0.0 ; ignoreRepeatTimer <= 0.3 ; ignoreRepeatTimer = ignoreRepeatTimer + 0.05){
	// 					for (float tapAssistanceTimer = 0.0 ; tapAssistanceTimer <= 0.3 ; tapAssistanceTimer = tapAssistanceTimer + 0.05){
	// 						// (*ofs) << holdDuration[HD_Index] << " " << holdDurationTimer << " " << ignoreRepeat[IR_Index] << " " << ignoreRepeatTimer << " " << tapAssistance[TA_Index] << " " << tapAssistanceTimer << " ";
	// 						// cout<<holdDuration[HD_Index] << " " << holdDurationTimer << " " << ignoreRepeat[IR_Index] << " " << ignoreRepeatTimer << " " << tapAssistance[TA_Index] << " " << tapAssistanceTimer << " "<<endl;
	// 						dataMod.clear();
	// 						//cout<<"Begin To Filter data in " <<" " <<HD_Index  <<" " <<IR_Index <<" " << TA_Index <<" "<< holdDurationTimer <<" "<< ignoreRepeatTimer <<" " << tapAssistanceTimer<<endl;
	// 						for (iterString = (*tasks).begin() ; iterString != (*tasks).end() ; iterString++){
	// 							dataMod[(*iterString)] = new json();
	// 							FilterOneTask((*iterString), &((*data)[(*iterString)]), 
	// 								holdDuration[HD_Index], holdDurationTimer, 
	// 								ignoreRepeat[IR_Index], ignoreRepeatTimer, 
	// 								tapAssistance[TA_Index], tapAssistanceTimer
	// 							);
	// 						}

	// 						cout<<" Filter End"<<endl;
	// 						successRate = _MyTouchTask.GetSuccessRate2(tasks, &dataMod);
							

	// 						for (iterString = (*tasks).begin() ; iterString != (*tasks).end() ; iterString++){
	// 							delete dataMod[(*iterString)];
	// 						}

	// 						if (successRate>successRateMax){
	// 							Choose_HD_Index_temp=HD_Index;
	// 							Choose_IR_Index_temp=IR_Index;
	// 							Choose_TA_Index_temp=TA_Index;
	// 							Choose_holdDurationTimer_temp=holdDurationTimer;
	// 							Choose_ignoreRepeatTimer_temp=ignoreRepeatTimer;
	// 							Choose_tapAssistanceTimer_temp=tapAssistanceTimer;
	// 							successRateMax=successRate;
	// 						}

	// 						//successRate = _GestureClassification.GestureClassify(tasks, &dataMod);
	// 						cout << successRate << endl;
	// 						//return;


							

	// 						/*
	// 						if (successRate == successRateMax){
	// 							TouchAccommodationsPara para;
	// 							para.holdDuration = holdDuration[HD_Index];
	// 							para.ignoreRepeat = ignoreRepeat[IR_Index];
	// 							para.tapAssistance =  tapAssistance[TA_Index];
	// 							para.holdDurationTimer = holdDurationTimer;
	// 							para.ignoreRepeatTimer = ignoreRepeatTimer;
	// 							para.tapAssistanceTimer = tapAssistanceTimer;
	// 							bestParameter.push_back(para);
	// 						} else if (successRate > successRateMax){
	// 							bestParameter.clear();
	// 							TouchAccommodationsPara para;
	// 							para.holdDuration = holdDuration[HD_Index];
	// 							para.ignoreRepeat = ignoreRepeat[IR_Index];
	// 							para.tapAssistance =  tapAssistance[TA_Index];
	// 							para.holdDurationTimer = holdDurationTimer;
	// 							para.ignoreRepeatTimer = ignoreRepeatTimer;
	// 							para.tapAssistanceTimer = tapAssistanceTimer;
	// 							bestParameter.push_back(para);
	// 						}
	// 						cout << holdDuration[HD_Index] << " " << holdDurationTimer << " "
	// 							 << ignoreRepeat[IR_Index] << " " << ignoreRepeatTimer << " "
	// 							 << tapAssistance[TA_Index] << " " << tapAssistanceTimer << " "
	// 							 << successRate << endl;
	// 						*/
	// 						if (tapAssistance[TA_Index] == tapAssistanceOff){
	// 							break;
	// 						}
	// 					}
	// 					if (ignoreRepeat[IR_Index] == ignoreRepeatOff){
	// 						break;
	// 					}
	// 				}
	// 				if (holdDuration[HD_Index] == holdDurationOff){
	// 					break;
	// 				}
	// 			}
	// 		}
	// 	}
	// }

	// *Choose_HD_Index=Choose_HD_Index_temp;
	// *Choose_IR_Index=Choose_IR_Index_temp;
	// *Choose_TA_Index=Choose_TA_Index_temp;
	// *Choose_holdDurationTimer=Choose_holdDurationTimer_temp;
	// *Choose_ignoreRepeatTimer=Choose_ignoreRepeatTimer_temp;
	// *Choose_tapAssistanceTimer=Choose_tapAssistanceTimer_temp;


	// cout<<"Choose: "<<Choose_HD_Index<<" "<<Choose_IR_Index<<" "<<Choose_TA_Index<<" "<<Choose_holdDurationTimer<<" "<<Choose_ignoreRepeatTimer<<" "<<Choose_tapAssistanceTimer<<" Success Rate "<<successRateMax<<endl;
	// //return Choose_HD_Index,Choose_IR_Index,Choose_TA_Index,Choose_holdDurationTimer,Choose_ignoreRepeatTimer,Choose_tapAssistanceTimer
}

void TouchAccommodations::FindBestParameter(ofstream* ofs, vector<string> *tasks, json *data,int *Choose_HD_Index, int *Choose_IR_Index,int *Choose_TA_Index,float *Choose_holdDurationTimer,float *Choose_ignoreRepeatTimer,float *Choose_tapAssistanceTimer){

	printf("GoFindBest\n");

	//_MyTouchTask.SetScreenSize(double((*data)["deviceInfo"]["screenSize"][0]), double((*data)["deviceInfo"]["screenSize"][1]));
	_MyTouchTask.SetOutputStream(ofs);

	vector<string>::iterator iterString;

	bestParameter.clear();
	// Hold Duration (range = 0.10 - 4.00, delta = 0.05)
	HoldDuration holdDuration[2] = {holdDurationOff, holdDurationOn};
	// Ignore Repeat (range = 0.10 - 4.00, delta = 0.05)
	IgnoreRepeat ignoreRepeat[2] = {ignoreRepeatOff, ignoreRepeatOn};
	// Tap Assistance (range = 0.10 - 4.00, delta = 0.05)
	TapAssistance tapAssistance[3] = {tapAssistanceOff, tapAssistanceInit, tapAssistanceFinal};

	double successRateMax = -1.0;
	double successRate;
	
	int Choose_HD_Index_temp=0;
	int Choose_IR_Index_temp=0;
	int Choose_TA_Index_temp=0;
	float Choose_holdDurationTimer_temp=0.0;
	float Choose_ignoreRepeatTimer_temp=0.0;
	float Choose_tapAssistanceTimer_temp=0.0;

	for (int HD_Index = 0 ; HD_Index < 2 ; HD_Index++){
		for (int IR_Index = 0 ; IR_Index < 2 ; IR_Index++){
			for (int TA_Index = 0 ; TA_Index < 3 ; TA_Index++){
				//cout << HD_Index << " " << IR_Index << " " << TA_Index << endl;
				//cout << holdDuration[HD_Index] << " " << ignoreRepeat[IR_Index] << " " << tapAssistance[TA_Index] << endl;
				for (float holdDurationTimer = fromTime ; holdDurationTimer <= toTime ; holdDurationTimer = holdDurationTimer + 0.05){
					for (float ignoreRepeatTimer = fromTime ; ignoreRepeatTimer <= toTime ; ignoreRepeatTimer = ignoreRepeatTimer + 0.05){
						for (float tapAssistanceTimer = fromTime ; tapAssistanceTimer <= toTime ; tapAssistanceTimer = tapAssistanceTimer + 0.05){
							// (*ofs) << holdDuration[HD_Index] << " " << holdDurationTimer << " " << ignoreRepeat[IR_Index] << " " << ignoreRepeatTimer << " " << tapAssistance[TA_Index] << " " << tapAssistanceTimer << " ";
							// cout<<holdDuration[HD_Index] << " " << holdDurationTimer << " " << ignoreRepeat[IR_Index] << " " << ignoreRepeatTimer << " " << tapAssistance[TA_Index] << " " << tapAssistanceTimer << " "<<endl;
							dataMod.clear();
							//cout<<"Begin To Filter data in " <<" " <<HD_Index  <<" " <<IR_Index <<" " << TA_Index <<" "<< holdDurationTimer <<" "<< ignoreRepeatTimer <<" " << tapAssistanceTimer<<endl;
							for (iterString = (*tasks).begin() ; iterString != (*tasks).end() ; iterString++){
								dataMod[(*iterString)] = new json();
								FilterOneTask((*iterString), &((*data)[(*iterString)]), 
									holdDuration[HD_Index], holdDurationTimer, 
									ignoreRepeat[IR_Index], ignoreRepeatTimer, 
									tapAssistance[TA_Index], tapAssistanceTimer
								);
							}

							//cout<<" Filter End"<<endl;
							successRate = _MyTouchTask.GetSuccessRate2(tasks, &dataMod,0);
							

							for (iterString = (*tasks).begin() ; iterString != (*tasks).end() ; iterString++){
								delete dataMod[(*iterString)];
							}

							if (successRate>successRateMax){
								Choose_HD_Index_temp=HD_Index;
								Choose_IR_Index_temp=IR_Index;
								Choose_TA_Index_temp=TA_Index;
								Choose_holdDurationTimer_temp=holdDurationTimer;
								Choose_ignoreRepeatTimer_temp=ignoreRepeatTimer;
								Choose_tapAssistanceTimer_temp=tapAssistanceTimer;
								successRateMax=successRate;
							}

							//successRate = _GestureClassification.GestureClassify(tasks, &dataMod);
							//cout << successRate << endl;
							//return;


							

							/*
							if (successRate == successRateMax){
								TouchAccommodationsPara para;
								para.holdDuration = holdDuration[HD_Index];
								para.ignoreRepeat = ignoreRepeat[IR_Index];
								para.tapAssistance =  tapAssistance[TA_Index];
								para.holdDurationTimer = holdDurationTimer;
								para.ignoreRepeatTimer = ignoreRepeatTimer;
								para.tapAssistanceTimer = tapAssistanceTimer;
								bestParameter.push_back(para);
							} else if (successRate > successRateMax){
								bestParameter.clear();
								TouchAccommodationsPara para;
								para.holdDuration = holdDuration[HD_Index];
								para.ignoreRepeat = ignoreRepeat[IR_Index];
								para.tapAssistance =  tapAssistance[TA_Index];
								para.holdDurationTimer = holdDurationTimer;
								para.ignoreRepeatTimer = ignoreRepeatTimer;
								para.tapAssistanceTimer = tapAssistanceTimer;
								bestParameter.push_back(para);
							}
							cout << holdDuration[HD_Index] << " " << holdDurationTimer << " "
								 << ignoreRepeat[IR_Index] << " " << ignoreRepeatTimer << " "
								 << tapAssistance[TA_Index] << " " << tapAssistanceTimer << " "
								 << successRate << endl;
							*/
							if (tapAssistance[TA_Index] == tapAssistanceOff){
								break;
							}
						}
						if (ignoreRepeat[IR_Index] == ignoreRepeatOff){
							break;
						}
					}
					if (holdDuration[HD_Index] == holdDurationOff){
						break;
					}
				}
			}
		}
	}

	*Choose_HD_Index=Choose_HD_Index_temp;
	*Choose_IR_Index=Choose_IR_Index_temp;
	*Choose_TA_Index=Choose_TA_Index_temp;
	*Choose_holdDurationTimer=Choose_holdDurationTimer_temp;
	*Choose_ignoreRepeatTimer=Choose_ignoreRepeatTimer_temp;
	*Choose_tapAssistanceTimer=Choose_tapAssistanceTimer_temp;


	cout<<"Choose: "<<Choose_HD_Index<<" "<<Choose_IR_Index<<" "<<Choose_TA_Index<<" "<<Choose_holdDurationTimer<<" "<<Choose_ignoreRepeatTimer<<" "<<Choose_tapAssistanceTimer<<" Success Rate "<<successRateMax<<endl;
	//return Choose_HD_Index,Choose_IR_Index,Choose_TA_Index,Choose_holdDurationTimer,Choose_ignoreRepeatTimer,Choose_tapAssistanceTimer
}

void TouchAccommodations::FilterOneTask(string taskName, json *taskData,
 HoldDuration holdDuration, double holdDurationTimer, 
 IgnoreRepeat ignoreRepeat, double ignoreRepeatTimer, 
 TapAssistance tapAssistance, double tapAssistanceTimer){
	//cout << (*taskData) << endl;
	//(*taskData)["trials"][0]["rawTouchTracks"][0]["rawTouches"][0]["timestamp"]
	//cout << (*taskDataMod[taskName]) << endl;

	vector<bool>::iterator iterBool;

	*(dataMod[taskName]) = *taskData;
	//(*(dataMod[taskName]))["trials"][0]["rawTouchTracks"] = json::array();
	//cout << *taskData << endl << endl;
	//cout << *(dataMod[taskName]) << endl << endl << endl;

	int trialNum = (*taskData)["trials"].size();
	//cout << trialNum << endl;

	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){

		int trackNum = (*taskData)["trials"][trialIndex]["rawTouchTracks"].size();
		for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
			(*(dataMod[taskName]))["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"] = json::array();
		}
		//cout << trackNum << endl; // how many tracks?

		// There may be more than one track within a trial
		vector<int> trackIndexArr(trackNum, 0);
		vector<bool> trackEndedArr(trackNum, false);
		vector<bool> trackTouchedArr(trackNum, false);
		//cout << trackIndexArr.size() << endl;

		// Constant
		double TapAssistanceFinalLocationThreshold = 42.0; // unit: pt

		// Initialization
		bool isTouched = false;
		double timestampReferenceForHoldDuration = 0.0;
		bool flagInitForTapAssistance = false;
		double timestampReferenceForTapAssistance = 0.0;
		double locationReferenceForInitTapAssistnace[2] = {0, 0};
		double locationReferenceForFinalTapAssistance[2] = {0, 0};
		double timestampReferenceForIgnoreRepeat = -numeric_limits<double>::infinity();

		json *rawTouchTracks = &((*taskData)["trials"][trialIndex]["rawTouchTracks"]);

		while (find(trackEndedArr.begin(), trackEndedArr.end(), false) != trackEndedArr.end()){
			double timestampNext = numeric_limits<double>::infinity();
			int trackNext;
			for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
				if (!trackEndedArr[trackIndex] && (*rawTouchTracks)[trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"] < timestampNext){
					timestampNext = (*rawTouchTracks)[trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"];
					trackNext = trackIndex;
				}
			}

			json touchPoint = (*rawTouchTracks)[trackNext]["rawTouches"][trackIndexArr[trackNext]];

			////// IMPORTANT //////
			// IGNORE REPEAT //
			if (ignoreRepeat == ignoreRepeatOn){
				if (touchPoint["timestamp"] < timestampReferenceForIgnoreRepeat + ignoreRepeatTimer){
					trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1;
					if (trackIndexArr[trackNext] >= (*rawTouchTracks)[trackNext]["rawTouches"].size()){
						trackEndedArr[trackNext] = true;
					}
					continue;
				}
			}

			// HOLD DURATION //
			if (!isTouched){
				isTouched = true;
				timestampReferenceForHoldDuration = touchPoint["timestamp"];
				locationReferenceForInitTapAssistnace[0] = touchPoint["location"][0];
				locationReferenceForInitTapAssistnace[1] = touchPoint["location"][1];
			}

			trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1;
			if (trackIndexArr[trackNext] >= (*rawTouchTracks)[trackNext]["rawTouches"].size()){
				trackEndedArr[trackNext] = true;
				trackTouchedArr[trackNext] = false;
			} else {
				trackTouchedArr[trackNext] = true;
			}

			if (holdDuration == holdDurationOn){
				if (touchPoint["timestamp"] < timestampReferenceForHoldDuration + holdDurationTimer){
					// DO NOTHING
					if (find(trackTouchedArr.begin(), trackTouchedArr.end(), true) == trackTouchedArr.end()){
						isTouched = false;
					}
					continue;
				}
			}

			// TAP ASSISTANCE //
			if (!flagInitForTapAssistance){
				flagInitForTapAssistance = true;
				timestampReferenceForTapAssistance = touchPoint["timestamp"];
				locationReferenceForFinalTapAssistance[0] = touchPoint["location"][0];
				locationReferenceForFinalTapAssistance[1] = touchPoint["location"][1];
			}

			if (tapAssistance == tapAssistanceInit){
				if (touchPoint["timestamp"] < timestampReferenceForTapAssistance + tapAssistanceTimer){
					// It would send touch event if there is no touch
					if (find(trackTouchedArr.begin(), trackTouchedArr.end(), true) == trackTouchedArr.end()){
						touchPoint["location"][0] = locationReferenceForInitTapAssistnace[0];
						touchPoint["location"][1] = locationReferenceForInitTapAssistnace[1];
						
						(*(dataMod[taskName]))["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].push_back(touchPoint);
					}
				} else {
					(*(dataMod[taskName]))["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].push_back(touchPoint);
				}
			} else if (tapAssistance == tapAssistanceFinal){
				if (touchPoint["touchPoint"] < timestampReferenceForTapAssistance + tapAssistanceTimer){
					if ((locationReferenceForFinalTapAssistance[0]-double(touchPoint["location"][0])) * (locationReferenceForFinalTapAssistance[0]-double(touchPoint["location"][0])) +
						(locationReferenceForFinalTapAssistance[1]-double(touchPoint["location"][1])) * (locationReferenceForFinalTapAssistance[1]-double(touchPoint["location"][1])) >=
						TapAssistanceFinalLocationThreshold * TapAssistanceFinalLocationThreshold){
						timestampReferenceForTapAssistance = touchPoint["timestamp"];
						locationReferenceForFinalTapAssistance[0] = touchPoint["location"][0];
						locationReferenceForFinalTapAssistance[1] = touchPoint["location"][1];
					}
					// It would send touch event if there is no touch
					if (find(trackTouchedArr.begin(), trackTouchedArr.end(), true) == trackTouchedArr.end()){
						(*(dataMod[taskName]))["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].push_back(touchPoint);
					}
				} else {
					(*(dataMod[taskName]))["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].push_back(touchPoint);
				}
			} else if (tapAssistance == tapAssistanceOff){
				(*(dataMod[taskName]))["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].push_back(touchPoint);
			}

			if (find(trackTouchedArr.begin(), trackTouchedArr.end(), true) == trackTouchedArr.end()){
				isTouched = false;
				flagInitForTapAssistance = false;
				timestampReferenceForIgnoreRepeat = touchPoint["timestamp"];
			}
		}
		
	}
}