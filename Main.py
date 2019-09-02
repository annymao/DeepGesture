from __future__ import division, print_function, absolute_import
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout, Flatten, Conv3D, MaxPool3D, BatchNormalization, Input
from keras.optimizers import RMSprop,Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
from keras.callbacks import ReduceLROnPlateau, TensorBoard
import keras

import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from os import listdir
from os.path import isfile,isdir,join
import json


def load_model(User,CrossValidationIndex,tGrid,Mode):
    if Mode=='Dynamic':
        JsonName='TrainedModel/Final/Dynamic/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.json'
        f = open(JsonName, 'r')
        model_json = f.read()
        f.close()

        loaded_model = model_from_json(model_json)
        loaded_model.load_weights('TrainedModel/Final/Dynamic/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.h5')

        print("Model Loaded.", JsonName)
        return loaded_model
    elif Mode=='Fixed':
        JsonName='TrainedModel/Final/Fixed/'+str(User)+'/model_3DCNN_Fixed_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.json'
        f = open(JsonName, 'r')
        model_json = f.read()
        f.close()

        loaded_model = model_from_json(model_json)
        loaded_model.load_weights('TrainedModel/Final/Fixed/'+str(User)+'/model_3DCNN_Fixed_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.h5')

        print("Model Loaded.", JsonName)
        return loaded_model
    elif Mode=='Dynamic_Simulator':
        JsonName='TrainedModel/Final/Dynamic_Simulator/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.json'
        f = open(JsonName, 'r')
        model_json = f.read()
        f.close()

        loaded_model = model_from_json(model_json)
        loaded_model.load_weights('TrainedModel/Final/Dynamic_Simulator/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.h5')

        print("Model Loaded.", JsonName)
        return loaded_model

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
        Trainend=(cvindex+DataLen-10)%DataLen
    
        # generate index of train and validate
        if Trainstart>Trainend:
            # ex: datalen = 30 trainStart = 15 trainEnd = 5
            # validIndex = range(30)[5:15] -> index 5~14 
            # trainIndex = 0~4,15~29
            ValidIndex=np.array(range(DataLen)[Trainend:Trainstart])
            TrainIndex=list(set(range(DataLen))-(set(ValidIndex)))
        else:
            TrainIndex=np.array(range(DataLen)[Trainstart:Trainend])
            ValidIndex=list(set(range(DataLen))-(set(TrainIndex)))
        
        
        
        ####################
        TrainData_OneTask=list()
        TrainDataDict_OneTask=dict()
        # for every index in trainIndex(every trial in task trials)
        for iTrial in TrainIndex:
            TrainTotalTrail=TrainTotalTrail+1
            FilterDataDict=data_noCrossValidation[task]['trials'][iTrial]
            TrainData_OneTask.append(FilterDataDict) 
        
        # TrainDataDict[task]['trials']
        TrainDataDict_OneTask['trials']=TrainData_OneTask
        TrainDataDict[task]=TrainDataDict_OneTask
        
        ValidData_OneTask=list()
        ValidDataDict_OneTask=dict()
        #print("Separate ","Train",TrainIndex,"Valid: ",ValidIndex)
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

# Read data from json file
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

# Map data to grid
def FindIndexOfMatrix(dataX,dataY,dataT,GridSize,TimeGrid):
    import numpy as np
    IndexX=int(np.floor(dataX/GridSize))
    IndexY=int(np.floor(dataY/GridSize))
    if TimeGrid==0:
        print("Grid Error")
    IndexT=int(np.floor(dataT/TimeGrid))
    return IndexX,IndexY,IndexT 


def ComputeVelocity2(Point_t,Point_t_1):
    import numpy as np
    
    vx=(Point_t[0]-Point_t_1[0])
    vy=(Point_t[1]-Point_t_1[1])
    return vx,vy
def ComputeVelocity(Point_t,Point_t_1):
    import numpy as np
    
    vx=(Point_t[0]-Point_t_1[0])/(Point_t[2]-Point_t_1[2])
    vy=(Point_t[1]-Point_t_1[1])/(Point_t[2]-Point_t_1[2])
    return vx,vy
def ComputeTheta(P1X,P1Y,P2X,P2Y):
      dx=P2X-P1X
      dy=P2Y-P1Y
      import numpy
      import math
      if dx*dx+dy*dy>0:
        if dy>0:
            return math.acos(dx/np.sqrt(dx*dx+dy*dy))*180.0/math.pi
        else:
            return 360-math.acos(dx/np.sqrt(dx*dx+dy*dy))*180.0/math.pi
      
      return np.nan



def InterpolationIndexOfMatrix(X0,Y0,X1,Y1,GridSize,MaxSpeed):

    dx=X1-X0
    dy=Y1-Y0
    
    #print("Device",Device_info)

    if dx>MaxSpeed:
        #print("dx",dx)
        dx=MaxSpeed
    elif dx<-MaxSpeed:
        #print("dx",dx)
        dx=-MaxSpeed

    if dy>MaxSpeed:
        #print("dy",dy)
        dy=MaxSpeed
    elif dy<-MaxSpeed:
        #print("dy",dy)
        dy=-MaxSpeed

    IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
    IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

    return IndexX,IndexY
    
def InterpolationIndexOfMatrix_Speed(X0,Y0,T0,X1,Y1,T1,GridSize,MaxSpeed):

    dt=T1-T0
    if dt==0:
        dx=0
        dy=0
    else:
        dx=(X1-X0)/dt
        dy=(Y1-Y0)/dt
    
    #print("Device",Device_info)

    if dx>MaxSpeed:
        #print("dx",dx)
        dx=MaxSpeed
    elif dx<-MaxSpeed:
        #print("dx",dx)
        dx=-MaxSpeed

    if dy>MaxSpeed:
        #print("dy",dy)
        dy=MaxSpeed
    elif dy<-MaxSpeed:
        #print("dy",dy)
        dy=-MaxSpeed

    IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
    IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

    return IndexX,IndexY
def FindIndexOfMatrix_BasedPreviousPoint_FixedResponseTime(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime):
    import numpy as np
    

    #######2

    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=BaseTime


    X0=Point['previousLocation'][0]
    Y0=Point['previousLocation'][1]
    #X0=Point_0['location'][0]
    #Y0=Point_0['location'][1]

    dt=T-T0
    dx=X-X0
    dy=Y-Y0
    
    #print("Device",Device_info)

    if dx>MaxSpeed:
        #print("dx",dx)
        dx=MaxSpeed
    elif dx<-MaxSpeed:
        #print("dx",dx)
        dx=-MaxSpeed

    if dy>MaxSpeed:
        #print("dy",dy)
        dy=MaxSpeed
    elif dy<-MaxSpeed:
        #print("dy",dy)
        dy=-MaxSpeed

    IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
    IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((100/2))))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((100/2))))


    if TimeGrid==0:
        print("Grid Error")
    IndexT=int(np.floor(dt/TimeGrid))
    
    

    #print(IndexX,IndexY,IndexT,dx,dy)

    return IndexX,IndexY,IndexT 
def FindIndexOfMatrix_BasedPreviousPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,PreviousEventTime):
    import numpy as np

    #######2

    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=PreviousEventTime


    X0=Point['previousLocation'][0]
    Y0=Point['previousLocation'][1]
    # X0=Point_0['location'][0]
    # Y0=Point_0['location'][1]

    dt=T-T0
    dx=X-X0
    dy=Y-Y0
    
    #print("Device",Device_info)

    if dx>MaxSpeed:
        #print("dx",dx)
        dx=MaxSpeed
    elif dx<-MaxSpeed:
        #print("dx",dx)
        dx=-MaxSpeed

    if dy>MaxSpeed:
        #print("dy",dy)
        dy=MaxSpeed
    elif dy<-MaxSpeed:
        #print("dy",dy)
        dy=-MaxSpeed

    IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
    IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((100/2))))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((100/2))))


    # if abs(IndexX)>210:
    #     print("dx",dx)
    # if abs(IndexY)>110:
    #     print("dy",dy)

    if TimeGrid==0:
        print("Grid Error")
    #IndexT=int(np.ceil(dt/TimeGrid))
    IndexT=int(np.floor(dt/TimeGrid))
    
    

    #print(IndexX,IndexY,IndexT,dx,dy)

    return IndexX,IndexY,IndexT 


def FindIndexOfMatrix_BasedFirstPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,PreviousEventTime):
    import numpy as np
 
    #######2

    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=PreviousEventTime


    #X0=Point['previousLocation'][0]
    #Y0=Point['previousLocation'][1]
    X0=Point_0['location'][0]
    Y0=Point_0['location'][1]

    dt=T-T0
    dx=X-X0
    dy=Y-Y0
    
    #print("Device",Device_info)

    if dx>MaxSpeed:
        #print("dx",dx)
        dx=MaxSpeed
    elif dx<-MaxSpeed:
        #print("dx",dx)
        dx=-MaxSpeed

    if dy>MaxSpeed:
        #print("dy",dy)
        dy=MaxSpeed
    elif dy<-MaxSpeed:
        #print("dy",dy)
        dy=-MaxSpeed

    IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
    IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((100/2))))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((100/2))))




    if TimeGrid==0:
        print("Grid Error")
    IndexT=int(np.floor(dt/TimeGrid))
    
    

    #print(IndexX,IndexY,IndexT,dx,dy)

    return IndexX,IndexY,IndexT 

def FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed):
    import numpy as np

    #######2

    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=Point_0['timestamp']


    X0=Point['previousLocation'][0]
    Y0=Point['previousLocation'][1]
    # X0=Point_0['location'][0]
    # Y0=Point_0['location'][1]

    dt=T-T0
    dx=X-X0
    dy=Y-Y0
    
    #print("Device",Device_info)

    if dx>MaxSpeed:
        #print("dx",dx)
        dx=MaxSpeed
    elif dx<-MaxSpeed:
        #print("dx",dx)
        dx=-MaxSpeed

    if dy>MaxSpeed:
        #print("dy",dy)
        dy=MaxSpeed
    elif dy<-MaxSpeed:
        #print("dy",dy)
        dy=-MaxSpeed

    IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
    IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((100/2))))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((100/2))))


    # if abs(IndexX)>210:
    #     print("dx",dx)
    # if abs(IndexY)>110:
    #     print("dy",dy)

    if TimeGrid==0:
        print("Grid Error")
    IndexT=int(np.ceil(dt/TimeGrid))
    
    

    #print(IndexX,IndexY,IndexT,dx,dy)

    return IndexX,IndexY,IndexT 


def JsonToCube_NoInterpolation_FixedResponseTime(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid):
    import numpy as np
    # GridNum_InX=int(np.ceil(Device_info[0]/GridSize))+10
    # GridNum_InY=int(np.ceil(Device_info[1]/GridSize))+10
  
    GridNum_InX=int(np.ceil(2*MaxSpeed/GridSize))+1
    GridNum_InY=int(np.ceil(2*MaxSpeed/GridSize))+1
    Channel=1
    #print("ArraySize",GridNum_InX,GridNum_InY,TimeFrameNum,Channel)
    TimeGrid=tGrid
    AllDataX=list()
    AllDataY=list()
    Task=0
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        #print("------",task,"------")
        if task=='tapTask':
            Task=0
        else:
            Task=1

        for iTrial in range(len(JsonData[task]['trials'])):
            JsonData[task]['trials'][iTrial]=LabelTrialEvent(JsonData[task]['trials'][iTrial])
            DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
            BaseTime=JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']

            for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

                    Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                    Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                    if (BaseTime<=Point['timestamp']) & (BaseTime+TimeGrid*TimeFrameNum >=Point['timestamp']):

                        Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint_FixedResponseTime(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                        #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                        
                        if Time_In<TimeFrameNum:
                            #Time_In=TimeFrameNum-1
                            DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                            # if Point['phase']=='ended':
                            #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

            AllDataX.append(DataMatrix)
            AllDataY.append(Task)
        #Task=Task+1
        

    return np.array(AllDataX),np.array(AllDataY)


def JsonToCube_NoInterpolation(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid):
    import numpy as np
    # GridNum_InX=int(np.ceil(Device_info[0]/GridSize))+10
    # GridNum_InY=int(np.ceil(Device_info[1]/GridSize))+10

    RecordTrial=list()
    RecodrdIndex=0


    GridNum_InX=int(np.ceil(2*MaxSpeed/GridSize))+1
    GridNum_InY=int(np.ceil(2*MaxSpeed/GridSize))+1
    Channel=1
    #print("ArraySize",GridNum_InX,GridNum_InY,TimeFrameNum,Channel)
    TimeGrid=tGrid
    AllDataX=list()
    AllDataY=list()
    Task=0
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        #print("------",task,"------")
        if task=='tapTask':
            Task=0;
        else:
            Task=1;

        #Mode1


        #Mode2
        for iTrial in range(len(JsonData[task]['trials'])):
            AllEventTime=list()
            
            for panevent_t in range(len(JsonData[task]['trials'][iTrial]['panEvents'])):
               
                if JsonData[task]['trials'][iTrial]['panEvents'][panevent_t]['state']!='changed':
                    AllEventTime.append(float(JsonData[task]['trials'][iTrial]['panEvents'][panevent_t]['timestamp']))

                

            for tapevent_t in range(len(JsonData[task]['trials'][iTrial]['tapEvents'])):
                AllEventTime.append(float(JsonData[task]['trials'][iTrial]['tapEvents'][tapevent_t]['timestamp']))


            SortedAllTouchEventTime=sorted(AllEventTime)

            #JsonData[task]['trials'][iTrial]=LabelTrialEvent(JsonData[task]['trials'][iTrial])
            for eventT in SortedAllTouchEventTime:
                RecodrdIndex=RecodrdIndex+1
                DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))


                BaseTime=eventT-TimeGrid*TimeFrameNum
                for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                    for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

                        Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                        #Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]
                        Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                        if (BaseTime<=Point['timestamp']) & (eventT>=Point['timestamp']):

                            Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                            
                            #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedFirstPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                            
                            if Time_In<TimeFrameNum:
                                #Time_In=TimeFrameNum-1
                                DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                                # if Point['phase']=='ended':
                                #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

                AllDataX.append(DataMatrix)
                AllDataY.append(Task)
            RecordTrial.append(RecodrdIndex)
        #Task=Task+1


    return np.array(AllDataX),np.array(AllDataY),RecordTrial


def JsonToCube_NoInterpolation_Simulator(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid):
    import numpy as np
    # GridNum_InX=int(np.ceil(Device_info[0]/GridSize))+10
    # GridNum_InY=int(np.ceil(Device_info[1]/GridSize))+10

    RecordTrial=list()
    RecodrdIndex=0


    GridNum_InX=int(np.ceil(2*MaxSpeed/GridSize))+1
    GridNum_InY=int(np.ceil(2*MaxSpeed/GridSize))+1
    Channel=1
    #print("ArraySize",GridNum_InX,GridNum_InY,TimeFrameNum,Channel)
    TimeGrid=tGrid
    AllDataX=list()
    AllDataY=list()
    Task=0
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        #print("------",task,"------")
        if task=='tapTask':
            Task=0;
        else:
            Task=1;

        #Mode1

        #Mode2
        for iTrial in range(len(JsonData[task]['trials'])):
            # 

            # for tapevent_t in range(len(JsonData[task]['trials'][iTrial]['tapEvents'])):
            #     AllEventTime.append(float(JsonData[task]['trials'][iTrial]['tapEvents'][tapevent_t]['timestamp']))


            SimluatorTime=list()
            for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                if iFinger==1:
                    SimluatorTime.append(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp'])
                if len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])>1:
                    SimluatorTime.append(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][3]['timestamp'])

               


            SortedSimluatorTime=sorted(SimluatorTime)
            ProcssTimeList=SortedSimluatorTime

            #SortedAllTouchEventTime=sorted(AllEventTime)
            SortedAllTouchEventTime=ProcssTimeList

            #JsonData[task]['trials'][iTrial]=LabelTrialEvent(JsonData[task]['trials'][iTrial])
            for eventT in SortedAllTouchEventTime:
                RecodrdIndex=RecodrdIndex+1
                DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))

                BaseTime=eventT-TimeGrid*TimeFrameNum
                for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                    for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

                        Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                        #Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]
                        Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                        if (BaseTime<=Point['timestamp']) & (eventT>=Point['timestamp']):
                   
                            Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                            
                            #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedFirstPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                            
                            if Time_In<TimeFrameNum:
                                #Time_In=TimeFrameNum-1
                                DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                                # if Point['phase']=='ended':
                                #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

                AllDataX.append(DataMatrix)
                AllDataY.append(Task)
            RecordTrial.append(RecodrdIndex)
        #Task=Task+1


    return np.array(AllDataX),np.array(AllDataY),RecordTrial



def ComputeTimeGrid(JsonData,TimeFrameNum):
    ##TouchEndedTime
    import numpy as np
    TouchEndedTime=list()
    for iFinger in range(len(JsonData)):
        for iPoint in range(len(JsonData[iFinger]["rawTouches"])):
            if JsonData[iFinger]["rawTouches"][iPoint]['phase']=='ended':
                TouchEndedTime.append(JsonData[iFinger]["rawTouches"][iPoint]['timestamp'])
    if len(TouchEndedTime)==0:
        for iFinger in range(len(JsonData)):
            for iPoint in range(len(JsonData[iFinger]["rawTouches"])):
    
                TouchEndedTime.append(JsonData[iFinger]["rawTouches"][len(JsonData[iFinger]["rawTouches"])-1]['timestamp'])
    DataTimeNum=np.min(TouchEndedTime)-JsonData[0]["rawTouches"][0]['timestamp']
    if DataTimeNum==0:
        DataTimeNum=np.max(TouchEndedTime)-JsonData[0]["rawTouches"][0]['timestamp']
    if DataTimeNum==0:
        return -1
    return DataTimeNum/9




# Translate data to color
def array_to_color(array, cmap="Oranges"):
    s_m = plt.cm.ScalarMappable(cmap=cmap)
    return s_m.to_rgba(array)[:,:-1]



