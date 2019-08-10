def ComputeTheta(P1X,P1Y,P2X,P2Y):
    import numpy as np
    dx=P2X-P1X
    dy=P2Y-P1Y
    import math
    
    if dy>0:
        return math.acos(dx/np.sqrt(dx*dx+dy*dy))*180.0/math.pi
    else:
        return 360-math.acos(dx/np.sqrt(dx*dx+dy*dy))*180.0/math.pi
    
def Cosin_distance(vector1,vector2):
    dot_product=0.0
    normA=0.0
    normB=0.0
    for a,b in zip(vector1,vector2):
        dot_product+=a*b
        normA+=a**2
        normB+=b**2
    if normA==0.0 or normB==0.0:
        return None
    else:
        return dot_product/((normA*normB)**0.5)
def LabelAllTrue(TaskData):
    for iTrial in range(len(TaskData)):
        for iFinger in range(len(TaskData[iTrial]["rawTouchTracks"])):
            for iPoint in range(len(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])): 
                    TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True
    return TaskData
def LabelFalse(TaskData,iTrial,iFinger,iPoint):
    TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=False


def FilteredJson(TaskData):
    FinalTaskData=list()
    for iTrial in range(len(TaskData)):
        
        FilterDataDict=dict()
        FilterData=list()
        for iFinger in range(len(TaskData[iTrial]["rawTouchTracks"])):
            EachFinger=list()
            for iPoint in range(len(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                if TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    EachFinger.append(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint])
                    
            
            if len(EachFinger)!=0:
                EachFingerDict={'rawTouches':EachFinger}
                FilterData.append(EachFingerDict)
        
        FilterDataDict={'rawTouchTracks':FilterData,'targetDirection':TaskData[iTrial]['targetDirection']}
        FinalTaskData.append(FilterDataDict) 
    return FinalTaskData
def LabelByPersonalTouch(myTask,Device_info,HD,TA,IG,IG_state,AT,JerkT):   
    import numpy as np
    for TestTrial in range(len(myTask)):
        iTrial=TestTrial
        
        if len(myTask[iTrial]["rawTouchTracks"])>0:
            EarliestTimeStamp=9999999999999999999999999999999999999
            EachFingerTime=np.zeros((len(myTask[iTrial]["rawTouchTracks"]),2))
            #print(len(myTask[iTrial]["rawTouchTracks"]))
            for iFinger in range(len(myTask[iTrial]["rawTouchTracks"])):
                EarliestTimeStamp=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                EachFingerTime[iFinger][0]=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                EachFingerTime[iFinger][1]=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][len(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp']
            #print(EachFingerTime)
            EarliestTimeStamp=np.min(EachFingerTime[:][0])
            #EarliestEndTimeStamp=np.min(EachFingerTime[:][1])
            TA_EarliestTimeStamp=999999999999999999999999999
            for iFinger in range(len(myTask[iTrial]["rawTouchTracks"])):
                for iPoint in range(len(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                    if myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']<EarliestTimeStamp+HD:
                        LabelFalse(myTask,TestTrial,iFinger,iPoint)
                        
                    elif (myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']>EarliestTimeStamp+HD)&(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']<EarliestTimeStamp+HD+TA):
                        if TA_EarliestTimeStamp>myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']:
                            TA_EarliestTimeStamp=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']
                        if IG_state==1:  #最初位置
                            if myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']!=TA_EarliestTimeStamp:
                                LabelFalse(myTask,TestTrial,iFinger,iPoint)
                        elif IG_state==2:
                            LabelFalse(myTask,TestTrial,iFinger,iPoint)
                            if iPoint==len(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])-1:
                                myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]['label']=True
                    else:
                        if IG_state==2:
                            myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]['label']=True
                        
                        #整個螢幕都沒有 才觸發IG
                        TriggerIG=True
                        for i in range(iFinger):
                            if EachFingerTime[iFinger][0]<EachFingerTime[i][1]:
                                TriggerIG=False
                        if TriggerIG==True:
                            if(iFinger>0):
                                LastEndStamp=np.min(EachFingerTime.transpose(1,0)[1][range(iFinger)])
                                if myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']<LastEndStamp+IG:
                                    LabelFalse(myTask,TestTrial,iFinger,iPoint)

                    if AT!=0:
                        if iPoint==3:
                            positionX1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                            positionY1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                            positionT1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                             
                            positionX2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                            positionY2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                            positionT2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]
                             
                            positionX3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                            positionY3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                            positionT3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                             
                            V1=np.sqrt((positionX2-positionX1)*(positionX2-positionX1)+(positionY2-positionY1)*(positionY2-positionY1))/(positionT2-positionT1)
                            V2=np.sqrt((positionX3-positionX2)*(positionX3-positionX2)+(positionY3-positionY2)*(positionY3-positionY2))/(positionT3-positionT2)
                             
                            accelerate=(V2-V1)/((positionT3-positionT1)/2)
                            if abs(accelerate)>abs(AT):
                                LabelFalse(myTask,TestTrial,iFinger,iPoint)
                    if JerkT!=0:
                        if iPoint>3:
                            positionX0=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][0]/Device_info[0]
                            positionY0=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][1]/Device_info[1]
                            positionT0=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["timestamp"]

                            positionX1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                            positionY1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                            positionT1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                             
                            positionX2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                            positionY2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                            positionT2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]
                             
                            positionX3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                            positionY3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                            positionT3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                             
                            V0=np.sqrt((positionX1-positionX0)*(positionX1-positionX0)+(positionY1-positionY0)*(positionY1-positionY0))/(positionT1-positionT0) 
                            V1=np.sqrt((positionX2-positionX1)*(positionX2-positionX1)+(positionY2-positionY1)*(positionY2-positionY1))/(positionT2-positionT1)
                            V2=np.sqrt((positionX3-positionX2)*(positionX3-positionX2)+(positionY3-positionY2)*(positionY3-positionY2))/(positionT3-positionT2)
                            
                            accelerate1=(V1-V0)/((positionT2-positionT0)/2)
                            accelerate2=(V2-V1)/((positionT3-positionT1)/2)

                            jerk=(accelerate2-accelerate1)


                            if abs(accelerate1)>abs(AT):
                                LabelFalse(myTask,TestTrial,iFinger,iPoint)
                            if abs(jerk)>abs(JerkT):
                                LabelFalse(myTask,TestTrial,iFinger,iPoint)
                    

                    
     

