def ComputeTheta(P1X,P1Y,P2X,P2Y):
    dx=P2X-P1X
    dy=P2Y-P1Y
    import math
    
    if dy>0:
        return math.acos(dx/np.sqrt(dx*dx+dy*dy))*180.0/math.pi
    else:
        return 360-math.acos(dx/np.sqrt(dx*dx+dy*dy))*180.0/math.pi
    

def PredictAngleModel(TrainingData,Device_info):
    import numpy as np
    import TaskSuccessVerify as tv
    import matplotlib.pyplot as plt
    import math
    
            
            #plt.legend(loc='upper right')
    
    OffsetX=list()
    OffsetY=list()
    EachTrialDistance=list()
    EachTrialTheta=list() # training output

    ##training features
    EachTrialVelocity_t_Theta=list()
    EachTrialVelocity_t_1_Theta=list()
    EachTrialAccelerate_t_Theta=list()
    EachTrialAveMove_t_Theta=list()
    EachAveVelocityTheta_Cos=list()

    TotalTrials=len(TrainingData['tapTask']['trials'])
    for iTrial in range(TotalTrials):
        EachTrialOffsetX=list()
        EachTrialOffsetY=list()
        Velocity_t_Theta_List_Cos=list()

        TargetX=TrainingData['tapTask']['trials'][iTrial]["targetFrame"][0][0]+ TrainingData['tapTask']['trials'][iTrial]["targetFrame"][1][0]*0.5
        TargetY=TrainingData['tapTask']['trials'][iTrial]["targetFrame"][0][1]+ TrainingData['tapTask']['trials'][iTrial]["targetFrame"][1][1]*0.5
        
        if (TargetX<Device_info[0]/2)&( TargetY<Device_info[1]/2):
            pltcolor='red'
        elif (TargetX<Device_info[0]/2)& (TargetY>Device_info[1]/2):
            pltcolor='green'
        elif (TargetX>Device_info[0]/2 )& (TargetY>Device_info[1]/2):
            pltcolor='blue'
        elif (TargetX>Device_info[0]/2 )& (TargetY<Device_info[1]/2):
            pltcolor='yellow'
        else:
            pltcolor='gray'
        #print(TargetX,TargetY ,Device_info[0]/2,Device_info[1]/2,pltcolor)
        #if tv.TapTask(TrainingData['tapTask']['trials'][iTrial],iTrial)==True:
        if True==True:
            for iFinger in range(len(TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"])):
                Point_0_location=TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['location']
                for iPoint in range(1,len(TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])): 
                    
                    Point_t_location=TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location']
                    Point_t_1_location=TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['previousLocation']
                    Point_t_2_location=TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]['previousLocation']
                    
                    dx=Point_t_location[0]-TargetX
                    dy=Point_t_location[1]-TargetY
                    if (abs(dx)<100) & (abs(dy)<100):
                        
                        EachTrialOffsetX.append(dx)
                        EachTrialOffsetY.append(dy)
                        TargetTheta=ComputeTheta(TargetX,TargetY,Point_t_location[0],Point_t_location[1])
                        


                        


                        Velocity_t_Theta=ComputeTheta(Point_t_1_location[0],Point_t_1_location[1],Point_t_location[0],Point_t_location[1])

                        Velocity_t_1_Theta=ComputeTheta(Point_t_2_location[0],Point_t_2_location[1],Point_t_1_location[0],Point_t_1_location[1])
                        Accelerate_t_Theta=ComputeTheta(Point_t_1_location[0]-Point_t_2_location[0],Point_t_1_location[1]-Point_t_2_location[1],Point_t_location[0]-Point_t_1_location[0],Point_t_location[1]-Point_t_1_location[1])
                        AveMove_t_Theta=ComputeTheta(Point_0_location[0],Point_0_location[1],Point_t_location[0],Point_t_location[1])
                        EachTrialDistance.append(np.sqrt(dx*dx+dy*dy))


                        


                        if (math.isnan(TargetTheta)==False)&(math.isnan(Velocity_t_Theta)==False)&(math.isnan(Velocity_t_1_Theta)==False)&(math.isnan(Accelerate_t_Theta)==False)&(math.isnan(AveMove_t_Theta)==False):
                            
                            EachTrialTheta.append(TargetTheta)
                            EachTrialVelocity_t_Theta.append(Velocity_t_Theta)
                            EachTrialVelocity_t_1_Theta.append(Velocity_t_1_Theta)
                            EachTrialAccelerate_t_Theta.append(Accelerate_t_Theta)
                            EachTrialAveMove_t_Theta.append(AveMove_t_Theta)
                            Velocity_t_Theta_List_Cos.append(np.cos(Velocity_t_Theta))
                            EachAveVelocityTheta_Cos.append(np.mean(Velocity_t_Theta_List_Cos))
                        
                        OffsetX.append(dx)
                        OffsetY.append(dy)
            #print(iTrial,"dx:",EachTrialOffsetX,"dy",EachTrialOffsetY)
            
            #plt.scatter(EachTrialOffsetX,EachTrialOffsetY,c=pltcolor)
    # plt.subplot(2,1,1)
    # plt.hist(EachTrialTheta,bins='auto')
    # plt.subplot(2,1,2)
    # plt.hist(EachTrialDistance,bins='auto')

    # plt.show()

    EachTrialTheta_Cos=np.cos(EachTrialTheta)
    EachTrialVelocity_t_Theta_Cos=np.cos(EachTrialVelocity_t_Theta)
    EachTrialVelocity_t_1_Theta_Cos=np.cos(EachTrialVelocity_t_1_Theta)
    EachTrialAccelerate_t_Theta_Cos=np.cos(EachTrialAccelerate_t_Theta)
    EachTrialAveMove_t_Theta_Cos=np.cos(EachTrialAveMove_t_Theta)
    
    EachTrialTheta_Sin=np.sin(EachTrialTheta)
    EachTrialVelocity_t_Theta_Sin=np.sin(EachTrialVelocity_t_Theta)
    EachTrialVelocity_t_1_Theta_Sin=np.sin(EachTrialVelocity_t_1_Theta)
    EachTrialAccelerate_t_Theta_Sin=np.sin(EachTrialAccelerate_t_Theta)
    EachTrialAveMove_t_Theta_Sin=np.sin(EachTrialAveMove_t_Theta)

    from sklearn.linear_model import LinearRegression
    #X_cos=np.array([EachTrialVelocity_t_Theta_Cos,EachTrialVelocity_t_1_Theta_Cos,EachTrialAccelerate_t_Theta_Cos,EachTrialAveMove_t_Theta_Cos]).transpose(1,0)
    #X_cos=np.array([EachTrialAccelerate_t_Theta_Cos,EachTrialAveMove_t_Theta_Cos]).transpose(1,0)
    X_cos=np.array([EachAveVelocityTheta_Cos,EachTrialAveMove_t_Theta_Cos,EachTrialAccelerate_t_Theta_Cos,EachTrialVelocity_t_Theta_Cos,EachTrialVelocity_t_1_Theta_Cos]).transpose(1,0)
    
    #Test=np.array([EachTrialTheta_Cos,EachAveVelocityTheta_Cos,EachTrialVelocity_t_Theta,EachTrialVelocity_t_1_Theta,EachTrialAccelerate_t_Theta,EachTrialAveMove_t_Theta]).transpose(1,0)
    Test=np.array([EachTrialTheta_Cos,EachAveVelocityTheta_Cos]).transpose(1,0)
    
    print(Test)
    Reg_Cos=LinearRegression().fit(X=X_cos,y=EachTrialTheta_Cos)
    print(Reg_Cos.score(X_cos,EachTrialTheta_Cos))

    return np.mean(OffsetX),np.mean(OffsetY)
         
       