def Visualize(Data):
    import matplotlib.pyplot as plt
    
    
    for t in range(len(Data[0][0])):
        X=list()
        Y=list()
        for indexx in range(len(Data)):
            for indexy in range(len(Data[0])):
                if Data[indexx][indexy][t]>0:
                    X.append(indexx)
                    Y.append(indexy)
        plt.subplot(len(Data[0][0])/5,5,t+1)
        plt.scatter(X,Y)
        plt.xlim(0,len(Data))
        plt.ylim(0,len(Data[0]))
            #plt.legend(loc='upper right')
    plt.show()
    
   
def Visualize2(Data,Y):
    import matplotlib.pyplot as plt
    
    # if Y==0:
    #     task='Tap'
    # elif Y==1:
    #     task='swipe'
    # elif Y==2:
    #     task='horizontalScroll'
    # elif Y==3:
    #     task='verticalScroll'
    if Y==0:
        task='Tap'
    elif Y==1:
        task='Pan'
    for t in range(len(Data[0][0])):
        X=list()
        Y=list()
        for indexx in range(len(Data)):
            for indexy in range(len(Data[0])):
                if Data[indexx][indexy][t][0]>0:
                    X.append(indexx)
                    Y.append(indexy)
        plt.subplot(len(Data[0][0])/5,5,t+1)
        plt.scatter(X,Y)
        plt.xlim(0,len(Data))
        plt.ylim(0,len(Data[0]))
        plt.title(task)
            #plt.legend(loc='upper right')
    plt.show()


#### Model

# Conv2D layer
def Conv(filters=16, kernel_size=(3,3,3), activation='relu', input_shape=None):
    if input_shape:
        return Conv3D(filters=filters, kernel_size=kernel_size, padding='Same', activation=activation, input_shape=input_shape)
    else:
        return Conv3D(filters=filters, kernel_size=kernel_size, padding='Same', activation=activation)

# Define Model
def CNN(input_dim, num_classes):
    model = Sequential()

    model.add(Conv(8, (3,3,3), input_shape=input_dim))
    model.add(Conv(16, (3,3,3)))
    # model.add(BatchNormalization())
    model.add(MaxPool3D())
    # model.add(Dropout(0.25))

    model.add(Conv(32, (3,3,3)))
    model.add(Conv(64, (3,3,3)))
    model.add(BatchNormalization())
    model.add(MaxPool3D())
    model.add(Dropout(0.25))

    model.add(Flatten())

    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_classes, activation='softmax'))

    return model
def One_hot_Decode(OneHot):
    #print(OneHot)
    for i in range(len(OneHot)):
        if OneHot[i]==1:
            return i

def ThreeDCNN(input_dim, num_classes):
    model = Sequential()
    model.add(Conv(16, (3,3,3), input_shape=input_dim))
    model.add(MaxPool3D())
    model.add(Conv(32, (3,3,3), input_shape=input_dim))
    model.add(MaxPool3D())
    model.add(Conv(64, (3,3,3), input_shape=input_dim))
    model.add(MaxPool3D())
    model.add(Dropout(0.25))
    model.add(Flatten())
    #model.add(Dense(128, init='normal', activation='relu'))
    model.add(Dense(64, activation="relu", kernel_initializer="normal"))
    model.add(Dropout(0.25))
    model.add(Dense(num_classes, activation='softmax'))
    # model.add(BatchNormalization())
    

    return model

# Train Model
def train(optimizer, scheduler):
    global model

    print("Training...")
    model.compile(optimizer = 'adam' , loss = "categorical_crossentropy", metrics=["accuracy"])

    model.fit(x=X_train, y=y_train, batch_size=batch_size, epochs=epochs, validation_split=0.15,
                    verbose=2, callbacks=[scheduler, tensorboard])

def evaluate(ValidIndex,AllTaskValidIndex,DefaultSuccessRate,RecordTrial,tGrid):
    global model

    pred = model.predict(X_test)
    pred = np.argmax(pred, axis=1)
    #print(pred)

    DetailString=""
    start=True
    TrialLabel=0
    TapTrial=0
    TapSuccess=0
    PanTrial=0
    PanSuccess=0
    
    for i in range(len(pred)):
        if start==True:
            TrialLabel=One_hot_Decode(y_test[i])
            TrialPredict=list()
        TrialPredict.append(pred[i])
        DetailString+=" "+str(pred[i]) +" / "+str(One_hot_Decode(y_test[i]))
        if i in RecordTrial:
            start=True
            DetailString+=" $$ "
            if TrialLabel==0:
                TapTrial=TapTrial+1
                if 0 in TrialPredict:
                    if 1 not in TrialPredict:
                        TapSuccess=TapSuccess+1
            if TrialLabel==1:
                PanTrial=PanTrial+1
                if 1 in TrialPredict:
                    if 0 not in TrialPredict:
                        PanSuccess=PanSuccess+1




    ValidData=""
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        ValidData+=" "+str(task)
        for i in range(len(AllTaskValidIndex[task])):
            ValidData+=" "+str(AllTaskValidIndex[task][i])
    dataString=str(User)+" "+str(ValidIndex)+" Accuracy: "+str(accuracy_score(to_categorical(pred, num_classes=2),y_test))+" Grid "+str(tGrid)+" Detail: "+DetailString+" ValidData: "+ValidData
    print("Default:",DefaultSuccessRate)
    print(dataString)
    print("==================")
    print("Tap: ", TapSuccess," ",TapTrial," Pan ",PanSuccess," ",PanTrial)
    print("===== evaluate End =====")



def evaluate_TapOptimizer(ValidIndex,AllTaskValidIndex,DefaultSuccessRate,Validation_Data_2,FactorEventCountDict_Tap,FactorEventCountDict_Pan):
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

        FingerCenterDict=dict()

        PossibleX=list()
        PossibleY=list()

        for iFinger in range(len(OutputData["rawTouchTracks"])):
            
            CandidateData=list()
            for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                 
                 if iPoint==0 or iPoint==1:
                     accelerate=0
                 else:


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
                         LabelFalse(OutputData,iFinger,iPoint-2)
                     
                     if (AverageX2-positionX3)*(AverageX2-positionX3)+(AverageY2-positionY3)*(AverageY2-positionY3)>TapAllowableMovement*TapAllowableMovement:
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
                    LabelFalse(OutputData,iFinger,ThisClusterFinalPoint[i][0])
                    if distance<=Distance:
                        Distance=distance
                        SelectedPoint=ThisClusterFinalPoint[i][0]
                OutputData["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['label']=True
                
                FingerCenterDict[str(iFinger)]=[Xave,Yave]
                PossibleX.append(Xave)
                PossibleY.append(Yave)
            FingerCenterDict[str(iFinger)]=[positionx,positiony]  
            PossibleX.append(positionx)
            PossibleY.append(positiony)

        
        DataPointNum=0
        for iFinger in range(len(OutputData["rawTouchTracks"])):
            for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                 if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    DataPointNum=DataPointNum+1

        return OutputData,[np.mean(PossibleX),np.mean(PossibleY)]



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
    

    def FindImproveFactor(TrialTask,pred,y):
        if y==0: #Tap Task
            DefaultSystemError=False
            if len(TrialTask['panEvents'])>0:
                DefaultSystemError=True
            if len(TrialTask['tapEvents'])==0:
                DefaultSystemError=True
            if DefaultSystemError==True:
                if pred==0:
                    eventstring=TrialTask['myEvent']
                    print(eventstring)
                    return eventstring,1,0

        if y==1:
            DefaultSystemError=False
            if len(TrialTask['panEvents'])==0:
                DefaultSystemError=True
            if len(TrialTask['tapEvents'])>0:
                DefaultSystemError=True
            if DefaultSystemError==True:
                if pimproveFactorred==1:
                    eventstring=TrialTask['myEvent']
                    print(eventstring)
                    return eventstring,0,1

        return 'NoAction',0,0




    import TaskSuccessVerify as tv
    



    global model

    pred = model.predict(X_test)
    pred = np.argmax(pred, axis=1)
    #print(pred)

    DetailString=""

    taptempindex=list()
    for i in range(len(pred)):
        DetailString+=" "+str(pred[i]) +" / "+str(One_hot_Decode(y_test[i]))


        if One_hot_Decode(y_test[i])==0:
            if One_hot_Decode(y_test[i])==pred[i]:
                taptempindex.append(i)

    ValidData=""

    OptimzerSuccess=0
    DefaultSuccess=0
    RecognizedTapTrials=0
    

    factorTrialCount=0
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        ValidData+=" "+str(task)
        for i in range(len(AllTaskValidIndex[task])):
            FactorEventCountDict_Tap['TrialNum']=FactorEventCountDict_Tap['TrialNum']+1
            FactorEventCountDict_Pan['TrialNum']=FactorEventCountDict_Pan['TrialNum']+1
            #Validation_Data_2[task]['trials'][i]
            ImprovedTrial_EventString,TapImprove,PanImprove=FindImproveFactor(Validation_Data_2[task]['trials'][i],pred[factorTrialCount],One_hot_Decode(y_test[factorTrialCount]))
            if ImprovedTrial_EventString!='NoAction':
                if TapImprove==1:   #是Tap improve
                    FactorEventCountDict_Tap[ImprovedTrial_EventString]=FactorEventCountDict_Tap[ImprovedTrial_EventString]+1
                if PanImprove==1:
                    FactorEventCountDict_Pan[ImprovedTrial_EventString]=FactorEventCountDict_Pan[ImprovedTrial_EventString]+1

            factorTrialCount=factorTrialCount+1

            ValidData+=" "+str(AllTaskValidIndex[task][i])
            if i in taptempindex:   ##代表是正確的
                if task =='tapTask':   #再確認
                    RecognizedTapTrials=RecognizedTapTrials+1
                    TrialToOptimzer=AllTaskValidIndex[task][i]
                    #print(AllTaskValidIndex[task],TrialToOptimzer,len(Validation_Data_2[task]['trials']))
                    TaskData=Validation_Data_2[task]['trials'][i]

                    OptimizedData=LabelTrue(TaskData)
                    OptimizedData,OutPutPoint=LabelByMyAlgorithm(OptimizedData)
                    
                    FilteredOptimizedData=FilteredJsonOneTrial(OptimizedData)

            

                    if tv.TapTask_SuccessVerify(FilteredOptimizedData):
                        OptimzerSuccess=OptimzerSuccess+1


                    defaultfalse=0
                    for tapindex in range(len(TaskData['tapEvents'])):
                        #print(TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex'])
                        #Y=TaskData['tapEvents'][tapindex]['location'][0]
                        #X=Device_info[0]-TaskData['tapEvents'][tapindex]['location'][1]

                        X=TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][0]
                        Y=TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][1]
                        print(X,Y," vs ",TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][0],TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][1])
                        
                        if (abs(X - TaskData["targetFrame"][0][0] -TaskData["targetFrame"][1][0]*0.5) > TaskData["targetFrame"][1][0]*0.5)|(abs(Y- TaskData["targetFrame"][0][1] - TaskData["targetFrame"][1][1]*0.5) >TaskData["targetFrame"][1][1]*0.5):
                                # cout << "First touch point is not correct" << endl;
                        
                        #print((NewTaskData["targetFrame"][0][0]),(NewTaskData["targetFrame"][0][1]),(NewTaskData["targetFrame"][1][0]),(NewTaskData["targetFrame"][1][1]),NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0],NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] )
                            #print("First Touch")
                            defaultfalse=1
                    if defaultfalse==0:
                        DefaultSuccess=DefaultSuccess+1

                  # Y=TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][1]

    if RecognizedTapTrials!=0:
        dataString=str(User)+" "+str(ValidIndex)+" Accuracy: "+str(accuracy_score(to_categorical(pred, num_classes=2),y_test))+" Grid "+str(tGrid)+" Detail: "+DetailString+" ValidData: "+ValidData +" TapOptimizerResults " + str(DefaultSuccess/RecognizedTapTrials)+ " " +str(DefaultSuccess)+ " / "+str(RecognizedTapTrials) +" vs " +str(OptimzerSuccess/RecognizedTapTrials)+" "+str(OptimzerSuccess)+ " / "+str(RecognizedTapTrials) 
    else:
        dataString=str(User)+" "+str(ValidIndex)+" Accuracy: "+str(accuracy_score(to_categorical(pred, num_classes=2),y_test))+" Grid "+str(tGrid)+" Detail: "+DetailString+" ValidData: "+ValidData 
    print("Default:",DefaultSuccessRate)
    print(dataString)



    if RecognizedTapTrials!=0:
        return DefaultSuccess/RecognizedTapTrials,OptimzerSuccess/RecognizedTapTrials,accuracy_score(to_categorical(pred, num_classes=2),y_test)
    else:
        return 1234567,1234567,accuracy_score(to_categorical(pred, num_classes=2),y_test)

def save_model(User,CrossValidationIndex,tGrid,mode):

    global model

    model_json = model.to_json()
    if mode=='Dynamic':
        with open('TrainedModel/Final/Dynamic/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.json', 'w') as f:
            f.write(model_json)

        model.save_weights('TrainedModel/Final/Dynamic/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.h5')

        print('Model Saved.')
    elif mode=='Fixed':
        with open('TrainedModel/Final/Fixed/'+str(User)+'/model_3DCNN_Fixed_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.json', 'w') as f:
            f.write(model_json)

        model.save_weights('TrainedModel/Final/Fixed/'+str(User)+'/model_3DCNN_Fixed_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.h5')

        print('Model Saved.')


    elif mode=='Dynamic_Simulator':
        with open('TrainedModel/Final/Dynamic_Simulator/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.json', 'w') as f:
            f.write(model_json)

        model.save_weights('TrainedModel/Final/Dynamic_Simulator/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.h5')

        print('Model Saved.')



def RecognitionTimeProcess_Interpolation(JsonData,RecognitionTime,mode):
    import math
    def sigmoid(x):
        return 1/(1+math.exp(-x))
    AllData=dict()
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        TrialDataDict=dict()
        TrialDataList=list()
        for iTrial in range(len(JsonData[task]['trials'])): 
            #JsonData[task]['trials'][iTrial]=LabelTrialEvent(JsonData[task]['trials'][iTrial])
            #print("Test2========:",JsonData[task]['trials'][iTrial]['myEvent'])
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
                        ##interpolation
                        if mode==0:
                            if iPoint<len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])-1:
                                if timestamp-MinTimeStamp<RecognitionTime:
                                    nexttimestamp=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint+1]["timestamp"]
                                    if nexttimestamp-timestamp>0.001:
                                        InterpolateNum=int((nexttimestamp-timestamp)/0.001)

                                        StartPoint=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                                        EndPoint=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint+1]
                                        for Interpolateindex in range(InterpolateNum):
                                            ratio=(Interpolateindex+1)/(InterpolateNum+1)
                                            InterpolatePointDict=dict()
                                            Interpolate_timestamp=StartPoint["timestamp"]*(1-ratio)+EndPoint["timestamp"]*ratio
                                            Interpolate_previousLocationX=StartPoint["previousLocation"][0]*(1-ratio)+EndPoint["previousLocation"][0]*ratio
                                            Interpolate_previousLocationY=StartPoint["previousLocation"][1]*(1-ratio)+EndPoint["previousLocation"][1]*ratio
                                            Interpolate_locationX=StartPoint["location"][0]*(1-ratio)+EndPoint["location"][0]*ratio
                                            Interpolate_locationY=StartPoint["location"][1]*(1-ratio)+EndPoint["location"][1]*ratio


                                            InterpolatePointDict["timestamp"]=Interpolate_timestamp
                                            InterpolatePointDict["previousLocation"]=[Interpolate_previousLocationX,Interpolate_previousLocationY]
                                            InterpolatePointDict["location"]=[Interpolate_locationX,Interpolate_locationY]
                                            InterpolatePointDict['phase']='moved'
                                            PointDataList.append(InterpolatePointDict)
                        elif mode==1:
                            if iPoint<len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])-1:
                                if timestamp-MinTimeStamp<RecognitionTime:
                                    nexttimestamp=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint+1]["timestamp"]
                                    if nexttimestamp-timestamp>0.0001:
                                        InterpolateNum=int((nexttimestamp-timestamp)/0.0001)

                                        StartPoint=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                                        EndPoint=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint+1]
                                        for Interpolateindex in range(InterpolateNum):
                                            ratio=(Interpolateindex+0)/(InterpolateNum+1)
                                            ratio2=(Interpolateindex+2)/(InterpolateNum+1)

                                            interpolationpoint1_Interpolate_timestamp=StartPoint["timestamp"]*(1-ratio)+EndPoint["timestamp"]*ratio
                                            interpolationpoint1_previousLocationX=StartPoint["previousLocation"][0]*(1-ratio)+EndPoint["previousLocation"][0]*ratio
                                            interpolationpoint1_previousLocationY=StartPoint["previousLocation"][1]*(1-ratio)+EndPoint["previousLocation"][1]*ratio
                                            interpolationpoint1_locationX=StartPoint["location"][0]*(1-ratio)+EndPoint["location"][0]*ratio
                                            interpolationpoint1_locationY=StartPoint["location"][1]*(1-ratio)+EndPoint["location"][1]*ratio

                                            interpolationpoint2_Interpolate_timestamp=StartPoint["timestamp"]*(1-ratio2)+EndPoint["timestamp"]*ratio2
                                            interpolationpoint2_previousLocationX=StartPoint["previousLocation"][0]*(1-ratio2)+EndPoint["previousLocation"][0]*ratio2
                                            interpolationpoint2_previousLocationY=StartPoint["previousLocation"][1]*(1-ratio2)+EndPoint["previousLocation"][1]*ratio2
                                            interpolationpoint2_locationX=StartPoint["location"][0]*(1-ratio2)+EndPoint["location"][0]*ratio2
                                            interpolationpoint2_locationY=StartPoint["location"][1]*(1-ratio2)+EndPoint["location"][1]*ratio2

                                            interpolationRatio=sigmoid(np.random.normal(0,1,1))

                                            InterpolatePointDict=dict()
                                            Interpolate_timestamp=interpolationpoint1_Interpolate_timestamp+interpolationRatio*(interpolationpoint2_Interpolate_timestamp-interpolationpoint1_Interpolate_timestamp)
                                            Interpolate_previousLocationX=interpolationpoint1_previousLocationX+interpolationRatio*(interpolationpoint2_previousLocationX-interpolationpoint1_previousLocationX)
                                            Interpolate_previousLocationY=interpolationpoint1_previousLocationY+interpolationRatio*(interpolationpoint2_previousLocationY-interpolationpoint1_previousLocationY)
                                            Interpolate_locationX=interpolationpoint1_locationX+interpolationRatio*(interpolationpoint2_locationX-interpolationpoint1_locationX)
                                            Interpolate_locationY=interpolationpoint1_locationY+interpolationRatio*(interpolationpoint2_locationY-interpolationpoint1_locationY)


                                            InterpolatePointDict["timestamp"]=Interpolate_timestamp
                                            InterpolatePointDict["previousLocation"]=[Interpolate_previousLocationX,Interpolate_previousLocationY]
                                            InterpolatePointDict["location"]=[Interpolate_locationX,Interpolate_locationY]
                                            InterpolatePointDict['phase']='moved'
                                            PointDataList.append(InterpolatePointDict)





                    PointDataDict['rawTouches']=PointDataList
                    #PointDataDict={'rawTouches':PointDataList}
                    FingerDataList.append(PointDataDict)

                
                FingerDataDict['rawTouchTracks']=FingerDataList
                FingerDataDict['tapEvents']=JsonData[task]['trials'][iTrial]['tapEvents']
                FingerDataDict['swipeEvents']=JsonData[task]['trials'][iTrial]['swipeEvents']
                FingerDataDict['panEvents']=JsonData[task]['trials'][iTrial]['panEvents']
                FingerDataDict['rotationEvents']=JsonData[task]['trials'][iTrial]['rotationEvents']
                FingerDataDict['pinchEvents']=JsonData[task]['trials'][iTrial]['pinchEvents']
                FingerDataDict['longPressEvents']=JsonData[task]['trials'][iTrial]['longPressEvents']
                #FingerDataDict['myEvent']=JsonData[task]['trials'][iTrial]['myEvent']
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

