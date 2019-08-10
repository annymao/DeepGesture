#include "GestureClassification.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
GestureClassification::GestureClassification(){
	
}

double GestureClassification::GestureClassify(vector<string> *tasks, map<string, json*> *data){
	successRate = 0.0;

	vector<string> AllTasks {"tapTask", "longPressTask", "swipeTask", "horizontalScrollTask", "verticalScrollTask", "pinchTask", "rotationTask"};

	for (vector<string>::iterator iter = AllTasks.begin() ; iter != AllTasks.end() ; iter++){
		if (find((*tasks).begin(), (*tasks).end(), (*iter)) != (*tasks).end()){
			if ((*iter) == "tapTask"){
				
				(*ofs) << " " << TapTask((*data)[(*iter)]<<" "<<VerticalScrollTask((*data)[(*iter)])<< " " << HorizontalScrollTask((*data)[(*iter)])<< " " << SwipeTask((*data)[(*iter)]);
				cout<<" tapTask " << TapTask((*data)[(*iter)]<<" "<<VerticalScrollTask((*data)[(*iter)])<< " " << HorizontalScrollTask((*data)[(*iter)])<< " " << SwipeTask((*data)[(*iter)])<<endl;
			}  else if ((*iter) == "verticalScrollTask"){
				//cout << (*iter) << " "  << VerticalScrollTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << TapTask((*data)[(*iter)]<<" "<<VerticalScrollTask((*data)[(*iter)])<< " " << HorizontalScrollTask((*data)[(*iter)])<< " " << SwipeTask((*data)[(*iter)]);
				cout<<" VSTask " << TapTask((*data)[(*iter)]<<" "<<VerticalScrollTask((*data)[(*iter)])<< " " << HorizontalScrollTask((*data)[(*iter)])<< " " << SwipeTask((*data)[(*iter)])<<endl;
			
				//successRate = successRate + VerticalScrollTask((*data)[(*iter)]);
			} else if ((*iter) == "horizontalScrollTask"){
				//cout << (*iter) << " "  << HorizontalScrollTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << TapTask((*data)[(*iter)]<<" "<<VerticalScrollTask((*data)[(*iter)])<< " " << HorizontalScrollTask((*data)[(*iter)])<< " " << SwipeTask((*data)[(*iter)]);
				cout<<" HSTask " << TapTask((*data)[(*iter)]<<" "<<VerticalScrollTask((*data)[(*iter)])<< " " << HorizontalScrollTask((*data)[(*iter)])<< " " << SwipeTask((*data)[(*iter)])<<endl;
			
				//successRate = successRate + HorizontalScrollTask((*data)[(*iter)]);
			} else if ((*iter) == "swipeTask"){
				//cout << (*iter) << " "  << SwipeTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << TapTask((*data)[(*iter)]<<" "<<VerticalScrollTask((*data)[(*iter)])<< " " << HorizontalScrollTask((*data)[(*iter)])<< " " << SwipeTask((*data)[(*iter)]);
				cout<<" SWTask " << TapTask((*data)[(*iter)]<<" "<<VerticalScrollTask((*data)[(*iter)])<< " " << HorizontalScrollTask((*data)[(*iter)])<< " " << SwipeTask((*data)[(*iter)])<<endl;
			
				//successRate = successRate + SwipeTask((*data)[(*iter)]);
			}else if ((*iter) == "pinchTask"){
				//cout << (*iter) << " "  << PinchTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << ;
				//successRate = successRate + PinchTask((*data)[(*iter)]);
			} else if ((*iter) == "rotationTask"){
				(*ofs) << " " << ;
				//successRate = successRate + RotationTask((*data)[(*iter)]);
			}
			else if ((*iter) == "longPressTask"){
				//cout << (*iter) << " "  << LongPressTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << ;
				//successRate = successRate + LongPressTask((*data)[(*iter)]);
			}
		}else {
			(*ofs) << " " << 0;
		}
	}


	
	(*ofs) << endl;
	return successRate;
}
double GestureClassification::Classify(json* TaskData){
	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){


	}

}
double MyTouchTask::TapTask(json* tapTaskData){
	//cout << (*taskData) << endl;
	double successRate = 0.0;
	int successNum = 0;
	int trialNum = (*tapTaskData)["trials"].size();

	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){
		//cout << trialIndex << " " << (*tapTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*tapTaskData)["trials"][trialIndex]["success"] << " ";
		int trackNum = (*tapTaskData)["trials"][trialIndex]["rawTouchTracks"].size();
		if (trackNum >= 1){
			bool noTouchPoint = true;
			int trackIndex, touchPointNum;
			for (trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
				touchPointNum = (*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size();
				if (touchPointNum == 0){
					continue;
				} else {
					noTouchPoint = false;
					break;
				}
			}
			if (noTouchPoint){
				//cout << "No touch point" << endl;
				continue;
			}
			
			if (double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointNum-1]["timestamp"]) - 
				double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["timestamp"]) > TapMaximumDuration){
				//cout << "Timeout" << endl;
				continue;
			}

			if (abs(double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][0]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][0][0]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5) > double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5 ||
				abs(double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][1]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][0][1]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5) > double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5){
				//cout << "First touch point is not correct" << endl;
				continue;
			}
			
			bool isInAllowableMovement = true;
			for (int touchPointIndex = 0 ; touchPointIndex < touchPointNum ; touchPointIndex++){
				double dx = double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][0]) - double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][0]);
				double dy = double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][1]) - double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][1]);
				if (dx * dx + dy * dy >= TapAllowableMovement * TapAllowableMovement){
					isInAllowableMovement = false;
					break;
				}
			}
			if (!isInAllowableMovement){
				//cout << "Move larger than allowable movement" << endl;
				continue;
			}

			//cout << "Tap!!" << endl;
			successNum = successNum + 1;
		} else {
			//cout << "No track" << endl;
			continue;
		}
	}
	//cout << trialNum << endl;
	successRate = double(successNum) / double(trialNum);

	//return successRate;
	return double(successNum);
}



