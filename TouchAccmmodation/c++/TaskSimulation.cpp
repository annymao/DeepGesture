#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include "complete/TouchAccommodations.h"
//#include "cget/include/nlohmann/json.hpp"
#include "json.hpp"
using namespace std;
using json = nlohmann::json;

// ref: https://github.com/nlohmann/json#arbitrary-types-conversions

int main(int argc, char *argv[]){
	
	//cout << argc << endl;
	//for (int i = 0 ; i < argc ; i++){
	//	cout << argv[i] << " ";
	//}
	//cout << endl;

	//json data;
	//cin >> data;

	double fromTime, toTime;

	//cin >> fromTime >> toTime;

	fromTime = atof(argv[1]);
	toTime = atof(argv[2]);

	string filePath(argv[3]);


	cout << fromTime << " " << toTime << endl;

	string userName, fileName;
	string User;
	string CVIndex;

	User=argv[4];
	//CVIndex=argv[5];
	string UserArray[13]={"3001","3002","3003","3005","3006","3007","3008","3009","3010","3011","3012","3014","3015"};
	for(int userindex=0;userindex<13;userindex=userindex+1){

	string User=UserArray[userindex];

	int Choose_HD_Index=0;
	int Choose_IR_Index=0;
	int Choose_TA_Index=0;
	float Choose_holdDurationTimer=0.0;
	float Choose_ignoreRepeatTimer=0.0;
	float Choose_tapAssistanceTimer=0.0;

	int TapFlag, LongPressFlag, SwipeFlag, HorizontalScrollTask, VerticalScrollTask, PinchTask, RotationTask;

	// while(cin >> userName >> fileName >> TapFlag >> LongPressFlag >> SwipeFlag >> HorizontalScrollTask >> VerticalScrollTask >> PinchTask >> RotationTask){
	// 	cout << userName << " " << fileName << " " << TapFlag << " " << LongPressFlag << " " << SwipeFlag << " " << HorizontalScrollTask << " " << VerticalScrollTask << " " << PinchTask << " " << RotationTask << endl;

		TouchAccommodations touchAccommodations = TouchAccommodations(fromTime, toTime);

	// 	// Set tasks
	// 	vector<string> tasks;
	// 	if (TapFlag == 1){
	// 		tasks.push_back("tapTask");
	// 	}
	// 	if (LongPressFlag == 1){
	// 		tasks.push_back("longPressTask");
	// 	}
	// 	if (SwipeFlag == 1){
	// 		tasks.push_back("swipeTask");
	// 	}
	// 	if (HorizontalScrollTask == 1){
	// 		tasks.push_back("horizontalScrollTask");
	// 	}
	// 	if (VerticalScrollTask == 1){
	// 		tasks.push_back("verticalScrollTask");
	// 	}
	// 	if (PinchTask == 1){
	// 		tasks.push_back("pinchTask");
	// 	}
	// 	if (RotationTask == 1){
	// 		tasks.push_back("rotationTask");
	// 	}

	// 	// Load data
		vector<string> tasks;
		tasks.push_back("tapTask");
		tasks.push_back("swipeTask");
		tasks.push_back("horizontalScrollTask");
		tasks.push_back("verticalScrollTask");

		string CVIndexArray[6]={"0","9","18","27","36","45"};
		for(int cvindex=0;cvindex<6;cvindex=cvindex+1){


		string CVIndex=CVIndexArray[cvindex];
		json data,Testdata;

		string TrainFileName,TestFileName;
		TrainFileName="SeparateData/"+User+"/"+User+"_"+CVIndex+"_Train.json";
		TestFileName="SeparateData/"+User+"/"+User+"_"+CVIndex+"_Test.json";


		ifstream ifs(TrainFileName, ifstream::in);
		cout << TrainFileName <<" " << endl;


		ifs >> data;
		ifs.close();

		ofstream ofs(filePath + "/Result/" + userName + ".csv", ofstream::out);

		//touchAccommodations.SimulationDefaultRecognizer(&ofs, &tasks, &data);
		
		// touchAccommodations.FindBestParameter(&ofs, &tasks, &data,&Choose_HD_Index,&Choose_IR_Index,&Choose_TA_Index,&Choose_holdDurationTimer,&Choose_ignoreRepeatTimer,&Choose_tapAssistanceTimer);

		// cout<<&Choose_HD_Index<<" "<<&Choose_IR_Index<<" "<<&Choose_TA_Index<<" "<<&Choose_holdDurationTimer<<" "<<&Choose_ignoreRepeatTimer<<" "<<&Choose_tapAssistanceTimer<<endl;

		// ifstream iifs(TestFileName, ifstream::in);
		// cout << TestFileName <<" " << endl;


		// iifs >> Testdata;
		// iifs.close();

		// cout<<"==============Test================== "<<User<<" "<< CVIndex <<" ==============="<<endl;
		// touchAccommodations.TestParameter(&ofs, &tasks, &Testdata,&Choose_HD_Index,&Choose_IR_Index,&Choose_TA_Index,&Choose_holdDurationTimer,&Choose_ignoreRepeatTimer,&Choose_tapAssistanceTimer);



		}


}



        //cout << data <<" " << endl;
	// 	ofs.close();

	//}

	// Tap, LP, Swipe, H, V, P, R

	//cout << j["tapTask"]["trials"].size() << endl;
	//cout << data["tapTask"]["trials"][0]["rawTouchTracks"][0]["rawTouches"][0]["timestamp"] << endl;
	//double tmp = data["tapTask"]["trials"][0]["rawTouchTracks"][0]["rawTouches"][0]["timestamp"];
	//cout << setprecision(17) << tmp << endl;
	//cout << typeid(double(data["tapTask"]["trials"][0]["rawTouchTracks"][0]["rawTouches"][0]["timestamp"])).name() << endl;

	//TouchAccommodations touchAccommodations = TouchAccommodations();

	//vector<string> tasks {"tapTask"};
	//vector<string> tasks {"longPressTask"};
	//vector<string> tasks {"horizontalScrollTask"};
	//vector<string> tasks {"verticalScrollTask"};
	//vector<string> tasks {"horizontalScrollTask", "verticalScrollTask"};
	//vector<string> tasks {"swipeTask"};
	//vector<string> tasks {"pinchTask"};
	//vector<string> tasks {"rotationTask"};
	//vector<string> tasks {"tapTask", "longPressTask"};
	//vector<string> tasks {"tapTask", "scrollTask"};

	//touchAccommodations.FindBestParameter(&tasks, &data);

	return 0;
}