def RecognitionTimeProcess_NoInterpolation(JsonData,RecognitionTime):

    AllData=dict()
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        TrialDataDict=dict()
        TrialDataList=list()
        for iTrial in range(len(JsonData[task]['trials'])): 
            #JsonData[task]['trials'][iTrial]=LabelTrialEvent(JsonData[task]['trials'][iTrial])
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
                FingerDataDict['rotationEvents']=JsonData[task]['trials'][iTrial]['rotationEvents']
                FingerDataDict['pinchEvents']=JsonData[task]['trials'][iTrial]['pinchEvents']
                FingerDataDict['longPressEvents']=JsonData[task]['trials'][iTrial]['longPressEvents']
                #FingerDataDict['myEvent']=JsonData[task]['trials'][iTrial]['myEvent']


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



def LabelTrialEvent(GraphData):
    def OtherEventFuc(Data):
        OtherEvent=0
        if len(Data['rotationEvents'])>0:
            OtherEvent=1
        if len(Data['pinchEvents'])>0:
            OtherEvent=1
        if len(Data['longPressEvents'])>0:
            OtherEvent=1
        return OtherEvent
    labels=['Only Tap ,No Other Event','OtherEvents With Tap','Only Scroll ,No Other Event','OtherEvents With Scroll','Tap Scroll ,No Other Event','OtherEvents With Scroll and Tap','Only OtherEvents','NoEvent']
    OnlyTap_Count=0
    
    TapScroll_Count=0
    OnlyScroll_Count=0

    
    NoEvent_Count=0
    OtherEventCount_Tap=0
    OtherEventCount_Scroll=0
    OtherEventCount_Tap_Scroll=0

    OnlyOtherEvent=0

    OtherEvent=OtherEventFuc(GraphData)
    if len(GraphData['tapEvents'])>0:
        if len(GraphData['panEvents'])==0:
            if OtherEvent==0:
                OnlyTap_Count=OnlyTap_Count+1
                EventString='Tap'
                #print('OnlyTap_Count')
    
    if len(GraphData['tapEvents'])>0:
        if len(GraphData['panEvents'])>0:
            if OtherEvent==0:
                TapScroll_Count=TapScroll_Count+1
                EventString='TapPan'
                #print('TapScroll_Count')


    if len(GraphData['tapEvents'])==0:
        if len(GraphData['panEvents'])>0:
            if OtherEvent==0:
                NumberOfPanBegan=0
                for i in range(len(GraphData['panEvents'])):
                    if GraphData['panEvents'][i]['state']=='began':
                        NumberOfPanBegan=NumberOfPanBegan+1
                OnlyScroll_Count=OnlyScroll_Count+1
                EventString='Pan'
                #print('OnlyScroll_Count')
               
    if len(GraphData['tapEvents'])==0:
        if len(GraphData['panEvents'])==0: 
            if OtherEvent>0:
                OnlyOtherEvent=OnlyOtherEvent+1
                EventString='Others'
                #print('OnlyOtherEvent')

    if len(GraphData['tapEvents'])==1:
        if len(GraphData['panEvents'])==0:
            if OtherEvent>0:
                OtherEventCount_Tap=OtherEventCount_Tap+1
                EventString='TapOthers'
                #print('OtherEventCount_Tap')
    if len(GraphData['tapEvents'])==2:
        if len(GraphData['panEvents'])==0:
            if OtherEvent>0:
                OtherEventCount_Tap=OtherEventCount_Tap+1
                EventString='TapOthers'
                #print('OtherEventCount_Tap')
    if len(GraphData['tapEvents'])>=3:
        if len(GraphData['panEvents'])==0:
            if OtherEvent>0:
                OtherEventCount_Tap=OtherEventCount_Tap+1
                EventString='TapOthers'
                #print(' OtherEventCount_Tap')
    if len(GraphData['tapEvents'])>0:
        if len(GraphData['panEvents'])>0:
            if OtherEvent>0:
                OtherEventCount_Tap_Scroll=OtherEventCount_Tap_Scroll+1
                EventString='TapPanOthers'
                #print('OtherEventCount_Tap_Scroll')
    if len(GraphData['tapEvents'])==0:
        if len(GraphData['panEvents'])>0:
            if OtherEvent>0:
                NumberOfPanBegan=0
                for i in range(len(GraphData['panEvents'])):
                    if GraphData['panEvents'][i]['state']=='began':
                        NumberOfPanBegan=NumberOfPanBegan+1
                if NumberOfPanBegan==1:

                    OtherEventCount_Scroll=OtherEventCount_Scroll+1
                elif NumberOfPanBegan>1:
                    OtherEventCount_Scroll=OtherEventCount_Scroll+1
                EventString='PanOthers'
                #print('OtherEventCount_Scroll')

    if len(GraphData['tapEvents'])==0:
        if len(GraphData['panEvents'])==0:
            if OtherEvent==0:
                NoEvent_Count=NoEvent_Count+1
                EventString='NoEvent'

    GraphData['myEvent']=EventString
    return GraphData



