#include "MyTouchTask.h"

MyTouchTask::MyTouchTask(){
	
}

double PanDefault(json* TaskData);
double TapDefault(json* TaskData);
double MyTouchTask::GetSuccessRate(vector<string> *tasks, map<string, json*> *data){
	successRate = 0.0;

	vector<string> AllTasks {"tapTask", "longPressTask", "swipeTask", "horizontalScrollTask", "verticalScrollTask", "pinchTask", "rotationTask"};

	for (vector<string>::iterator iter = AllTasks.begin() ; iter != AllTasks.end() ; iter++){
		if (find((*tasks).begin(), (*tasks).end(), (*iter)) != (*tasks).end()){
			if ((*iter) == "tapTask"){
				//cout << (*iter) << " "  << TapTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << TapTask((*data)[(*iter)]);
				//successRate = successRate + TapTask((*data)[(*iter)]);
			} else if ((*iter) == "longPressTask"){
				//cout << (*iter) << " "  << LongPressTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << LongPressTask((*data)[(*iter)]);
				//successRate = successRate + LongPressTask((*data)[(*iter)]);
			} else if ((*iter) == "verticalScrollTask"){
				//cout << (*iter) << " "  << VerticalScrollTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << VerticalScrollTask((*data)[(*iter)]);
				//successRate = successRate + VerticalScrollTask((*data)[(*iter)]);
			} else if ((*iter) == "horizontalScrollTask"){
				//cout << (*iter) << " "  << HorizontalScrollTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << HorizontalScrollTask((*data)[(*iter)]);
				//successRate = successRate + HorizontalScrollTask((*data)[(*iter)]);
			} else if ((*iter) == "swipeTask"){
				//cout << (*iter) << " "  << SwipeTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << SwipeTask((*data)[(*iter)]);
				//successRate = successRate + SwipeTask((*data)[(*iter)]);
			} else if ((*iter) == "pinchTask"){
				//cout << (*iter) << " "  << PinchTask((*data)[(*iter)]) << endl;
				(*ofs) << " " << PinchTask((*data)[(*iter)]);
				//successRate = successRate + PinchTask((*data)[(*iter)]);
			} else if ((*iter) == "rotationTask"){
				(*ofs) << " " << RotationTask((*data)[(*iter)]);
				//successRate = successRate + RotationTask((*data)[(*iter)]);
			}
		} else {
			(*ofs) << " " << 0;
		}
	}
	
	(*ofs) << endl;
	return successRate;
}





double MyTouchTask::GetSuccessRate2(vector<string> *tasks, map<string, json*> *data,int mode){
	double successRate = 0.0;
	double Success2=0.0;
	double DefaultSuccess=0.0;
	vector<string> AllTasks {"tapTask", "longPressTask", "swipeTask", "horizontalScrollTask", "verticalScrollTask", "pinchTask", "rotationTask"};

	for (vector<string>::iterator iter = AllTasks.begin() ; iter != AllTasks.end() ; iter++){
		if (find((*tasks).begin(), (*tasks).end(), (*iter)) != (*tasks).end()){
			if ((*iter) == "tapTask"){
				//double tapSuccessrate=0;
				double tapSuccessrate=ClassificationTask((*data)[(*iter)],0,mode) ;
				double tapDefaultSuccess=TapDefault((*data)[(*iter)]);
				//cout << "TapTask "<< tapDefaultSuccess<<" vs "<< tapSuccessrate<<" "<<  endl;
				Success2=Success2+tapSuccessrate;
				DefaultSuccess=DefaultSuccess+tapDefaultSuccess;
				//(*ofs) << " " << tapSuccessrate;


				//cout << (*iter) << " "  << TapTask((*data)[(*iter)]) << endl;
				
				//successRate = successRate + TapTask((*data)[(*iter)]);
			}  else if ((*iter) == "verticalScrollTask"){
				//double vpSuccessrate=0;
				double vpSuccessrate=ClassificationTask((*data)[(*iter)],1,mode) ;
				double panDefaultSuccess=PanDefault((*data)[(*iter)]);
				//cout << "PanTask "<< panDefaultSuccess<<" vs "<< vpSuccessrate<<" "<< endl;
				Success2=Success2+vpSuccessrate;
				DefaultSuccess=DefaultSuccess+panDefaultSuccess;
				//cout << (*iter) << " "  << VerticalScrollTask((*data)[(*iter)]) << endl;
				//(*ofs) << " " << vpSuccessrate;
				//successRate = successRate + VerticalScrollTask((*data)[(*iter)]);
			} else if ((*iter) == "horizontalScrollTask"){
				//double hpSuccessrate=0;
				double hpSuccessrate=ClassificationTask((*data)[(*iter)],1,mode) ;
				double panDefaultSuccess=PanDefault((*data)[(*iter)]);
				//cout << "PanTask "<< panDefaultSuccess<<" vs "<< hpSuccessrate <<" "<<  endl;
				Success2=Success2+hpSuccessrate;
				DefaultSuccess=DefaultSuccess+panDefaultSuccess;
				//cout << (*iter) << " "  << HorizontalScrollTask((*data)[(*iter)]) << endl;
				//(*ofs) << " " << hpSuccessrate;
				//successRate = successRate + HorizontalScrollTask((*data)[(*iter)]);
			} else if ((*iter) == "swipeTask"){
				//double swipeSuccessrate=0;
				double swipeSuccessrate=ClassificationTask((*data)[(*iter)],1,mode) ;
				double panDefaultSuccess=PanDefault((*data)[(*iter)]);

				Success2=Success2+swipeSuccessrate;
				DefaultSuccess=DefaultSuccess+panDefaultSuccess;
				//cout << "PanTask "<< panDefaultSuccess<<" vs "<< swipeSuccessrate<<" "<<  endl;
				//cout << (*iter) << " "  << SwipeTask((*data)[(*iter)]) << endl;
				//(*ofs) << " " << swipeSuccessrate;
				//successRate = successRate + SwipeTask((*data)[(*iter)]);
			} else if ((*iter) == "pinchTask"){
				//cout << (*iter) << " "  << PinchTask((*data)[(*iter)]) << endl;
				//(*ofs) << " " << PinchTask((*data)[(*iter)]);
				//successRate = successRate + PinchTask((*data)[(*iter)]);
			} else if ((*iter) == "rotationTask"){
				//(*ofs) << " " << RotationTask((*data)[(*iter)]);
				//successRate = successRate + RotationTask((*data)[(*iter)]);
			}
		} else {
			//(*ofs) << " " << 0;
		}
	}
	/*
	for (map<string, json*>::iterator iter = (*data).begin() ; iter != (*data).end() ; iter++){
		//cout << (*iter).first << endl;
		if ((*iter).first == "tapTask"){
			//cout << (*iter).first << " "  << TapTask((*iter).second) << endl;
			(*ofs) << " " << TapTask((*iter).second);
			//successRate = successRate + TapTask((*iter).second);
		} else if ((*iter).first == "longPressTask"){
			//cout << (*iter).first << " "  << LongPressTask((*iter).second) << endl;
			(*ofs) << " " << LongPressTask((*iter).second);
			//successRate = successRate + LongPressTask((*iter).second);
		} else if ((*iter).first == "verticalScrollTask"){
			//cout << (*iter).first << " "  << VerticalScrollTask((*iter).second) << endl;
			(*ofs) << " " << VerticalScrollTask((*iter).second);
			//successRate = successRate + VerticalScrollTask((*iter).second);
		} else if ((*iter).first == "horizontalScrollTask"){
			//cout << (*iter).first << " "  << HorizontalScrollTask((*iter).second) << endl;
			(*ofs) << " " << HorizontalScrollTask((*iter).second);
			//successRate = successRate + HorizontalScrollTask((*iter).second);
		} else if ((*iter).first == "swipeTask"){
			//cout << (*iter).first << " "  << SwipeTask((*iter).second) << endl;
			(*ofs) << " " << SwipeTask((*iter).second);
			//successRate = successRate + SwipeTask((*iter).second);
		} else if ((*iter).first == "pinchTask"){
			//cout << (*iter).first << " "  << PinchTask((*iter).second) << endl;
			(*ofs) << " " << PinchTask((*iter).second);
			//successRate = successRate + PinchTask((*iter).second);
		} else if ((*iter).first == "rotationTask"){
			//cout << (*iter).first << " "  << RotationTask((*iter).second) << endl;
			(*ofs) << " " << RotationTask((*iter).second);
			//successRate = successRate + RotationTask((*iter).second);
		}
	}*/

	//(*ofs) <<"Overall: "<<DefaultSuccess/4.0<<" vs "<<Success2/4.0;
	//(*ofs) << endl;
	//cout<<"Overall: "<<DefaultSuccess/4.0<<" vs "<<Success2/4.0 <<endl;
	return Success2/4.0 ;
}

