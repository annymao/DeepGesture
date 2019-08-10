def CrossValidation(cvindex,data_noCrossValidation):
    import numpy as np
    
    
    TrainDataDict=dict()
    ValidDataDict=dict()
    
    ValidTaskStartIndex=0
    ValidTaskStartIndexArray=list()

    AllTaskValidIndex=dict()

    TrainTotalTrail=0
    ValidTotalTrail=0
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        
        
        DataLen=len(data_noCrossValidation[task]['trials'])
        Trainstart=cvindex%DataLen
        Trainend=(cvindex+DataLen-10)%DataLen;
    
        if Trainstart>Trainend:
            ValidIndex=np.array(range(DataLen)[Trainend:Trainstart])
            TrainIndex=list(set(range(DataLen))-(set(ValidIndex)))
        else:
            TrainIndex=np.array(range(DataLen)[Trainstart:Trainend])
            ValidIndex=list(set(range(DataLen))-(set(TrainIndex)))
        
        
        
        ####################
        TrainData_OneTask=list()
        TrainDataDict_OneTask=dict()
        
        for iTrial in TrainIndex:
            TrainTotalTrail=TrainTotalTrail+1
            FilterDataDict=data_noCrossValidation[task]['trials'][iTrial]
            TrainData_OneTask.append(FilterDataDict) 
        
        
        TrainDataDict_OneTask['trials']=TrainData_OneTask
        TrainDataDict[task]=TrainDataDict_OneTask
        
        ValidData_OneTask=list()
        ValidDataDict_OneTask=dict()
        #print(ValidIndex)
        AllTaskValidIndex[task]=ValidIndex
        for iTrial in ValidIndex:
            ValidTotalTrail=ValidTotalTrail+1
            FilterDataDict=dict()
           
            FilterDataDict=data_noCrossValidation[task]['trials'][iTrial]
            ValidTaskStartIndexArray.append(ValidTaskStartIndex)
            
            ValidData_OneTask.append(FilterDataDict) 
           
          
        ValidDataDict_OneTask['trials']=ValidData_OneTask
        ValidTaskStartIndex=ValidTaskStartIndex+len(ValidData_OneTask)
        ValidDataDict[task]=ValidDataDict_OneTask    
            
    print("TotalTrials",TrainTotalTrail,ValidTotalTrail)  
    return TrainDataDict,ValidDataDict,ValidIndex,ValidTaskStartIndexArray,AllTaskValidIndex


def ReadData(path_0,file_0):
    for i in range(len(file_0)):
        with open(path_0+file_0[i]) as json_file: 
            
            data_0= json.load(json_file)
            
            if file_0[i]!=file_0[0]:
                try:
                    data['horizontalScrollTask']=data_0['horizontalScrollTask']
                except:
                    print("No file")
                try:
                    data['verticalScrollTask']=data_0['verticalScrollTask']
                except:
                    print("No file")
                try:
                    data['tapTask']=data_0['tapTask']
                except:
                    print("No file")
                try:
                    data['swipeTask']=data_0['swipeTask']
                    
                except:
                    print("No file")
            elif file_0[i]==file_0[0]:
                data=data_0
                try:
                    data['horizontalScrollTask']=data_0['horizontalScrollTask']
                except:
                    print("No file")
                try:
                    data['verticalScrollTask']=data_0['verticalScrollTask']
                except:
                    print("No file")
                try:
                    data['tapTask']=data_0['tapTask']
                except:
                    print("No file")
                try:
                    data['swipeTask']=data_0['swipeTask']
                    
                except:
                    print("No file")
                
    #print(data['tapTask'])
    Device_info=data['deviceInfo']['screenSize']
    return data,Device_info

