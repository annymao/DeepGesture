#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:18:17 2019

@author: mhci430
"""

from __future__ import print_function
import random
#import tensorflow as tf
#from tensorflow.contrib import rnn
import DataPreProcess_Final as dp
import numpy as np
from os import listdir
from os.path import isfile,isdir,join
import json
import Optimizer.TapOptimizer as tapopt
import Optimizer.ScrollOptimizer as scrollopt
import Optimizer.SwipeOptimizer as swipeopt
import sys
import TaskSuccessVerify as tv

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
    
def ComputeJerk(Point_t,Point_t_1,Point_t_2,Point_t_3):
    ##backward
    import numpy as np
    h=((Point_t[2]-Point_t_1[2])+(Point_t_1[2]-Point_t_2[2])+(Point_t_2[2]-Point_t_3[2]))/3
    JerkX=(Point_t[0]-3*Point_t_1[0]+3*Point_t_2[0]-Point_t_3[0])/(h*h*h)
    JerkY=(Point_t[1]-3*Point_t_1[1]+3*Point_t_2[1]-Point_t_3[1])/(h*h*h)

    return np.sqrt(JerkX*JerkX+JerkY*JerkY)
def ComputeAccelerate(Point_t,Point_t_1,Point_t_2):
    ##backward
    import numpy as np
    h=((Point_t[2]-Point_t_1[2])+(Point_t_1[2]-Point_t_2[2]))/2
    aX=(Point_t[0]-2*Point_t_1[0]+Point_t_2[0])/(h*h)
    aY=(Point_t[1]-2*Point_t_1[1]+Point_t_2[1])/(h*h)
    return np.sqrt(aX*aX+aY*aY)
def ComputeVelocity(Point_t,Point_t_1):
    import numpy as np
    
    vx=(Point_t[0]-Point_t_1[0])/(Point_t[2]-Point_t_1[2])
    vy=(Point_t[1]-Point_t_1[1])/(Point_t[2]-Point_t_1[2])
    return np.sqrt(vx*vx+vy*vy)

def LabelAllTrue(TaskData):
    for iTrial in range(len(TaskData)):
        for iFinger in range(len(TaskData[iTrial]["rawTouchTracks"])):
            for iPoint in range(len(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])): 
                    TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True
    return TaskData
def LabelAllTrue2(TaskData):
    for iTrial in range(len(TaskData)):
        for iFinger in range(len(TaskData[iTrial]["rawTouchTracks"])):
            for iPoint in range(len(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])): 
                    TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True
    return TaskData
def LabelFalse(TaskData,iTrial,iFinger,iPoint):
    TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=False

def LabelFalse2(TaskData,iFinger,iPoint):
    TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=False

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
        
        FilterDataDict={'rawTouchTracks':FilterData}
        FinalTaskData.append(FilterDataDict) 
    return FinalTaskData
def FilteredJson2(TaskData):
    FinalTaskData=list()
   
    FilterDataDict=dict()
    FilterData=list()
    for iFinger in range(len(TaskData["rawTouchTracks"])):
        EachFinger=list()
        for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
            if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                EachFinger.append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint])
                
        
        if len(EachFinger)!=0:
            EachFingerDict={'rawTouches':EachFinger}
            FilterData.append(EachFingerDict)
    
    FilterDataDict={'rawTouchTracks':FilterData,'tapEvents':TaskData['tapEvents'],'panEvents':TaskData['panEvents']}
    FinalTaskData.append(FilterDataDict) 
    return FinalTaskData
    
def LabelByPersonalTouch(myTask,Device_info,HD,TA,IG,IG_state,AT,JerkT):   
    import numpy as np
   
    if len(myTask["rawTouchTracks"])>0:
        EarliestTimeStamp=9999999999999999999999999999999999999
        EachFingerTime=np.zeros((len(myTask["rawTouchTracks"]),2))
        #print(len(myTask[iTrial]["rawTouchTracks"]))
        for iFinger in range(len(myTask["rawTouchTracks"])):
            EarliestTimeStamp=myTask["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
            EachFingerTime[iFinger][0]=myTask["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
            EachFingerTime[iFinger][1]=myTask["rawTouchTracks"][iFinger]["rawTouches"][len(myTask["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp']
        #print(EachFingerTime)
        EarliestTimeStamp=np.min(EachFingerTime[:][0])
        #EarliestEndTimeStamp=np.min(EachFingerTime[:][1])
        TA_EarliestTimeStamp=999999999999999999999999999
        for iFinger in range(len(myTask["rawTouchTracks"])):
            for iPoint in range(len(myTask["rawTouchTracks"][iFinger]["rawTouches"])):
                if myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']<EarliestTimeStamp+HD:
                    LabelFalse2(myTask,iFinger,iPoint)
                    
                elif (myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']>EarliestTimeStamp+HD)&(myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']<EarliestTimeStamp+HD+TA):
                    if TA_EarliestTimeStamp>myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']:
                        TA_EarliestTimeStamp=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']
                    if IG_state==1:  #最初位置
                        if myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']!=TA_EarliestTimeStamp:
                            LabelFalse2(myTask,iFinger,iPoint)
                    elif IG_state==2:
                        LabelFalse2(myTask,iFinger,iPoint)
                        if iPoint==len(myTask["rawTouchTracks"][iFinger]["rawTouches"])-1:
                            myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]['label']=True
                else:
                    if IG_state==2:
                        myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]['label']=True
                    
                    #整個螢幕都沒有 才觸發IG
                    TriggerIG=True
                    for i in range(iFinger):
                        if EachFingerTime[iFinger][0]<EachFingerTime[i][1]:
                            TriggerIG=False
                    if TriggerIG==True:
                        if(iFinger>0):
                            LastEndStamp=np.min(EachFingerTime.transpose(1,0)[1][range(iFinger)])
                            if myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']<LastEndStamp+IG:
                                LabelFalse2(myTask,iFinger,iPoint)

                if AT!=0:
                    if iPoint>=2:
                        X1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                        Y1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                        T1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                         
                        X2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                        Y2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                        T2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]
                         
                        X3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                        Y3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                        T3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                         
                        V3=ComputeVelocity([X3,Y3,T3],[X2,Y2,T2])
                        V2=ComputeVelocity([X2,Y2,T2],[X1,Y1,T1])


                        accelerate=ComputeAccelerate([X3,Y3,T3],[X2,Y2,T2],[X1,Y1,T1])

                        # if abs(accelerate)>abs(AT):
                        #     LabelFalse2(myTaskiFinger,iPoint)

                       

                if JerkT!=0:
                    if iPoint>2:
                        X0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][0]/Device_info[0]
                        Y0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][1]/Device_info[1]
                        T0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["timestamp"]

                        X1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                        Y1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                        T1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                         
                        X2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                        Y2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                        T2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]
                         
                        X3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                        Y3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                        T3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                        


                        accelerate1=ComputeAccelerate([X3,Y3,T3],[X2,Y2,T2],[X1,Y1,T1])
                        accelerate2=ComputeAccelerate([X2,Y2,T2],[X1,Y1,T1],[X0,Y0,T0])
                        

                        jerk=ComputeJerk([X3,Y3,T3],[X2,Y2,T2],[X1,Y1,T1],[X0,Y0,T0])

                        #print("accelerate",accelerate1,accelerate2," Threshold ",AT, "jerk",jerk," Threshold ",JerkT)
                        #print(abs(accelerate1-accelerate2)," vs ",jerk)
                        if abs(accelerate1-accelerate2)>JerkT:
                            LabelFalse2(myTask,iFinger,iPoint)
                

def RecognitionTimeProcess(JsonData,RecognitionTime):

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
                        if timestamp-MinTimeStamp<RecognitionTime:
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

def LabelByHuman_Classify(myTask,Device_info):
    import sklearn
    from sklearn import cluster
    import numpy as np
    
    JerkListEachTrial=list()
    for iFinger in range(len(myTask["rawTouchTracks"])):
        CandidateData=list()
        HistoryVelocity=np.zeros(4)
        HistoryAccelerate=np.zeros(3)
        Historyindex_V=0
        Historyindex_A=0
        for iPoint in range(len(myTask["rawTouchTracks"][iFinger]["rawTouches"])):
            Historyindex_V=iPoint%4
            Historyindex_A=iPoint%3
            if iPoint==3:  
                X0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][0]/Device_info[0]
                Y0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][1]/Device_info[1]
                T0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["timestamp"]

                X1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                Y1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                T1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]

                X2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                Y2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                T2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]

                X3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                Y3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                T3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]

                V3=ComputeVelocity([X3,Y3,T3],[X2,Y2,T2])
                V2=ComputeVelocity([X2,Y2,T2],[X1,Y1,T1])
                V1=ComputeVelocity([X1,Y1,T1],[X0,Y0,T0])
                Ave_Velocity=(V2+V1)/2
                Similarity=Cosin_distance([V3],[Ave_Velocity])
                # if Similarity is not None:
                #     if Similarity<0:
                #         LabelFalse2(myTask,iFinger,iPoint)

                HistoryVelocity[2]=V3
                HistoryVelocity[1]=V2
                HistoryVelocity[0]=V1

                
                if V3-V2>0:
                    LabelFalse2(myTask,iFinger,iPoint)
                else:
                    LabelFalse2(myTask,iFinger,iPoint-1)

                if V2-V1>0:
                    LabelFalse2(myTask,iFinger,iPoint-1)
                else:
                    LabelFalse2(myTask,iFinger,iPoint-2)


                JerkListEachTrial.append(ComputeJerk([X3,Y3,T3],[X2,Y2,T2],[X1,Y1,T1],[X0,Y0,T0]))
                # if ComputeJerk([X3,Y3,T3],[X2,Y2,T2],[X1,Y1,T1],[X0,Y0,T0])>0.02:
                #     LabelFalse2(myTask,iFinger,iPoint)
            elif iPoint==4: 
                X0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-4]["location"][0]/Device_info[0]
                Y0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-4]["location"][1]/Device_info[1]
                T0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-4]["timestamp"]
                 
                X1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][0]/Device_info[0]
                Y1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][1]/Device_info[1]
                T1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["timestamp"]
                 
                X2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                Y2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]

                T2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                 
                X3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                Y3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                T3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]

                X4=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                Y4=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                T4=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]

                V4=ComputeVelocity([X4,Y4,T4],[X3,Y3,T3])
                V3=ComputeVelocity([X3,Y3,T3],[X2,Y2,T2])
                V2=ComputeVelocity([X2,Y2,T2],[X1,Y1,T1])
                V1=ComputeVelocity([X1,Y1,T1],[X0,Y0,T0])

                Ave_Velocity=(V3+V2+V1)/3

                A1=ComputeAccelerate([X2,Y2,T2],[X1,Y1,T1],[X0,Y0,T0])
                A2=ComputeAccelerate([X3,Y3,T3],[X2,Y2,T2],[X1,Y1,T1])
                A3=ComputeAccelerate([X4,Y4,T4],[X3,Y3,T3],[X2,Y2,T2])
                     
                Ave_accelerate=(A1+A2)/2
                 
                 
                
                ChracterVector=[A3,V4]
                ReferenceVector=[Ave_accelerate,Ave_Velocity]
                 
                 
                Similarity=Cosin_distance(ChracterVector,ReferenceVector)
                

                # if Similarity is not None:
                #     if Similarity<0:
                #         LabelFalse2(myTask,iFinger,iPoint)
                         #if iPoint>3:
                
                HistoryVelocity[3]=V4

                HistoryAccelerate[2]=A3
                HistoryAccelerate[1]=A2
                HistoryAccelerate[0]=A1
                
                # if A3-Ave_accelerate>0:
                #     LabelFalse2(myTask,iFinger,iPoint)
                JerkListEachTrial.append(ComputeJerk([X4,Y4,T4],[X3,Y3,T3],[X2,Y2,T2],[X1,Y1,T1]))
                  # if ComputeJerk([X4,Y4,T4],[X3,Y3,T3],[X2,Y2,T2],[X1,Y1,T1])>0.02:
                #     LabelFalse2(myTask,TestTrial,iFinger,iPoint)          
                #              #if (myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]['label']==True)&(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]['label']==True)&(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]['label']==True):
                             #  LabelFalse(myTask,TestTrial,iFinger,iPoint)
        
                if V4-V3>0:
                    LabelFalse2(myTask,iFinger,iPoint)
                else:
                    LabelFalse2(myTask,iFinger,iPoint-1)

                if V3-V2>0:
                    LabelFalse2(myTask,iFinger,iPoint-1)
                else:
                    LabelFalse2(myTask,iFinger,iPoint-2)

                if V2-V1>0:
                    LabelFalse2(myTask,iFinger,iPoint-2)
                else:
                    LabelFalse2(myTask,iFinger,iPoint-3)


            elif iPoint>4:
                X0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-4]["location"][0]/Device_info[0]
                Y0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-4]["location"][1]/Device_info[1]
                T0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-4]["timestamp"]
                 
                X1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][0]/Device_info[0]
                Y1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][1]/Device_info[1]
                T1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["timestamp"]
                 
                X2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                Y2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]

                T2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                 
                X3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                Y3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                T3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]

                X4=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                Y4=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                T4=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]

                V4=ComputeVelocity([X4,Y4,T4],[X3,Y3,T3])
                V3=ComputeVelocity([X3,Y3,T3],[X2,Y2,T2])
                V2=ComputeVelocity([X2,Y2,T2],[X1,Y1,T1])
                V1=ComputeVelocity([X1,Y1,T1],[X0,Y0,T0])

                Ave_Velocity=(V3+V2+V1)/3

                A1=ComputeAccelerate([X2,Y2,T2],[X1,Y1,T1],[X0,Y0,T0])
                A2=ComputeAccelerate([X3,Y3,T3],[X2,Y2,T2],[X1,Y1,T1])
                A3=ComputeAccelerate([X4,Y4,T4],[X3,Y3,T3],[X2,Y2,T2])

                Ave_accelerate=(A1+A2)/2
                ChracterVector=[V4,A3]
                ReferenceVector=[np.mean(HistoryVelocity),np.mean(HistoryAccelerate)]
                #ReferenceVector=[V3,A2]
                 
                 
                Similarity=Cosin_distance(ChracterVector,ReferenceVector)
                

                # if Similarity is not None:
                #     if Similarity<0.99:
                #         LabelFalse2(myTask,iFinger,iPoint)

                # if A3-Ave_accelerate>0:
                #     LabelFalse2(myTask,iFinger,iPoint)
                HistoryVelocity[Historyindex_V]=V4
                HistoryAccelerate[Historyindex_A]=A3
                
                if V4-V3>0:
                    LabelFalse2(myTask,iFinger,iPoint)
                else:
                    LabelFalse2(myTask,iFinger,iPoint-1)

                if V3-V2>0:
                    LabelFalse2(myTask,iFinger,iPoint-1)
                else:
                    LabelFalse2(myTask,iFinger,iPoint-2)

                if V2-V1>0:
                    LabelFalse2(myTask,iFinger,iPoint-2)
                else:
                    LabelFalse2(myTask,iFinger,iPoint-3)
    return myTask ,JerkListEachTrial
                  
def TaskThresholdClassification(NewTaskData):
    import TaskSuccessVerify as tv
    TapMaximumDuration = tv.TapMaximumDuration; #paper  350 ms

    TapAllowableMovement = tv.TapAllowableMovement; #paper 5mm iOS 實測大約3mm (20points)




    SwipeMaximumDuration = tv.SwipeMaximumDuration;

    SwipeMinimumMovement = tv.SwipeMinimumMovement;

    SwipeMinimumVelocity = tv.SwipeMinimumVelocity;
    ##0 no data ,1:tap. , 2:swipe.  3:pan
    ##數入的是單單純純的rawtouchdata
    FingerNum=len(NewTaskData["rawTouchTracks"]);
    if(FingerNum<1):
        #print("No Finger")
        return 0
    noTouchPoint=True
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        touchpointnum=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"]);    
        if touchpointnum>0:
            noTouchPoint=False

    if noTouchPoint==True:
        #print("No Touch Point")
        return 0

    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        if(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])>0):
            TimeDuration=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]
            if TimeDuration>TapMaximumDuration:
                FinalPoint=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1]["location"]
                InitialPoint=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"]
                dx=FinalPoint[0]-InitialPoint[0]
                dy=FinalPoint[1]-InitialPoint[1]

                if abs(dx)>abs(dy):
                    return 3   #任何一個點大於門檻都為 scroll
                elif abs(dx)<=abs(dy):
                    return 4

    WhichFingerCanSwipe=np.zeros(FingerNum)
    Recognized=False
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        for iPoint in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
            if NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]>=SwipeMaximumDuration:
                if Recognized==False:
                    finalRecognizedDirection = "none";
                continue
            PointPosition=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"]
            dx = PointPosition[0] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0];
            dy = PointPosition[1] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1];
            
            #print(dx * dx + dy * dy,"vs",SwipeMinimumMovement * SwipeMinimumMovement)
            if (dx * dx + dy * dy >= SwipeMinimumMovement * SwipeMinimumMovement):    
                WhichFingerCanSwipe[iFinger] = True;
                    
            if WhichFingerCanSwipe[iFinger] ==True:
                PointPosition=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"]
                prePointPosition=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"]
                dx=PointPosition[0] - prePointPosition[0]
                dy=PointPosition[1] - prePointPosition[1]
                
                dt=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"] -NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"];
                v=np.sqrt(dx * dx + dy * dy)/dt;
                
                if (abs(v) >= SwipeMinimumVelocity):
                    return 2
    Tap_InCircle=True
    Tap_InTime=True
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        if(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])>0):
            TimeDuration=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]
        for touchPointIndex in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
            dx=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][0] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0];
            dy=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][1] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1];
            if dx*dx+dy*dy >TapAllowableMovement*TapAllowableMovement:
                TapInCircle=False
            if TimeDuration>TapMaximumDuration:
                Tap_InTime=False
    if (Tap_InCircle==True) & (Tap_InTime==True):
        return 1


    for iFinger in range(len(NewTaskData["rawTouchTracks"])):     
        FinalPoint=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][-1]["location"]
        InitialPoint=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"]
        dx=FinalPoint[0]-InitialPoint[0]
        dy=FinalPoint[1]-InitialPoint[1]

        if abs(dx)>abs(dy):
            return 3   #任何一個點大於門檻都為 scroll
        elif abs(dx)<=abs(dy):
            return 4
             

def Classification_TrainPersonalTouch(TrianData,Device_info,parameters_range):
    import TaskSuccessVerify as tv
    import numpy as np
    
    AllNewSucess=list()
    for HDIndex in np.arange(parameters_range[0],parameters_range[1],0.05):
        
        HD=HDIndex
        #print(HD)
        TA=0.0
        for TAIndex in np.arange(parameters_range[2],parameters_range[3],0.05):
            #print("TA in range:",parameters_range[2],parameters_range[3])
            #TA=TA+0.1
            TA=TAIndex
            #print(TA)
            IG=0
            for IGIndex in np.arange(parameters_range[4],parameters_range[5],0.05):
                #print("IG in range:",parameters_range[4],parameters_range[5])
                #IG=IG+0.1
                IG=IGIndex
                #print("IG",IG)
                for IG_state in np.arange(0,parameters_range[6],1):
                    #print("IG_state",IG_state)

                    #for ATIndex in np.arange(parameters_range[7],parameters_range[8],500):
                    for ATIndex in range(1):
                        #print("AT ",ATIndex,"in range:",parameters_range[6],parameters_range[7])
                        #AT=AT+0.05
                        AT=ATIndex
                        #print("AT",AT)
                        #for JerkTIndex in np.arange(parameters_range[9],parameters_range[10],1):
                        for JerkIndex in range(1):
                            #print("Jerk ",JerkTIndex,"in range:",parameters_range[8],parameters_range[9])
                            #JerkT=JerkT+0.05
                            JerkT=JerkIndex
                            #print("JerkT",JerkT)
                            OriTrue=0
                            NewTrue=0

                            for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
                                if task=='tapTask':
                                    targetTask=1
                                elif task=='swipeTask':
                                    targetTask=2
                                elif task=='horizontalScrollTask':
                                    targetTask=2
                                elif task=='verticalScrollTask':
                                    targetTask=2
                                TaskData=TrianData[task]['trials']
                                #Device_info=data['deviceInfo']['screenSize']
                                LabelAllTrue(TaskData)
                               
                                
                                
                                for TestTrial in range(len(TaskData)):
                                    LabelByPersonalTouch(TaskData[TestTrial],Device_info,HD,TA,IG,IG_state,AT,JerkT)
                                    # if tv.TaskThresholdClassification(FilteredJson2(TaskData[TestTrial])[0])==targetTask:

                                    if tv.SimulationGestureRecognizer_NoSwipe(FilteredJson2(TaskData[TestTrial])[0])==targetTask:
                                    #if tv.SwipeTask(FilteredJson(TaskData)[TestTrial],TestTrial)==True:
                                        NewTrue=NewTrue+1
                                    #print("Trial:",(TestTrial),"oringinal:",(TapTask(data['tapTask']['trials'][TestTrial],TestTrial)),"Filtered",(TapTask(FilteredJson(data['tapTask']['trials'])[TestTrial],TestTrial)))
                                    #print("-----")
                                #print(OriTrue,"vs",NewTrue,"in" ,HD,TA,IG,IG_state) 
                            AllNewSucess.append([NewTrue,HD,TA,IG,IG_state,AT,JerkT])
    #print(AllNewSucess)

    ChooseHD=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][1]
    ChooseTA=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][2]
    ChooseIG=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][3]
    ChooseIG_state=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][4]
    ChooseAT=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][5]
    ChooseJerkT=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][6]
    Ein=AllNewSucess[np.where(np.max(np.array(AllNewSucess).transpose(1,0)[0])==np.array(AllNewSucess).transpose(1,0)[0])[0][0]][0]
    #print("Train Result: ",OriTrue,"vs",Ein,"in" ,ChooseHD,ChooseTA,ChooseIG,ChooseIG_state,ChooseAT,ChooseJerkT) 
    #print("Max Success",np.max(np.array(AllNewSucess).transpose(1,0)[0]))
    return [ChooseHD,ChooseTA,ChooseIG,ChooseIG_state,ChooseAT,ChooseJerkT]


def CrossValidation(cvindex,data_noCrossValidation):
    
    
    
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
                    pass
                    #print("No file")
                try:
                    data['verticalScrollTask']=data_0['verticalScrollTask']
                except:
                    pass
                    #print("No file")
                try:
                    data['tapTask']=data_0['tapTask']
                except:
                    pass
                    #print("No file")
                try:
                    data['swipeTask']=data_0['swipeTask']
                    
                except:
                    pass
                    #print("No file")
            elif file_0[i]==file_0[0]:
                data=data_0
                try:
                    data['horizontalScrollTask']=data_0['horizontalScrollTask']
                except:
                    pass
                    #print("No file")
                try:
                    data['verticalScrollTask']=data_0['verticalScrollTask']
                except:
                    pass
                    #print("No file")
                try:
                    data['tapTask']=data_0['tapTask']
                except:
                    pass
                    #print("No file")
                try:
                    data['swipeTask']=data_0['swipeTask']
                    
                except:
                    pass
                    #print("No file")
                
    #print(data['tapTask'])
    Device_info=data['deviceInfo']['screenSize']
    return data,Device_info

def AllTrialDefault(User,rc):
    data_NoCrossValidation,Device_info=ReadData(path,file)
    iOSEventSuccess=0  
    TrialCount=0 
    data_NoCrossValidation_RecognitionTime=RecognitionTimeProcess(data_NoCrossValidation,rc)
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        #for task in ['horizontalScrollTask','verticalScrollTask']:
            EachTaskClassifySuccess=0
            if task=='tapTask':
                targettask=1
            elif task=='swipeTask':
                targettask=2
            elif task=='horizontalScrollTask':
                targettask=2
            elif task=='verticalScrollTask':
                targettask=2

            ClassifyTaskData=data_NoCrossValidation_RecognitionTime[task]['trials']
            #print(ClassifyTaskData[0])
            for iTrial in range(len(data_NoCrossValidation_RecognitionTime[task]['trials'])):
                
                TrialCount=TrialCount+1
                
                defaultRecognizer=0
                
                if len(ClassifyTaskData[iTrial]['tapEvents'])>0:
                    if len(ClassifyTaskData[iTrial]['swipeEvents'])==0:
                        if len(ClassifyTaskData[iTrial]['panEvents'])==0:
                        
                            defaultRecognizer=1
                if len(ClassifyTaskData[iTrial]['swipeEvents'])>0:
                    if len(ClassifyTaskData[iTrial]['tapEvents'])==0:
                        defaultRecognizer=2
                if len(ClassifyTaskData[iTrial]['panEvents'])>0:
                    if len(ClassifyTaskData[iTrial]['tapEvents'])==0:
                        if len(ClassifyTaskData[iTrial]['swipeEvents'])==0:
                            if task=='verticalScrollTask' or task=='horizontalScrollTask' :
                                if ClassifyTaskData[iTrial]['axis']=='horizontal':

                                    defaultRecognizer=2
                                elif ClassifyTaskData[iTrial]['axis']=='vertical':
                                    defaultRecognizer=2
                if targettask==defaultRecognizer:
                        iOSEventSuccess=iOSEventSuccess+1
                   
    print(User,"AllTrial Default Test: ",iOSEventSuccess/TrialCount)

def EvaluateTouchAccommodation(f,rc):
    for recognitiontime in range(1):
        EachRC=list()
        EachRC2=list()
        EachiOSRC=list()
        EachTouchAccommodation=list()
        for cvIndex in range(6):
            
            cvIndex=cvIndex*9%100
        # for cvIndex in range(8):
            
        #     cvIndex=cvIndex*4%7

            data_NoCrossValidation,Device_info=ReadData(path,file)
           
            data_NoCrossValidation_RecognitionTime=RecognitionTimeProcess(data_NoCrossValidation,rc)
            #print(AA['swipeTask']['trials'][0]["rawTouchTracks"][0]["rawTouches"])
            
            Training_Data,Validation_Data,ValidIndex,ValidTaskStartIndexArray,AllTaskValidIndex=CrossValidation(cvIndex,data_NoCrossValidation_RecognitionTime)
            
            

            # # ClassificationResult=np.hstack((Test_DataY,Test_DataY))
            # #######################################Training the personaltouch setting#######################################
            PersonalTouch_ClassificationParameters=Classification_TrainPersonalTouch(Training_Data,Device_info,parameters_range)

            # #SwipeModel=swipeopt.SwipeOptimizer_TrainMyAlgorithm(Training_Data)

            # #ClassifyParaString=str(cvIndex)+" Classify  Accommodation: "+str(PersonalTouch_ClassificationParameters)+" inRange: "+str(parameters_range)+"\n"
            
            # #ff.write(ClassifyParaString)
            

            # # print("For Classify",PersonalTouch_ClassificationParameters)
            # # NewTrue=0
            # # for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
            # #     if task=='tapTask':
            # #         targetTask=1
            # #     elif task=='swipeTask':
            # #         targetTask=2
            # #     elif task=='horizontalScrollTask':
            # #         targetTask=3
            # #     elif task=='verticalScrollTask':
            # #         targetTask=4
            # #     TaskData=Training_Data[task]['trials']
            # #     #Device_info=data['deviceInfo']['screenSize']
                
                
                
                
            # #     for TestTrial in range(len(TaskData)):
                    
            # #         if TaskThresholdClassification(TaskData[TestTrial])==targetTask:
            # #         #if tv.SwipeTask(FilteredJson(TaskData)[TestTrial],TestTrial)==True:
            # #             NewTrue=NewTrue+1
            # # print("NoAccommodation",NewTrue)
        


            TrialCount=0
            ClassifySuccess_TouchAccommodation=0
            ClassifySuccess_Default=0
            ClassifySuccess_Default2=0
            iOSEventSuccess=0

            EachTaskClassifyResult=list()

            # ##Default

            for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
            #for task in ['horizontalScrollTask','verticalScrollTask']:
                #print("ˇ----------",task,"----------ˇ")
                EachTaskClassifySuccess=0
                if task=='tapTask':
                    targettask=1
                elif task=='swipeTask':
                    targettask=2
                elif task=='horizontalScrollTask':
                    targettask=2
                elif task=='verticalScrollTask':
                    targettask=2

                ClassifyTaskData=Validation_Data[task]['trials']
                #print(ClassifyTaskData[0])
                for iTrial in range(len(Validation_Data[task]['trials'])):
                    
                    TrialCount=TrialCount+1
                    
                    defaultRecognizer=0
                    
                    # if len(ClassifyTaskData[iTrial]['tapEvents'])>0:
                    #     if len(ClassifyTaskData[iTrial]['swipeEvents'])==0:
                    #         if len(ClassifyTaskData[iTrial]['panEvents'])==0:
                            
                    #             defaultRecognizer=1
                    # if len(ClassifyTaskData[iTrial]['swipeEvents'])>0:
                    #     if len(ClassifyTaskData[iTrial]['tapEvents'])==0:
                    #         defaultRecognizer=2
                    # if len(ClassifyTaskData[iTrial]['panEvents'])>0:
                    #     if len(ClassifyTaskData[iTrial]['tapEvents'])==0:
                    #         if len(ClassifyTaskData[iTrial]['swipeEvents'])==0:
                    #             if task=='verticalScrollTask' or task=='horizontalScrollTask' :
                    #                 if ClassifyTaskData[iTrial]['axis']=='horizontal':

                    #                     defaultRecognizer=2
                    #                 elif ClassifyTaskData[iTrial]['axis']=='vertical':
                    #                     defaultRecognizer=2

                   
                    if len(ClassifyTaskData[iTrial]['tapEvents'])>0:
                        if len(ClassifyTaskData[iTrial]['panEvents'])==0:
                            
                            defaultRecognizer=1
                    if len(ClassifyTaskData[iTrial]['panEvents'])>0:
                        if len(ClassifyTaskData[iTrial]['tapEvents'])==0:
                            defaultRecognizer=2


                    #classifyresult_default=tv.TaskThresholdClassification(ClassifyTaskData[iTrial]) 
                    classifyresult_default=tv.SimulationGestureRecognizer_NoSwipe(ClassifyTaskData[iTrial]) 
                    #classifyresult_default=tv.SimulationGestureRecognizer_Android(ClassifyTaskData[iTrial]) 

                    #classifyresult_default2=tv.TaskThresholdClassification(ClassifyTaskData[iTrial]) 
                    if targettask==classifyresult_default:
                       ClassifySuccess_Default=ClassifySuccess_Default+1
                    # else:
                    #     print("Simulate",targettask,"vs",classifyresult_default)
                    if targettask==defaultRecognizer:
                        iOSEventSuccess=iOSEventSuccess+1
                    # else:
                    #     print("Default",targettask,"vs",defaultRecognizer)

                    # if targettask==classifyresult_default2:
                    #    ClassifySuccess_Default2=ClassifySuccess_Default2+1
                    # else:
                    #     print(task,defaultRecognizer)
            EachRC.append(ClassifySuccess_Default/TrialCount)
            EachiOSRC.append(iOSEventSuccess/TrialCount)
            EachRC2.append(ClassifySuccess_Default2/TrialCount)

            #DataString=str(rc) +" "+str(cvIndex)+" Default: "+ str(ClassifySuccess_Default) +" / "+str(TrialCount)
            #print(DataString)

            ##TouchAccommodation
            RecordFalseTrial=dict()
            
            for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
                RecodeFalseTrial_list=list()
                EachTaskClassifySuccess=0
                if task=='tapTask':
                    targettask=1
                elif task=='swipeTask':
                    targettask=2
                elif task=='horizontalScrollTask':
                    targettask=2
                elif task=='verticalScrollTask':
                    targettask=2

                for iTrial in range(len(Validation_Data[task]['trials'])):
                    
                    ClassifyTaskData=Validation_Data[task]['trials']
                    LabelAllTrue(ClassifyTaskData)
                    #LabelByHuman_Classify(ClassifyTaskData[],Device_info)
                    LabelByPersonalTouch(ClassifyTaskData[iTrial],Device_info,PersonalTouch_ClassificationParameters[0],PersonalTouch_ClassificationParameters[1],PersonalTouch_ClassificationParameters[2],PersonalTouch_ClassificationParameters[3],PersonalTouch_ClassificationParameters[4],PersonalTouch_ClassificationParameters[5])
                    #classifyresult_touchaccomodation=tv.TaskThresholdClassification(FilteredJson2(ClassifyTaskData[iTrial])[0]) #PersonalTouch classify
                    classifyresult_touchaccomodation=tv.SimulationGestureRecognizer_NoSwipe(FilteredJson2(ClassifyTaskData[iTrial])[0]) #PersonalTouch classify
                    #classifyresult_touchaccomodation=tv.SimulationGestureRecognizer_Android(FilteredJson2(ClassifyTaskData[iTrial])[0]) #PersonalTouch classify
                    
                    if targettask==classifyresult_touchaccomodation:
                       ClassifySuccess_TouchAccommodation=ClassifySuccess_TouchAccommodation+1
                    else:
                        RecodeFalseTrial_list.append(AllTaskValidIndex[task][iTrial])
                
                RecordFalseTrial[task]=RecodeFalseTrial_list  
            EachTouchAccommodation.append(ClassifySuccess_TouchAccommodation/TrialCount)
            compare=[iOSEventSuccess/TrialCount,ClassifySuccess_Default/TrialCount,ClassifySuccess_TouchAccommodation/TrialCount]
            DataString=str(cvIndex)+" "+str(compare)+" Default: "+ str(ClassifySuccess_Default) +" / "+str(TrialCount)+" TouchAccommodation: " + str(ClassifySuccess_TouchAccommodation) +" / "+str(TrialCount)+" AccommodationParameters: "+str(PersonalTouch_ClassificationParameters)+" inRange: "+str(parameters_range)+" ErrorRecord: (tap) "+ str(RecordFalseTrial['tapTask']) +" / "+str(AllTaskValidIndex['tapTask'])+" (swipe) "+ str(RecordFalseTrial['swipeTask'])+" / "+str(AllTaskValidIndex['swipeTask'])+" (hscroll) "+ str(RecordFalseTrial['horizontalScrollTask'])+" / "+str(AllTaskValidIndex['horizontalScrollTask'])+" (vscroll) "+ str(RecordFalseTrial['verticalScrollTask'])+" / "+str(AllTaskValidIndex['verticalScrollTask'])+"\n"
            #print(DataString)
            f.write(DataString)
            

            
            
            # #
        #print(str(np.mean(EachiOSRC))," ",str(rc)+" "+str(np.mean(EachRC))," ",str(np.mean(EachRC2)))
        f.write("\n")
        f.write("\n")
        f.write("=================================")
        f.write("\n")
        OverallResultString=str(User)+"Default: "+str(np.mean(EachiOSRC))+" Simulate: "+str(np.mean(EachRC))+" TouchAccommodation: "+str(np.mean(EachTouchAccommodation))
        #print(OverallResultString)
        print(str(User)+" "+str(np.mean(EachiOSRC))+" "+str(np.mean(EachRC))+" TouchAccommodation: "+str(np.mean(EachTouchAccommodation)))
        f.write(OverallResultString)
        rc=rc+0.1

if len(sys.argv)!=9:
    print("輸入六個參數：userid與參數範圍（hd,ta,ig,igstate,at）")
    sys.exit(1)
parameters_range=[float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]),float(sys.argv[8])]

UserString=[sys.argv[1]]
for User in ['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']:
#for User in ['2001','2002','2003','2004','2005','2006','2007','2008','2009','2012','2013']:
#for User in ['3005']:
#for User in UserString:

    path='StudyData/NewData/'+User+'/'
    #path='StudyData/OldData/'+User+'/'
    from datetime import datetime
    TimeNow=datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    WritingFileName='Result/TouchAccommodation/'+User+"_"+str(sys.argv[3])+"_"+str(sys.argv[5])+"_"+str(sys.argv[7])+"_"+str(sys.argv[8])+"_"+TimeNow+'.txt'
    #WritingFileNamePara='Parameters/Classify/'+User+"_ThresholdBased_"+TimeNow+'.txt'

    f=open(WritingFileName,'a')

    f#f=open(WritingFileNamePara,'a')
    files=listdir(path)
    file=list()
    for i in range(len(files)):
        if files[i][-4:]=='json':
            file.append(files[i])
    rc=1000000

    
    #AllTrialDefault(User,rc)
    
    EvaluateTouchAccommodation(f,rc)


    