def LabelByHuman_Swipe(myTask,Device_info):
    import sklearn
    from sklearn import cluster
    import numpy as np
    for TestTrial in range(len(myTask)):
        iTrial=TestTrial
        for iFinger in range(len(myTask[iTrial]["rawTouchTracks"])):
            
            CandidateData=list()
            for iPoint in range(len(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                 
                
                 if iPoint==0 or iPoint==1 or iPoint==2:
                     accelerate_t_2=0
                     accelerate_t_1=0
                     accelerate=0
                     positionRadius1=0
                     positionRadius2=0
                     positionRadius3=0
                     Similarity=1
                     PointTheta_t=0
                     PointTheta_t_1=0
                 else:

                     positionX0=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0]/Device_info[0]
                     positionY0=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1]/Device_info[1]
                     

                     positionX1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][0]/Device_info[0]
                     positionY1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][1]/Device_info[1]
                     
                     positionX2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                     positionY2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                     
                     positionX3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                     positionY3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                     
                     positionX4=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                     positionY4=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                     
                     PointTheta_t=ComputeTheta(positionX3,positionY3,positionX4,positionY4)
                     PointTheta_t_1=ComputeTheta(positionX2,positionY2,positionX3,positionY3)
                     PointTheta_t_2=ComputeTheta(positionX1,positionY1,positionX2,positionY2)

                    
                     Point_to_Point0_Theta=ComputeTheta(positionX0,positionY0,positionX4,positionY4)
                     Point_1_to_Point0_Theta=ComputeTheta(positionX0,positionY0,positionX3,positionY3)
                     Point_2_to_Point0_Theta=ComputeTheta(positionX0,positionY0,positionX2,positionY2)
                     Point_3_to_Point0_Theta=ComputeTheta(positionX0,positionY0,positionX1,positionY1)
                     
                     PointTheta_t_Cos=np.cos(PointTheta_t)
                     PointTheta_t_1_Cos=np.cos(PointTheta_t_1)
                     PointTheta_t_2_Cos=np.cos(PointTheta_t_2)

                     PointTheta_t_Sin=np.sin(PointTheta_t)
                     PointTheta_t_1_Sin=np.sin(PointTheta_t_1)
                     PointTheta_t_2_Sin=np.sin(PointTheta_t_2)

                     Point_to_Point0_Theta_Cos=np.cos(Point_to_Point0_Theta)
                     Point_1_to_Point0_Theta_Cos=np.cos(Point_1_to_Point0_Theta)
                     Point_2_to_Point0_Theta_Cos=np.cos(Point_2_to_Point0_Theta)
                     Point_3_to_Point0_Theta_Cos=np.cos(Point_3_to_Point0_Theta)

                     Point_to_Point0_Theta_Sin=np.sin(Point_to_Point0_Theta)
                     Point_1_to_Point0_Theta_Sin=np.sin(Point_1_to_Point0_Theta)
                     Point_2_to_Point0_Theta_Sin=np.sin(Point_2_to_Point0_Theta)
                     Point_3_to_Point0_Theta_Sin=np.sin(Point_3_to_Point0_Theta)


                     Ave_PointTheta_Cos=np.mean([PointTheta_t_1_Cos,PointTheta_t_2_Cos])
                     Ave_PointTheta_Sin=np.mean([PointTheta_t_1_Sin,PointTheta_t_2_Sin])

                     Ave_PointToZeroTheta_Cos=np.mean([Point_1_to_Point0_Theta_Cos,Point_2_to_Point0_Theta_Cos,Point_3_to_Point0_Theta_Cos])
                     Ave_PointToZeroTheta_Sin=np.mean([Point_1_to_Point0_Theta_Sin,Point_2_to_Point0_Theta_Sin,Point_3_to_Point0_Theta_Sin])
                     
                     
                     ChracterVector=[PointTheta_t_Cos,PointTheta_t_Sin,Point_to_Point0_Theta_Cos,Point_to_Point0_Theta_Sin]
                     ReferenceVector=[Ave_PointTheta_Cos,Ave_PointTheta_Sin,Ave_PointToZeroTheta_Cos,Ave_PointToZeroTheta_Sin]
                     
                     
                     Similarity=Cosin_distance(ChracterVector,ReferenceVector)
                     


                 if Similarity is not None:
                     if Similarity<0:
                        LabelFalse(myTask,TestTrial,iFinger,iPoint)
                             #if iPoint>3:
                                
                                 #if (myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]['label']==True)&(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]['label']==True)&(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]['label']==True):
                                 #  LabelFalse(myTask,TestTrial,iFinger,iPoint)
    return myTask