def evaluate_BasediOS(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,Validation_Data_2):
    

    #每個event 預測都用固定的 time-grid
    def VerifyTap(TaskData):
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

                FingerCenterDict=dict()

                PossibleX=list()
                PossibleY=list()

                for iFinger in range(len(OutputData["rawTouchTracks"])):
                    
                    CandidateData=list()
                    for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                         
                         if iPoint==0 or iPoint==1:
                             accelerate=0
                         else:
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
                                 LabelFalse(OutputData,iFinger,iPoint-2)
                             
                             if (AverageX2-positionX3)*(AverageX2-positionX3)+(AverageY2-positionY3)*(AverageY2-positionY3)>TapAllowableMovement*TapAllowableMovement:
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
                            LabelFalse(OutputData,iFinger,ThisClusterFinalPoint[i][0])
                            if distance<=Distance:
                                Distance=distance
                                SelectedPoint=ThisClusterFinalPoint[i][0]
                        OutputData["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['label']=True
                        
                        FingerCenterDict[str(iFinger)]=[Xave,Yave]
                        PossibleX.append(Xave)
                        PossibleY.append(Yave)
                    FingerCenterDict[str(iFinger)]=[positionx,positiony]  
                    PossibleX.append(positionx)
                    PossibleY.append(positiony)


                DataPointNum=0
                for iFinger in range(len(OutputData["rawTouchTracks"])):
                    for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                         if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                            DataPointNum=DataPointNum+1


                return OutputData,[np.mean(PossibleX),np.mean(PossibleY)]



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
    
        DefaultSuccess=0
       
        OptimzerSuccess=0
        defaultfalse=0
        # RecognizedTapTrials=RecognizedTapTrials
        TrialToOptimzer=AllTaskValidIndex[task][i]
        #print(AllTaskValidIndex[task],TrialToOptimzer,len(Validation_Data_2[task]['trials']))
        #TaskData=Validation_Data_2[task]['trials'][i]

        OptimizedData=LabelTrue(TaskData)
        OptimizedData,OutPutPoint=LabelByMyAlgorithm(OptimizedData)

        FilteredOptimizedData=FilteredJsonOneTrial(OptimizedData)

       

        if tv.TapTask_SuccessVerify(FilteredOptimizedData):

                OptimzerSuccess=1


        
        for tapindex in range(len(TaskData['tapEvents'])):
                #print(TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex'])
                #Y=TaskData['tapEvents'][tapindex]['location'][0]
                #X=Device_info[0]-TaskData['tapEvents'][tapindex]['location'][1]

                X=TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][0]
                Y=TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][1]
                #print(X,Y," vs ",TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][0],TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][1])

                if (abs(X - TaskData["targetFrame"][0][0] -TaskData["targetFrame"][1][0]*0.5) > TaskData["targetFrame"][1][0]*0.5)|(abs(Y- TaskData["targetFrame"][0][1] - TaskData["targetFrame"][1][1]*0.5) >TaskData["targetFrame"][1][1]*0.5):
                        # cout << "First touch point is not correct" << endl;

                #print((NewTaskData["targetFrame"][0][0]),(NewTaskData["targetFrame"][0][1]),(NewTaskData["targetFrame"][1][0]),(NewTaskData["targetFrame"][1][1]),NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0],NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] )
                    #print("First Touch")
                    defaultfalse=1
        if defaultfalse==0:
                DefaultSuccess=1

        return  DefaultSuccess,OptimzerSuccess

    #TapVerify End
    def JsonToCube_NoInterpolation_AllBegan_OnTrial(JsonDataOneTrial,task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,PredictModel):

        def TimeInRange(PreviousEventTime,PresentEventTime,TouchPhaseTime):
            for t in TouchPhaseTime:
                if (t>=PreviousEventTime) & (t<=PresentEventTime):
                    return True
            return False
        def FindIndexOfMatrix_AllBegan(Point,BaseTime,GridSize,TimeGrid,Device_info,MaxSpeed):
            import numpy as np
           

            #######2

            X=Point['location'][0]
            Y=Point['location'][1]
            T=Point['timestamp']

            
            T0=BaseTime


            X0=Point['previousLocation'][0]
            Y0=Point['previousLocation'][1]
            # X0=Point_0['location'][0]
            # Y0=Point_0['location'][1]

            dt=T-T0
            dx=X-X0
            dy=Y-Y0
            
            #print("Device",Device_info)

            if dx>MaxSpeed:
                #print("dx",dx)
                dx=MaxSpeed
            elif dx<-MaxSpeed:
                #print("dx",dx)
                dx=-MaxSpeed

            if dy>MaxSpeed:
                #print("dy",dy)
                dy=MaxSpeed
            elif dy<-MaxSpeed:
                #print("dy",dy)
                dy=-MaxSpeed

            IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
            IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

          

            if TimeGrid==0:
                print("Grid Error")
            IndexT=int(np.ceil(dt/TimeGrid))
            
            

            #print(IndexX,IndexY,IndexT,dx,dy)

            return IndexX,IndexY,IndexT 


        import numpy as np
        # GridNum_InX=int(np.ceil(Device_info[0]/GridSize))+10
        # GridNum_InY=int(np.ceil(Device_info[1]/GridSize))+10
      
        GridNum_InX=int(np.ceil(2*MaxSpeed/GridSize))+1
        GridNum_InY=int(np.ceil(2*MaxSpeed/GridSize))+1
        Channel=1
        #print("ArraySize",GridNum_InX,GridNum_InY,TimeFrameNum,Channel)
        TimeGrid=float(tGrid)
        AllDataX=list()
        AllDataY=list()
        Task=0
        
        if task=='tapTask':
            Task=0;
        else:
            Task=1;

            

        ###find Began
        AllTouchBeganTime=list()
        AllTouchEndTime=list()
        AllEventTime=list()
        for iFinger in range(len(JsonDataOneTrial["rawTouchTracks"])):
            for iPoint in range(len(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"])):
                    if JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='began':
                            AllTouchBeganTime.append(float(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
                    if JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='ended':
                            AllTouchEndTime.append(float(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
        for panevent_t in range(len(JsonDataOneTrial['panEvents'])):
           
            AllEventTime.append(float(JsonDataOneTrial['panEvents'][panevent_t]['timestamp']))

        for tapevent_t in range(len(JsonDataOneTrial['tapEvents'])):
            AllEventTime.append(float(JsonDataOneTrial['tapEvents'][tapevent_t]['timestamp']))


        SortedAllTouchEventTime=sorted(AllEventTime)
        SortedAllTouchBeganTime=sorted(AllTouchBeganTime)
        SortedAllTouchEndTime=sorted(AllTouchEndTime)


       
        ProcssTimeList=SortedAllTouchEventTime
        if len(ProcssTimeList)==0:
            print("No pan No Tap")
            ProcssTimeList=SortedAllTouchEndTime
        
        touchBeganPredict='?????'

        CNNEvent=list()
        for began_T in ProcssTimeList:
                # previousEventTime=sortAllEventTime[event_t＿index-1]
                # presentEventTime=sortAllEventTime[event_t＿index]

                #BaseTime=began_T-TimeFrameNum*tGrid
                BaseTime=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']

                TimeGrid=(began_T-BaseTime)/10


                TouchBeganEvent=False
                for begantime in SortedAllTouchBeganTime:
                    if (BaseTime<=begantime)&(began_T>begantime):
                          TouchBeganEvent=True  

                TouchEndEvent=False
                for endtime in SortedAllTouchEndTime:
                    if (BaseTime<=endtime)&(began_T>endtime):
                          TouchEndEvent=True  

            #print(began_T,began_T in SortedAllTouchEndTime,began_T in SortedAllTouchBeganTime)
            #if TimeInRange(began_T-TimeFrameNum*tGrid,began_T+TimeFrameNum*tGrid,SortedAllTouchEndTime):

                predictX=list()
                predictY=list()
                DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
                
                

                # if BaseTime<JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']:
                #     BaseTime=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']

                for iFinger in range(len(JsonDataOneTrial["rawTouchTracks"])):
                    for iPoint in range(len(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"])):

                        Point_0=JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][0]
                        Point=JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]

                        if (BaseTime<=Point['timestamp']) &  (began_T>=Point['timestamp']):
                        #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                            Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_AllBegan(Point,BaseTime,GridSize,TimeGrid,Device_info,MaxSpeed)
                            
                            if Time_In<TimeFrameNum:
                                #Time_In=TimeFrameNum-1
                                DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                                # if Point['phase']=='ended':
                                #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

            #######Matrix Ready Go Predict
                predictX.append(DataMatrix)
                predictY.append(Task)


                y_test = to_categorical(np.array(predictY), num_classes=2)

                
                X_test  = np.array(predictX).reshape(-1, np.array(predictX).shape[1], np.array(predictX).shape[2], np.array(predictX).shape[3], 1)

                if TouchBeganEvent==True:

                    pred = PredictModel.predict(X_test)
                        #print("pred",pred)
                    prediction = np.argmax(pred, axis=1)[0]
                        #print("pred1",prediction)
                    touchBeganPredict=str(prediction)
                else:
            #print(CNNEvent)
                    if touchBeganPredict=='1':
                        pred = PredictModel.predict(X_test)
                        prediction=AdjustPrediction(pred)
                    else:
                        pred = PredictModel.predict(X_test)
                        #print("pred",pred)
                        prediction = np.argmax(pred, axis=1)[0]
                                #print("pred1",prediction)
                        touchBeganPredict=str(prediction)

                CNNEvent.append(prediction)

        print(task,len(JsonDataOneTrial['tapEvents']),len(JsonDataOneTrial['panEvents'])," vs ",(0 in CNNEvent),(1 in CNNEvent))
        ##每個event 的predict 結束 
        #來驗證tap optimzer
        #print("Predict",len(CNNEvent),len(ProcssTimeList))
        if task=='swipeTask' or task=='horizontalScrollTask' or task=='verticalScrollTask':
                  

            if len(CNNEvent)>0:
                if 1 in CNNEvent:
                    if 0 not in CNNEvent :
                            return True
                    return False
                return False
            return False
                    
        elif task=='tapTask':
            #print("Tap False?",len(np.where(CNNEvent==1)[0]))
            if len(CNNEvent)>0:
                    if 1 not in CNNEvent :
                            if 0 in CNNEvent:
                                    return True
                            return False
                    return False
            return False
    #####


    import numpy as np

    TotalCount=0
    SuccessCount=0
    DefaultSuccessCount=0
    DetailString=""

    TapDefaultSuccess=0
    TapMyTapSuccess=0
    TapAllAfterCNN=0

    #####Task 分類用 Validation_Data 因為有內差 。  Tap優化用 Validation_Data_2 因為沒有內差
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        for iTrial in range(len(Validation_Data[task]['trials'])):
            TotalCount=TotalCount+1
            CNNSuccess=JsonToCube_NoInterpolation_AllBegan_OnTrial(Validation_Data[task]['trials'][iTrial],task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,ModelDict[tGrid])

            if CNNSuccess==True:

                SuccessCount=SuccessCount+1
    print("SuccessRate:",DefaultSuccessCount/TotalCount," vs ",SuccessCount/TotalCount,"   After CNN Tap ", TapDefaultSuccess/TapAllAfterCNN," vs ",  TapMyTapSuccess/TapAllAfterCNN)


    ValidData=""
   
   
    if TapAllAfterCNN!=0:

        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,TapDefaultSuccess/TapAllAfterCNN,TapMyTapSuccess/TapAllAfterCNN

    else:
        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,1234567,1234567



def evaluate_DynamicTime(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,Validation_Data_2):
    

    #每個event 預測都用固定的 time-grid
    def VerifyTap(TaskData):
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

                FingerCenterDict=dict()

                PossibleX=list()
                PossibleY=list()

                for iFinger in range(len(OutputData["rawTouchTracks"])):
                    
                    CandidateData=list()
                    for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                         
                         if iPoint==0 or iPoint==1:
                             accelerate=0
                         else:


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
                                 LabelFalse(OutputData,iFinger,iPoint-2)
                             
                             if (AverageX2-positionX3)*(AverageX2-positionX3)+(AverageY2-positionY3)*(AverageY2-positionY3)>TapAllowableMovement*TapAllowableMovement:
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
                            LabelFalse(OutputData,iFinger,ThisClusterFinalPoint[i][0])
                            if distance<=Distance:
                                Distance=distance
                                SelectedPoint=ThisClusterFinalPoint[i][0]
                        OutputData["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['label']=True
                        
                        FingerCenterDict[str(iFinger)]=[Xave,Yave]
                        PossibleX.append(Xave)
                        PossibleY.append(Yave)
                    FingerCenterDict[str(iFinger)]=[positionx,positiony]  
                    PossibleX.append(positionx)
                    PossibleY.append(positiony)

                DataPointNum=0
                for iFinger in range(len(OutputData["rawTouchTracks"])):
                    for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                         if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                            DataPointNum=DataPointNum+1


                return OutputData,[np.mean(PossibleX),np.mean(PossibleY)]



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
    
        DefaultSuccess=0
        FirstTouchSuccess=0
        EndedTouchSuccess=0
        OptimzerSuccess=0
        defaultfalse=0


        # RecognizedTapTrials=RecognizedTapTrials
        TrialToOptimzer=AllTaskValidIndex[task][i]
        #print(AllTaskValidIndex[task],TrialToOptimzer,len(Validation_Data_2[task]['trials']))
        #TaskData=Validation_Data_2[task]['trials'][i]

        OptimizedData=LabelTrue(TaskData)
        OptimizedData,OutPutPoint=LabelByMyAlgorithm(OptimizedData)

        FilteredOptimizedData=FilteredJsonOneTrial(OptimizedData)

       
        TargetX=TaskData["targetFrame"][0][0] +TaskData["targetFrame"][1][0]*0.5
        TargetY=TaskData["targetFrame"][0][1] + TaskData["targetFrame"][1][1]*0.5

        if tv.TapTask_SuccessVerify(FilteredOptimizedData):

                OptimzerSuccess=1


        if len(TaskData['tapEvents'])>0:
            #print(TaskData['tapEvents'][0]['locationOfTouchAtIndex'])
            
            Y=TaskData['tapEvents'][0]['location'][0]
            X=Device_info[0]-TaskData['tapEvents'][0]['location'][1]

            tempX=TaskData['tapEvents'][0]['locationOfTouchAtIndex']['0'][0]
            tempY=TaskData['tapEvents'][0]['locationOfTouchAtIndex']['0'][1]
            #print(X,Y," vs ",TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][0],TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][1])

           
            if (abs(X - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(Y- TargetY) >TaskData["targetFrame"][1][1]*0.5):
                    # cout << "First touch point is not correct" << endl;

            #print((NewTaskData["targetFrame"][0][0]),(NewTaskData["targetFrame"][0][1]),(NewTaskData["targetFrame"][1][0]),(NewTaskData["targetFrame"][1][1]),NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0],NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] )
                #print("First Touch")
                print("BasedPanEventLocationFalse","Target",TargetX,TargetY," tapevent: ",X,Y," locationOfTouchAtIndex: ",tempX,tempY)
                DefaultSuccess=0
            else:
                DefaultSuccess=1
        else:
            DefaultSuccess=0
            print("BasedPanEventLocationFalse: No TapEventQQ")


        FirstTouchX=TaskData["rawTouchTracks"][0]["rawTouches"][0]["location"][0]
        FirstTouchY=TaskData["rawTouchTracks"][0]["rawTouches"][0]["location"][1]
        EndedTouchX=TaskData["rawTouchTracks"][0]["rawTouches"][len(TaskData["rawTouchTracks"][0]["rawTouches"])-1]["location"][0]
        EndedTouchY=TaskData["rawTouchTracks"][0]["rawTouches"][len(TaskData["rawTouchTracks"][0]["rawTouches"])-1]["location"][1]

        FirstTouchSuccess=0
        EndedTouchSuccess=0
        
        if (abs(FirstTouchX - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(FirstTouchY- TargetY) >TaskData["targetFrame"][1][1]*0.5):
                
            
            FirstTouchSuccess=0
        else:
            FirstTouchSuccess=1

        if (abs(EndedTouchX - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(EndedTouchY- TargetY) >TaskData["targetFrame"][1][1]*0.5):
                
            
            EndedTouchSuccess=0
        else:
            EndedTouchSuccess=1



        return  DefaultSuccess,FirstTouchSuccess,EndedTouchSuccess,OptimzerSuccess

    #TapVerify End
    def JsonToCube_NoInterpolation_DynamicTime_OnTrial(JsonDataOneTrial,task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,ModelDict):

        def AdjustPrediction(pred):
            if pred[0][0]>0.999:
                    return 0
            else:
                    return 1

        def ModelChoose(TimeGrid,ModelDict):

            return ModelDict[TimeGrid],TimeGrid,10
            #return ModelDict[0.05],0.05,10

        def TimeInRange(PreviousEventTime,PresentEventTime,TouchPhaseTime):
            for t in TouchPhaseTime:
                if (t>=PreviousEventTime) & (t<=PresentEventTime):
                    return True
            return False
        def FindIndexOfMatrix_AllBegan(Point,BaseTime,GridSize,TimeGrid,Device_info,MaxSpeed):
            import numpy as np
           

            #######2

            X=Point['location'][0]
            Y=Point['location'][1]
            T=Point['timestamp']

            
            T0=BaseTime


            X0=Point['previousLocation'][0]
            Y0=Point['previousLocation'][1]
            # X0=Point_0['location'][0]
            # Y0=Point_0['location'][1]

            dt=T-T0
            dx=X-X0
            dy=Y-Y0
            
            #print("Device",Device_info)

            if dx>MaxSpeed:
                #print("dx",dx)
                dx=MaxSpeed
            elif dx<-MaxSpeed:
                #print("dx",dx)
                dx=-MaxSpeed

            if dy>MaxSpeed:
                #print("dy",dy)
                dy=MaxSpeed
            elif dy<-MaxSpeed:
                #print("dy",dy)
                dy=-MaxSpeed

            IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
            IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

          

            if TimeGrid==0:
                print("Grid Error")
            IndexT=int(np.ceil(dt/TimeGrid))
            
            

            #print(IndexX,IndexY,IndexT,dx,dy)

            return IndexX,IndexY,IndexT 


        import numpy as np
        # GridNum_InX=int(np.ceil(Device_info[0]/GridSize))+10
        # GridNum_InY=int(np.ceil(Device_info[1]/GridSize))+10
      
        
        #print("ArraySize",GridNum_InX,GridNum_InY,TimeFrameNum,Channel)
        TimeGrid=float(tGrid)
        AllDataX=list()
        AllDataY=list()
        Task=0
        
        if task=='tapTask':
            Task=0;
        else:
            Task=1;

            

        ###find Began
        PredictNum=0
        AllTouchBeganTime=list()
        AllTouchEndTime=list()
        AllEventTime=list()
        AllEventAndEndedTime=list()

        

        for iFinger in range(len(JsonDataOneTrial["rawTouchTracks"])):
            for iPoint in range(len(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"])):
                    if JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='began':
                            AllTouchBeganTime.append(float(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
                    if JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='ended':
                            AllTouchEndTime.append(float(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
                            AllEventAndEndedTime.append(float(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
        for panevent_t in range(len(JsonDataOneTrial['panEvents'])):
            if JsonDataOneTrial['panEvents'][panevent_t]['state']!='changed':
                #print(JsonDataOneTrial['panEvents'][panevent_t]['state'])
                AllEventTime.append(float(JsonDataOneTrial['panEvents'][panevent_t]['timestamp']))
                AllEventAndEndedTime.append(float(JsonDataOneTrial['panEvents'][panevent_t]['timestamp']))
                PredictNum=PredictNum+1

        for tapevent_t in range(len(JsonDataOneTrial['tapEvents'])):
            AllEventTime.append(float(JsonDataOneTrial['tapEvents'][tapevent_t]['timestamp']))
            AllEventAndEndedTime.append(float(JsonDataOneTrial['tapEvents'][tapevent_t]['timestamp']))
            PredictNum=PredictNum+1


        SortedAllTouchEventTime=sorted(AllEventTime)
        SortedAllTouchBeganTime=sorted(AllTouchBeganTime)
        SortedAllTouchEndTime=sorted(AllTouchEndTime)
        SortedAllTouchEventAndEndedTime=sorted(AllEventAndEndedTime)


       
        #ProcssTimeList=SortedAllTouchEventTime
        ProcssTimeList=SortedAllTouchEventAndEndedTime
        if len(ProcssTimeList)==0:
            print("No pan No Tap")
            ProcssTimeList=SortedAllTouchEndTime
        
        touchBeganPredict='?????'
        
        CNNEvent=list()
        for began_T in ProcssTimeList:
            BaseTime=began_T-TimeGrid*TimeFrameNum
            FirstTouchTime=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']

            #TimeGrid=(began_T-FirstTouchTime)/10

            PredictModel,TimeGrid,MaxSpeed=ModelChoose(TimeGrid,ModelDict)
            #print("PredictModel Shape",PredictModel.layers[0].output_shape[1])
            if PredictModel.layers[0].output_shape[1]==81:
                MaxSpeed=10
            elif PredictModel.layers[0].output_shape[1]==41:
                MaxSpeed=10

            GridNum_InX=int(np.ceil(2*MaxSpeed/GridSize))+1
            GridNum_InY=int(np.ceil(2*MaxSpeed/GridSize))+1
            Channel=1

            TouchBeganEvent=False
            for begantime in SortedAllTouchBeganTime:
                if (BaseTime<=begantime)&(began_T>begantime):
                      TouchBeganEvent=True  

            TouchEndEvent=False
            for endtime in SortedAllTouchEndTime:
                if (BaseTime<=endtime)&(began_T>endtime):
                      TouchEndEvent=True  


        #print(began_T,began_T in SortedAllTouchEndTime,began_T in SortedAllTouchBeganTime)
        #if TimeInRange(began_T-TimeFrameNum*tGrid,began_T+TimeFrameNum*tGrid,SortedAllTouchEndTime):

            predictX=list()
            predictY=list()
            DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
            
            BaseTime=began_T-TimeGrid*TimeFrameNum
            #print("EventTime ",began_T," BaseTime ",BaseTime," RecognitionTime ",began_T-BaseTime)
            for iFinger in range(len(JsonDataOneTrial["rawTouchTracks"])):
                for iPoint in range(len(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"])):

                    Point_0=JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][0]
                    #Point_0=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]
                    Point=JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]

                    
                    if (BaseTime<=Point['timestamp']) &  (began_T>=Point['timestamp']):

                        #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                        Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                        #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedFirstPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                         
                        #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_AllBegan(Point,BaseTime,GridSize,TimeGrid,Device_info,MaxSpeed)
                        
                        if Time_In<TimeFrameNum:
                            #Time_In=TimeFrameNum-1
                            DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                            # if Point['phase']=='ended':
                            #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

        #######Matrix Ready Go Predict
            predictX.append(DataMatrix)
            predictY.append(Task)


            y_test = to_categorical(np.array(predictY), num_classes=2)

            
            X_test  = np.array(predictX).reshape(-1, np.array(predictX).shape[1], np.array(predictX).shape[2], np.array(predictX).shape[3], 1)


            pred = PredictModel.predict(X_test)
                #print("pred",pred)
            prediction = np.argmax(pred, axis=1)[0]
                #print("pred1",prediction)
            touchBeganPredict=str(prediction)


            CNNEvent.append(prediction)


        #print(task,"EventNum: ", PredictNum ,len(JsonDataOneTrial['tapEvents']),len(JsonDataOneTrial['panEvents'])," vs ",(0 in CNNEvent),(1 in CNNEvent),CNNEvent)
        
        ##每個event 的predict 結束 
        #來驗證tap optimzer
        #print("Predict",len(CNNEvent),len(ProcssTimeList))
        if task=='swipeTask' or task=='horizontalScrollTask' or task=='verticalScrollTask':
                  

            if len(CNNEvent)>0:
                if 1 in CNNEvent:
                    if 0 not in CNNEvent :
                            return True,CNNEvent
                    return False,CNNEvent
                return False,CNNEvent
            return False,CNNEvent
                    
        elif task=='tapTask':
            #print("Tap False?",len(np.where(CNNEvent==1)[0]))
            if len(CNNEvent)>0:
                    if 1 not in CNNEvent :
                            if 0 in CNNEvent:
                                    return True,CNNEvent
                            return False,CNNEvent
                    return False,CNNEvent
            return False,CNNEvent
    #####


    import numpy as np

    TotalCount=0
    SuccessCount=0
    DefaultSuccessCount=0
    DetailString=""

    TapDefaultSuccess=0
    TapFirstTouchSuccess=0
    TapEndTouchSuccess=0
    TapMyTapSuccess=0
    
    TapAllAfterCNN=0
    HPanAllAfterCNN=0
    VPanAllAfterCNN=0
    SwipeAllAfterCNN=0

    TapTotal=0
    HPanTotal=0
    VPanTotal=0
    SwipeTotal=0



    SwipeImproveTotal=0
    SwipeImprovebyNoPanNoTap=0
    SwipeImprovebyNoPanHaveTap=0
    SwipeImprovebyHavePanHaveTap=0

    HPanImproveTotal=0
    HPanImprovebyNoPanNoTap=0
    HPanImprovebyNoPanHaveTap=0
    HPanImprovebyHavePanHaveTap=0

    VPanImproveTotal=0
    VPanImprovebyNoPanNoTap=0
    VPanImprovebyNoPanHaveTap=0
    VPanImprovebyHavePanHaveTap=0

    TapImproveTotal=0
    TapImprovebyNoPanNoTap=0
    TapImprovebyHavePanNoTap=0
    TapImprovebyHavePanHaveTap=0


    #####Task 分類用 Validation_Data 因為有內差 。  Tap優化用 Validation_Data_2 因為沒有內差
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        MikeCheck_SingleFinger_CNNTapRecongized=0
        MikeCheck_MultiFinger_CNNTapRecongized=0
        MikeCheck_SingleFinger_DefaultTapRecongized=0
        MikeCheck_MultiFinger_DefaultTapRecongized=0
        MikeCheck_SingleFinger_Num=0
        MikeCheck_MultiFinger_Num=0

        for iTrial in range(len(Validation_Data[task]['trials'])):
            TotalCount=TotalCount+1
            
            CNNSuccess,CNNEvent=JsonToCube_NoInterpolation_DynamicTime_OnTrial(Validation_Data[task]['trials'][iTrial],task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,ModelDict)
            

            if HaveTouchPoint(Validation_Data[task]['trials'][iTrial]):


                if task=='swipeTask':
                    if len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])==1:
                        MikeCheck_SingleFinger_Num=MikeCheck_SingleFinger_Num+1
                        if 0 in CNNEvent:
                            MikeCheck_SingleFinger_CNNTapRecongized=MikeCheck_SingleFinger_CNNTapRecongized+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                            MikeCheck_SingleFinger_DefaultTapRecongized=MikeCheck_SingleFinger_DefaultTapRecongized+1

                    elif len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])>1:
                        MikeCheck_MultiFinger_Num=MikeCheck_MultiFinger_Num+1
                        if 0 in CNNEvent:
                            MikeCheck_MultiFinger_CNNTapRecongized=MikeCheck_MultiFinger_CNNTapRecongized+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                            MikeCheck_MultiFinger_DefaultTapRecongized=MikeCheck_MultiFinger_DefaultTapRecongized+1


                    SwipeTotal=SwipeTotal+1

                    if CNNSuccess==True:
                        SwipeAllAfterCNN=SwipeAllAfterCNN+1

                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                            if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                    DefaultSuccessCount=DefaultSuccessCount+1
                            else:
                                if CNNSuccess==True: 
                                    SwipeImproveTotal=SwipeImproveTotal+1
                                    SwipeImprovebyNoPanNoTap=SwipeImprovebyNoPanNoTap+1
                                    ##Improve by No tap no pan

                    else:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                            if CNNSuccess==True: 
                                SwipeImproveTotal=SwipeImproveTotal+1
                                SwipeImprovebyHavePanHaveTap=SwipeImprovebyHavePanHaveTap+1
                               
                                ##Improve by have tap have pan

                        else:
                            if CNNSuccess==True: 
                                SwipeImproveTotal=SwipeImproveTotal+1
                                SwipeImprovebyNoPanHaveTap=SwipeImprovebyNoPanHaveTap+1
                                ##Improve by have tap no pan 


                elif task=='horizontalScrollTask':
                    if len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])==1:
                        MikeCheck_SingleFinger_Num=MikeCheck_SingleFinger_Num+1
                        if 0 in CNNEvent:
                            MikeCheck_SingleFinger_CNNTapRecongized=MikeCheck_SingleFinger_CNNTapRecongized+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                            MikeCheck_SingleFinger_DefaultTapRecongized=MikeCheck_SingleFinger_DefaultTapRecongized+1

                    elif len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])>1:
                        MikeCheck_MultiFinger_Num=MikeCheck_MultiFinger_Num+1
                        if 0 in CNNEvent:
                            MikeCheck_MultiFinger_CNNTapRecongized=MikeCheck_MultiFinger_CNNTapRecongized+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                            MikeCheck_MultiFinger_DefaultTapRecongized=MikeCheck_MultiFinger_DefaultTapRecongized+1

                    HPanTotal=HPanTotal+1
                    if CNNSuccess==True:
                        HPanAllAfterCNN=HPanAllAfterCNN+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                            if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                    DefaultSuccessCount=DefaultSuccessCount+1
                            else:
                                if CNNSuccess==True: 
                                    HPanImproveTotal=HPanImproveTotal+1
                                    HPanImprovebyNoPanNoTap=HPanImprovebyNoPanNoTap+1
                                    ##Improve by No tap no pan

                    else:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                            if CNNSuccess==True: 
                                HPanImproveTotal=HPanImproveTotal+1
                                HPanImprovebyHavePanHaveTap=HPanImprovebyHavePanHaveTap+1
                               
                                ##Improve by have tap have pan

                        else:
                            if CNNSuccess==True: 
                                HPanImproveTotal=HPanImproveTotal+1
                                HPanImprovebyNoPanHaveTap=HPanImprovebyNoPanHaveTap+1
                                ##Improve by have tap no pan 


                elif task=='verticalScrollTask':
                    if len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])==1:
                        MikeCheck_SingleFinger_Num=MikeCheck_SingleFinger_Num+1
                        if 0 in CNNEvent:
                            MikeCheck_SingleFinger_CNNTapRecongized=MikeCheck_SingleFinger_CNNTapRecongized+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                            MikeCheck_SingleFinger_DefaultTapRecongized=MikeCheck_SingleFinger_DefaultTapRecongized+1

                    elif len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])>1:
                        MikeCheck_MultiFinger_Num=MikeCheck_MultiFinger_Num+1
                        if 0 in CNNEvent:
                            MikeCheck_MultiFinger_CNNTapRecongized=MikeCheck_MultiFinger_CNNTapRecongized+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                            MikeCheck_MultiFinger_DefaultTapRecongized=MikeCheck_MultiFinger_DefaultTapRecongized+1

                    VPanTotal=VPanTotal+1
                    if CNNSuccess==True:
                        VPanAllAfterCNN=VPanAllAfterCNN+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                            if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                    DefaultSuccessCount=DefaultSuccessCount+1
                            else:
                                if CNNSuccess==True: 
                                    VPanImproveTotal=VPanImproveTotal+1
                                    VPanImprovebyNoPanNoTap=VPanImprovebyNoPanNoTap+1
                                    ##Improve by No tap no pan

                    else:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                            if CNNSuccess==True: 
                                VPanImproveTotal=VPanImproveTotal+1
                                VPanImprovebyHavePanHaveTap=VPanImprovebyHavePanHaveTap+1
                               
                                ##Improve by have tap have pan

                        else:
                            if CNNSuccess==True: 
                                VPanImproveTotal=VPanImproveTotal+1
                                VPanImprovebyNoPanHaveTap=VPanImprovebyNoPanHaveTap+1
                                ##Improve by have tap no pan 

                elif task=='tapTask':
                    if len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])==1:
                        MikeCheck_SingleFinger_Num=MikeCheck_SingleFinger_Num+1
                        if 0 in CNNEvent:
                            MikeCheck_SingleFinger_CNNTapRecongized=MikeCheck_SingleFinger_CNNTapRecongized+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                            MikeCheck_SingleFinger_DefaultTapRecongized=MikeCheck_SingleFinger_DefaultTapRecongized+1

                    elif len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])>1:
                        MikeCheck_MultiFinger_Num=MikeCheck_MultiFinger_Num+1
                        if 0 in CNNEvent:
                            MikeCheck_MultiFinger_CNNTapRecongized=MikeCheck_MultiFinger_CNNTapRecongized+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                            MikeCheck_MultiFinger_DefaultTapRecongized=MikeCheck_MultiFinger_DefaultTapRecongized+1

                    TapTotal=TapTotal+1
                    if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
                            if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                                    DefaultSuccessCount=DefaultSuccessCount+1
                            else:
                                if CNNSuccess==True: 
                                    TapImproveTotal=TapImproveTotal+1
                                    TapImprovebyNoPanNoTap=TapImprovebyNoPanNoTap+1
                                    ##Improve by No tap no pan

                    else:
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                            if CNNSuccess==True: 
                                TapImproveTotal=TapImproveTotal+1
                                TapImprovebyHavePanHaveTap=TapImprovebyHavePanHaveTap+1
                               
                                ##Improve by have tap have pan

                        else:
                            if CNNSuccess==True: 
                                TapImproveTotal=TapImproveTotal+1
                                TapImprovebyHavePanNoTap=TapImprovebyHavePanNoTap+1
                                ##Improve by no tap have pan 

                    if CNNSuccess==True:
                        TapAllAfterCNN=TapAllAfterCNN+1
                        defaultTap,firsttouch,endedtouch,MyTap=VerifyTap(Validation_Data_2[task]['trials'][iTrial])
                        TapDefaultSuccess=TapDefaultSuccess+defaultTap
                        TapMyTapSuccess=TapMyTapSuccess+MyTap
                        TapFirstTouchSuccess=TapFirstTouchSuccess+firsttouch
                        TapEndTouchSuccess=TapEndTouchSuccess+endedtouch


                if CNNSuccess==True:

                    SuccessCount=SuccessCount+1
        
        print(task,ValidIndex,"Single ",MikeCheck_SingleFinger_DefaultTapRecongized," / ",MikeCheck_SingleFinger_Num," vs ",MikeCheck_SingleFinger_CNNTapRecongized," / ",MikeCheck_SingleFinger_Num," Multi ",MikeCheck_MultiFinger_DefaultTapRecongized," / ",MikeCheck_MultiFinger_Num," vs ",MikeCheck_MultiFinger_CNNTapRecongized," / ",MikeCheck_MultiFinger_Num,)


    ValidData=""
   
    print("---Improve By---","TapTask: ",TapImprovebyHavePanHaveTap,TapImprovebyNoPanNoTap,TapImprovebyHavePanNoTap,TapImproveTotal,"---Improve By---")
    print("---Improve By---","SwipeTask: ",SwipeImprovebyHavePanHaveTap,SwipeImprovebyNoPanNoTap,SwipeImprovebyNoPanHaveTap,SwipeImproveTotal,"---Improve By---")
    print("---Improve By---","HPanTask: ",HPanImprovebyHavePanHaveTap,HPanImprovebyNoPanNoTap,HPanImprovebyNoPanHaveTap,HPanImproveTotal,"---Improve By---")
    print("---Improve By---","VPanTask: ",VPanImprovebyHavePanHaveTap,VPanImprovebyNoPanNoTap,VPanImprovebyNoPanHaveTap,VPanImproveTotal,"---Improve By---")
    

    if TapAllAfterCNN!=0:
        print("SuccessRate:",DefaultSuccessCount/TotalCount," vs ",SuccessCount/TotalCount," Confusion: ", " TapTask ",TapAllAfterCNN," ",TapTotal," SwipeTask ", SwipeAllAfterCNN,"  ",SwipeTotal," HPanTask ", HPanAllAfterCNN,"  ",HPanTotal," VPanTask ", VPanAllAfterCNN,"  ",VPanTotal,"   After CNN Tap ", TapDefaultSuccess/TapAllAfterCNN,TapFirstTouchSuccess/TapAllAfterCNN,TapEndTouchSuccess/TapAllAfterCNN," vs ",  TapMyTapSuccess/TapAllAfterCNN)

        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,TapDefaultSuccess/TapAllAfterCNN,TapFirstTouchSuccess/TapAllAfterCNN,TapEndTouchSuccess/TapAllAfterCNN,TapMyTapSuccess/TapAllAfterCNN

    else:
        print("SuccessRate:",DefaultSuccessCount/TotalCount," vs ",SuccessCount/TotalCount," Confusion: ", " TapTask ",TapAllAfterCNN,"  ",TapTotal," SwipeTask ", SwipeAllAfterCNN,"  ",SwipeTotal," HPanTask ", HPanAllAfterCNN,"  ",HPanTotal," VPanTask ", VPanAllAfterCNN,"  ",VPanTotal,"   After CNN Tap : NO Success")
        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,1234567,1234567,1234567,1234567



########################################################



def evaluate_DynamicTime_BasedSimulator(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,Validation_Data_2):
    

    #每個event 預測都用固定的 time-grid
    def VerifyTap(TaskData):
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

                FingerCenterDict=dict()

                PossibleX=list()
                PossibleY=list()

                for iFinger in range(len(OutputData["rawTouchTracks"])):
                    
                    CandidateData=list()
                    for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                         
                         if iPoint==0 or iPoint==1:
                             accelerate=0
                         else:

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
                                 LabelFalse(OutputData,iFinger,iPoint-2)
                             
                             if (AverageX2-positionX3)*(AverageX2-positionX3)+(AverageY2-positionY3)*(AverageY2-positionY3)>TapAllowableMovement*TapAllowableMovement:
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
                        largestCluster=np.argmax(np.bincount(ChooseLabel))
                        
                        ThisClusterFinalPoint=list()
                        
                        for i in range(len(CandidateData)):
                            CheckPoint=CandidateData[i][0]
                            
                            if(ChooseLabel[i]!=largestCluster):
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
                            LabelFalse(OutputData,iFinger,ThisClusterFinalPoint[i][0])
                            if distance<=Distance:
                                Distance=distance
                                SelectedPoint=ThisClusterFinalPoint[i][0]
                        OutputData["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['label']=True
                        
                        FingerCenterDict[str(iFinger)]=[Xave,Yave]
                        PossibleX.append(Xave)
                        PossibleY.append(Yave)
                    FingerCenterDict[str(iFinger)]=[positionx,positiony]  
                    PossibleX.append(positionx)
                    PossibleY.append(positiony)
                DataPointNum=0
                for iFinger in range(len(OutputData["rawTouchTracks"])):
                    for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                         if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                            DataPointNum=DataPointNum+1
                return OutputData,[np.mean(PossibleX),np.mean(PossibleY)]



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
    
        DefaultSuccess=0
        FirstTouchSuccess=0
        EndedTouchSuccess=0
        OptimzerSuccess=0
        defaultfalse=0


        # RecognizedTapTrials=RecognizedTapTrials
        TrialToOptimzer=AllTaskValidIndex[task][i]
        #print(AllTaskValidIndex[task],TrialToOptimzer,len(Validation_Data_2[task]['trials']))
        #TaskData=Validation_Data_2[task]['trials'][i]

        OptimizedData=LabelTrue(TaskData)
        OptimizedData,OutPutPoint=LabelByMyAlgorithm(OptimizedData)

        FilteredOptimizedData=FilteredJsonOneTrial(OptimizedData)

       
        TargetX=TaskData["targetFrame"][0][0] +TaskData["targetFrame"][1][0]*0.5
        TargetY=TaskData["targetFrame"][0][1] + TaskData["targetFrame"][1][1]*0.5

        if tv.TapTask_SuccessVerify(FilteredOptimizedData):

                OptimzerSuccess=1


        if len(TaskData['tapEvents'])>0:
            #print(TaskData['tapEvents'][0]['locationOfTouchAtIndex'])
            
            Y=TaskData['tapEvents'][0]['location'][0]
            X=Device_info[0]-TaskData['tapEvents'][0]['location'][1]

            tempX=TaskData['tapEvents'][0]['locationOfTouchAtIndex']['0'][0]
            tempY=TaskData['tapEvents'][0]['locationOfTouchAtIndex']['0'][1]
            #print(X,Y," vs ",TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][0],TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][1])

           
            if (abs(X - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(Y- TargetY) >TaskData["targetFrame"][1][1]*0.5):
                    # cout << "First touch point is not correct" << endl;

            #print((NewTaskData["targetFrame"][0][0]),(NewTaskData["targetFrame"][0][1]),(NewTaskData["targetFrame"][1][0]),(NewTaskData["targetFrame"][1][1]),NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0],NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] )
                #print("First Touch")
                print("BasedPanEventLocationFalse","Target",TargetX,TargetY," tapevent: ",X,Y," locationOfTouchAtIndex: ",tempX,tempY)
                DefaultSuccess=0
            else:
                DefaultSuccess=1
        else:
            DefaultSuccess=0
            print("BasedPanEventLocationFalse: No TapEventQQ")


        FirstTouchX=TaskData["rawTouchTracks"][0]["rawTouches"][0]["location"][0]
        FirstTouchY=TaskData["rawTouchTracks"][0]["rawTouches"][0]["location"][1]
        EndedTouchX=TaskData["rawTouchTracks"][0]["rawTouches"][len(TaskData["rawTouchTracks"][0]["rawTouches"])-1]["location"][0]
        EndedTouchY=TaskData["rawTouchTracks"][0]["rawTouches"][len(TaskData["rawTouchTracks"][0]["rawTouches"])-1]["location"][1]

        FirstTouchSuccess=0
        EndedTouchSuccess=0
        
        if (abs(FirstTouchX - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(FirstTouchY- TargetY) >TaskData["targetFrame"][1][1]*0.5):
                
            
            FirstTouchSuccess=0
        else:
            FirstTouchSuccess=1

        if (abs(EndedTouchX - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(EndedTouchY- TargetY) >TaskData["targetFrame"][1][1]*0.5):
                
            
            EndedTouchSuccess=0
        else:
            EndedTouchSuccess=1



        return  DefaultSuccess,FirstTouchSuccess,EndedTouchSuccess,OptimzerSuccess

    #TapVerify End
    def JsonToCube_NoInterpolation_DynamicTime_OnTrial_BasedSimulator(JsonDataOneTrial,task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,ModelDict):

        def AdjustPrediction(pred):
            if pred[0][0]>0.999:
                    return 0
            else:
                    return 1

        def ModelChoose(TimeGrid,ModelDict):

            return ModelDict[TimeGrid],TimeGrid,10
            #return ModelDict[0.05],0.05,10

        def TimeInRange(PreviousEventTime,PresentEventTime,TouchPhaseTime):
            for t in TouchPhaseTime:
                if (t>=PreviousEventTime) & (t<=PresentEventTime):
                    return True
            return False
        def FindIndexOfMatrix_AllBegan(Point,BaseTime,GridSize,TimeGrid,Device_info,MaxSpeed):
            import numpy as np
           

            #######2

            X=Point['location'][0]
            Y=Point['location'][1]
            T=Point['timestamp']

            
            T0=BaseTime


            X0=Point['previousLocation'][0]
            Y0=Point['previousLocation'][1]
            # X0=Point_0['location'][0]
            # Y0=Point_0['location'][1]

            dt=T-T0
            dx=X-X0
            dy=Y-Y0
            
            #print("Device",Device_info)

            if dx>MaxSpeed:
                #print("dx",dx)
                dx=MaxSpeed
            elif dx<-MaxSpeed:
                #print("dx",dx)
                dx=-MaxSpeed

            if dy>MaxSpeed:
                #print("dy",dy)
                dy=MaxSpeed
            elif dy<-MaxSpeed:
                #print("dy",dy)
                dy=-MaxSpeed

            IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
            IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

          

            if TimeGrid==0:
                print("Grid Error")
            IndexT=int(np.ceil(dt/TimeGrid))
            
            

            #print(IndexX,IndexY,IndexT,dx,dy)

            return IndexX,IndexY,IndexT 


        import numpy as np
        # GridNum_InX=int(np.ceil(Device_info[0]/GridSize))+10
        # GridNum_InY=int(np.ceil(Device_info[1]/GridSize))+10
      
        
        #print("ArraySize",GridNum_InX,GridNum_InY,TimeFrameNum,Channel)
        TimeGrid=float(tGrid)
        AllDataX=list()
        AllDataY=list()
        Task=0
        
        if task=='tapTask':
            Task=0;
        else:
            Task=1;

            

        ###find Began
        PredictNum=0
        AllTouchBeganTime=list()
        AllTouchEndTime=list()
        AllEventTime=list()
        AllEventAndEndedTime=list()

        

        for iFinger in range(len(JsonDataOneTrial["rawTouchTracks"])):
            for iPoint in range(len(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"])):
                    if JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='began':
                            AllTouchBeganTime.append(float(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
                    if JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='ended':
                            AllTouchEndTime.append(float(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
                            AllEventAndEndedTime.append(float(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
        for panevent_t in range(len(JsonDataOneTrial['panEvents'])):
            if JsonDataOneTrial['panEvents'][panevent_t]['state']!='changed':
                #print(JsonDataOneTrial['panEvents'][panevent_t]['state'])
                AllEventTime.append(float(JsonDataOneTrial['panEvents'][panevent_t]['timestamp']))
                AllEventAndEndedTime.append(float(JsonDataOneTrial['panEvents'][panevent_t]['timestamp']))
                PredictNum=PredictNum+1

        for tapevent_t in range(len(JsonDataOneTrial['tapEvents'])):
            AllEventTime.append(float(JsonDataOneTrial['tapEvents'][tapevent_t]['timestamp']))
            AllEventAndEndedTime.append(float(JsonDataOneTrial['tapEvents'][tapevent_t]['timestamp']))
            PredictNum=PredictNum+1


        SortedAllTouchEventTime=sorted(AllEventTime)
        SortedAllTouchBeganTime=sorted(AllTouchBeganTime)
        SortedAllTouchEndTime=sorted(AllTouchEndTime)
        SortedAllTouchEventAndEndedTime=sorted(AllEventAndEndedTime)


       
        ProcssTimeList=SortedAllTouchEventTime


        #ProcssTimeList=SortedAllTouchEventAndEndedTime

        if len(ProcssTimeList)==0:
            print("No pan No Tap")
            ProcssTimeList=SortedAllTouchEndTime
        

        SimluatorTime=list()
        for iFinger in range(len(JsonDataOneTrial["rawTouchTracks"])):
            if iFinger==1:
                SimluatorTime.append(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][len(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp'])
            if len(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"])>1:
                SimluatorTime.append(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][3]['timestamp'])

           


        SortedSimluatorTime=sorted(SimluatorTime)
        ProcssTimeList=SortedSimluatorTime


        touchBeganPredict='?????'
        
        CNNEvent=list()
        for began_T in ProcssTimeList:
            BaseTime=began_T-TimeGrid*TimeFrameNum
            FirstTouchTime=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']

            #TimeGrid=(began_T-FirstTouchTime)/10

            PredictModel,TimeGrid,MaxSpeed=ModelChoose(TimeGrid,ModelDict)
            #print("PredictModel Shape",PredictModel.layers[0].output_shape[1])
            if PredictModel.layers[0].output_shape[1]==81:
                MaxSpeed=10
            elif PredictModel.layers[0].output_shape[1]==41:
                MaxSpeed=10

            GridNum_InX=int(np.ceil(2*MaxSpeed/GridSize))+1
            GridNum_InY=int(np.ceil(2*MaxSpeed/GridSize))+1
            Channel=1

            TouchBeganEvent=False
            for begantime in SortedAllTouchBeganTime:
                if (BaseTime<=begantime)&(began_T>begantime):
                      TouchBeganEvent=True  

            TouchEndEvent=False
            for endtime in SortedAllTouchEndTime:
                if (BaseTime<=endtime)&(began_T>endtime):
                      TouchEndEvent=True  


        #print(began_T,began_T in SortedAllTouchEndTime,began_T in SortedAllTouchBeganTime)
        #if TimeInRange(began_T-TimeFrameNum*tGrid,began_T+TimeFrameNum*tGrid,SortedAllTouchEndTime):

            predictX=list()
            predictY=list()
            DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
            
            BaseTime=began_T-TimeGrid*TimeFrameNum
            #print("EventTime ",began_T," BaseTime ",BaseTime," RecognitionTime ",began_T-BaseTime)
            for iFinger in range(len(JsonDataOneTrial["rawTouchTracks"])):
                for iPoint in range(len(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"])):

                    Point_0=JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][0]
                    #Point_0=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]
                    Point=JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]

                    
                    if (BaseTime<=Point['timestamp']) &  (began_T>=Point['timestamp']):
                    #if (began_T-TimeGrid*TimeFrameNum<=Point['timestamp']) & (began_T>=Point['timestamp']):

                        #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                        #Point_0['timestamp']=began_T-TimeGrid*TimeFrameNum


                        #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                        Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                        #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedFirstPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                         
                        #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_AllBegan(Point,BaseTime,GridSize,TimeGrid,Device_info,MaxSpeed)
                        
                        if Time_In<TimeFrameNum:
                            #Time_In=TimeFrameNum-1
                            DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                            # if Point['phase']=='ended':
                            #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

        #######Matrix Ready Go Predict
            predictX.append(DataMatrix)
            predictY.append(Task)


            y_test = to_categorical(np.array(predictY), num_classes=2)

            
            X_test  = np.array(predictX).reshape(-1, np.array(predictX).shape[1], np.array(predictX).shape[2], np.array(predictX).shape[3], 1)


            pred = PredictModel.predict(X_test)
                #print("pred",pred)
            prediction = np.argmax(pred, axis=1)[0]
                #print("pred1",prediction)
            touchBeganPredict=str(prediction)
            CNNEvent.append(prediction)


        #print(task,"EventNum: ", PredictNum ,len(JsonDataOneTrial['tapEvents']),len(JsonDataOneTrial['panEvents'])," vs ",(0 in CNNEvent),(1 in CNNEvent),CNNEvent)
        
        ##每個event 的predict 結束 
        #來驗證tap optimzer
        #print("Predict",len(CNNEvent),len(ProcssTimeList))
        if task=='swipeTask' or task=='horizontalScrollTask' or task=='verticalScrollTask':
                  

            if len(CNNEvent)>0:
                if 1 in CNNEvent:
                    if 0 not in CNNEvent :
                            return True,CNNEvent
                    return False,CNNEvent
                return False,CNNEvent
            return False,CNNEvent
                    
        elif task=='tapTask':
            #print("Tap False?",len(np.where(CNNEvent==1)[0]))
            if len(CNNEvent)>0:
                    if 1 not in CNNEvent :
                            if 0 in CNNEvent:
                                    return True,CNNEvent
                            return False,CNNEvent
                    return False,CNNEvent
            return False,CNNEvent
    #####


    import numpy as np

    TotalCount=0
    SuccessCount=0
    DefaultSuccessCount=0
    DetailString=""

    TapDefaultSuccess=0
    TapFirstTouchSuccess=0
    TapEndTouchSuccess=0
    TapMyTapSuccess=0
    
    TapAllAfterCNN=0
    HPanAllAfterCNN=0
    VPanAllAfterCNN=0
    SwipeAllAfterCNN=0

    TapTotal=0
    HPanTotal=0
    VPanTotal=0
    SwipeTotal=0



    SwipeImproveTotal=0
    SwipeImprovebyNoPanNoTap=0
    SwipeImprovebyNoPanHaveTap=0
    SwipeImprovebyHavePanHaveTap=0

    HPanImproveTotal=0
    HPanImprovebyNoPanNoTap=0
    HPanImprovebyNoPanHaveTap=0
    HPanImprovebyHavePanHaveTap=0

    VPanImproveTotal=0
    VPanImprovebyNoPanNoTap=0
    VPanImprovebyNoPanHaveTap=0
    VPanImprovebyHavePanHaveTap=0

    TapImproveTotal=0
    TapImprovebyNoPanNoTap=0
    TapImprovebyHavePanNoTap=0
    TapImprovebyHavePanHaveTap=0


    #####Task 分類用 Validation_Data 因為有內差 。  Tap優化用 Validation_Data_2 因為沒有內差

    TapSingle=0
    TapMulti=0
    SwipeSingle=0
    SwipeMulti=0
    HPanSingle=0
    HPanMulti=0
    VPanSingle=0
    VPanMulti=0


    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        MikeCheck_SingleFinger_CNNTapRecongized=0
        MikeCheck_MultiFinger_CNNTapRecongized=0
        MikeCheck_SingleFinger_DefaultTapRecongized=0
        MikeCheck_MultiFinger_DefaultTapRecongized=0
        MikeCheck_SingleFinger_Num=0
        MikeCheck_MultiFinger_Num=0

        for iTrial in range(len(Validation_Data[task]['trials'])):
            TotalCount=TotalCount+1
            

            CNNSuccess,CNNEvent=JsonToCube_NoInterpolation_DynamicTime_OnTrial_BasedSimulator(Validation_Data[task]['trials'][iTrial],task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,ModelDict)
            

            


            if task=='swipeTask':
                if len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])==1:
                    MikeCheck_SingleFinger_Num=MikeCheck_SingleFinger_Num+1
                    if 0 not in CNNEvent:
                        if 1 in CNNEvent:
                            MikeCheck_SingleFinger_CNNTapRecongized=MikeCheck_SingleFinger_CNNTapRecongized+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                            MikeCheck_SingleFinger_DefaultTapRecongized=MikeCheck_SingleFinger_DefaultTapRecongized+1

                elif len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])>1:

                    MikeCheck_MultiFinger_Num=MikeCheck_MultiFinger_Num+1
                    if 0 not in CNNEvent:
                        if 1 in CNNEvent:
                            MikeCheck_MultiFinger_CNNTapRecongized=MikeCheck_MultiFinger_CNNTapRecongized+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                            MikeCheck_MultiFinger_DefaultTapRecongized=MikeCheck_MultiFinger_DefaultTapRecongized+1


                SwipeTotal=SwipeTotal+1

                if CNNSuccess==True:
                    SwipeAllAfterCNN=SwipeAllAfterCNN+1

                if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                DefaultSuccessCount=DefaultSuccessCount+1
                        else:
                            if CNNSuccess==True: 
                                SwipeImproveTotal=SwipeImproveTotal+1
                                SwipeImprovebyNoPanNoTap=SwipeImprovebyNoPanNoTap+1
                                ##Improve by No tap no pan

                else:
                    if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                        if CNNSuccess==True: 
                            SwipeImproveTotal=SwipeImproveTotal+1
                            SwipeImprovebyHavePanHaveTap=SwipeImprovebyHavePanHaveTap+1
                           
                            ##Improve by have tap have pan

                    else:
                        if CNNSuccess==True: 
                            SwipeImproveTotal=SwipeImproveTotal+1
                            SwipeImprovebyNoPanHaveTap=SwipeImprovebyNoPanHaveTap+1
                            ##Improve by have tap no pan 


            elif task=='horizontalScrollTask':
                if len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])==1:
                    MikeCheck_SingleFinger_Num=MikeCheck_SingleFinger_Num+1
                    if 0 not in CNNEvent:
                        if 1 in CNNEvent:
                            MikeCheck_SingleFinger_CNNTapRecongized=MikeCheck_SingleFinger_CNNTapRecongized+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                            MikeCheck_SingleFinger_DefaultTapRecongized=MikeCheck_SingleFinger_DefaultTapRecongized+1

                elif len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])>1:

                    MikeCheck_MultiFinger_Num=MikeCheck_MultiFinger_Num+1
                    if 0 not in CNNEvent:
                        if 1 in CNNEvent:
                            MikeCheck_MultiFinger_CNNTapRecongized=MikeCheck_MultiFinger_CNNTapRecongized+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                            MikeCheck_MultiFinger_DefaultTapRecongized=MikeCheck_MultiFinger_DefaultTapRecongized+1

                HPanTotal=HPanTotal+1
                if CNNSuccess==True:
                    HPanAllAfterCNN=HPanAllAfterCNN+1
                if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                DefaultSuccessCount=DefaultSuccessCount+1
                        else:
                            if CNNSuccess==True: 
                                HPanImproveTotal=HPanImproveTotal+1
                                HPanImprovebyNoPanNoTap=HPanImprovebyNoPanNoTap+1
                                ##Improve by No tap no pan

                else:
                    if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                        if CNNSuccess==True: 
                            HPanImproveTotal=HPanImproveTotal+1
                            HPanImprovebyHavePanHaveTap=HPanImprovebyHavePanHaveTap+1
                           
                            ##Improve by have tap have pan

                    else:
                        if CNNSuccess==True: 
                            HPanImproveTotal=HPanImproveTotal+1
                            HPanImprovebyNoPanHaveTap=HPanImprovebyNoPanHaveTap+1
                            ##Improve by have tap no pan 


            elif task=='verticalScrollTask':
                if len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])==1:
                    MikeCheck_SingleFinger_Num=MikeCheck_SingleFinger_Num+1
                    if 0 not in CNNEvent:
                        if 1 in CNNEvent:
                            MikeCheck_SingleFinger_CNNTapRecongized=MikeCheck_SingleFinger_CNNTapRecongized+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                            MikeCheck_SingleFinger_DefaultTapRecongized=MikeCheck_SingleFinger_DefaultTapRecongized+1

                elif len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])>1:

                    MikeCheck_MultiFinger_Num=MikeCheck_MultiFinger_Num+1
                    if 0 not in CNNEvent:
                        if 1 in CNNEvent:
                            MikeCheck_MultiFinger_CNNTapRecongized=MikeCheck_MultiFinger_CNNTapRecongized+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                            MikeCheck_MultiFinger_DefaultTapRecongized=MikeCheck_MultiFinger_DefaultTapRecongized+1

                VPanTotal=VPanTotal+1
                if CNNSuccess==True:
                    VPanAllAfterCNN=VPanAllAfterCNN+1
                if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                DefaultSuccessCount=DefaultSuccessCount+1
                        else:
                            if CNNSuccess==True: 
                                VPanImproveTotal=VPanImproveTotal+1
                                VPanImprovebyNoPanNoTap=VPanImprovebyNoPanNoTap+1
                                ##Improve by No tap no pan

                else:
                    if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                        if CNNSuccess==True: 
                            VPanImproveTotal=VPanImproveTotal+1
                            VPanImprovebyHavePanHaveTap=VPanImprovebyHavePanHaveTap+1
                           
                            ##Improve by have tap have pan

                    else:
                        if CNNSuccess==True: 
                            VPanImproveTotal=VPanImproveTotal+1
                            VPanImprovebyNoPanHaveTap=VPanImprovebyNoPanHaveTap+1
                            ##Improve by have tap no pan 

            elif task=='tapTask':
                if len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])==1:
                    MikeCheck_SingleFinger_Num=MikeCheck_SingleFinger_Num+1
                    if 0 in CNNEvent:
                        if 1 not in CNNEvent:
                            MikeCheck_SingleFinger_CNNTapRecongized=MikeCheck_SingleFinger_CNNTapRecongized+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
                            MikeCheck_SingleFinger_DefaultTapRecongized=MikeCheck_SingleFinger_DefaultTapRecongized+1

                elif len(Validation_Data[task]['trials'][iTrial]["rawTouchTracks"])>1:

                    MikeCheck_MultiFinger_Num=MikeCheck_MultiFinger_Num+1
                    if 0 in CNNEvent:
                        if 1 not in CNNEvent:
                            MikeCheck_MultiFinger_CNNTapRecongized=MikeCheck_MultiFinger_CNNTapRecongized+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
                            MikeCheck_MultiFinger_DefaultTapRecongized=MikeCheck_MultiFinger_DefaultTapRecongized+1

                TapTotal=TapTotal+1
                if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                                DefaultSuccessCount=DefaultSuccessCount+1
                        else:
                            if CNNSuccess==True: 
                                TapImproveTotal=TapImproveTotal+1
                                TapImprovebyNoPanNoTap=TapImprovebyNoPanNoTap+1
                                ##Improve by No tap no pan

                else:
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                        if CNNSuccess==True: 
                            TapImproveTotal=TapImproveTotal+1
                            TapImprovebyHavePanHaveTap=TapImprovebyHavePanHaveTap+1
                           
                            ##Improve by have tap have pan

                    else:
                        if CNNSuccess==True: 
                            TapImproveTotal=TapImproveTotal+1
                            TapImprovebyHavePanNoTap=TapImprovebyHavePanNoTap+1
                            ##Improve by no tap have pan 

                if CNNSuccess==True:
                    TapAllAfterCNN=TapAllAfterCNN+1
                    defaultTap,firsttouch,endedtouch,MyTap=VerifyTap(Validation_Data_2[task]['trials'][iTrial])
                    TapDefaultSuccess=TapDefaultSuccess+defaultTap
                    TapMyTapSuccess=TapMyTapSuccess+MyTap
                    TapFirstTouchSuccess=TapFirstTouchSuccess+firsttouch
                    TapEndTouchSuccess=TapEndTouchSuccess+endedtouch


            if CNNSuccess==True:

                SuccessCount=SuccessCount+1
        
        #print(task,ValidIndex,"Single ",MikeCheck_SingleFinger_DefaultTapRecongized," / ",MikeCheck_SingleFinger_Num," vs ",MikeCheck_SingleFinger_CNNTapRecongized," / ",MikeCheck_SingleFinger_Num," Multi ",MikeCheck_MultiFinger_DefaultTapRecongized," / ",MikeCheck_MultiFinger_Num," vs ",MikeCheck_MultiFinger_CNNTapRecongized," / ",MikeCheck_MultiFinger_Num,)
        print(task,"Single ",MikeCheck_SingleFinger_DefaultTapRecongized," / ",MikeCheck_SingleFinger_Num," vs ",MikeCheck_SingleFinger_CNNTapRecongized," / ",MikeCheck_SingleFinger_Num," Multi ",MikeCheck_MultiFinger_DefaultTapRecongized," / ",MikeCheck_MultiFinger_Num," vs ",MikeCheck_MultiFinger_CNNTapRecongized," / ",MikeCheck_MultiFinger_Num,)
        

        if MikeCheck_SingleFinger_Num>0:
            if task =='tapTask':
               
                #TapSingle=MikeCheck_SingleFinger_CNNTapRecongized/MikeCheck_SingleFinger_Num
                TapSingle=MikeCheck_SingleFinger_DefaultTapRecongized/MikeCheck_SingleFinger_Num
            elif task=='swipeTask':
                
                #SwipeSingle=MikeCheck_SingleFinger_CNNTapRecongized/MikeCheck_SingleFinger_Num
                SwipeSingle=MikeCheck_SingleFinger_DefaultTapRecongized/MikeCheck_SingleFinger_Num

            elif task=='horizontalScrollTask':
                #HPanSingle=MikeCheck_SingleFinger_CNNTapRecongized/MikeCheck_SingleFinger_Num
                HPanSingle=MikeCheck_SingleFinger_DefaultTapRecongized/MikeCheck_SingleFinger_Num
               
            elif task=='verticalScrollTask':
                #VPanSingle=MikeCheck_SingleFinger_CNNTapRecongized/MikeCheck_SingleFinger_Num
                VPanSingle=MikeCheck_SingleFinger_DefaultTapRecongized/MikeCheck_SingleFinger_Num
               
        else:
            TapSingle=1234
            SwipeSingle=1234
            HPanSingle=1234
            VPanSingle=1234


        if MikeCheck_MultiFinger_Num>0:
            if task =='tapTask':
               
                TapMulti=MikeCheck_MultiFinger_CNNTapRecongized/MikeCheck_MultiFinger_Num;
                #TapMulti=MikeCheck_MultiFinger_DefaultTapRecongized/MikeCheck_MultiFinger_Num;
                
            elif task=='swipeTask':
           
                SwipeMulti=MikeCheck_MultiFinger_CNNTapRecongized/MikeCheck_MultiFinger_Num;
                
                #SwipeMulti=MikeCheck_MultiFinger_DefaultTapRecongized/MikeCheck_MultiFinger_Num;

            elif task=='horizontalScrollTask':
               
                HPanMulti=MikeCheck_MultiFinger_CNNTapRecongized/MikeCheck_MultiFinger_Num;
                #HPanMulti=MikeCheck_MultiFinger_DefaultTapRecongized/MikeCheck_MultiFinger_Num;
            elif task=='verticalScrollTask':
                
                VPanMulti=MikeCheck_MultiFinger_CNNTapRecongized/MikeCheck_MultiFinger_Num;
                #VPanMulti=MikeCheck_MultiFinger_DefaultTapRecongized/MikeCheck_MultiFinger_Num;
        else:
            TapMulti=1234
            SwipeMulti=1234
            HPanMulti=1234
            VPanMulti=1234
   

    ValidData=""
   
    print("---Improve By---","TapTask: ",TapImprovebyHavePanHaveTap,TapImprovebyNoPanNoTap,TapImprovebyHavePanNoTap,TapImproveTotal,"---Improve By---")
    print("---Improve By---","SwipeTask: ",SwipeImprovebyHavePanHaveTap,SwipeImprovebyNoPanNoTap,SwipeImprovebyNoPanHaveTap,SwipeImproveTotal,"---Improve By---")
    print("---Improve By---","HPanTask: ",HPanImprovebyHavePanHaveTap,HPanImprovebyNoPanNoTap,HPanImprovebyNoPanHaveTap,HPanImproveTotal,"---Improve By---")
    print("---Improve By---","VPanTask: ",VPanImprovebyHavePanHaveTap,VPanImprovebyNoPanNoTap,VPanImprovebyNoPanHaveTap,VPanImproveTotal,"---Improve By---")
    

    if TapAllAfterCNN!=0:
        print("SuccessRate:",DefaultSuccessCount/TotalCount," vs ",SuccessCount/TotalCount," Confusion: ", " TapTask ",TapAllAfterCNN," ",TapTotal," SwipeTask ", SwipeAllAfterCNN,"  ",SwipeTotal," HPanTask ", HPanAllAfterCNN,"  ",HPanTotal," VPanTask ", VPanAllAfterCNN,"  ",VPanTotal,"   After CNN Tap ", TapDefaultSuccess/TapAllAfterCNN,TapFirstTouchSuccess/TapAllAfterCNN,TapEndTouchSuccess/TapAllAfterCNN," vs ",  TapMyTapSuccess/TapAllAfterCNN)

        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,TapDefaultSuccess/TapAllAfterCNN,TapFirstTouchSuccess/TapAllAfterCNN,TapEndTouchSuccess/TapAllAfterCNN,TapMyTapSuccess/TapAllAfterCNN,TapSingle,TapMulti,SwipeSingle,SwipeMulti,HPanSingle,HPanMulti,VPanSingle,VPanMulti

    else:
        print("SuccessRate:",DefaultSuccessCount/TotalCount," vs ",SuccessCount/TotalCount," Confusion: ", " TapTask ",TapAllAfterCNN,"  ",TapTotal," SwipeTask ", SwipeAllAfterCNN,"  ",SwipeTotal," HPanTask ", HPanAllAfterCNN,"  ",HPanTotal," VPanTask ", VPanAllAfterCNN,"  ",VPanTotal,"   After CNN Tap : NO Success")
        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,1234567,1234567,1234567,1234567,TapSingle,TapMulti,SwipeSingle,SwipeMulti,HPanSingle,HPanMulti,VPanSingle,VPanMulti


def HaveTouchPoint(TaskData):
    for iFinger in range(len(TaskData["rawTouchTracks"])):
        if len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])>0:
            return True
    return False
        



