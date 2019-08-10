
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
        
        FilterDataDict={'rawTouchTracks':FilterData,'initialPosition':TaskData[iTrial]['initialPosition']}
        FinalTaskData.append(FilterDataDict) 
    return FinalTaskData

def LabelAllTrue(TaskData):
    for iTrial in range(len(TaskData)):
        for iFinger in range(len(TaskData[iTrial]["rawTouchTracks"])):
            for iPoint in range(len(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])): 
                    TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True
    return TaskData
def LabelFalse(TaskData,iTrial,iFinger,iPoint):
    TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=False


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
                    

                    
     

def LabelByHuman_Pan(myTask,Device_info,Accelerate_Threshold):
    import sklearn
    from sklearn import cluster
    import numpy as np
    for TestTrial in range(len(myTask)):
        iTrial=TestTrial
        for iFinger in range(len(myTask[iTrial]["rawTouchTracks"])):
            
            CandidateData=list()
            for iPoint in range(len(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                 
                
                 if iPoint==0 or iPoint==1:
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
                     positionX1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                     positionY1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                     positionT1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                     positionRadius1=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["majorRadius"]
                     
                     positionX2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                     positionY2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                     positionT2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]
                     positionRadius2=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["majorRadius"]
                     
                     positionX3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                     positionY3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                     positionT3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                     positionRadius3=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["majorRadius"]
                     
                     V1=np.sqrt((positionX2-positionX1)*(positionX2-positionX1)+(positionY2-positionY1)*(positionY2-positionY1))/(positionT2-positionT1)
                     V2=np.sqrt((positionX3-positionX2)*(positionX3-positionX2)+(positionY3-positionY2)*(positionY3-positionY2))/(positionT3-positionT2)
                     
                     PointTheta_t=ComputeTheta(positionX2,positionY2,positionX3,positionY3)
                     PointTheta_t_1=ComputeTheta(positionX1,positionY1,positionX2,positionY2)
                    
                     #accelerate=(V2-V1)/((positionT3-positionT1)/2)
                     accelerate=(V2-V1)
                     
                     if iPoint>3:
                         positionX0=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][0]/Device_info[0]
                         positionY0=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][1]/Device_info[1]
                         positionT0=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["timestamp"]
                         positionRadius0=myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["majorRadius"]
                         
                         PointTheta_t_2=ComputeTheta(positionX0,positionY0,positionX1,positionY1)
                         
                         Velocity_t=V2
                         Velocity_t_1=V1
                         
                         Velocity_t_2=np.sqrt((positionX1-positionX0)*(positionX1-positionX0)+(positionY1-positionY0)*(positionY1-positionY0))/(positionT1-positionT0)
        
                         a1=Velocity_t_1-Velocity_t_2
                         a2=Velocity_t-Velocity_t_1
                         aa=a2-a1
                        
                     else:
                         Velocity_t=V2
                         Velocity_t_1=V1
                         
                         Velocity_t_2=0
                         PointTheta_t_2=PointTheta_t_1
                         
                         aa=0
                         
                     Ave_accelerate=(accelerate_t_1+accelerate_t_2)/2
                     Ave_Radius=(positionRadius1+positionRadius2)/2
                     Ave_Velocity=(Velocity_t_1+Velocity_t_2)/2
                     Ave_Theta=(PointTheta_t_2+Velocity_t_1)/2
                     
                     #ChracterVector=[positionRadius3,Velocity_t]
                     #ReferenceVector=[Ave_Radius,Ave_Velocity]
                     ChracterVector=[accelerate,Velocity_t]
                     ReferenceVector=[Ave_accelerate,Ave_Velocity]
                     #ChracterVector=[accelerate,PointTheta_t]
                     #ReferenceVector=[Ave_accelerate,Ave_Theta]
                     #ChracterVector=[Velocity_t]
                     #ReferenceVector=[Ave_Velocity]
                     
                     
                     Similarity=Cosin_distance(ChracterVector,ReferenceVector)
                     accelerate_t_2=accelerate_t_1
                     accelerate_t_1=accelerate
                     

                 if Similarity is not None:
                     if Similarity<0:
                         if accelerate>Accelerate_Threshold:
                             if abs(aa)>0.001:
                                 LabelFalse(myTask,TestTrial,iFinger,iPoint)
                             #if iPoint>3:
                                
                                 #if (myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]['label']==True)&(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]['label']==True)&(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]['label']==True):
                                 #  LabelFalse(myTask,TestTrial,iFinger,iPoint)
    return myTask