def RecognitionTimeProcess_NoInterpolation(JsonData,RecognitionTime):

    AllData=dict()
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        TrialDataDict=dict()
        TrialDataList=list()
        for iTrial in range(len(JsonData[task]['trials'])): 
            EachTrialUniquetimeStamp=list()
            for iTrack in range(len(JsonData[task]['trials'][iTrial]['rawTouchTracks'])):
                for iPoint in range(len(JsonData[task]['trials'][iTrial]['rawTouchTracks'][iTrack]['rawTouches'])):
                    EachTrialUniquetimeStamp.append(JsonData[task]['trials'][iTrial]['rawTouchTracks'][iTrack]['rawTouches'][iPoint]['timestamp'])
            if len(EachTrialUniquetimeStamp)>0:
                #print(EachTrialUniquetimeStamp)
                MinTimeStamp=np.min(np.array(EachTrialUniquetimeStamp)) 
                FingerDataDict=dict()
                FingerDataList=list()
                for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                    PointDataDict=dict()
                    PointDataList=list()
                    for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                        timestamp=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]


                        #if timestamp-MinTimeStamp<RecognitionTime:
                        PointDataList.append(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint])

                    PointDataDict['rawTouches']=PointDataList
                    #PointDataDict={'rawTouches':PointDataList}
                    FingerDataList.append(PointDataDict)

                
                FingerDataDict['rawTouchTracks']=FingerDataList
                FingerDataDict['tapEvents']=JsonData[task]['trials'][iTrial]['tapEvents']
                FingerDataDict['swipeEvents']=JsonData[task]['trials'][iTrial]['swipeEvents']
                FingerDataDict['panEvents']=JsonData[task]['trials'][iTrial]['panEvents']
                if task=='horizontalScrollTask':
                    FingerDataDict['axis']=JsonData[task]['trials'][iTrial]['axis']
                if task=='verticalScrollTask':
                    FingerDataDict['axis']=JsonData[task]['trials'][iTrial]['axis']
                     
                if task=='tapTask':
                    FingerDataDict['targetFrame']=JsonData[task]['trials'][iTrial]['targetFrame']
                #print(JsonData[task]['trials'][iTrial])
              
                #FingerDataDict={'rawTouchTracks':FingerDataList}
                TrialDataList.append(FingerDataDict)
            else:
                for iTrack in range(len(JsonData[task]['trials'][iTrial]['rawTouchTracks'])):
                    for iPoint in range(len(JsonData[task]['trials'][iTrial]['rawTouchTracks'][iTrack]['rawTouches'])):
                        print(JsonData[task]['trials'][iTrial]['rawTouchTracks'][iTrack]['rawTouches'][iPoint])

        TrialDataDict['trials']=TrialDataList     
        #TrialDataDict={'trials':TrialDataList}
        AllData[task]=TrialDataDict
    
    return AllData

def SaveJsonFile(JsonData,FileName):
	import json
	
	with open(FileName,'w') as file_object:
		json.dump(JsonData,file_object)




if __name__ == '__main__':
	from os import listdir
	from os.path import isfile,isdir,join
	import json
	#User=sys.argv[1]
	for User in ['3001','3009','3010','3014','3015','3012','3008','3007','3006','3003','3002','3005','3011']:
	#for User in ['3001','3009','3010','3014']:
	#for kkkkkkk in range(1):

		path='StudyData/NewData/'+User+'/'

		files=listdir(path)
		file=list()
		for i in range(len(files)):
		    if files[i][-4:]=='json':
		        file.append(files[i])


		data_NoCrossValidation,Device_info=ReadData(path,file)

		#data_NoCrossValidation_RecognitionTime=RecognitionTimeProcess_NoInterpolation(data_NoCrossValidation,rc)
		for cvIndex in range(6):
		 

			cvIndex=cvIndex*9%100
			WritingTrainFileName='StudyData/SeparateData/'+str(User)+"/"+str(User)+"_"+str(cvIndex)+"_Train.json"
			WritingTestFileName='StudyData/SeparateData/'+str(User)+"/"+str(User)+"_"+str(cvIndex)+"_Test.json"

			Training_Data,Validation_Data,ValidIndex,ValidTaskStartIndexArray,AllTaskValidIndex=CrossValidation(cvIndex,data_NoCrossValidation)
			SaveJsonFile(Training_Data,WritingTrainFileName)
			SaveJsonFile(Validation_Data,WritingTestFileName)