double MyTouchTask::HorizontalScrollTask(json* horizontalScrollTaskData){
	//cout << (*taskData) << endl;
	double successRate = 0.0;
	double successNum = 0;
	int trialNum = (*horizontalScrollTaskData)["trials"].size();

	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){
		//cout << trialIndex << " " << (*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*horizontalScrollTaskData)["trials"][trialIndex]["success"] << " ";
		int trackNum = (*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"].size();
		if (trackNum >= 1){

			double initialPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["initialPosition"][0]);
			double targetPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["targetPosition"][0]);
			//double predictedPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["predictedPosition"][0]);
			//double endDraggingPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["endDraggingPosition"][0]);
			double movement = 0;

			vector<int> trackIndexArr(trackNum, 0);
			vector<bool> trackEndedArr(trackNum, false);
			vector<bool> trackTouchedArr(trackNum, false);
			vector<double> trackInitPos(trackNum, 0);
			vector<double> trackLastPos(trackNum, 0);
			vector<double> trackLastMovement(trackNum, 0);
			vector<double> trackLastTimestamp(trackNum, 0);

			bool isScroll = false;

			while (find(trackEndedArr.begin(), trackEndedArr.end(), false) != trackEndedArr.end()){
				// Find which touch point is the next touch point we need to calculate
				double timestampNext = numeric_limits<double>::infinity();
				int trackNext = -1;
				for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
					if (!trackEndedArr[trackIndex] && (*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size() != 0 && double((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]) < timestampNext){
						timestampNext = double((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]);
						trackNext = trackIndex;
					}
				}

				// If each track is ended, break this loop
				if (trackNext == -1){
					break;
				}

				// Set this track "touched"
				trackTouchedArr[trackNext] = true;

				// Get the position x
				double posX = double((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][0]);
				double timestamp = double((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["timestamp"]);

				// If this touch point is the first point of this track, save into "trackInitPos"
				// Else: calculate the movement
				//   If "isScroll", check whether this touch point would make scroll view move
				//   Else: check whether this touch point would make scroll view start scroll
				if (trackIndexArr[trackNext] > 0){
					trackLastMovement[trackNext] = posX - trackLastPos[trackNext];
					if (!isScroll){
						if (abs(posX - trackInitPos[trackNext]) >= PanHysteresis){
							isScroll = true;
						}
					} else {
						bool isMaxMovement = true;
						for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
							if (trackTouchedArr[trackIndex] && trackIndexArr[trackIndex] > 1 && trackIndex != trackNext){
								if (abs(trackLastMovement[trackNext]) < abs(trackLastMovement[trackIndex])){
									isMaxMovement = false;
									break;
								}
							}
						}

						if (!isMaxMovement){
							//cout << "Not use this touch point!" << endl;
						} else {
							movement = movement - trackLastMovement[trackNext];
						}
					}
				} else {
					trackInitPos[trackNext] = posX;
				}

				if (trackIndexArr[trackNext] == (*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].size() - 1){
					// One track end
					isScroll = false;
					for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
						if (trackTouchedArr[trackIndex]){
							trackTouchedArr[trackIndex] = false;
							trackEndedArr[trackIndex] = true;
						}
					}
					movement = movement - PanMagicNumberX * (posX - trackLastPos[trackNext])/(timestamp - trackLastTimestamp[trackNext]);
					//cout << (posX - trackLastPos[trackNext])/(timestamp - trackLastTimestamp[trackNext]) << " ";
				}

				trackLastPos[trackNext] = posX;
				trackLastTimestamp[trackNext] = timestamp;

				trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1;
			}

			double finalPosition = initialPosition + movement;

			//cout << initialPosition << " " << movement << " " << finalPosition << " " << targetPosition << " ";

			//cout << finalPosition << " " << predictedPosition << endl;

			double scaler, dx;
			if (initialPosition > targetPosition){
				scaler = initialPosition - (targetPosition + screenSizeX * 0.25);
			} else {
				scaler = targetPosition - (initialPosition + screenSizeX);				
			}
			if (finalPosition > targetPosition){
				dx = max(0.0, finalPosition - (targetPosition + screenSizeX * 0.25));
			} else {
				dx = max(0.0, targetPosition - (finalPosition + screenSizeX));
			}
			successNum = successNum + max(0.0, (1.0 - dx / scaler));

			//cout << 1.0 - dx / scaler << endl;

			/*
			if ((finalPosition <= targetPosition && targetPosition <= finalPosition + screenSizeX) || (finalPosition <= targetPosition + screenSizeX/4 && targetPosition + screenSizeX/4 <= finalPosition + screenSizeX)){
				successNum = successNum + 1;
				//cout << "success" << endl;
			} else {
				//cout << "fail" << endl;
			}*/
			

			//cout << movement << " " << predictedPosition << " " << predictedPosition - (initialPosition + movement) << " " << predictedPosition - endDraggingPosition;
			//cout << endl;
			//cout << initialPosition - movement << " " << initialPosition - movement + screenSizeX << " ";

			//cout << "Horizontal Scroll!!" << endl;
			//successNum = successNum + 1;

			/*
			int trackIndexStart = 0;
			while((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndexStart]["rawTouches"].size() == 0){
				trackIndexStart = trackIndexStart + 1;
			}

			while (trackIndexStart != trackNum){
				for (int trackIndex = trackIndexStart ; trackIndex < trackNum ; trackIndex++){

				}
			}
			double timestamp = double((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndexStart]["rawTouches"][0]["timestamp"])

			bool noTouchPoint = true;
			int trackIndex, touchPointNum;
			for (trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
				touchPointNum = (*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size();
				if (touchPointNum == 0){
					continue;
				} else {
					noTouchPoint = false;
					break;
				}
			}
			if (noTouchPoint){
				cout << "No touch point" << endl;
				continue;
			}

			double initialPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["initialPosition"][0]);
			double targetPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["targetPosition"][0]);
			double predictedPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["predictedPosition"][0]);
			double movement = 0;

			bool isScroll = false;
			double startScrollPosition;
			for (int touchPointIndex = 0 ; touchPointIndex < touchPointNum ; touchPointIndex++){
				double dx = double((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][0]) - double((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][0]);
				if (dx * dx >= PanHysteresis * PanHysteresis){
					isScroll = true;
					movement = double((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointNum-1]["location"][0]) - double((*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][0]);
					//cout << movement << endl;
					break;
				}
			}
			if (!isScroll){
				cout << "No scroll" << endl;
				continue;
			}

			int panEventNum = (*horizontalScrollTaskData)["trials"][trialIndex]["panEvents"].size();
			double panFinalVelocity = double((*horizontalScrollTaskData)["trials"][trialIndex]["panEvents"][panEventNum-1]["velocity"][0]);
			//movement = movement + 0.5 * panFinalVelocity;
			cout << movement << " " << predictedPosition << " " << predictedPosition - (initialPosition - movement) << " " << panFinalVelocity << " " << (predictedPosition - (initialPosition - movement))/panFinalVelocity << " ";

			//cout << initialPosition - movement << " " << initialPosition - movement + screenSizeX << " ";

			cout << "Horizontal Scroll!!" << endl;
			successNum = successNum + 1;*/
		} else {
			//cout << "No track" << endl;
			continue;
		}
	}

	//cout << trialNum << endl;
	successRate = double(successNum) / double(trialNum);

	//return successRate;
	return successNum;
}