def ScrollOptimizer_TrainPersonalTouch(ValidationData,Device_info,direction,parameters_range):
    import TaskSuccessVerify as tv
    import numpy as np
    
    HD=0
    TA=0.0
    IG=0
    AllNewSucess=list()
    for HDIndex in np.arange(parameters_range[0],parameters_range[1],0.1):
        #HD=HD+0.1
        #print("HD in range:",parameters_range[0],parameters_range[1])
        HD=HDIndex
        #print(HD)
        TA=0.0
        for TAIndex in np.arange(parameters_range[2],parameters_range[3],0.1):
            #print("TA in range:",parameters_range[2],parameters_range[3])
            #TA=TA+0.1
            TA=TAIndex
            #print(TA)
            IG=0
            for IGIndex in np.arange(parameters_range[4],parameters_range[5],0.1):
                #print("IG in range:",parameters_range[4],parameters_range[5])
                #IG=IG+0.1
                IG=IGIndex
                #print("IG",IG)
                for IG_state in np.arange(0,parameters_range[6],1):
                    #print("IG_state",IG_state)
                    for ATIndex in np.arange(parameters_range[7],parameters_range[8],500):
                        #print("AT ",ATIndex,"in range:",parameters_range[6],parameters_range[7])
                        #AT=AT+0.05
                        AT=ATIndex
                        #print("AT",AT)
                        for JerkTIndex in np.arange(parameters_range[9],parameters_range[10],50000):
                            #print("Jerk ",JerkTIndex,"in range:",parameters_range[8],parameters_range[9])
                            #JerkT=JerkT+0.05
                            JerkT=JerkTIndex
                            Performamce=list()
                            if direction==0:
                                TaskData=ValidationData['horizontalScrollTask']['trials']
                            elif direction==1:
                                TaskData=ValidationData['verticalScrollTask']['trials']
                            #Device_info=data['deviceInfo']['screenSize']
                            LabelAllTrue(TaskData)
                            OriTrue=0
                            NewTrue=0
                            
                            LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state,AT,JerkT)

                            for TestTrial in range(len(TaskData)):
                                Performamce.append(tv.PanTask(FilteredJson(TaskData)[TestTrial],TestTrial,Device_info,direction))
                                
                            AllNewSucess.append([np.mean(Performamce),HD,TA,IG,IG_state,AT,JerkT])
    
    ChooseHD=AllNewSucess[np.where(np.min(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][1]
    ChooseTA=AllNewSucess[np.where(np.min(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][2]
    ChooseIG=AllNewSucess[np.where(np.min(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][3]
    ChooseIG_state=AllNewSucess[np.where(np.min(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][4]
    ChooseAT=AllNewSucess[np.where(np.min(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][5]
    ChooseJerkT=AllNewSucess[np.where(np.min(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][6]
    
    #Ein=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][0]
    #print("Train Result: ",OriTrue,"vs",Ein,"in" ,ChooseHD,ChooseTA,ChooseIG,ChooseIG_state) 
    return [ChooseHD,ChooseTA,ChooseIG,ChooseIG_state,ChooseAT,ChooseJerkT]

                                  
def ScrollOptimizer_MyAlgorithm(ValidationData,Training_Data,Device_info,iTrial,direction):
    import TaskSuccessVerify as tv
    if direction==0:
        TaskData=ValidationData['horizontalScrollTask']['trials']
    else: 
        TaskData=ValidationData['verticalScrollTask']['trials']
    Accelerate_Threshold=0;

    OptimizedData=LabelAllTrue(TaskData)
    #print(len(OptimizedData))
    OptimizedData=LabelByHuman_Pan(OptimizedData,Device_info,Accelerate_Threshold)
    OptimizedData=FilteredJson(OptimizedData)
    #OptimizedData2=AdjustLocation(OptimizedData,Xadjust,Yadjust)

    

    return tv.PanTask(OptimizedData[iTrial],iTrial,Device_info,direction)


def ScrollOptimizer_TestPersonalTouch(ValidationData,Device_info,iTrial,HD,TA,IG,IG_state,AT,JerkT,direction):
    import TaskSuccessVerify as tv
    if direction==0:
        TaskData=ValidationData['horizontalScrollTask']['trials']
    elif direction==1:
        TaskData=ValidationData['verticalScrollTask']['trials']
    
    LabelAllTrue(TaskData)
    LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state,AT,JerkT)


    #print("iOS:",tv.TapTask(ValidationData['tapTask']['trials'][iTrial],iTrial),"vs","MyTouch",tv.TapTask(FilteredJson(TaskData)[iTrial],iTrial)) 
    return tv.PanTask(TaskData[iTrial],iTrial,Device_info,direction),tv.PanTask(FilteredJson(TaskData)[iTrial],iTrial,Device_info,direction)