double TapDefault(json* TaskData){
	double successRate = 0.0;
	int successNum = 0;
	double tapSuccess = 0.0;
	double panSuccess =0;

	// cout <<"TaskIndex"<<taskIndex<<endl;
	int trialNum = (*TaskData)["trials"].size();
	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){

		


		// cout <<"Tap Start !!!"<<endl;
		int tapDetect = (*TaskData)["trials"][trialIndex]["tapEvents"].size();
		int panDetect = (*TaskData)["trials"][trialIndex]["panEvents"].size();

		if (panDetect==0){
			if( tapDetect>0){
				tapSuccess =tapSuccess +1;

			}


		}

	}

	return double(tapSuccess)/double(trialNum);

}


double PanDefault(json* TaskData){
	double successRate = 0.0;
	int successNum = 0;
	double tapSuccess = 0.0;
	double panSuccess =0;

	// cout <<"TaskIndex"<<taskIndex<<endl;
	int trialNum = (*TaskData)["trials"].size();
	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){

		


		// cout <<"Tap Start !!!"<<endl;
		int tapDetect = (*TaskData)["trials"][trialIndex]["tapEvents"].size();
		int panDetect = (*TaskData)["trials"][trialIndex]["panEvents"].size();

		if (panDetect>0){
			if( tapDetect==0){
				panSuccess =panSuccess +1;

			}


		}

	}

	return double(panSuccess)/double(trialNum);

}