double MyTouchTask::VerticalScrollTask(json* verticalScrollTaskData){
	//cout << (*taskData) << endl;
	double successRate = 0.0;
	int successNum = 0;
	int trialNum = (*verticalScrollTaskData)["trials"].size();

	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){
		//cout << trialIndex << " " << (*verticalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*verticalScrollTaskData)["trials"][trialIndex]["success"] << " ";
		int trackNum = (*verticalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"].size();
		if (trackNum >= 1){

			double initialPosition = double((*verticalScrollTaskData)["trials"][trialIndex]["initialPosition"][1]);
			double targetPosition = double((*verticalScrollTaskData)["trials"][trialIndex]["targetPosition"][1]);
			double predictedPosition = double((*verticalScrollTaskData)["trials"][trialIndex]["predictedPosition"][1]);
			double endDraggingPosition = double((*verticalScrollTaskData)["trials"][trialIndex]["endDraggingPosition"][1]);
			double movement = 0;

			vector<int> trackIndexArr(trackNum, 0);
			vector<bool> trackEndedArr(trackNum, false);
			vector<bool> trackTouchedArr(trackNum, false);
			vector<double> trackInitPos(trackNum, 0);
			vector<double> trackLastPos(trackNum, 0);
			vector<double> trackLastMovement(trackNum, 0);
			vector<double> trackLastTimestamp(trackNum, 0);

			bool isScroll = false;

			while (find(trackEndedArr.begin(), trackEndedArr.end(), false) != trackEndedArr.end()){
				// Find which touch point is the next touch point we need to calculate
				double timestampNext = numeric_limits<double>::infinity();
				int trackNext = -1;
				for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
					if (!trackEndedArr[trackIndex] && (*verticalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size() != 0 && double((*verticalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]) < timestampNext){
						timestampNext = double((*verticalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]);
						trackNext = trackIndex;
					}
				}

				// If each track is ended, break this loop
				if (trackNext == -1){
					break;
				}

				// Set this track "touched"
				trackTouchedArr[trackNext] = true;

				// Get the position x
				double posY = double((*verticalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][1]);
				double timestamp = double((*verticalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["timestamp"]);

				// If this touch point is the first point of this track, save into "trackInitPos"
				// Else: calculate the movement
				//   If "isScroll", check whether this touch point would make scroll view move
				//   Else: check whether this touch point would make scroll view start scroll
				if (trackIndexArr[trackNext] > 0){
					trackLastMovement[trackNext] = posY - trackLastPos[trackNext];
					if (!isScroll){
						if (abs(posY - trackInitPos[trackNext]) >= PanHysteresis){
							isScroll = true;
						}
					} else {
						bool isMaxMovement = true;
						for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
							if (trackTouchedArr[trackIndex] && trackIndexArr[trackIndex] > 1 && trackIndex != trackNext){
								if (abs(trackLastMovement[trackNext]) < abs(trackLastMovement[trackIndex])){
									isMaxMovement = false;
									break;
								}
							}
						}

						if (!isMaxMovement){
							//cout << "Not use this touch point!" << endl;
						} else {
							movement = movement - trackLastMovement[trackNext];
						}
					}
				} else {
					trackInitPos[trackNext] = posY;
				}

				if (trackIndexArr[trackNext] == (*verticalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].size() - 1){
					// One track end
					isScroll = false;
					for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
						if (trackTouchedArr[trackIndex]){
							trackTouchedArr[trackIndex] = false;
							trackEndedArr[trackIndex] = true;
						}
					}
					movement = movement - PanMagicNumberY * (posY - trackLastPos[trackNext])/(timestamp - trackLastTimestamp[trackNext]);
					//cout << (posY - trackLastPos[trackNext])/(timestamp - trackLastTimestamp[trackNext]) << " ";
				}

				trackLastPos[trackNext] = posY;
				trackLastTimestamp[trackNext] = timestamp;

				trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1;
			}

			double finalPosition = initialPosition + movement;

			//cout << initialPosition << " " << movement << " " << finalPosition << " " << targetPosition << " " << predictedPosition << " ";

			//cout << finalPosition << " " << predictedPosition << endl;

			double scaler, dy;
			if (initialPosition > targetPosition){
				scaler = initialPosition - (targetPosition + screenSizeY * 0.25);
			} else {
				scaler = targetPosition - (initialPosition + screenSizeY);	
			}
			if (finalPosition > targetPosition){
				dy = max(0.0, finalPosition - (targetPosition + screenSizeY * 0.25));
			} else {
				dy = max(0.0, targetPosition - (finalPosition + screenSizeY));
			}
			successNum = successNum + max(0.0, (1.0 - dy / scaler));
			/*
			if ((finalPosition <= targetPosition && targetPosition <= finalPosition + screenSizeY) || (finalPosition <= targetPosition + screenSizeY/4 && targetPosition + screenSizeY/4 <= finalPosition + screenSizeY)){
				successNum = successNum + 1;
				//cout << "success" << endl;
			} else {
				//cout << "fail" << endl;
			}*/

		} else {
			//cout << "No track" << endl;
			continue;
		}
	}

	//cout << trialNum << endl;
	successRate = double(successNum) / double(trialNum);

	//return successRate;
	return successNum;
}