def FilteredJson(InputTaskData):
    FinalTaskData=list()
    for iTrial in range(len(InputTaskData)):
        
        FilterDataDict=dict()
        FilterData=list()
        for iFinger in range(len(InputTaskData[iTrial]["rawTouchTracks"])):
            EachFinger=list()
            for iPoint in range(len(InputTaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                if InputTaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    EachFinger.append(InputTaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint])
                    
            
            if len(EachFinger)!=0:
                EachFingerDict={'rawTouches':EachFinger}
                FilterData.append(EachFingerDict)
        
        FilterDataDict={'rawTouchTracks':FilterData,'targetFrame':InputTaskData[iTrial]["targetFrame"]}
        FinalTaskData.append(FilterDataDict) 
    return FinalTaskData
def LabelFalse(InputTaskData,iTrial,iFinger,iPoint):
    InputTaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=False

def LabelByHuman(myTask,Device_info):
    import sklearn
    from sklearn import cluster
    import numpy as np
    import TaskSuccessVerify as tv
    OutputData=myTask
    TapAllowableMovement=tv.TapAllowableMovement
    for TestTrial in range(len(OutputData)):
        iTrial=TestTrial
        ReferFingerIndex=0
        PointsAfterCluster=0;
        CandidateDataInFinger=list()
        for iFinger in range(len(OutputData[iTrial]["rawTouchTracks"])):
            
            CandidateData=list()
            for iPoint in range(len(OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                 
                 TargetX=OutputData[iTrial]["targetFrame"][0][0]+ OutputData[iTrial]["targetFrame"][1][0]*0.5
                 TargetY=OutputData[iTrial]["targetFrame"][0][1]+ OutputData[iTrial]["targetFrame"][1][1]*0.5
                 
#                 if (abs(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0] - TargetX) > myTask[iTrial]["targetFrame"][1][0]*0.5)|(abs(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1] - TargetY) > myTask[iTrial]["targetFrame"][1][1]*0.5):
#                     LabelFalse(myTask,TestTrial,iFinger,iPoint)
#                 
                 
                 if iPoint==0 or iPoint==1:
                     accelerate=0
                 else:
                     positionX1=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                     positionY1=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                     positionT1=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                     
                     positionX2=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                     positionY2=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                     positionT2=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]
                     
                     positionX3=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                     positionY3=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                     positionT3=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                     
                     V1=np.sqrt((positionX2-positionX1)*(positionX2-positionX1)+(positionY2-positionY1)*(positionY2-positionY1))/(positionT2-positionT1)
                     V2=np.sqrt((positionX3-positionX2)*(positionX3-positionX2)+(positionY3-positionY2)*(positionY3-positionY2))/(positionT3-positionT2)
                     
                     accelerate=V2-V1
                 #print((TestTrial),(iFinger),(iPoint),(accelerate))
                 if accelerate>0:
                     LabelFalse(OutputData,TestTrial,iFinger,iPoint)
                 if iPoint!=0 & iPoint!=1: 
                     positionX1=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]
                     positionY1=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]
                     
                     positionX2=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]
                     positionY2=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]
                     
                     positionX3=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]
                     positionY3=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]
                    
                     AverageX1=np.mean([positionX2,positionX3])
                     AverageY1=np.mean([positionY2,positionY3])
                     AverageX2=np.mean([positionX1,positionX2])
                     AverageY2=np.mean([positionY1,positionY2])
                     
                     if (AverageX1-positionX1)*(AverageX1-positionX1)+(AverageY1-positionY1)*(AverageY1-positionY1)>TapAllowableMovement*TapAllowableMovement:
                         LabelFalse(OutputData,TestTrial,iFinger,iPoint-2)
                     
                     if (AverageX2-positionX3)*(AverageX2-positionX3)+(AverageY2-positionY3)*(AverageY2-positionY3)>TapAllowableMovement*TapAllowableMovement:
                         LabelFalse(OutputData,TestTrial,iFinger,iPoint) 
                 if OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                      positionx=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]
                      positiony=OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]
                      #AllData.append([timestamp,previousLocationX,previousLocationY,majorRadius,locationX,locationY])

                      CandidateData.append([iPoint,positionx,positiony])
            for iPoint in range(len(OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                if OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    CandidateDataInFinger.append([iFinger,iPoint])
            if len(CandidateData)>1:
                maxScore=0
                
                if len(CandidateData)>2:
                    for nCluster in range(2,len(CandidateData)):
                        kmeans_fit = cluster.KMeans(n_clusters = nCluster).fit(np.array(CandidateData))
                        cluster_labels = kmeans_fit.labels_
                        #print(cluster_labels)
                        #print("KmeanScore: ",sklearn.metrics.silhouette_score(CandidateData,cluster_labels))
                        if maxScore<=sklearn.metrics.silhouette_score(CandidateData,cluster_labels):
                            maxScore=sklearn.metrics.silhouette_score(CandidateData,cluster_labels)
                            
                            ChooseLabel=cluster_labels
                            #print("Choose",nCluster,ChooseLabel)
                elif len(CandidateData)==2:
                    kmeans_fit = cluster.KMeans(n_clusters = 2).fit(np.array(CandidateData))
                    cluster_labels = kmeans_fit.labels_
                    ChooseLabel=cluster_labels
                #print(chooseNcluster)
                
                
                #kmeans_fit = cluster.KMeans(n_clusters = chooseNcluster).fit(np.array(CandidateData))
                #cluster_labels = kmeans_fit.labels_
                #print(ChooseLabel)
                #print(CandidateData,len(CandidateData))
                largestCluster=np.argmax(np.bincount(ChooseLabel))
                
                ThisClusterFinalPoint=list()
                
                for i in range(len(CandidateData)):
                    CheckPoint=CandidateData[i][0]
                    
                    if(ChooseLabel[i]!=largestCluster):
                        LabelFalse(OutputData,TestTrial,iFinger,CheckPoint)
                    else:
                        ThisClusterFinalPoint.append(CandidateData[i])
                ##找出離該劇類中心最近點為代表
                Xave=np.mean(np.array(ThisClusterFinalPoint).transpose(1,0)[1])
                Yave=np.mean(np.array(ThisClusterFinalPoint).transpose(1,0)[2])
                Distance=9999999999999999999999999
                SelectedPoint=0
                for i in range(len(ThisClusterFinalPoint)):
                    distance=np.sqrt((ThisClusterFinalPoint[i][1]-Xave)*(ThisClusterFinalPoint[i][1]-Xave)+(ThisClusterFinalPoint[i][2]-Yave)*(ThisClusterFinalPoint[i][2]-Yave))
                    LabelFalse(OutputData,TestTrial,iFinger,ThisClusterFinalPoint[i][0])
                    if distance<=Distance:
                        Distance=distance
                        SelectedPoint=ThisClusterFinalPoint[i][0]
                OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['label']=True
        ####最後解決ｍｕlti fingers
#        CandidateDataInFinger=list()
#        for iFinger in range(len(myTask[iTrial]["rawTouchTracks"])):
#            for iPoint in range(len(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
#                if myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
#                    CandidateDataInFinger.append([iFinger,iPoint])
        DataPointNum=0
        for iFinger in range(len(OutputData[iTrial]["rawTouchTracks"])):
            for iPoint in range(len(OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                 if OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    DataPointNum=DataPointNum+1
                    
        if len(CandidateDataInFinger)>1:
            largestClusterFinger=np.argmax(np.bincount(np.array(CandidateDataInFinger).transpose(1,0)[0]))
            
            for i in range(len(CandidateDataInFinger)):
                CheckPoint=CandidateDataInFinger[i][1]
                if(CandidateDataInFinger[i][0]!=largestClusterFinger):
                    if DataPointNum>0:
                        LabelFalse(OutputData,iTrial,CandidateDataInFinger[i][0],CheckPoint)
                        DataPointNum=DataPointNum-1
    return OutputData
def LabelAllTrue(InputData):
    OutputData=InputData
    for iTrial in range(len(InputData)):
        for iFinger in range(len(InputData[iTrial]["rawTouchTracks"])):
            for iPoint in range(len(InputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])): 
                    OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True
    return OutputData

def Gaussian2DModel(TrainingData,Device_info):
    import numpy as np
    import TaskSuccessVerify as tv
    import matplotlib.pyplot as plt
    LabelAllTrue(TrainingData['tapTask']['trials'])
    LabelByHuman(TrainingData['tapTask']['trials'],Device_info)
            #plt.legend(loc='upper right')
    
    OffsetX=list()
    OffsetY=list()
    TotalTrials=len(TrainingData['tapTask']['trials'])
    for iTrial in range(TotalTrials):
        EachTrialOffsetX=list()
        EachTrialOffsetY=list()
        TargetX=TrainingData['tapTask']['trials'][iTrial]["targetFrame"][0][0]+ TrainingData['tapTask']['trials'][iTrial]["targetFrame"][1][0]*0.5
        TargetY=TrainingData['tapTask']['trials'][iTrial]["targetFrame"][0][1]+ TrainingData['tapTask']['trials'][iTrial]["targetFrame"][1][1]*0.5
                    
        if tv.TapTask(TrainingData['tapTask']['trials'][iTrial],iTrial)==True:
        #if True==True:
            for iFinger in range(len(TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"])):
                for iPoint in range(len(TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])): 
                    #if TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    if True==True:
                        dx=TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]-TargetX
                        dy=TrainingData['tapTask']['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]-TargetY
                        if (abs(dx)<100.0)& (abs(dy)<100.0):
                            OffsetX.append(dx)
                            OffsetY.append(dy)
                            EachTrialOffsetX.append(dx)
                            EachTrialOffsetY.append(dy)

    return np.mean(OffsetX),np.mean(OffsetY)
    

def AdjustLocation(InputData,xmean,ymean):

    OutputData=InputData
    for iTrial in range(len(InputData)):
        for iFinger in range(len(InputData[iTrial]["rawTouchTracks"])):
            for iPoint in range(len(InputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]=InputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]-xmean
                OutputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]=InputData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]-ymean
    
    return OutputData


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
                    

                    
                    
def TapOptimizer_Graph(TaskData,Step):
    def LabelTrue(InputData):
        OutputData=InputData
        for iFinger in range(len(InputData["rawTouchTracks"])):
            for iPoint in range(len(InputData["rawTouchTracks"][iFinger]["rawTouches"])): 
                    OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True
        return OutputData

    def LabelFalse(InputTaskData,iFinger,iPoint):
        InputTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=False


    def LabelByMyAlgorithm(myTask):
        import sklearn
        from sklearn import cluster
        import numpy as np
        import TaskSuccessVerify as tv
        OutputData=myTask
        TapAllowableMovement=tv.TapAllowableMovement
        
        
        ReferFingerIndex=0
        PointsAfterCluster=0;
        CandidateDataInFinger=list()
        for iFinger in range(len(OutputData["rawTouchTracks"])):
            
            CandidateData=list()
            for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                 
                 if iPoint==0 or iPoint==1:
                     accelerate=0
                 else:
                     # positionX1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                     # positionY1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                     # positionT1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                     
                     # positionX2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                     # positionY2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                     # positionT2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]
                     
                     # positionX3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                     # positionY3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                     # positionT3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]


                     positionX1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]
                     positionY1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]
                     positionT1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                     
                     positionX2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]
                     positionY2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]
                     positionT2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]
                     
                     positionX3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]
                     positionY3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]
                     positionT3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                     
                     
                     V1=np.sqrt((positionX2-positionX1)*(positionX2-positionX1)+(positionY2-positionY1)*(positionY2-positionY1))/(positionT2-positionT1)
                     V2=np.sqrt((positionX3-positionX2)*(positionX3-positionX2)+(positionY3-positionY2)*(positionY3-positionY2))/(positionT3-positionT2)
                     
                     accelerate=V2-V1
                 #print((TestTrial),(iFinger),(iPoint),(accelerate))
                 if accelerate>0:
                     if Step>1:
                        LabelFalse(OutputData,iFinger,iPoint)
                 if iPoint!=0 & iPoint!=1: 
                     positionX1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]
                     positionY1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]
                     
                     positionX2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]
                     positionY2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]
                     
                     positionX3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]
                     positionY3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]
                    
                     AverageX1=np.mean([positionX2,positionX3])
                     AverageY1=np.mean([positionY2,positionY3])
                     AverageX2=np.mean([positionX1,positionX2])
                     AverageY2=np.mean([positionY1,positionY2])
                     
                     if (AverageX1-positionX1)*(AverageX1-positionX1)+(AverageY1-positionY1)*(AverageY1-positionY1)>TapAllowableMovement*TapAllowableMovement:
                         if Step>2:
                            LabelFalse(OutputData,iFinger,iPoint-2)
                     
                     if (AverageX2-positionX3)*(AverageX2-positionX3)+(AverageY2-positionY3)*(AverageY2-positionY3)>TapAllowableMovement*TapAllowableMovement:
                         if Step>2:
                            LabelFalse(OutputData,iFinger,iPoint) 
                 if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                      positionx=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]
                      positiony=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]
                      #AllData.append([timestamp,previousLocationX,previousLocationY,majorRadius,locationX,locationY])

                      CandidateData.append([iPoint,positionx,positiony])
            for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    CandidateDataInFinger.append([iFinger,iPoint])
            if len(CandidateData)>1:
                maxScore=0
                
                if len(CandidateData)>2:
                    for nCluster in range(2,len(CandidateData)):
                        kmeans_fit = cluster.KMeans(n_clusters = nCluster).fit(np.array(CandidateData))
                        cluster_labels = kmeans_fit.labels_
                        #print(cluster_labels)
                        #print("KmeanScore: ",sklearn.metrics.silhouette_score(CandidateData,cluster_labels))
                        if maxScore<=sklearn.metrics.silhouette_score(CandidateData,cluster_labels):
                            maxScore=sklearn.metrics.silhouette_score(CandidateData,cluster_labels)
                            
                            ChooseLabel=cluster_labels
                            #print("Choose",nCluster,ChooseLabel)
                elif len(CandidateData)==2:
                    kmeans_fit = cluster.KMeans(n_clusters = 2).fit(np.array(CandidateData))
                    cluster_labels = kmeans_fit.labels_
                    ChooseLabel=cluster_labels
                #print(chooseNcluster)
                
                
                #kmeans_fit = cluster.KMeans(n_clusters = chooseNcluster).fit(np.array(CandidateData))
                #cluster_labels = kmeans_fit.labels_
                #print(ChooseLabel)
                #print(CandidateData,len(CandidateData))
                largestCluster=np.argmax(np.bincount(ChooseLabel))
                
                ThisClusterFinalPoint=list()
                
                for i in range(len(CandidateData)):
                    CheckPoint=CandidateData[i][0]
                    
                    if(ChooseLabel[i]!=largestCluster):
                        if  Step>3:
                            LabelFalse(OutputData,iFinger,CheckPoint)
                    else:
                        ThisClusterFinalPoint.append(CandidateData[i])
                ##找出離該劇類中心最近點為代表
                Xave=np.mean(np.array(ThisClusterFinalPoint).transpose(1,0)[1])
                Yave=np.mean(np.array(ThisClusterFinalPoint).transpose(1,0)[2])
                Distance=9999999999999999999999999
                SelectedPoint=0
                for i in range(len(ThisClusterFinalPoint)):
                    distance=np.sqrt((ThisClusterFinalPoint[i][1]-Xave)*(ThisClusterFinalPoint[i][1]-Xave)+(ThisClusterFinalPoint[i][2]-Yave)*(ThisClusterFinalPoint[i][2]-Yave))
                    if Step>3:
                        LabelFalse(OutputData,iFinger,ThisClusterFinalPoint[i][0])
                    if distance<=Distance:
                        Distance=distance
                        SelectedPoint=ThisClusterFinalPoint[i][0]
                OutputData["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['label']=True
        ####最後解決ｍｕlti fingers
#        CandidateDataInFinger=list()
#        for iFinger in range(len(myTask[iTrial]["rawTouchTracks"])):
#            for iPoint in range(len(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
#                if myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
#                    CandidateDataInFinger.append([iFinger,iPoint])
        
        DataPointNum=0
        for iFinger in range(len(OutputData["rawTouchTracks"])):
            for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                 if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    DataPointNum=DataPointNum+1
        
        if len(CandidateDataInFinger)>1:
            largestClusterFinger=np.argmax(np.bincount(np.array(CandidateDataInFinger).transpose(1,0)[0]))
            
            for i in range(len(CandidateDataInFinger)):
                CheckPoint=CandidateDataInFinger[i][1]
                if(CandidateDataInFinger[i][0]!=largestClusterFinger):
                    if DataPointNum>0:
                        if Step>4:
                            LabelFalse(OutputData,CandidateDataInFinger[i][0],CheckPoint)
                            DataPointNum=DataPointNum-1
        MaxTime=0
        FinalFinger=0
        FinalFingerPoint=0


       

        for iFinger in range(len(OutputData["rawTouchTracks"])):
            for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):

                 if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    print("remain",iFinger,iPoint)
                    t=OutputData["rawTouchTracks"][iFinger]["rawTouches"][len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp']- OutputData["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                    if t>MaxTime:
                        if Step>5:
                            LabelFalse(OutputData,FinalFinger,FinalFingerPoint)
                            MaxTime=t
                            FinalFinger=iFinger
                            FinalFingerPoint=iPoint
                            OutputData["rawTouchTracks"][FinalFinger]["rawTouches"][FinalFingerPoint]['label']=True
                    else:
                        if Step>5:
                            LabelFalse(OutputData,iFinger,iPoint)



        print("Final:",FinalFinger,FinalFingerPoint)
        return OutputData



    def FilteredJsonOneTrial(InputTaskData):
       
        FilterDataDict=dict()
        FilterData=list()
        for iFinger in range(len(InputTaskData["rawTouchTracks"])):
            EachFinger=list()
            for iPoint in range(len(InputTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
                if InputTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    EachFinger.append(InputTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint])
                    
            
            if len(EachFinger)!=0:
                EachFingerDict={'rawTouches':EachFinger}
                FilterData.append(EachFingerDict)
        
        FilterDataDict={'rawTouchTracks':FilterData,'targetFrame':InputTaskData["targetFrame"]}
        
        return FilterDataDict
    import TaskSuccessVerify as tv
    OptimizedData=LabelTrue(TaskData)
    OptimizedData=LabelByMyAlgorithm(OptimizedData)
    FilteredOptimizedData=FilteredJsonOneTrial(OptimizedData)

    
    return OptimizedData,tv.TapTaskOneTrial(FilteredOptimizedData)



def tapOptimizer_MyAlgorithm(ValidationData,Training_Data,Device_info,iTrial):
    import TaskSuccessVerify as tv
    TaskData=ValidationData['tapTask']['trials']
    Xadjust,Yadjust=Gaussian2DModel(Training_Data,Device_info)
    
    
    OptimizedData=LabelAllTrue(TaskData)
    OptimizedData=LabelByHuman(OptimizedData,Device_info)
    OptimizedData=FilteredJson(OptimizedData)
    #OptimizedData2=AdjustLocation(OptimizedData,Xadjust,Yadjust)

    OriTrue=0
    NewTrue=0
    # for i in range(len(TaskData)):
    #     if tv.TapTask(ValidationData['tapTask']['trials'][i],i)==True:
    #         OriTrue=OriTrue+1
    #     if tv.TapTask(OptimizedData[i],i)==True:
    #         NewTrue=NewTrue+1
    #print("iOS",tv.TapTask(ValidationData['tapTask']['trials'][iTrial],iTrial),"vs","MyMethod",tv.TapTask(OptimizedData[iTrial],iTrial)) 
    return tv.TapTask(OptimizedData[iTrial],iTrial)

def tapOptimizer_TrainPersonalTouch(ValidationData,Device_info,parameters_range):
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
                            TaskData=ValidationData['tapTask']['trials']
                            #Device_info=data['deviceInfo']['screenSize']
                            LabelAllTrue(TaskData)
                            OriTrue=0
                            NewTrue=0
                            
                            LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state,AT,JerkT)
                            for TestTrial in range(len(TaskData)):
                                if tv.TapTask(TaskData[TestTrial],TestTrial)==True:
                                    OriTrue=OriTrue+1
                                if tv.TapTask(FilteredJson(TaskData)[TestTrial],TestTrial)==True:
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

def tapOptimizer_TestPersonalTouch(ValidationData,Device_info,iTrial,HD,TA,IG,IG_state,AT,JerkT):
    import TaskSuccessVerify as tv
    TaskData=ValidationData['tapTask']['trials']
    LabelAllTrue(TaskData)
    LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state,AT,JerkT)

    #print("iOS:",tv.TapTask(ValidationData['tapTask']['trials'][iTrial],iTrial),"vs","MyTouch",tv.TapTask(FilteredJson(TaskData)[iTrial],iTrial)) 
    return tv.TapTask(ValidationData['tapTask']['trials'][iTrial],iTrial),tv.TapTask(FilteredJson(TaskData)[iTrial],iTrial)