def evaluate_FixedTime(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,Validation_Data_2):
    

    #每個event 預測都用固定的 time-grid
    def VerifyTap(TaskData):
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

                FingerCenterDict=dict()

                PossibleX=list()
                PossibleY=list()

                for iFinger in range(len(OutputData["rawTouchTracks"])):
                    
                    CandidateData=list()
                    for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                         
                         if iPoint==0 or iPoint==1:
                             accelerate=0
                         else:
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
                                 LabelFalse(OutputData,iFinger,iPoint-2)
                             
                             if (AverageX2-positionX3)*(AverageX2-positionX3)+(AverageY2-positionY3)*(AverageY2-positionY3)>TapAllowableMovement*TapAllowableMovement:
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

                        largestCluster=np.argmax(np.bincount(ChooseLabel))
                        
                        ThisClusterFinalPoint=list()
                        
                        for i in range(len(CandidateData)):
                            CheckPoint=CandidateData[i][0]
                            
                            if(ChooseLabel[i]!=largestCluster):
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
                            LabelFalse(OutputData,iFinger,ThisClusterFinalPoint[i][0])
                            if distance<=Distance:
                                Distance=distance
                                SelectedPoint=ThisClusterFinalPoint[i][0]
                        OutputData["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['label']=True
                        
                        FingerCenterDict[str(iFinger)]=[Xave,Yave]
                        PossibleX.append(Xave)
                        PossibleY.append(Yave)
                    FingerCenterDict[str(iFinger)]=[positionx,positiony]  
                    PossibleX.append(positionx)
                    PossibleY.append(positiony)

                DataPointNum=0
                for iFinger in range(len(OutputData["rawTouchTracks"])):
                    for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                         if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                            DataPointNum=DataPointNum+1

                return OutputData,[np.mean(PossibleX),np.mean(PossibleY)]



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
    
        DefaultSuccess=0
        FirstTouchSuccess=0
        EndedTouchSuccess=0
        OptimzerSuccess=0
        defaultfalse=0


        # RecognizedTapTrials=RecognizedTapTrials
        TrialToOptimzer=AllTaskValidIndex[task][i]
        #print(AllTaskValidIndex[task],TrialToOptimzer,len(Validation_Data_2[task]['trials']))
        #TaskData=Validation_Data_2[task]['trials'][i]

        OptimizedData=LabelTrue(TaskData)
        OptimizedData,OutPutPoint=LabelByMyAlgorithm(OptimizedData)

        FilteredOptimizedData=FilteredJsonOneTrial(OptimizedData)

       
        TargetX=TaskData["targetFrame"][0][0] +TaskData["targetFrame"][1][0]*0.5
        TargetY=TaskData["targetFrame"][0][1] + TaskData["targetFrame"][1][1]*0.5

        if tv.TapTask_SuccessVerify(FilteredOptimizedData):

                OptimzerSuccess=1


        if len(TaskData['tapEvents'])>0:
            #print(TaskData['tapEvents'][0]['locationOfTouchAtIndex'])
            
            Y=TaskData['tapEvents'][0]['location'][0]
            X=Device_info[0]-TaskData['tapEvents'][0]['location'][1]

            tempX=TaskData['tapEvents'][0]['locationOfTouchAtIndex']['0'][0]
            tempY=TaskData['tapEvents'][0]['locationOfTouchAtIndex']['0'][1]
            #print(X,Y," vs ",TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][0],TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex']['0'][1])

           
            if (abs(X - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(Y- TargetY) >TaskData["targetFrame"][1][1]*0.5):
                    # cout << "First touch point is not correct" << endl;

            #print((NewTaskData["targetFrame"][0][0]),(NewTaskData["targetFrame"][0][1]),(NewTaskData["targetFrame"][1][0]),(NewTaskData["targetFrame"][1][1]),NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0],NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] )
                #print("First Touch")
                print("BasedPanEventLocationFalse","Target",TargetX,TargetY," tapevent: ",X,Y," locationOfTouchAtIndex: ",tempX,tempY,"orignaltaplocation: ",TaskData['tapEvents'][0]['location'][0],TaskData['tapEvents'][0]['location'][1]," DeviceInfo: ",Device_info[0],Device_info[1])

                Y2=Device_info[1]-TaskData['tapEvents'][0]['location'][0]
                X2=TaskData['tapEvents'][0]['location'][1]
                if (abs(X2 - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(Y2- TargetY) >TaskData["targetFrame"][1][1]*0.5):
            
                    print("BasedPanEventLocationFalse222","Target",TargetX,TargetY," tapevent: ",X2,Y2," locationOfTouchAtIndex: ",tempX,tempY,"orignaltaplocation: ",TaskData['tapEvents'][0]['location'][0],TaskData['tapEvents'][0]['location'][1]," DeviceInfo: ",Device_info[0],Device_info[1])

                    DefaultSuccess=0
                else:
                    DefaultSuccess=1
            else:
                DefaultSuccess=1
        else:
            DefaultSuccess=0
            print("BasedPanEventLocationFalse: No TapEventQQ")


        FirstTouchX=TaskData["rawTouchTracks"][0]["rawTouches"][0]["location"][0]
        FirstTouchY=TaskData["rawTouchTracks"][0]["rawTouches"][0]["location"][1]
        EndedTouchX=TaskData["rawTouchTracks"][0]["rawTouches"][len(TaskData["rawTouchTracks"][0]["rawTouches"])-1]["location"][0]
        EndedTouchY=TaskData["rawTouchTracks"][0]["rawTouches"][len(TaskData["rawTouchTracks"][0]["rawTouches"])-1]["location"][1]

        FirstTouchSuccess=0
        EndedTouchSuccess=0
        
        if (abs(FirstTouchX - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(FirstTouchY-TargetY) >TaskData["targetFrame"][1][1]*0.5):
                
            
            FirstTouchSuccess=0
        else:
            FirstTouchSuccess=1

        if (abs(EndedTouchX - TargetX) > TaskData["targetFrame"][1][0]*0.5)|(abs(EndedTouchY- TargetY) >TaskData["targetFrame"][1][1]*0.5):
                
            
            EndedTouchSuccess=0
        else:
            EndedTouchSuccess=1



        return  DefaultSuccess,FirstTouchSuccess,EndedTouchSuccess,OptimzerSuccess


    #TapVerify End
    def JsonToCube_NoInterpolation_FixedTime_OnTrial(JsonDataOneTrial,task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,ModelDict):

        def AdjustPrediction(pred):
            if pred[0][0]>0.999:
                    return 0
            else:
                    return 1

        def ModelChoose(TimeGrid,ModelDict):

            return ModelDict[TimeGrid],TimeGrid,10
            #return ModelDict[0.05],0.05,10

        def TimeInRange(PreviousEventTime,PresentEventTime,TouchPhaseTime):
            for t in TouchPhaseTime:
                if (t>=PreviousEventTime) & (t<=PresentEventTime):
                    return True
            return False
        
        import numpy as np
        # GridNum_InX=int(np.ceil(Device_info[0]/GridSize))+10
        # GridNum_InY=int(np.ceil(Device_info[1]/GridSize))+10
        
        
        #print("ArraySize",GridNum_InX,GridNum_InY,TimeFrameNum,Channel)
        TimeGrid=float(tGrid)
        AllDataX=list()
        AllDataY=list()
        Task=0
        
        if task=='tapTask':
            Task=0;
        else:
            Task=1;

            

        ###find Began

        GridNum_InX=int(np.ceil(2*MaxSpeed/GridSize))+1
        GridNum_InY=int(np.ceil(2*MaxSpeed/GridSize))+1
        Channel=1


        PredictModel,TimeGrid,MaxSpeed=ModelChoose(TimeGrid,ModelDict)
        
        predictX=list()
        predictY=list()
        DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
        
        

      
        BaseTime=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
        #print("EventTime ",began_T," BaseTime ",BaseTime," RecognitionTime ",began_T-BaseTime)
        for iFinger in range(len(JsonDataOneTrial["rawTouchTracks"])):
            for iPoint in range(len(JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"])):

                Point_0=JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][0]
                #Point_0=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]
                Point=JsonDataOneTrial["rawTouchTracks"][iFinger]["rawTouches"][iPoint]

                
                if (BaseTime<=Point['timestamp']) &  (BaseTime+TimeGrid*TimeFrameNum>=Point['timestamp']):
                #if (began_T-TimeGrid*TimeFrameNum<=Point['timestamp']) & (began_T>=Point['timestamp']):

                    
                    Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint_FixedResponseTime(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                    #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedFirstPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                     
                    #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_AllBegan(Point,BaseTime,GridSize,TimeGrid,Device_info,MaxSpeed)
                    
                    if Time_In<TimeFrameNum:
                        #Time_In=TimeFrameNum-1
                        DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                        # if Point['phase']=='ended':
                        #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

    #######Matrix Ready Go Predict
        predictX.append(DataMatrix)
        predictY.append(Task)


        y_test = to_categorical(np.array(predictY), num_classes=2)

        
        X_test  = np.array(predictX).reshape(-1, np.array(predictX).shape[1], np.array(predictX).shape[2], np.array(predictX).shape[3], 1)


        pred = PredictModel.predict(X_test)
            #print("pred",pred)
        prediction = np.argmax(pred, axis=1)[0]
            #print("pred1",prediction)
        touchBeganPredict=str(prediction)

       

        #print(task,"EventNum: ", PredictNum ,len(JsonDataOneTrial['tapEvents']),len(JsonDataOneTrial['panEvents'])," vs ",(0 in CNNEvent),(1 in CNNEvent),CNNEvent)
        ##每個event 的predict 結束 
        #來驗證tap optimzer
        #print("Predict",len(CNNEvent),len(ProcssTimeList))
        if task=='swipeTask' or task=='horizontalScrollTask' or task=='verticalScrollTask':
            if prediction==1:
                return True
            else:
                return False

           
                    
        elif task=='tapTask':
            if prediction==0:
                return True
            else:
                return False
           
    #####


    import numpy as np

    TotalCount=0
    SuccessCount=0
    DefaultSuccessCount=0
    DetailString=""

    TapDefaultSuccess=0
    TapMyTapSuccess=0
    TapFirstTouchSuccess=0
    TapEndTouchSuccess=0
    
    TapAllAfterCNN=0
    HPanAllAfterCNN=0
    VPanAllAfterCNN=0
    SwipeAllAfterCNN=0

    TapTotal=0
    HPanTotal=0
    VPanTotal=0
    SwipeTotal=0





    #####Task 分類用 Validation_Data 因為有內差 。  Tap優化用 Validation_Data_2 因為沒有內差
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        for iTrial in range(len(Validation_Data[task]['trials'])):
            TotalCount=TotalCount+1
            
            CNNSuccess=JsonToCube_NoInterpolation_FixedTime_OnTrial(Validation_Data[task]['trials'][iTrial],task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,ModelDict)
            
            if task=='swipeTask':
                SwipeTotal=SwipeTotal+1
            elif task=='horizontalScrollTask':
                HPanTotal=HPanTotal+1
            elif task=='verticalScrollTask':
                VPanTotal=VPanTotal+1
            elif task=='tapTask':
                    TapTotal=TapTotal+1

            if HaveTouchPoint(Validation_Data[task]['trials'][iTrial]):

            #if True:
                if task=='swipeTask':
                   
                    if CNNSuccess==True:
                        SwipeAllAfterCNN=SwipeAllAfterCNN+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                            if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                    DefaultSuccessCount=DefaultSuccessCount+1


                elif task=='horizontalScrollTask':
                   
                    if CNNSuccess==True:
                        HPanAllAfterCNN=HPanAllAfterCNN+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                            if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                    DefaultSuccessCount=DefaultSuccessCount+1


                elif task=='verticalScrollTask':
                    
                    if CNNSuccess==True:
                        VPanAllAfterCNN=VPanAllAfterCNN+1
                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                            if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                    DefaultSuccessCount=DefaultSuccessCount+1

                elif task=='tapTask':
                    
                    if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
                            if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                                    DefaultSuccessCount=DefaultSuccessCount+1

                    if CNNSuccess==True:
                        TapAllAfterCNN=TapAllAfterCNN+1
                        defaultTap,firsttouch,endedtouch,MyTap=VerifyTap(Validation_Data_2[task]['trials'][iTrial])
                        TapDefaultSuccess=TapDefaultSuccess+defaultTap
                        TapMyTapSuccess=TapMyTapSuccess+MyTap
                        TapFirstTouchSuccess=TapFirstTouchSuccess+firsttouch
                        TapEndTouchSuccess=TapEndTouchSuccess+endedtouch

               
                if CNNSuccess==True:

                    SuccessCount=SuccessCount+1
    

    ValidData=""
   
   
    if TapAllAfterCNN!=0:
        print("SuccessRate:",DefaultSuccessCount/TotalCount," vs ",SuccessCount/TotalCount," Confusion: ", " TapTask ",TapAllAfterCNN," ",TapTotal," SwipeTask ", SwipeAllAfterCNN,"  ",SwipeTotal," HPanTask ", HPanAllAfterCNN,"  ",HPanTotal," VPanTask ", VPanAllAfterCNN,"  ",VPanTotal,"   After CNN Tap ", TapDefaultSuccess/TapAllAfterCNN,TapFirstTouchSuccess/TapAllAfterCNN,TapEndTouchSuccess/TapAllAfterCNN," vs ",  TapMyTapSuccess/TapAllAfterCNN)

        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,TapDefaultSuccess/TapAllAfterCNN,TapFirstTouchSuccess/TapAllAfterCNN,TapEndTouchSuccess/TapAllAfterCNN,TapMyTapSuccess/TapAllAfterCNN

    else:
        print("SuccessRate:",DefaultSuccessCount/TotalCount," vs ",SuccessCount/TotalCount," Confusion: ", " TapTask ",TapAllAfterCNN,"  ",TapTotal," SwipeTask ", SwipeAllAfterCNN,"  ",SwipeTotal," HPanTask ", HPanAllAfterCNN,"  ",HPanTotal," VPanTask ", VPanAllAfterCNN,"  ",VPanTotal,"   After CNN Tap : NO Success")
        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,1234567,1234567,1234567,1234567



  
def Visualize2(Data,Y,channel):
    import matplotlib.pyplot as plt
    
    # if Y==0:
    #     task='Tap'
    # elif Y==1:
    #     task='swipe'
    # elif Y==2:
    #     task='horizontalScroll'
    # elif Y==3:
    #     task='verticalScroll'
    if Y==0:
        task='Tap'
    elif Y==1:
        task='Pan'
    for t in range(len(Data[0][0])):
        X=list()
        Y=list()
        for indexx in range(len(Data)):
            for indexy in range(len(Data[0])):
                if Data[indexx][indexy][t][channel]>0:
                    X.append(indexx)
                    Y.append(indexy)
        plt.subplot(len(Data[0][0])/5,5,t+1)
        plt.scatter(X,Y)
        plt.xlim(0,len(Data))
        plt.ylim(0,len(Data[0]))
        plt.title(task)
            #plt.legend(loc='upper right')
    plt.show()






if __name__ == '__main__':
    User=sys.argv[1]
    ResponseMode=sys.argv[2]
    TrainingMode=sys.argv[3]
    startCV=int(sys.argv[4])
    endCV=int(sys.argv[5])

        
    AllCrossValidationSuccess=list()
    Default_AllCrossValidationSuccess=list()
            
    TapDefaultSuccessList=list()
    TapMyalgoSuccessList=list()
    TapFirstSuccessList=list()
    TapEndSuccessList=list()

    from datetime import datetime
    TimeNow=datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    #tGrid=float(sys.argv[2])

    sns.set_style('white')

    from sklearn.metrics import confusion_matrix, accuracy_score

    # Hyper Parameter
    batch_size = 10
    epochs = 30

    # Set up TensorBoard
    tensorboard = TensorBoard(batch_size=batch_size)


    # ANNY-NOTE: input path
    path='StudyData/NewData/'+User+'/'

    # ANNY-NOTE: output path
    WritingFileName='Result/Classify/'+User+"_"+str(sys.argv[6])+"_3DCNN_"+TimeNow+'.txt'
    
    #f=open(WritingFileName,'a')

    print("Open File:",WritingFileName)
    ## ANNY-NOTE: Maybe not used

    from datetime import datetime
    TimeNow=datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    #WritingFileName='Result/Classify/'+User+"_ThresholdBased_"+TimeNow+'.txt'
    #WritingFileNamePara='Parameters/Classify/'+User+"_ThresholdBased_"+TimeNow+'.txt'

    #f=open(WritingFileName,'a')

    #ff=open(WritingFileNamePara,'a')
    files=listdir(path)
    file=list()
    for i in range(len(files)):
        if files[i][-4:]=='json':
            file.append(files[i])
    #for cvIndex in range(1):

    #rc=tGrid*10
    if ResponseMode=='Fixed':
        rc=float(sys.argv[6])*10   #比快
    else:
        rc=5000   #為了train 所有evnet 

    data_NoCrossValidation,Device_info=ReadData(path,file)
    if TrainingMode!='2':
        data_NoCrossValidation_RecognitionTime=RecognitionTimeProcess_Interpolation(data_NoCrossValidation,rc,1)
        data_NoCrossValidation_RecognitionTime_NoInterpolation=RecognitionTimeProcess_NoInterpolation(data_NoCrossValidation,rc)
    else:
        data_NoCrossValidation_RecognitionTime=RecognitionTimeProcess_Interpolation(data_NoCrossValidation,rc,1)
        data_NoCrossValidation_RecognitionTime_NoInterpolation=RecognitionTimeProcess_NoInterpolation(data_NoCrossValidation,rc)

    DefualtTap=list()

    MyTap=list()
    ClassifySuccessList=list()

    TapSingleList=list()
    TapMultiList=list()
    SwipeSingleList=list()
    SwipeMultiList=list()
    HPanSingleList=list()
    HPanMultiList=list()
    VPanSingleList=list()
    VPanMultiList=list()

    # crossValidation
    for cvIndex in range(startCV,endCV):
     
        
        cvIndex=cvIndex*9%100
        # validation or training
        if TrainingMode!='2':
            Training_Data,Validation_Data,ValidIndex,ValidTaskStartIndexArray,AllTaskValidIndex=CrossValidation(cvIndex,data_NoCrossValidation_RecognitionTime)
            Training_Data_2,Validation_Data_2,ValidIndex_2,ValidTaskStartIndexArray_2,AllTaskValidIndex_2=CrossValidation(cvIndex,data_NoCrossValidation_RecognitionTime_NoInterpolation)
            
        if TrainingMode=='2':
            
            Training_Data_2,Validation_Data_2,ValidIndex_2,ValidTaskStartIndexArray_2,AllTaskValidIndex_2=CrossValidation(cvIndex,data_NoCrossValidation_RecognitionTime_NoInterpolation)
            Training_Data,Validation_Data,ValidIndex,ValidTaskStartIndexArray,AllTaskValidIndex=CrossValidation(cvIndex,data_NoCrossValidation_RecognitionTime)

       

      
        if ResponseMode=='Dynamic':
            if TrainingMode=='1':
                MaxSpeed=10
                # windowsize
                DynamicTime=float(sys.argv[6])
                DisGrid=float(sys.argv[7])
                MaxSpeed=float(sys.argv[8])

                [TrainDataX,TrainDataY,RecordTrial]=JsonToCube_NoInterpolation(Training_Data,Device_info,DisGrid,10,MaxSpeed,DynamicTime)
                [ValidDataX,ValidDataY,RecordTrial]=JsonToCube_NoInterpolation(Validation_Data,Device_info,DisGrid,10,MaxSpeed,DynamicTime)



                X_train = TrainDataX.reshape(-1, TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1)
                X_test  = ValidDataX.reshape(-1, ValidDataX.shape[1], ValidDataX.shape[2], ValidDataX.shape[3], 1)
                y_train = to_categorical(TrainDataY, num_classes=2)
                y_test = to_categorical(ValidDataY, num_classes=2)

                print(TrainDataX.shape)
                optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
                #optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
                scheduler = ReduceLROnPlateau(monitor='val_acc', patience=3, verbose=1, factor=0.5, min_lr=1e-5)

                model = ThreeDCNN((TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1), 2)

                print("Training... cvindex: ",cvIndex," timegrid: ",DynamicTime)
                
                train(optimizer, scheduler)
                save_model(User,cvIndex,DynamicTime,'Dynamic')

                DefaultSuccessCount=0
                TrialCount=0

                for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
   
                    for iTrial in range(len(Validation_Data[task]['trials'])):
                        TrialCount=TrialCount+1
                        if task=='swipeTask' or task=='horizontalScrollTask' or task=='verticalScrollTask':
                            if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                                    if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                            DefaultSuccessCount=DefaultSuccessCount+1
                        elif task=='tapTask':
                            #print("Tap False?",len(np.where(CNNEvent==1)[0]))
                            if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
                                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                                            DefaultSuccessCount=DefaultSuccessCount+1
                evaluate(cvIndex,AllTaskValidIndex,DefaultSuccessCount/TrialCount,RecordTrial,DynamicTime)
    

        elif ResponseMode=='Fixed':
            if TrainingMode=='1':
                FixedTimeGrid=float(sys.argv[6])
                #DynamicTime=float(tGrid)
                DisGrid=float(sys.argv[7])
                MaxSpeed=float(sys.argv[8])
               
                

                [TrainDataX,TrainDataY]=JsonToCube_NoInterpolation_FixedResponseTime(Training_Data,Device_info,DisGrid,10,MaxSpeed,FixedTimeGrid)
                [ValidDataX,ValidDataY]=JsonToCube_NoInterpolation_FixedResponseTime(Validation_Data,Device_info,DisGrid,10,MaxSpeed,FixedTimeGrid)


               

                X_train = TrainDataX.reshape(-1, TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1)
                X_test  = ValidDataX.reshape(-1, ValidDataX.shape[1], ValidDataX.shape[2], ValidDataX.shape[3], 1)
                y_train = to_categorical(TrainDataY, num_classes=2)
                y_test = to_categorical(ValidDataY, num_classes=2)





                #optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
                
                print(TrainDataX.shape)

                optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
                scheduler = ReduceLROnPlateau(monitor='val_acc', patience=3, verbose=1, factor=0.5, min_lr=1e-5)

                model = ThreeDCNN((TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1), 2)

               
                print("Training... cvindex: ",cvIndex," timegrid: ",FixedTimeGrid)

                # # print("Training...")
                
                train(optimizer, scheduler)
                save_model(User,cvIndex,FixedTimeGrid,'Fixed')
              
        elif ResponseMode=='Dynamic_Simulator':
            if TrainingMode=='1':
                MaxSpeed=10
                
                DynamicTime=float(sys.argv[6])
                DisGrid=float(sys.argv[7])
                MaxSpeed=float(sys.argv[8])

                [TrainDataX,TrainDataY,RecordTrial]=JsonToCube_NoInterpolation_Simulator(Training_Data,Device_info,DisGrid,10,MaxSpeed,DynamicTime)
                [ValidDataX,ValidDataY,RecordTrial]=JsonToCube_NoInterpolation_Simulator(Validation_Data,Device_info,DisGrid,10,MaxSpeed,DynamicTime)



                X_train = TrainDataX.reshape(-1, TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1)
                X_test  = ValidDataX.reshape(-1, ValidDataX.shape[1], ValidDataX.shape[2], ValidDataX.shape[3], 1)
                y_train = to_categorical(TrainDataY, num_classes=2)
                y_test = to_categorical(ValidDataY, num_classes=2)

                print(TrainDataX.shape)
                optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
                #optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
                scheduler = ReduceLROnPlateau(monitor='val_acc', patience=3, verbose=1, factor=0.5, min_lr=1e-5)

                model = ThreeDCNN((TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1), 2)

                print("Training... cvindex: ",cvIndex," timegrid: ",DynamicTime)
                
                train(optimizer, scheduler)
                save_model(User,cvIndex,DynamicTime,'Dynamic_Simulator')

                DefaultSuccessCount=0
                TrialCount=0

                for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
   
                    for iTrial in range(len(Validation_Data[task]['trials'])):
                        TrialCount=TrialCount+1
                        if task=='swipeTask' or task=='horizontalScrollTask' or task=='verticalScrollTask':
                            if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                                    if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                            DefaultSuccessCount=DefaultSuccessCount+1
                        elif task=='tapTask':
                            #print("Tap False?",len(np.where(CNNEvent==1)[0]))
                            if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
                                    if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                                            DefaultSuccessCount=DefaultSuccessCount+1
                evaluate(cvIndex,AllTaskValidIndex,DefaultSuccessCount/TrialCount,RecordTrial,DynamicTime)
    

        ##################Evaluation##############
        ##################Evaluation##############

        #####Default Recognizer########

        #
        
        if TrainingMode!='2':
            DefaultSuccessCount=0
            TrialCount=0

            TapTotal=0
            HPanTotal=0
            VPanTotal=0
            SwipeTotal=0

            TapSuccess=0
            HPanSuccess=0
            VPanSuccess=0
            SwipeSuccess=0


            for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:

                for iTrial in range(len(Validation_Data[task]['trials'])):
                    TrialCount=TrialCount+1
                    if task=='swipeTask':
                        SwipeTotal=SwipeTotal+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                                if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                        DefaultSuccessCount=DefaultSuccessCount+1
                                        SwipeSuccess=SwipeSuccess+1
                        

                    elif task=='horizontalScrollTask' :
                        HPanTotal=HPanTotal+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                                if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                        DefaultSuccessCount=DefaultSuccessCount+1
                                        HPanSuccess=HPanSuccess+1

                    elif task=='verticalScrollTask':
                        VPanTotal=VPanTotal+1
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                                if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                        DefaultSuccessCount=DefaultSuccessCount+1
                                        VPanSuccess=VPanSuccess+1
                                        


                    elif task=='tapTask':
                        TapTotal=TapTotal+1
                        #print("Tap False?",len(np.where(CNNEvent==1)[0]))
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
                                if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                                        DefaultSuccessCount=DefaultSuccessCount+1
                                        TapSuccess=TapSuccess+1

            print(User," cvIndex", cvIndex," Default Recognized!!: Tap: " ,TapSuccess,TapTotal," Swipe: ",SwipeSuccess,SwipeTotal," HPan: ", HPanSuccess,HPanTotal," VPan: ",VPanSuccess,VPanTotal)



       
        if ResponseMode=='Dynamic':
            GridSize=0.5
            MaxSpeed=10
            TimeFrameNum=10
            if TrainingMode=='0':
                DynamicTime=float(sys.argv[6])
                GridSize=float(sys.argv[7])
                MaxSpeed=float(sys.argv[8])
                ModelDict=dict()
                print("Validation....", User," cvIndex", cvIndex)
                #for t in [0.005,0.01,0.02,0.03,0.04,0.05]:
                #for t in [0.005,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]:
                for t in [DynamicTime]:
                    ModelDict[t]=load_model(User,cvIndex,t,'Dynamic')

                a,b,c,d,e,f=evaluate_DynamicTime(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,DynamicTime,Validation_Data_2)
                AllCrossValidationSuccess.append(b)
                Default_AllCrossValidationSuccess.append(a)
                if c!=1234567:
                    TapDefaultSuccessList.append(c)
                    TapFirstSuccessList.append(d)
                    TapEndSuccessList.append(e)
                    TapMyalgoSuccessList.append(f)


            if TrainingMode=='2':
                MaxSpeed=10
                DynamicTime=0.05
                [ValidDataX,ValidDataY,RecordTrial]=JsonToCube_NoInterpolation(Validation_Data_2,Device_info,0.25,10,MaxSpeed,DynamicTime)

                    
                for testindex in range(0,19):
               
                    Visualize2(ValidDataX[testindex],ValidDataY[testindex],0)
                    Visualize2(ValidDataX[-(testindex+1)],ValidDataY[-(testindex+1)],0)
                
                # testindex=testindex-10
                # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                # testindex=testindex-10
                # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
        elif ResponseMode=='Fixed':
            GridSize=0.5
            MaxSpeed=10
            TimeFrameNum=10
            if TrainingMode=='0':
                FixedTime=float(sys.argv[6])
                GridSize=float(sys.argv[7])
                MaxSpeed=float(sys.argv[8])
                ModelDict=dict()
                print("Validation....", User," cvIndex", cvIndex)
                #for t in [0.005,0.01,0.02,0.03,0.04,0.05]:
                #for t in [0.005,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]:
                for t in [FixedTime]:
                    ModelDict[t]=load_model(User,cvIndex,t,'Fixed')

                a,b,c,d,e,f=evaluate_FixedTime(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,FixedTime,Validation_Data_2)
                AllCrossValidationSuccess.append(b)
                Default_AllCrossValidationSuccess.append(a)
                if c!=1234567:
                    TapDefaultSuccessList.append(c)
                    TapFirstSuccessList.append(d)
                    TapEndSuccessList.append(e)
                    TapMyalgoSuccessList.append(f)


            if TrainingMode=='2':
                FixedTimeGrid=float(sys.argv[6])
                #DynamicTime=float(tGrid)
                DisGrid=float(sys.argv[7])
                MaxSpeed=float(sys.argv[8])
                
                #[ValidDataX,ValidDataY]=JsonToCube_NoInterpolation_FixedResponseTime(Validation_Data_2,Device_info,DisGrid,10,MaxSpeed,FixedTimeGrid)
                [ValidDataX,ValidDataY]=JsonToCube_NoInterpolation_FixedResponseTime(Validation_Data,Device_info,DisGrid,10,MaxSpeed,FixedTimeGrid)
                                

                for testindex in range(0,19):
               
                    Visualize2(ValidDataX[testindex],ValidDataY[testindex],0)
                    Visualize2(ValidDataX[-(testindex+1)],ValidDataY[-(testindex+1)],0)

        elif ResponseMode=='Dynamic_Simulator':
            GridSize=0.5
            MaxSpeed=10
            TimeFrameNum=10
            if TrainingMode=='0':
                DynamicTime=float(sys.argv[6])
                GridSize=float(sys.argv[7])
                MaxSpeed=float(sys.argv[8])
                ModelDict=dict()
                print("Validation....", User," cvIndex", cvIndex)
                #for t in [0.005,0.01,0.02,0.03,0.04,0.05]:
                #for t in [0.005,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]:
                for t in [DynamicTime]:
                    ModelDict[t]=load_model(User,cvIndex,t,'Dynamic_Simulator')

                a,b,c,d,e,f,TapSingle,TapMulti,SwipeSingle,SwipeMulti,HPanSingle,HPanMulti,VPanSingle,VPanMulti=evaluate_DynamicTime_BasedSimulator(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,DynamicTime,Validation_Data_2)
                AllCrossValidationSuccess.append(b)
                Default_AllCrossValidationSuccess.append(a)
                if c!=1234567:
                    TapDefaultSuccessList.append(c)
                    TapFirstSuccessList.append(d)
                    TapEndSuccessList.append(e)
                    TapMyalgoSuccessList.append(f)
                if TapSingle!=1234:
                    TapSingleList.append(TapSingle)
                if TapMulti!=1234:
                    TapMultiList.append(TapMulti)
                if SwipeSingle!=1234:
                    SwipeSingleList.append(SwipeSingle)
                if SwipeMulti!=1234:
                    SwipeMultiList.append(SwipeMulti)
                if HPanSingle!=1234:
                    HPanSingleList.append(HPanSingle)
                if HPanMulti!=1234:
                    HPanMultiList.append(HPanMulti)
                if VPanSingle!=1234:
                    VPanSingleList.append(VPanSingle)
                if VPanMulti!=1234:
                    VPanMultiList.append(VPanMulti)


            if TrainingMode=='2':
                MaxSpeed=10
                DynamicTime=0.05
                [ValidDataX,ValidDataY,RecordTrial]=JsonToCube_NoInterpolation(Validation_Data_2,Device_info,0.25,10,MaxSpeed,DynamicTime)

                    
                for testindex in range(0,19):
               
                    Visualize2(ValidDataX[testindex],ValidDataY[testindex],0)
                    Visualize2(ValidDataX[-(testindex+1)],ValidDataY[-(testindex+1)],0)
                
                # testindex=testindex-10
                # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                # testindex=testindex-10
                # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
        


    #print(str(User),"Mike Check: Tap ",np.mean(TapSingleList),np.mean(TapMultiList),np.mean(SwipeSingleList),np.mean(SwipeMultiList),np.mean(HPanSingleList),np.mean(HPanMultiList),np.mean(VPanSingleList),np.mean(VPanMultiList))          
    print(str(User)+" ResponseMode: ",ResponseMode,' Classify Success: ',np.mean(Default_AllCrossValidationSuccess)," vs ",np.mean(AllCrossValidationSuccess)," After CNN Tap ", np.mean(TapDefaultSuccessList),np.mean(TapFirstSuccessList),np.mean(TapEndSuccessList)," vs ",np.mean(TapMyalgoSuccessList))       