def SwipeOptimizer_TrainPersonalTouch(ValidationData,Device_info,parameters_range):
    import TaskSuccessVerify as tv
    import numpy as np
    
    HD=0
    TA=0.0
    IG=0
    AllNewSucess=list()
    for HDIndex in np.arange(parameters_range[0],parameters_range[1],0.1):
        #HD=HD+0.1
        
        HD=HDIndex
        #print(HD)
        TA=0.0
        for TAIndex in np.arange(parameters_range[2],parameters_range[3],0.1):
            #TA=TA+0.1
            TA=TAIndex
            #print(TA)
            IG=0
            for IGIndex in np.arange(parameters_range[4],parameters_range[5],0.1):
                
                #IG=IG+0.1
                IG=IGIndex
                #print("IG",IG)
                for IG_state in np.arange(0,3,1):
                    #print("IG_state",IG_state)
                    for ATIndex in np.arange(parameters_range[6],parameters_range[7],0.5):
                        #AT=AT+0.05
                        AT=ATIndex
                        #print("AT",AT)
                        for JerkTIndex in np.arange(parameters_range[8],parameters_range[9],0.5):
                            #JerkT=JerkT+0.05
                            JerkT=JerkTIndex
                            TaskData=ValidationData['swipeTask']['trials']
                            #Device_info=data['deviceInfo']['screenSize']
                            LabelAllTrue(TaskData)
                            OriTrue=0
                            NewTrue=0
                            
                            LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state,AT,JerkT)
                            for TestTrial in range(len(TaskData)):
                                if tv.SwipeTask(TaskData[TestTrial],TestTrial)==True:
                                    OriTrue=OriTrue+1
                                if tv.SwipeTask(FilteredJson(TaskData)[TestTrial],TestTrial)==True:
                                    NewTrue=NewTrue+1
                                #print("Trial:",(TestTrial),"oringinal:",(TapTask(data['tapTask']['trials'][TestTrial],TestTrial)),"Filtered",(TapTask(FilteredJson(data['tapTask']['trials'])[TestTrial],TestTrial)))
                                #print("-----")
                            #print(OriTrue,"vs",NewTrue,"in" ,HD,TA,IG,IG_state) 
                            AllNewSucess.append([NewTrue,HD,TA,IG,IG_state,AT,JerkT])
        
    ChooseHD=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][1]
    ChooseTA=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][2]
    ChooseIG=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][3]
    ChooseIG_state=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][4]
    ChooseAT=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][5]
    ChooseJerkT=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][6]
    
    #Ein=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][0]
    #print("Train Result: ",OriTrue,"vs",Ein,"in" ,ChooseHD,ChooseTA,ChooseIG,ChooseIG_state) 
    return [ChooseHD,ChooseTA,ChooseIG,ChooseIG_state,ChooseAT,ChooseJerkT]