double MyTouchTask::ClassificationTask(json* TaskData,int taskIndex,int mode){

	// ///// Original/////  Original///// Original///// Original/////  Original///// Original///// Original/////  Original///// Original


	double successRate = 0.0;
	int successNum = 0;
	
	//cout <<"TaskIndex"<<taskIndex<<endl;


	
	

	int trialNum = (*TaskData)["trials"].size();
	// cout <<"trialNum ???"<<trialNum <<endl;
	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){

		int tapSuccess = 0;
		int panSuccess =0;

		vector<int> GestureEvent;
		// cout <<"Tap Start !!!"<<endl;
		int trackNum = (*TaskData)["trials"][trialIndex]["rawTouchTracks"].size();
		bool CanTap=true;

		if (trackNum >= 1){
			bool noTouchPoint = true;
			int trackIndex, touchPointNum;
			for (trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
				touchPointNum = (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size();
				if (touchPointNum == 0){
					CanTap=false;
					continue;
				} else {
					noTouchPoint = false;
					break;
				}
			}
			if (noTouchPoint){
				//cout << "No touch point" << endl;
				//continue;
				CanTap=false;
			}
			

			//cout<<"touchPointNum "<<touchPointNum<<endl;
			//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方
			// for (trackIndex = 0 ; trackIndex < trackNum ; trackIndex++)
			// { //唯一改的地方
				touchPointNum = (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size();
				if (touchPointNum>=1){
					if (double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointNum-1]["timestamp"]) - 
						double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["timestamp"]) > TapMaximumDuration){
						//cout << "Timeout" << endl;
						//continue;
						CanTap=false;
					}
				}


				// if (abs(double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][0]) - double((*TaskData)["trials"][trialIndex]["targetFrame"][0][0]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5) > double((*TaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5 ||
				// 	abs(double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][1]) - double((*TaskData)["trials"][trialIndex]["targetFrame"][0][1]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5) > double((*TaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5){
				// 	//cout << "First touch point is not correct" << endl;
				// 	continue;
				// }
				
				bool isInAllowableMovement = true;
				for (int touchPointIndex = 0 ; touchPointIndex < touchPointNum ; touchPointIndex++){
					double dx = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][0]) - double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][0]);
					double dy = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][1]) - double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][1]);
					if (dx * dx + dy * dy >= TapAllowableMovement * TapAllowableMovement){
						isInAllowableMovement = false;
						break;
					}
				}
				if (!isInAllowableMovement){
					//cout << "Move larger than allowable movement" << endl;
					//continue;
					CanTap=false;
				}

				//cout << "Tap!!" << endl;
				if (CanTap==true){
				tapSuccess=1;
				GestureEvent.push_back(0);
				}
			
			
		} 	
	
		///////HorizontalPan//////////
		//cout << trialIndex << " " << (*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*horizontalScrollTaskData)["trials"][trialIndex]["success"] << " ";
		// cout <<"Hp Start !!!"<<endl;
		if (trackNum >= 1){
			// cout <<"trialIndex"<<trialIndex<<endl;

			// cout <<"initialPosition"<<(*TaskData)["trials"][trialIndex]["initialPosition"]<<endl;

			// double initialPosition = double((*TaskData)["trials"][trialIndex]["initialPosition"][0]);
			// double targetPosition = double((*TaskData)["trials"][trialIndex]["targetPosition"][0]);
			// //double predictedPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["predictedPosition"][0]);
			//double endDraggingPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["endDraggingPosition"][0]);
			// cout <<"initialPosition"<<initialPosition<<endl;
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

					if (!trackEndedArr[trackIndex] && (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size() != 0 && double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]) < timestampNext){
						timestampNext = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]);
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
				double posX = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][0]);
				double timestamp = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["timestamp"]);

				// cout <<"posX"<<posX<<timestamp<<endl;


				// If this touch point is the first point of this track, save into "trackInitPos"
				// Else: calculate the movement
				//   If "isScroll", check whether this touch point would make scroll view move
				//   Else: check whether this touch point would make scroll view start scroll
				if (trackIndexArr[trackNext] > 0){
					trackLastMovement[trackNext] = posX - trackLastPos[trackNext];
					if (!isScroll){
						if (abs(posX - trackInitPos[trackNext]) >= PanHysteresis){
							isScroll = true;
							panSuccess=1;
							GestureEvent.push_back(1);
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

				if (trackIndexArr[trackNext] == (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].size() - 1){
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

			// double finalPosition = initialPosition + movement;

			//cout << initialPosition << " " << movement << " " << finalPosition << " " << targetPosition << " ";

			//cout << finalPosition << " " << predictedPosition << endl;

			
		
		} 

		///////VerticalPan//////////

		// cout <<"Vp Start !!!"<<endl;
		if (trackNum >= 1){

			// double initialPosition = double((*TaskData)["trials"][trialIndex]["initialPosition"][1]);
			// double targetPosition = double((*TaskData)["trials"][trialIndex]["targetPosition"][1]);
			// double predictedPosition = double((*TaskData)["trials"][trialIndex]["predictedPosition"][1]);
			// double endDraggingPosition = double((*TaskData)["trials"][trialIndex]["endDraggingPosition"][1]);
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
					if (!trackEndedArr[trackIndex] && (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size() != 0 && double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]) < timestampNext){
						timestampNext = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]);
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
				double posY = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][1]);
				double timestamp = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["timestamp"]);

				// If this touch point is the first point of this track, save into "trackInitPos"
				// Else: calculate the movement
				//   If "isScroll", check whether this touch point would make scroll view move
				//   Else: check whether this touch point would make scroll view start scroll
				if (trackIndexArr[trackNext] > 0){
					trackLastMovement[trackNext] = posY - trackLastPos[trackNext];
					if (!isScroll){
						if (abs(posY - trackInitPos[trackNext]) >= PanHysteresis){
							isScroll = true;
							panSuccess=1;
							GestureEvent.push_back(1);
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

				if (trackIndexArr[trackNext] == (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].size() - 1){
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

			// double finalPosition = initialPosition + movement;

			

		}



		
 
	   

		// if (mode==1){
		// 	cout<<" GestureEvent ";
		// 	for(int i=0;i<GestureEvent.size();i++){
		// 	cout<<" "<<GestureEvent[i];
		// 	}
		// 	cout<<endl;
		// }


		if (taskIndex==0){//TapTask
			vector<int>::iterator it1 = find(GestureEvent.begin(), GestureEvent.end(), 0);
			int HaveTap=0;

			if (it1 != GestureEvent.end()){
		        HaveTap=1;
			
			}
		    else{
		       HaveTap=0;
		    }

		    vector<int>::iterator it2 = find(GestureEvent.begin(), GestureEvent.end(), 1);
			int HavePan=0;
			if (it2 != GestureEvent.end()){
		        HavePan=1;
			
			}
		    else{
		       HavePan=0;
		    }

			if (HavePan==0){
				if(HaveTap==1){
					successNum=successNum+1;
				}
			}


		}  

		else if(taskIndex==1){//PanTask

			vector<int>::iterator it3 = find(GestureEvent.begin(), GestureEvent.end(), 0);
			int HaveTap=0;
			if (it3 != GestureEvent.end()){
		        HaveTap=1;
			
			}
		    else{
		       HaveTap=0;
		    }

		    vector<int>::iterator it4 = find(GestureEvent.begin(), GestureEvent.end(), 1);
			int HavePan=0;
			if (it4 != GestureEvent.end())
			{
		        HavePan=1;
			
			}
		    else{
		       HavePan=0;
		    }




			if (HavePan==1){
				if(HaveTap==0){
					successNum=successNum+1;
				}
			}

		}


	}



	if (trialNum>=1){
	successRate = double(successNum) / double(trialNum);
		if (mode==1){
				cout<<" taskIndex "<<taskIndex<<" success: "<<successNum<<" "<<trialNum;
				
				cout<<endl;
			}
	}
	else{
		cout<<"No Trial"<<endl;
	}

	return successRate;




	///// Original/////  Original///// Original///// Original/////  Original///// Original///// Original/////  Original///// Original

	///hahahahhahadjfkjadkfjaw;efjk;fje;kㄍㄨㄜFJ;ㄑㄨㄤj

	///////New/////////New//////New/////////New///////New/////////New//////New/////////New///////New/////////New//////New/////////New



	// double successRate = 0.0;
	// int successNum = 0;
	
	// //cout <<"TaskIndex"<<taskIndex<<endl;


	
	

	// int trialNum = (*TaskData)["trials"].size();
	// // cout <<"trialNum ???"<<trialNum <<endl;
	// for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){

	// 	int tapSuccess = 0;
	// 	int panSuccess =0;

	// 	vector<int> GestureEvent;
	// 	// cout <<"Tap Start !!!"<<endl;
	// 	int trackNum = (*TaskData)["trials"][trialIndex]["rawTouchTracks"].size();
	// 	bool CanTap=true;

	// 	if (trackNum >= 1){
	// 		bool noTouchPoint = true;
	// 		int trackIndex, touchPointNum;
	// 		for (trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
	// 			touchPointNum = (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size();
	// 			if (touchPointNum == 0){
	// 				CanTap=false;
	// 				//continue;
	// 			} else {
	// 				noTouchPoint = false;
	// 				break;
	// 			}
	// 		}
	// 		if (noTouchPoint){
	// 			//cout << "No touch point" << endl;
	// 			//continue;
	// 			CanTap=false;
	// 		}
			

	// 		//cout<<"touchPointNum "<<touchPointNum<<endl;
	// 		//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方//唯一改的地方
	// 		for (trackIndex = 0 ; trackIndex < trackNum ; trackIndex++)
	// 		{ //唯一改的地方
	// 			touchPointNum = (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size();
	// 			if (touchPointNum>=1){
	// 				if (double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointNum-1]["timestamp"]) - 
	// 					double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["timestamp"]) > TapMaximumDuration){
	// 					//cout << "Timeout" << endl;
	// 					//continue;
	// 					CanTap=false;
	// 				}
	// 			}


	// 			// if (abs(double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][0]) - double((*TaskData)["trials"][trialIndex]["targetFrame"][0][0]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5) > double((*TaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5 ||
	// 			// 	abs(double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][1]) - double((*TaskData)["trials"][trialIndex]["targetFrame"][0][1]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5) > double((*TaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5){
	// 			// 	//cout << "First touch point is not correct" << endl;
	// 			// 	continue;
	// 			// }
				
	// 			bool isInAllowableMovement = true;
	// 			for (int touchPointIndex = 0 ; touchPointIndex < touchPointNum ; touchPointIndex++){
	// 				double dx = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][0]) - double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][0]);
	// 				double dy = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][1]) - double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][1]);
	// 				if (dx * dx + dy * dy >= TapAllowableMovement * TapAllowableMovement){
	// 					isInAllowableMovement = false;
	// 					break;
	// 				}
	// 			}
	// 			if (!isInAllowableMovement){
	// 				//cout << "Move larger than allowable movement" << endl;
	// 				//continue;
	// 				CanTap=false;
	// 			}

	// 			//cout << "Tap!!" << endl;
	// 			if (CanTap==true){
	// 			tapSuccess=1;
	// 			GestureEvent.push_back(0);
	// 			}
	// 		}
			
	// 	} 	
	
	// 	///////HorizontalPan//////////
	// 	//cout << trialIndex << " " << (*horizontalScrollTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*horizontalScrollTaskData)["trials"][trialIndex]["success"] << " ";
	// 	// cout <<"Hp Start !!!"<<endl;
	// 	if (trackNum >= 1){
	// 		// cout <<"trialIndex"<<trialIndex<<endl;

	// 		// cout <<"initialPosition"<<(*TaskData)["trials"][trialIndex]["initialPosition"]<<endl;

	// 		// double initialPosition = double((*TaskData)["trials"][trialIndex]["initialPosition"][0]);
	// 		// double targetPosition = double((*TaskData)["trials"][trialIndex]["targetPosition"][0]);
	// 		// //double predictedPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["predictedPosition"][0]);
	// 		//double endDraggingPosition = double((*horizontalScrollTaskData)["trials"][trialIndex]["endDraggingPosition"][0]);
	// 		// cout <<"initialPosition"<<initialPosition<<endl;
	// 		double movement = 0;

	// 		vector<int> trackIndexArr(trackNum, 0);
	// 		vector<bool> trackEndedArr(trackNum, false);
	// 		vector<bool> trackTouchedArr(trackNum, false);
	// 		vector<double> trackInitPos(trackNum, 0);
	// 		vector<double> trackLastPos(trackNum, 0);
	// 		vector<double> trackLastMovement(trackNum, 0);
	// 		vector<double> trackLastTimestamp(trackNum, 0);

	// 		bool isScroll = false;

	// 		while (find(trackEndedArr.begin(), trackEndedArr.end(), false) != trackEndedArr.end()){
	// 			// Find which touch point is the next touch point we need to calculate
	// 			double timestampNext = numeric_limits<double>::infinity();
	// 			int trackNext = -1;
	// 			for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){

	// 				if (!trackEndedArr[trackIndex] && (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size() != 0 && double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]) < timestampNext){
	// 					timestampNext = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]);
	// 					trackNext = trackIndex;
	// 				}
	// 			}

	// 			// If each track is ended, break this loop
	// 			if (trackNext == -1){
	// 				break;
	// 			}

	// 			// Set this track "touched"
	// 			trackTouchedArr[trackNext] = true;

	// 			// Get the position x
	// 			double posX = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][0]);
	// 			double timestamp = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["timestamp"]);

	// 			// cout <<"posX"<<posX<<timestamp<<endl;


	// 			// If this touch point is the first point of this track, save into "trackInitPos"
	// 			// Else: calculate the movement
	// 			//   If "isScroll", check whether this touch point would make scroll view move
	// 			//   Else: check whether this touch point would make scroll view start scroll
	// 			if (trackIndexArr[trackNext] > 0){
	// 				trackLastMovement[trackNext] = posX - trackLastPos[trackNext];
	// 				if (abs(posX - trackInitPos[trackNext]) >= PanHysteresis){
	// 						isScroll = true;
	// 						panSuccess=1;
	// 						GestureEvent.push_back(1);
	// 					}
	// 				if (!isScroll){
	// 					if (abs(posX - trackInitPos[trackNext]) >= PanHysteresis){
	// 						isScroll = true;
	// 						panSuccess=1;
	// 						GestureEvent.push_back(1);
	// 					}
	// 				} else {
	// 					bool isMaxMovement = true;
	// 					for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
	// 						if (trackTouchedArr[trackIndex] && trackIndexArr[trackIndex] > 1 && trackIndex != trackNext){
	// 							if (abs(trackLastMovement[trackNext]) < abs(trackLastMovement[trackIndex])){
	// 								isMaxMovement = false;
	// 								break;
	// 							}
	// 						}
	// 					}

	// 					if (!isMaxMovement){
	// 						//cout << "Not use this touch point!" << endl;
	// 					} else {
	// 						movement = movement - trackLastMovement[trackNext];
	// 					}
	// 				}
	// 			} else {
	// 				trackInitPos[trackNext] = posX;
	// 			}

	// 			if (trackIndexArr[trackNext] == (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].size() - 1){
	// 				// One track end
	// 				isScroll = false;
					
	// 				for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
	// 					if (trackTouchedArr[trackIndex]){
	// 						trackTouchedArr[trackIndex] = false;
	// 						trackEndedArr[trackIndex] = true;
	// 					}
	// 				}
	// 				movement = movement - PanMagicNumberX * (posX - trackLastPos[trackNext])/(timestamp - trackLastTimestamp[trackNext]);
	// 				//cout << (posX - trackLastPos[trackNext])/(timestamp - trackLastTimestamp[trackNext]) << " ";
	// 			}

	// 			trackLastPos[trackNext] = posX;
	// 			trackLastTimestamp[trackNext] = timestamp;

	// 			trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1;
	// 		}

	// 		// double finalPosition = initialPosition + movement;

	// 		//cout << initialPosition << " " << movement << " " << finalPosition << " " << targetPosition << " ";

	// 		//cout << finalPosition << " " << predictedPosition << endl;

			
		
	// 	} 

	// 	///////VerticalPan//////////

	// 	// cout <<"Vp Start !!!"<<endl;
	// 	if (trackNum >= 1){

	// 		// double initialPosition = double((*TaskData)["trials"][trialIndex]["initialPosition"][1]);
	// 		// double targetPosition = double((*TaskData)["trials"][trialIndex]["targetPosition"][1]);
	// 		// double predictedPosition = double((*TaskData)["trials"][trialIndex]["predictedPosition"][1]);
	// 		// double endDraggingPosition = double((*TaskData)["trials"][trialIndex]["endDraggingPosition"][1]);
	// 		double movement = 0;

	// 		vector<int> trackIndexArr(trackNum, 0);
	// 		vector<bool> trackEndedArr(trackNum, false);
	// 		vector<bool> trackTouchedArr(trackNum, false);
	// 		vector<double> trackInitPos(trackNum, 0);
	// 		vector<double> trackLastPos(trackNum, 0);
	// 		vector<double> trackLastMovement(trackNum, 0);
	// 		vector<double> trackLastTimestamp(trackNum, 0);

	// 		bool isScroll = false;

	// 		while (find(trackEndedArr.begin(), trackEndedArr.end(), false) != trackEndedArr.end()){
	// 			// Find which touch point is the next touch point we need to calculate
	// 			double timestampNext = numeric_limits<double>::infinity();
	// 			int trackNext = -1;
	// 			for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
	// 				if (!trackEndedArr[trackIndex] && (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size() != 0 && double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]) < timestampNext){
	// 					timestampNext = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]);
	// 					trackNext = trackIndex;
	// 				}
	// 			}

	// 			// If each track is ended, break this loop
	// 			if (trackNext == -1){
	// 				break;
	// 			}

	// 			// Set this track "touched"
	// 			trackTouchedArr[trackNext] = true;

	// 			// Get the position x
	// 			double posY = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][1]);
	// 			double timestamp = double((*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["timestamp"]);

	// 			// If this touch point is the first point of this track, save into "trackInitPos"
	// 			// Else: calculate the movement
	// 			//   If "isScroll", check whether this touch point would make scroll view move
	// 			//   Else: check whether this touch point would make scroll view start scroll
	// 			if (trackIndexArr[trackNext] > 0){
	// 				trackLastMovement[trackNext] = posY - trackLastPos[trackNext];
	// 				if (abs(posY - trackInitPos[trackNext]) >= PanHysteresis){
	// 					isScroll = true;
	// 					panSuccess=1;
	// 					GestureEvent.push_back(1);
	// 				}
	// 				if (!isScroll){
	// 					if (abs(posY - trackInitPos[trackNext]) >= PanHysteresis){
	// 						isScroll = true;
	// 						panSuccess=1;
	// 						GestureEvent.push_back(1);
	// 					}
	// 				} else {
	// 					bool isMaxMovement = true;
	// 					for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
	// 						if (trackTouchedArr[trackIndex] && trackIndexArr[trackIndex] > 1 && trackIndex != trackNext){
	// 							if (abs(trackLastMovement[trackNext]) < abs(trackLastMovement[trackIndex])){
	// 								isMaxMovement = false;
	// 								break;
	// 							}
	// 						}
	// 					}

	// 					if (!isMaxMovement){
	// 						//cout << "Not use this touch point!" << endl;
	// 					} else {
	// 						movement = movement - trackLastMovement[trackNext];
	// 					}
	// 				}
	// 			} else {
	// 				trackInitPos[trackNext] = posY;
	// 			}

	// 			if (trackIndexArr[trackNext] == (*TaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].size() - 1){
	// 				// One track end
	// 				isScroll = false;
					
	// 				for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
	// 					if (trackTouchedArr[trackIndex]){
	// 						trackTouchedArr[trackIndex] = false;
	// 						trackEndedArr[trackIndex] = true;
	// 					}
	// 				}
	// 				movement = movement - PanMagicNumberY * (posY - trackLastPos[trackNext])/(timestamp - trackLastTimestamp[trackNext]);
	// 				//cout << (posY - trackLastPos[trackNext])/(timestamp - trackLastTimestamp[trackNext]) << " ";
	// 			}

	// 			trackLastPos[trackNext] = posY;
	// 			trackLastTimestamp[trackNext] = timestamp;

	// 			trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1;
	// 		}

	// 		// double finalPosition = initialPosition + movement;

			

	// 	}



		
 
	   

	// 	// if (mode==1){
	// 	// 	cout<<" GestureEvent ";
	// 	// 	for(int i=0;i<GestureEvent.size();i++){
	// 	// 	cout<<" "<<GestureEvent[i];
	// 	// 	}
	// 	// 	cout<<endl;
	// 	// }


	// 	if (taskIndex==0){//TapTask
	// 		vector<int>::iterator it1 = find(GestureEvent.begin(), GestureEvent.end(), 0);
	// 		int HaveTap=0;

	// 		if (it1 != GestureEvent.end()){
	// 	        HaveTap=1;
			
	// 		}
	// 	    else{
	// 	       HaveTap=0;
	// 	    }

	// 	    vector<int>::iterator it2 = find(GestureEvent.begin(), GestureEvent.end(), 1);
	// 		int HavePan=0;
	// 		if (it2 != GestureEvent.end()){
	// 	        HavePan=1;
			
	// 		}
	// 	    else{
	// 	       HavePan=0;
	// 	    }

	// 		if (HavePan==0){
	// 			if(HaveTap==1){
	// 				successNum=successNum+1;
	// 			}
	// 		}


	// 	}  

	// 	else if(taskIndex==1){//PanTask

	// 		vector<int>::iterator it3 = find(GestureEvent.begin(), GestureEvent.end(), 0);
	// 		int HaveTap=0;
	// 		if (it3 != GestureEvent.end()){
	// 	        HaveTap=1;
			
	// 		}
	// 	    else{
	// 	       HaveTap=0;
	// 	    }

	// 	    vector<int>::iterator it4 = find(GestureEvent.begin(), GestureEvent.end(), 1);
	// 		int HavePan=0;
	// 		if (it4 != GestureEvent.end())
	// 		{
	// 	        HavePan=1;
			
	// 		}
	// 	    else{
	// 	       HavePan=0;
	// 	    }




	// 		if (HavePan==1){
	// 			if(HaveTap==0){
	// 				successNum=successNum+1;
	// 			}
	// 		}

	// 	}


	// }



	// if (trialNum>=1){
	// successRate = double(successNum) / double(trialNum);
	// 	if (mode==1){
	// 			cout<<" taskIndex "<<taskIndex<<" success: "<<successNum<<" "<<trialNum;
				
	// 			cout<<endl;
	// 		}
	// }
	// else{
	// 	cout<<"No Trial"<<endl;
	// }

	// return successRate;





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
	cout<<successNum<<" "<<trialNum <<" "<<successRate<<endl;
	return successRate;
}

double MyTouchTask::LongPressTask(json* longPressTaskData){
	//cout << (*taskData) << endl;
	double successRate = 0.0;
	int successNum = 0;
	int trialNum = (*longPressTaskData)["trials"].size();

	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){
		//cout << trialIndex << " " << (*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*longPressTaskData)["trials"][trialIndex]["success"] << " ";
		int trackNum = (*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"].size();
		if (trackNum >= 1){
			bool noTouchPoint = true;
			int trackIndex, touchPointNum;
			for (trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
				touchPointNum = (*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size();
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

			if (abs(double((*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][0]) - double((*longPressTaskData)["trials"][trialIndex]["targetFrame"][0][0]) - double((*longPressTaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5) > double((*longPressTaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5 ||
				abs(double((*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][1]) - double((*longPressTaskData)["trials"][trialIndex]["targetFrame"][0][1]) - double((*longPressTaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5) > double((*longPressTaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5){
				//cout << "First touch point is not correct" << endl;
				continue;
			}
			
			bool isLessThanMinimumLongPressDuration = true;
			bool isInAllowableMovement = true;
			for (int touchPointIndex = 0 ; touchPointIndex < touchPointNum ; touchPointIndex++){
				if (double((*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["timestamp"]) - 
					double((*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["timestamp"]) >= LongPressMinimumPressDuration){
					isLessThanMinimumLongPressDuration = false;
					break;
				}
				double dx = double((*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][0]) - double((*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][0]);
				double dy = double((*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][touchPointIndex]["location"][1]) - double((*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][0]["location"][1]);
				if (dx * dx + dy * dy >= LongPressAllowableMovement * LongPressAllowableMovement){
					isInAllowableMovement = false;
					break;
				}
			}
			if (isLessThanMinimumLongPressDuration){
				//cout << "Less than minimum long press duration" << endl;
				continue;
			}
			if (!isInAllowableMovement){
				//cout << "Move larger than allowable movement" << endl;
				continue;
			}

			//cout << "Long Press!!" << endl;
			successNum = successNum + 1;
		} else {
			//cout << "No track" << endl;
			continue;
		}
	}
	//cout << trialNum << endl;
	successRate = double(successNum) / double(trialNum);

	return successRate;
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

	return successRate;
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

	return successRate;
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

	return successRate;
}

double MyTouchTask::PinchTask(json* pinchTaskData){
	//cout << (*taskData) << endl;
	double successRate = 0.0;
	double successNum = 0;
	int trialNum = (*pinchTaskData)["trials"].size();

	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){
		//cout << trialIndex << " " << (*pinchTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*pinchTaskData)["trials"][trialIndex]["success"] << " ";
		int trackNum = (*pinchTaskData)["trials"][trialIndex]["rawTouchTracks"].size();
		if (trackNum >= 1){

			double initialSize = double((*pinchTaskData)["trials"][trialIndex]["initialSize"][0]);
			double targetSize = double((*pinchTaskData)["trials"][trialIndex]["targetSize"][0]);
			double resultSize = double((*pinchTaskData)["trials"][trialIndex]["resultSize"][0]);
			double finalSize = initialSize;

			double distance = 0;

			vector<int> trackIndexArr(trackNum, 0);
			vector<bool> trackEndedArr(trackNum, false);

			vector<int> trackFingerID(trackNum, -1);
			vector<int> FingerID;
			map<int, int> FingerIDTOTrack;

			double posx[2];
			double posy[2];
			double referenceDistance;
			double ratio;
			int pinchMode = 0;

			while (find(trackEndedArr.begin(), trackEndedArr.end(), false) != trackEndedArr.end()){
				// Find which touch point is the next touch point we need to calculate
				double timestampNext = numeric_limits<double>::infinity();
				int trackNext = -1;
				for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
					if (!trackEndedArr[trackIndex] && (*pinchTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size() != 0 && double((*pinchTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]) < timestampNext){
						timestampNext = double((*pinchTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]);
						trackNext = trackIndex;
					}
				}

				// If each track is ended, break this loop
				if (trackNext == -1){
					break;
				}

				double posX = double((*pinchTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][0]);
				double posY = double((*pinchTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][1]);

				if (trackIndexArr[trackNext] == 0){
					// If this touch point is the first point of this track, assign this track a finger id
					for (int fingerIDIndex = 0 ; ; fingerIDIndex++){
						if (find(FingerID.begin(), FingerID.end(), fingerIDIndex) == FingerID.end()){
							trackFingerID[trackNext] = fingerIDIndex;
							FingerID.push_back(fingerIDIndex);
							break;
						}
					}
				}

				if (trackFingerID[trackNext] == 0 || trackFingerID[trackNext] == 1){
					posx[trackFingerID[trackNext]] = posX;
					posy[trackFingerID[trackNext]] = posY;

					if (find(FingerID.begin(), FingerID.end(), 0) != FingerID.end() && find(FingerID.begin(), FingerID.end(), 1) != FingerID.end()){
						double dx = posx[0] - posx[1];
						double dy = posy[0] - posy[1];
						distance = sqrt(dx * dx + dy * dy);
						if (pinchMode == 0){
							referenceDistance = distance;
							pinchMode = 1;
						}
						if (pinchMode == 1 && abs(distance - referenceDistance) >= PinchHysteresis){
							referenceDistance = distance;
							pinchMode = 2;
						}
						if (pinchMode == 2){
							ratio = distance / referenceDistance;
						}
					}
				}

				if (trackIndexArr[trackNext] == (*pinchTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].size() - 1){
					// When a track is end, release the finger id of this track
					if ((trackFingerID[trackNext] == 0 || trackFingerID[trackNext] == 1)){
						if (pinchMode == 2){
							finalSize = finalSize * ratio;
						}
						pinchMode = 0;
					}
					FingerID.erase(find(FingerID.begin(), FingerID.end(), trackFingerID[trackNext]));
					trackEndedArr[trackNext] = true;
				}

				trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1;
			}

			successNum = successNum + max(0.0, (1-abs(finalSize-targetSize)/abs(targetSize-initialSize)));

			//cout << resultSize << " " << finalSize << endl;

		} else {
			//cout << "No track" << endl;
			continue;
		}
	}

	//cout << trialNum << endl;
	successRate = double(successNum) / double(trialNum);

	return successRate;
}

double MyTouchTask::RotationTask(json* rotationTaskData){
	//cout << (*taskData) << endl;
	double successRate = 0.0;
	double successNum = 0;
	int trialNum = (*rotationTaskData)["trials"].size();

	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){
		//cout << trialIndex << " " << (*rotationTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*rotationTaskData)["trials"][trialIndex]["success"] << " ";
		int trackNum = (*rotationTaskData)["trials"][trialIndex]["rawTouchTracks"].size();
		if (trackNum >= 1){

			double initialAngle = double((*rotationTaskData)["trials"][trialIndex]["initialAngle"]);
			double resultAngle = double((*rotationTaskData)["trials"][trialIndex]["resultAngle"]);
			double targetAngle = double((*rotationTaskData)["trials"][trialIndex]["targetAngle"]);
			double finalAngle = initialAngle;
			double deltaAngle = 0;

			vector<int> trackIndexArr(trackNum, 0);
			vector<bool> trackEndedArr(trackNum, false);

			vector<int> trackFingerID(trackNum, -1);
			vector<int> FingerID;
			map<int, int> FingerIDTOTrack;

			double posx[2];
			double posy[2];
			bool isRotate = false;
			bool isTwoTouched = false;

			while (find(trackEndedArr.begin(), trackEndedArr.end(), false) != trackEndedArr.end()){
				// Find which touch point is the next touch point we need to calculate
				double timestampNext = numeric_limits<double>::infinity();
				int trackNext = -1;
				for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
					if (!trackEndedArr[trackIndex] && (*rotationTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size() != 0 && double((*rotationTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]) < timestampNext){
						timestampNext = double((*rotationTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"][trackIndexArr[trackIndex]]["timestamp"]);
						trackNext = trackIndex;
					}
				}

				// If each track is ended, break this loop
				if (trackNext == -1){
					break;
				}

				double posX = double((*rotationTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][0]);
				double posY = double((*rotationTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"][trackIndexArr[trackNext]]["location"][1]);

				if (trackIndexArr[trackNext] == 0){
					// If this touch point is the first point of this track, assign this track a finger id
					for (int fingerIDIndex = 0 ; ; fingerIDIndex++){
						if (find(FingerID.begin(), FingerID.end(), fingerIDIndex) == FingerID.end()){
							trackFingerID[trackNext] = fingerIDIndex;
							FingerID.push_back(fingerIDIndex);
							break;
						}
					}
				}

				if (trackFingerID[trackNext] == 0 || trackFingerID[trackNext] == 1){
					if (find(FingerID.begin(), FingerID.end(), 0) != FingerID.end() && find(FingerID.begin(), FingerID.end(), 1) != FingerID.end()){
						if (!isTwoTouched){
							isTwoTouched = true;
						} else {
							double originAngle;
							double alterAngle;
							if (trackFingerID[trackNext] == 0){
								originAngle = atan2(posy[0]-posy[1], posx[0]-posx[1]);
								alterAngle = atan2(posY-posy[1], posX-posx[1]);
							} else if (trackFingerID[trackNext] == 1){
								originAngle = atan2(posy[1]-posy[0], posx[1]-posx[0]);
								alterAngle = atan2(posY-posy[0], posX-posx[0]);
							}
							if (abs(alterAngle - originAngle) >= RotationMaximumAngleEachTimestamp){
								if (alterAngle - originAngle > 0){
									deltaAngle = deltaAngle + (alterAngle - originAngle) - 2.0 * M_PI;
								} else {
									deltaAngle = deltaAngle + (alterAngle - originAngle) + 2.0 * M_PI;
								}
							} else {
								deltaAngle = deltaAngle + (alterAngle - originAngle);
							}
							if (!isRotate && abs(deltaAngle) >= RotationHysteresis){
								isRotate = true;
								deltaAngle = 0;
							}
						}						
					} else if (!isRotate){
						deltaAngle = 0;
					}
					posx[trackFingerID[trackNext]] = posX;
					posy[trackFingerID[trackNext]] = posY;
				}

				if (trackIndexArr[trackNext] == (*rotationTaskData)["trials"][trialIndex]["rawTouchTracks"][trackNext]["rawTouches"].size() - 1){
					// When a track is end, release the finger id of this track
					if (trackFingerID[trackNext] == 0 || trackFingerID[trackNext] == 1){
						if (isRotate &&
							((trackFingerID[trackNext] == 0 && find(FingerID.begin(), FingerID.end(), 1) == FingerID.end()) || 
							 (trackFingerID[trackNext] == 1 && find(FingerID.begin(), FingerID.end(), 0) == FingerID.end()))
						   ){
							finalAngle = finalAngle + deltaAngle;// - RotationHysteresis * deltaAngle / abs(deltaAngle);
							isRotate = false;
						}
						isTwoTouched = false;
						// Calculate the delta angle
						//double originAngle = atan2(referencePosY[1]-referencePosY[0], referencePosX[1]-referencePosX[0]);
						//double alterAngle = atan2(posy[1]-posy[0], posx[1]-posx[0]);

						//deltaAngle = deltaAngle + (alterAngle - originAngle);
					}
					FingerID.erase(find(FingerID.begin(), FingerID.end(), trackFingerID[trackNext]));
					trackEndedArr[trackNext] = true;
				}

				trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1;
			}

			// !!!DEBUG!!!
			successNum = successNum + max(0.0, (1-abs(finalAngle-targetAngle)/abs(targetAngle-initialAngle)));

			////
			//finalAngle = finalAngle + deltaAngle;
			//cout << deltaAngle << " " << targetAngle << " " << resultAngle << " " << finalAngle << endl;
			//cout << deltaAngle << " " << targetAngle << " " << fmod((finalAngle-resultAngle), double(M_PI)) << endl;
			//cout << deltaAngle << "\t" << finalAngle << "\t" << resultAngle << "\t" << initialAngle << "\t" << resultAngle - finalAngle <<  endl;

			//cout << resultAngle << " " << finalAngle << endl;

		} else {
			//cout << "No track" << endl;
			continue;
		}
	}

	//cout << trialNum << endl;
	successRate = double(successNum) / double(trialNum);

	return successRate;
}

void MyTouchTask::SetScreenSize(double x, double y){
	screenSizeX = x;
	screenSizeY = y;
}

void MyTouchTask::SetOutputStream(ofstream* _ofs){
	ofs = _ofs;
}

/*
double MyTouchTask::TapTask(json* tapTaskData){
	//cout << (*taskData) << endl;
	double successRate = 0.0;
	int successNum = 0;
	int trialNum = (*tapTaskData)["trials"].size();

	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){
		//cout << (*taskDataMod[taskName])(*taskDataMod)[trialIndex]["rawTouchTracks"][0] << " " << (*trialIter)["targetLocation"][1] << endl;
		cout << trialIndex << " " << (*tapTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*tapTaskData)["trials"][trialIndex]["success"];
		//if ((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"].size() > 1){
		//	cout << " Fasle1" << endl;
		//	continue;
		//} else {
			// TODO: multi-track
			int touchPointNum = (*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][0]["rawTouches"].size();
			if (touchPointNum == 0){
				cout << " Fasle2" << endl;
				continue;
			}
			if (double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][0]["rawTouches"][touchPointNum-1]["timestamp"]) - double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][0]["rawTouches"][0]["timestamp"]) > 1.5){
				cout << " Fasle3" << endl;
				continue;
			}
			bool tmp = false;
			for (int i = 0 ; i < (*tapTaskData)["trials"][trialIndex]["rawTouchTracks"].size() ; i++){
				if ((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][i]["rawTouches"].size() == 0){
					continue;
				}
				if (abs(double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][i]["rawTouches"][0]["location"][0]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][0][0]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5) <= double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][0])*0.5 &&
					abs(double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][i]["rawTouches"][0]["location"][1]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][0][1]) - double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5) <= double((*tapTaskData)["trials"][trialIndex]["targetFrame"][1][1])*0.5){
					tmp = true;
				}
			}
			if (!tmp){
				cout << " Fasle4" << endl;
				continue;
			}
			bool tmp2 = false;
			for (int touchPointIndex = 0 ; touchPointIndex < touchPointNum ; touchPointIndex++){
				double dx = double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][0]["rawTouches"][touchPointIndex]["location"][0]) - double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][0]["rawTouches"][0]["location"][0]);
				double dy = double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][0]["rawTouches"][touchPointIndex]["location"][1]) - double((*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][0]["rawTouches"][0]["location"][1]);
				if (dx * dx + dy * dy >= 45.0 * 45.0){
					cout << " Fasle5" << endl;
					tmp2 = true;
					break;
				}
			}
			if (tmp2){
				continue;
			}
			cout << " True" << endl;
			successNum = successNum + 1;
		//}
	}
	//cout << trialNum << endl;
	successRate = double(successNum) / double(trialNum);

	return successRate;
}

double MyTouchTask::LongPressTask(json* longPressTaskData){
	//cout << (*taskData) << endl;
	double successRate = 0.0;
	int successNum = 0;
	int trialNum = (*longPressTaskData)["trials"].size();



	for (int trialIndex = 0 ; trialIndex < trialNum ; trialIndex++){
		cout << trialIndex << " " << (*longPressTaskData)["trials"][trialIndex]["rawTouchTracks"].size() << " " << (*longPressTaskData)["trials"][trialIndex]["success"];

		bool isRecognized = false;

		int trackNum = (*tapTaskData)["trials"][trialIndex]["rawTouchTracks"].size();


		bool tmp1 = false;
		for (int trackIndex = 0 ; trackIndex < trackNum ; trackIndex++){
			int touchPointNum = (*tapTaskData)["trials"][trialIndex]["rawTouchTracks"][trackIndex]["rawTouches"].size();
			if (touchPointNum != 0){
				tmp1 = true;
			}
		}
		if (!tmp1){
			cout << " Fasle1" << endl;
			continue;
		}

	}
	//cout << trialNum << endl;
	successRate = double(successNum) / double(trialNum);

	return successRate;
}*/