double MyTouchTask::SwipeTask(json* swipeTaskData){
	//cout << (*taskData) << endl;
	double successRate = 0.0;
	int successNum = 0;
	int trialNum = (*swipeTaskData)["trials"].size();

	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){
		//cout << trialIndex << " " << (*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*swipeTaskData)["trials"][trialIndex]["success"] << " ";
		int trackNum = (*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"].size();
		if (trackNum >= 1){

			string recognizedDirection = (*swipeTaskData)["trials"][trialIndex]["recognizedDirection"];
			string targetDirection = (*swipeTaskData)["trials"][trialIndex]["targetDirection"];
			
			//cout << "OriRecognized: " << recognizedDirection << ", Target: " << targetDirection;

			vector<int> trackIndexArr(trackNum, 0);
			vector<bool> trackEndedArr(trackNum, false);

			vector<double> trackFirstTimestamp(trackNum, 0);
			vector<double> trackInitPosX(trackNum, 0);
			vector<double> trackInitPosY(trackNum, 0);
			vector<double> trackLastPosX(trackNum, 0);
			vector<double> trackLastPosY(trackNum, 0);
			vector<double> trackLastTimestamp(trackNum, 0);
			vector<bool> trackCanSwipe(trackNum, false);
			string finalRecognizedDirection = "none";

			while (find(trackEndedArr.begin(), trackEndedArr.end(), false) != trackEndedArr.end()){
				// Find which touch point is the next touch point we need to calculate
				double timestampNext = numeric_limits<double>::infinity();
				int trackNext = -1;
				for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
					if (!trackEndedArr[trackIndex] && (*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size() != 0 && double((*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]) < timestampNext){
						timestampNext = double((*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]);
						trackNext = trackIndex;
					}
				}

				// If each track is ended, break this loop
				if (trackNext == -1){
					break;
				}
/*
				// TODO: Swipe may be recognized before the end of the track
				//       therefore, we should analyze data through the timeline
				if (double((*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointNum-1]["timestamp"]) - 
					double((*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["timestamp"]) > SwipeMaximumDuration){
					cout << "Timeout" << endl;
					continue;
				}
*/
				double timestamp = double((*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["timestamp"]);
				double posX = double((*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][0]);
				double posY = double((*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][1]);

				if (trackIndexArr[trackNext] == 0){
					trackInitPosX[trackNext] = posX;
					trackInitPosY[trackNext] = posY;
					trackFirstTimestamp[trackNext] = timestamp;
				}

				if (timestamp - trackFirstTimestamp[trackNext] >= SwipeMaximumDuration){
					trackEndedArr[trackNext] = true;
					finalRecognizedDirection = "none";
					continue;
				}

				if (trackIndexArr[trackNext] != 0){
					double dx = posX - trackInitPosX[trackNext];
					double dy = posY - trackInitPosY[trackNext];
					if (dx * dx + dy * dy >= SwipeMinimumMovement * SwipeMinimumMovement){
						trackCanSwipe[trackNext] = true;
					}

					if (trackCanSwipe[trackNext]){
						dx = posX - trackLastPosX[trackNext];
						dy = posY - trackLastPosY[trackNext];
						double dt = timestamp - trackLastTimestamp[trackNext];
						double v = sqrt(dx * dx + dy * dy) / dt;
						if (abs(v) >= SwipeMinimumVelocity){
							if (abs(dy) >= abs(dx)){
								if (dy > 0){
									finalRecognizedDirection = "down";
									trackEndedArr[trackNext] = true;
									//continue;
									//break;
								} else if (dy < 0){
									finalRecognizedDirection = "up";
									trackEndedArr[trackNext] = true;
									//continue;
									//break;
								}
							} else {
								if (dx > 0){
									finalRecognizedDirection = "right";
									trackEndedArr[trackNext] = true;
									//continue;
									//break;
								} else if (dx < 0){
									finalRecognizedDirection = "left";
									trackEndedArr[trackNext] = true;
									//continue;
									//break;
								}
							}
						}
					}
				}

				trackLastPosX[trackNext] = posX;
				trackLastPosY[trackNext] = posY;
				trackLastTimestamp[trackNext] = timestamp;

				if (trackIndexArr[trackNext] == (*swipeTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].size() - 1){
					trackEndedArr[trackNext] = true;
				}

				trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1;
			}

			//cout << ", FinalRecognized: " << finalRecognizedDirection << ", Same? " << (recognizedDirection==finalRecognizedDirection) << endl;

			if (targetDirection==finalRecognizedDirection){
				successNum = successNum + 1;
			}
		} else {
			//cout << "No track" << endl;
			continue;
		}
	}

	//cout << trialNum << endl;
	successRate = double(successNum) / double(trialNum);

	//return successRate;
	return successNum;
}