def SwipeOptimizer_MyAlgorithm(ValidationData,Device_info,iTrial):
    import TaskSuccessVerify as tv
    TaskData=ValidationData['swipeTask']['trials']
    OptimizedData=LabelAllTrue(TaskData)
    #print(len(OptimizedData))
    OptimizedData=LabelByHuman_Swipe(OptimizedData,Device_info)
    OptimizedData=FilteredJson(OptimizedData)
    #OptimizedData2=AdjustLocation(OptimizedData,Xadjust,Yadjust)

    

    return tv.SwipeTask(OptimizedData[iTrial],iTrial)

def SwipeOptimizer_TrainMyAlgorithm(Training_Data):
    from sklearn.svm import SVC
    import DataPreProcess_Final as dp

    Train_X,Train_Y=dp.SwipeClassification_SVM_v2_DataPreProcess(Training_Data)
    #Valid_X,Valid_Y=dp.SwipeClassification_SVM_v1_DataPreProcess(ValidationData)
    SVM_Model=SVC(gamma='auto')

    SVM_Model.fit(Train_X,Train_Y)
    return SVM_Model


def SwipeOptimizer_TestMyAlgorithm(ValidationData,SVM_Model,iTrial):
    from sklearn.svm import SVC
    import DataPreProcess_Final as dp

    #Train_X,Train_Y=dp.SwipeClassification_SVM_v1_DataPreProcess(Validation_Data)
    Valid_X,Valid_Y=dp.SwipeClassification_SVM_v2_DataPreProcess(ValidationData)
    

    
    return SVM_Model.predict([Valid_X[iTrial]])==Valid_Y[iTrial]

def SwipeOptimizer_TestPersonalTouch(ValidationData,Device_info,iTrial,HD,TA,IG,IG_state,AT,JerkT):
    import TaskSuccessVerify as tv
    TaskData=ValidationData['swipeTask']['trials']
    LabelAllTrue(TaskData)
    LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state,AT,JerkT)

    #print("iOS:",tv.TapTask(ValidationData['tapTask']['trials'][iTrial],iTrial),"vs","MyTouch",tv.TapTask(FilteredJson(TaskData)[iTrial],iTrial)) 
    return tv.SwipeTask(ValidationData['swipeTask']['trials'][iTrial],iTrial),tv.SwipeTask(FilteredJson(TaskData)[iTrial],iTrial)


