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

# def load_model(User,CrossValidationIndex,tGrid):

#     JsonName='TrainedModel/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.json'
#     f = open(JsonName, 'r')
#     model_json = f.read()
#     f.close()

#     loaded_model = model_from_json(model_json)
#     loaded_model.load_weights('TrainedModel/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.h5')

#     print("Model Loaded. ",JsonName)
#     return loaded_model



def load_model(User,CrossValidationIndex,tGrid):
    JsonName='TrainedModel/Final/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.json'
    f = open(JsonName, 'r')
    model_json = f.read()
    f.close()

    loaded_model = model_from_json(model_json)
    loaded_model.load_weights('TrainedModel/Final/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.h5')

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
def FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed):
    import numpy as np
    # X=Point['location'][0]
    # Y=Point['location'][1]
    # T=Point['timestamp']

    # #X0=Point_0['location'][0]
    # #Y0=Point_0['location'][1]
    # T0=Point_0['timestamp']


    
    # dx=X-X0
    # dy=Y-Y0
    # dt=T-T0

    # CenterX=int(np.floor((0-Device_info[0]/2)/GridSize))
    # CenterY=int(np.floor((0-Device_info[1]/2)/GridSize))

    #IndexX=int(np.floor((dx+(Device_info[0])/2)/GridSize))-2
    #IndexY=int(np.floor((dy+(Device_info[1])/2)/GridSize))-2

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((Device_info[0])/2)/GridSize))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((Device_info[1])/2)/GridSize))

    #######2

    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=Point_0['timestamp']


    # X0=Point['previousLocation'][0]
    # Y0=Point['previousLocation'][1]
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


    # if abs(IndexX)>210:
    #     print("dx",dx)
    # if abs(IndexY)>110:
    #     print("dy",dy)

    if TimeGrid==0:
        print("Grid Error")
    IndexT=int(np.ceil(dt/TimeGrid))
    
    

    #print(IndexX,IndexY,IndexT,dx,dy)

    return IndexX,IndexY,IndexT 
def FindIndexOfMatrix_BasedPreviousPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,PreviousEventTime):
    import numpy as np
    # X=Point['location'][0]
    # Y=Point['location'][1]
    # T=Point['timestamp']

    # #X0=Point_0['location'][0]
    # #Y0=Point_0['location'][1]
    # T0=Point_0['timestamp']


    # dx=X-X0
    # dy=Y-Y0
    # dt=T-T0

    # CenterX=int(np.floor((0-Device_info[0]/2)/GridSize))
    # CenterY=int(np.floor((0-Device_info[1]/2)/GridSize))

    #IndexX=int(np.floor((dx+(Device_info[0])/2)/GridSize))-2
    #IndexY=int(np.floor((dy+(Device_info[1])/2)/GridSize))-2

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((Device_info[0])/2)/GridSize))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((Device_info[1])/2)/GridSize))

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
    IndexT=int(np.ceil(dt/TimeGrid))
    
    

    #print(IndexX,IndexY,IndexT,dx,dy)

    return IndexX,IndexY,IndexT 


def FindIndexOfMatrix_BasedFirstPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,PreviousEventTime):
    import numpy as np
    # X=Point['location'][0]
    # Y=Point['location'][1]
    # T=Point['timestamp']

    # #X0=Point_0['location'][0]
    # #Y0=Point_0['location'][1]
    # T0=Point_0['timestamp']


    # dx=X-X0
    # dy=Y-Y0
    # dt=T-T0

    # CenterX=int(np.floor((0-Device_info[0]/2)/GridSize))
    # CenterY=int(np.floor((0-Device_info[1]/2)/GridSize))

    #IndexX=int(np.floor((dx+(Device_info[0])/2)/GridSize))-2
    #IndexY=int(np.floor((dy+(Device_info[1])/2)/GridSize))-2

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((Device_info[0])/2)/GridSize))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((Device_info[1])/2)/GridSize))

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


    # if abs(IndexX)>210:
    #     print("dx",dx)
    # if abs(IndexY)>110:
    #     print("dy",dy)

    if TimeGrid==0:
        print("Grid Error")
    IndexT=int(np.floor(dt/TimeGrid))
    
    

    #print(IndexX,IndexY,IndexT,dx,dy)

    return IndexX,IndexY,IndexT 

def FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed):
    import numpy as np
    # X=Point['location'][0]
    # Y=Point['location'][1]
    # T=Point['timestamp']

    # #X0=Point_0['location'][0]
    # #Y0=Point_0['location'][1]
    # T0=Point_0['timestamp']


    # dx=X-X0
    # dy=Y-Y0
    # dt=T-T0

    # CenterX=int(np.floor((0-Device_info[0]/2)/GridSize))
    # CenterY=int(np.floor((0-Device_info[1]/2)/GridSize))

    #IndexX=int(np.floor((dx+(Device_info[0])/2)/GridSize))-2
    #IndexY=int(np.floor((dy+(Device_info[1])/2)/GridSize))-2

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((Device_info[0])/2)/GridSize))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((Device_info[1])/2)/GridSize))

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
def FindIndexOfMatrix_BasedPreviousPoint_twoChannel(Point,Point_1,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed):
    import numpy as np
    # X=Point['location'][0]
    # Y=Point['location'][1]
    # T=Point['timestamp']

    # #X0=Point_0['location'][0]
    # #Y0=Point_0['location'][1]
    # T0=Point_0['timestamp']


    # dx=X-X0
    # dy=Y-Y0
    # dt=T-T0

    # CenterX=int(np.floor((0-Device_info[0]/2)/GridSize))
    # CenterY=int(np.floor((0-Device_info[1]/2)/GridSize))

    #IndexX=int(np.floor((dx+(Device_info[0])/2)/GridSize))-2
    #IndexY=int(np.floor((dy+(Device_info[1])/2)/GridSize))-2

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((Device_info[0])/2)/GridSize))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((Device_info[1])/2)/GridSize))

    #######2

    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=Point_0['timestamp']


    X0=Point['previousLocation'][0]
    Y0=Point['previousLocation'][1]

    X_1=Point_1['previousLocation'][0]
    Y_1=Point_1['previousLocation'][1]

    # X0=Point_0['location'][0]
    # Y0=Point_0['location'][1]

    dt=T-T0
    dx=X-X0
    dy=Y-Y0

    dx1=X0-X_1
    dy1=Y0-Y_1

    dX=dx-dx1
    dY=dy-dy1
    
    #print("Device",Device_info)

    if dX>MaxSpeed:
        #print("dx",dx)
        dX=MaxSpeed
    elif dX<-MaxSpeed:
        #print("dx",dx)
        dX=-MaxSpeed

    if dY>MaxSpeed:
        #print("dy",dy)
        dY=MaxSpeed
    elif dY<-MaxSpeed:
        #print("dy",dy)
        dY=-MaxSpeed

    IndexX=int(np.floor((dX)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))
    IndexY=int(np.floor((dY)/GridSize))+int(np.floor(((MaxSpeed)/GridSize)))

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


def FindIndexOfMatrix_Augment(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,starttime):
    import numpy as np
    # X=Point['location'][0]
    # Y=Point['location'][1]
    # T=Point['timestamp']

    # #X0=Point_0['location'][0]
    # #Y0=Point_0['location'][1]
    # T0=Point_0['timestamp']


    
    # dx=X-X0
    # dy=Y-Y0
    # dt=T-T0

    # CenterX=int(np.floor((0-Device_info[0]/2)/GridSize))
    # CenterY=int(np.floor((0-Device_info[1]/2)/GridSize))

    #IndexX=int(np.floor((dx+(Device_info[0])/2)/GridSize))-2
    #IndexY=int(np.floor((dy+(Device_info[1])/2)/GridSize))-2

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((Device_info[0])/2)/GridSize))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((Device_info[1])/2)/GridSize))

    #######2

    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=starttime


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



def FindIndexOfMatrix_MovedMoved(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,starttime):
    import numpy as np
    
    #######2

    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=starttime


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

def FindIndexOfMatrix_TouchEnded(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed):
    import numpy as np
    # X=Point['location'][0]
    # Y=Point['location'][1]
    # T=Point['timestamp']

    # #X0=Point_0['location'][0]
    # #Y0=Point_0['location'][1]
    # T0=Point_0['timestamp']


    
    # dx=X-X0
    # dy=Y-Y0
    # dt=T-T0

    # CenterX=int(np.floor((0-Device_info[0]/2)/GridSize))
    # CenterY=int(np.floor((0-Device_info[1]/2)/GridSize))

    #IndexX=int(np.floor((dx+(Device_info[0])/2)/GridSize))-2
    #IndexY=int(np.floor((dy+(Device_info[1])/2)/GridSize))-2

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((Device_info[0])/2)/GridSize))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((Device_info[1])/2)/GridSize))

    #######2

    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=Point_0['timestamp']


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


    # if abs(IndexX)>210:
    #     print("dx",dx)
    # if abs(IndexY)>110:
    #     print("dy",dy)

    if TimeGrid==0:
        print("Grid Error")
    IndexT=int(np.ceil(dt/TimeGrid))
    
    

    #print(IndexX,IndexY,IndexT,dx,dy)

    return IndexX,IndexY,IndexT 


def FindIndexOfMatrix_Speed(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed):
    import numpy as np
    # X=Point['location'][0]
    # Y=Point['location'][1]
    # T=Point['timestamp']

    # #X0=Point_0['location'][0]
    # #Y0=Point_0['location'][1]
    # T0=Point_0['timestamp']


    
    # dx=X-X0
    # dy=Y-Y0
    # dt=T-T0

    # CenterX=int(np.floor((0-Device_info[0]/2)/GridSize))
    # CenterY=int(np.floor((0-Device_info[1]/2)/GridSize))

    #IndexX=int(np.floor((dx+(Device_info[0])/2)/GridSize))-2
    #IndexY=int(np.floor((dy+(Device_info[1])/2)/GridSize))-2

    #IndexX=int(np.floor((dx)/GridSize))+int(np.floor(((Device_info[0])/2)/GridSize))
    #IndexY=int(np.floor((dy)/GridSize))+int(np.floor(((Device_info[1])/2)/GridSize))

    #######2

   
    X=Point['location'][0]
    Y=Point['location'][1]
    T=Point['timestamp']

    
    T0=Point_0['timestamp']


    X0=Point['previousLocation'][0]
    Y0=Point['previousLocation'][1]
    dt=T-T0
    if dt==0:
        dx=0
        dy=0
    else:

        dx=(X-X0)/dt
        dy=(Y-Y0)/dt
    
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
    IndexT=int(np.floor(dt/TimeGrid))
    
    

    #print(IndexX,IndexY,IndexT,dx,dy)

    return IndexX,IndexY,IndexT 


def JsonToCube(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid):
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
            Task=0;
        else:
            Task=1;

        for iTrial in range(len(JsonData[task]['trials'])):
            DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
            

            for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):


                    

                    Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                    Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]

                    

                    
                    Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                    
                    if Time_In<TimeFrameNum:
                        #Time_In=TimeFrameNum-1
                        DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                        # if Point['phase']=='ended':
                        #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

                    if iPoint>0:
                        Point_t_1=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                        Grid_InX_t_1,Grid_InY_t_1,Time_In_t_1=FindIndexOfMatrix2(Point_t_1,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)

                        if Time_In<TimeFrameNum:
                            if Time_In-Time_In_t_1>1:
                                #print(Time_In-Time_In_t_1)
                                ## need to interpolate
                                BasedPointX=Point_t_1["location"][0]
                                BasedPointY=Point_t_1["location"][1]
                                
                                for it in range(1,Time_In-Time_In_t_1):
                                    ratio=(it)/(Time_In-Time_In_t_1)

                                    interpolatePointX=Point["location"][0]*ratio+Point_t_1["location"][0]*(1-ratio)
                                    interpolatePointY=Point["location"][1]*ratio+Point_t_1["location"][1]*(1-ratio)
                                    

                                    ix,iy=InterpolationIndexOfMatrix(BasedPointX,BasedPointY,interpolatePointX,interpolatePointY,GridSize,MaxSpeed)
                                    
                                    #print("Dt",Time_In-Time_In_t_1,"Interpolate?",Time_In-Time_In_t_1>1,it,ratio,"Point",interpolatePointX,interpolatePointY,"index",ix,iy)
                                    DataMatrix[ix][iy][Time_In_t_1+it][0]=DataMatrix[ix][iy][Time_In_t_1+it][0]+1
                                    BasedPointX=interpolatePointX
                                    BasedPointY=interpolatePointY



          
            AllDataX.append(DataMatrix)
            AllDataY.append(Task)
        #Task=Task+1
        

    return np.array(AllDataX),np.array(AllDataY)

def JsonToCube_NoInterpolation(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid):
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
            Task=0;
        else:
            Task=1;

        #Mode1
        # for iTrial in range(len(JsonData[task]['trials'])):
        #     JsonData[task]['trials'][iTrial]=LabelTrialEvent(JsonData[task]['trials'][iTrial])
        #     DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
            

        #     for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
        #         for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

        #             #Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
        #             Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]
        #             Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]

        #             #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
        #             Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                    
        #             if Time_In<TimeFrameNum:
        #                 #Time_In=TimeFrameNum-1
        #                 DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
        #                 # if Point['phase']=='ended':
        #                 #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

        #     AllDataX.append(DataMatrix)
        #     AllDataY.append(Task)
        # #Task=Task+1

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

                DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
                # BaseTime=eventT-TimeFrameNum*TimeGrid
                # BaseTime=JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
                # if eventT-JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']>1:
                #     BaseTime=eventT-TimeGrid*TimeFrameNum
                # else:
                #     BaseTime=JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']

                BaseTime=eventT-TimeGrid*TimeFrameNum
                for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                    for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

                        Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                        #Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]
                        Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                        if (BaseTime<=Point['timestamp']) & (eventT>=Point['timestamp']):
                            #Point_0['timestamp']=BaseTime
                            #Point_0['timestamp']=began_T-TimeGrid*TimeFrameNum
                            #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                            #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                            Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                            
                            #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedFirstPoint_PreviousEvent(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed,BaseTime)
                            
                            if Time_In<TimeFrameNum:
                                #Time_In=TimeFrameNum-1
                                DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                                # if Point['phase']=='ended':
                                #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

                AllDataX.append(DataMatrix)
                AllDataY.append(Task)
        #Task=Task+1


    return np.array(AllDataX),np.array(AllDataY)

def JsonToCube_NoInterpolation_twoChannel(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid):
    import numpy as np
    # GridNum_InX=int(np.ceil(Device_info[0]/GridSize))+10
    # GridNum_InY=int(np.ceil(Device_info[1]/GridSize))+10
  
    GridNum_InX=int(np.ceil(2*MaxSpeed/GridSize))+1
    GridNum_InY=int(np.ceil(2*MaxSpeed/GridSize))+1
    Channel=2
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

        for iTrial in range(len(JsonData[task]['trials'])):
            #JsonData[task]['trials'][iTrial]=LabelTrialEvent(JsonData[task]['trials'][iTrial])
            DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
            

            for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

                    Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                    Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]

                    #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                    Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                    
                    if Time_In<TimeFrameNum:
                        #Time_In=TimeFrameNum-1
                        DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                        DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+(Point['timestamp']-Point_0['timestamp'])
                        # if Point['phase']=='ended':
                        #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1
                    # if iPoint>1:
                    #     Point_1=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                    #     Grid_InX2,Grid_InY2,Time_In2=FindIndexOfMatrix_BasedPreviousPoint_twoChannel(Point,Point_1,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                    #     if Time_In<TimeFrameNum:
                    #         #Time_In=TimeFrameNum-1
                    #         DataMatrix[Grid_InX2][Grid_InY2][Time_In2][1]=DataMatrix[Grid_InX2][Grid_InY2][Time_In2][1]+1


            AllDataX.append(DataMatrix)
            AllDataY.append(Task)
        #Task=Task+1
        

    return np.array(AllDataX),np.array(AllDataY)

def JsonToCube_NoInterpolation_AllBegan(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid):

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
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        #print("------",task,"------")
        if task=='tapTask':
            Task=0;
        else:
            Task=1;

        for iTrial in range(len(JsonData[task]['trials'])):

            ###find Began
            AllTouchBeganTime=list()
            AllTouchEndTime=list()
            AllEventTime=list()
            for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                        if JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='began':
                                AllTouchBeganTime.append(float(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
                        if JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='ended':
                                AllTouchEndTime.append(float(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
            for panevent_t in range(len(JsonData[task]['trials'][iTrial]['panEvents'])):
               
                AllEventTime.append(float(JsonData[task]['trials'][iTrial]['panEvents'][panevent_t]['timestamp']))

                

            for tapevent_t in range(len(JsonData[task]['trials'][iTrial]['tapEvents'])):
                AllEventTime.append(float(JsonData[task]['trials'][iTrial]['tapEvents'][tapevent_t]['timestamp']))


            SortedAllTouchEventTime=sorted(AllEventTime)
            SortedAllTouchBeganTime=sorted(AllTouchBeganTime)
            SortedAllTouchEndTime=sorted(AllTouchEndTime)

            ProcssTimeList=SortedAllTouchEventTime
            if len(ProcssTimeList)==0:
                print("No pan No Tap")
                ProcssTimeList=SortedAllTouchBeganTime
            

            for began_T in ProcssTimeList:
                #print(began_T,began_T in SortedAllTouchEndTime,began_T in SortedAllTouchBeganTime)
                #if TimeInRange(began_T-TimeFrameNum*tGrid,began_T+TimeFrameNum*tGrid,SortedAllTouchEndTime):

                if TimeInRange(began_T-float(TimeFrameNum*tGrid),began_T+float(TimeFrameNum*tGrid),SortedAllTouchEndTime)|TimeInRange(began_T-TimeFrameNum*tGrid,began_T+TimeFrameNum*tGrid,SortedAllTouchBeganTime):
                    
                    DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
                    
                    BaseTime=began_T-TimeFrameNum*tGrid

                    if BaseTime<JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']:
                        BaseTime=JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
                    for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                        for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

                            Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                            Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                            if (BaseTime<=Point['timestamp']) &  (BaseTime +TimeFrameNum*tGrid >=Point['timestamp']):
                            #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                                Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_AllBegan(Point,BaseTime,GridSize,TimeGrid,Device_info,MaxSpeed)
                                
                                if Time_In<TimeFrameNum:
                                    #Time_In=TimeFrameNum-1
                                    DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                                    # if Point['phase']=='ended':
                                    #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

                    AllDataX.append(DataMatrix)
                    AllDataY.append(Task)
        #Task=Task+1
        
    print(np.array(AllDataX).shape)
    return np.array(AllDataX),np.array(AllDataY)


def JsonToCube_NoInterpolation_EventFromBegan(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid):

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
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        #print("------",task,"------")
        if task=='tapTask':
            Task=0;
        else:
            Task=1;

        for iTrial in range(len(JsonData[task]['trials'])):

            ###find Began
            AllTouchBeganTime=list()
            AllTouchEndTime=list()
            AllEventTime=list()
            for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                        if JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='began':
                                AllTouchBeganTime.append(float(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
                        if JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='ended':
                                AllTouchEndTime.append(float(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']))
            for panevent_t in range(len(JsonData[task]['trials'][iTrial]['panEvents'])):
               
                AllEventTime.append(float(JsonData[task]['trials'][iTrial]['panEvents'][panevent_t]['timestamp']))

                

            for tapevent_t in range(len(JsonData[task]['trials'][iTrial]['tapEvents'])):
                AllEventTime.append(float(JsonData[task]['trials'][iTrial]['tapEvents'][tapevent_t]['timestamp']))


            SortedAllTouchEventTime=sorted(AllEventTime)
            SortedAllTouchBeganTime=sorted(AllTouchBeganTime)
            SortedAllTouchEndTime=sorted(AllTouchEndTime)

            ProcssTimeList=SortedAllTouchEventTime
            if len(ProcssTimeList)==0:
                print("No pan No Tap")
                ProcssTimeList=SortedAllTouchEndTime
            
            DataAugmentIndex=0
            for began_T in ProcssTimeList:
                if DataAugmentIndex<=10:
                    
                    DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
                    
                    
                    BaseTime=JsonData[task]['trials'][iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
                    # TimeGrid=(began_T-BaseTime)/10
                    TimeGrid=0.01

                    
                    for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                        for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

                            Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                            Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                            if (BaseTime<=Point['timestamp']) &  (began_T >=Point['timestamp']):
                            #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                                Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_AllBegan(Point,BaseTime,GridSize,TimeGrid,Device_info,MaxSpeed)
                                
                                if Time_In<TimeFrameNum:
                                    #Time_In=TimeFrameNum-1
                                    DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                                    # if Point['phase']=='ended':
                                    #     DataMatrix[Grid_InX][Grid_InY][Time_In][1]=DataMatrix[Grid_InX][Grid_InY][Time_In][1]+1

                    AllDataX.append(DataMatrix)
                    AllDataY.append(Task)
                    DataAugmentIndex= DataAugmentIndex+1
        #Task=Task+1
        
    print(np.array(AllDataX).shape)
    return np.array(AllDataX),np.array(AllDataY)





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



def JsonToCube_TouchEnded(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid):
    import numpy as np
    # GridNum_InX=int(np.ceil(Device_info[0]/GridSize))+10
    # GridNum_InY=int(np.ceil(Device_info[1]/GridSize))+10
  
    GridNum_InX=int(np.ceil(2*MaxSpeed/GridSize))+1
    GridNum_InY=int(np.ceil(2*MaxSpeed/GridSize))+1
    Channel=2
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

        for iTrial in range(len(JsonData[task]['trials'])):
            DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
            
            TimeGrid=ComputeTimeGrid(JsonData[task]['trials'][iTrial]["rawTouchTracks"],TimeFrameNum)
            if TimeGrid!=-1:
                for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                    for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

                        Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                        Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]

                        

                        
                        Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                        Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                        
                        if Time_In<TimeFrameNum:
                            #Time_In=TimeFrameNum-1
                            DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                            if Point['phase']=='ended':
                                Grid_InX_End,Grid_InY_End,Time_In_End=FindIndexOfMatrix_TouchEnded(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                                DataMatrix[Grid_InX_End][Grid_InY_End][Time_In_End][1]=DataMatrix[Grid_InX_End][Grid_InY_End][Time_In_End][1]+1

                        if iPoint>0:
                            Point_t_1=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                            #Grid_InX_t_1,Grid_InY_t_1,Time_In_t_1=FindIndexOfMatrix2(Point_t_1,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                            Grid_InX_t_1,Grid_InY_t_1,Time_In_t_1=FindIndexOfMatrix_BasedPreviousPoint(Point_t_1,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)

                            if Time_In<TimeFrameNum:
                                if Time_In-Time_In_t_1>1:
                                    #print(Time_In-Time_In_t_1)
                                    ## need to interpolate
                                    BasedPointX=Point_t_1["location"][0]
                                    BasedPointY=Point_t_1["location"][1]
                                    
                                    for it in range(1,Time_In-Time_In_t_1):
                                        ratio=(it)/(Time_In-Time_In_t_1)

                                        interpolatePointX=Point["location"][0]*ratio+Point_t_1["location"][0]*(1-ratio)
                                        interpolatePointY=Point["location"][1]*ratio+Point_t_1["location"][1]*(1-ratio)
                                        

                                        ix,iy=InterpolationIndexOfMatrix(BasedPointX,BasedPointY,interpolatePointX,interpolatePointY,GridSize,MaxSpeed)
                                        
                                        #print("Dt",Time_In-Time_In_t_1,"Interpolate?",Time_In-Time_In_t_1>1,it,ratio,"Point",interpolatePointX,interpolatePointY,"index",ix,iy)
                                        DataMatrix[ix][iy][Time_In_t_1+it][0]=DataMatrix[ix][iy][Time_In_t_1+it][0]+1
                                        BasedPointX=interpolatePointX
                                        BasedPointY=interpolatePointY
            else:
                #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,1,Device_info,MaxSpeed)
                Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_BasedPreviousPoint(Point,Point_0,GridSize,1,Device_info,MaxSpeed)
                
                DataMatrix[Grid_InX][Grid_InY][0][0]=DataMatrix[Grid_InX][Grid_InY][0][0]+1      

          
            AllDataX.append(DataMatrix)
            AllDataY.append(Task)
        #Task=Task+1
        

    return np.array(AllDataX),np.array(AllDataY)




def JsonToCube_Speed(JsonData,Device_info,GridSize,TimeFrameNum,MaxSpeed):
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
        for iTrial in range(len(JsonData[task]['trials'])):
            DataMatrix=np.zeros((GridNum_InX,GridNum_InY,TimeFrameNum,Channel))
            

            for iFinger in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"])):
                for iPoint in range(len(JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):


                    



                    Point_0=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]
                    Point=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]

                    

                    
                    #Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix2(Point,Point_0,GridSize,TimeGrid,Device_info)
                    Grid_InX,Grid_InY,Time_In=FindIndexOfMatrix_Speed(Point,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)
                    
                    if Time_In<TimeFrameNum:
                        #Time_In=TimeFrameNum-1
                        DataMatrix[Grid_InX][Grid_InY][Time_In][0]=DataMatrix[Grid_InX][Grid_InY][Time_In][0]+1
                    if iPoint>0:
                        Point_t_1=JsonData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                        #Grid_InX_t_1,Grid_InY_t_1,Time_In_t_1=FindIndexOfMatrix2(Point_t_1,Point_0,GridSize,TimeGrid,Device_info)
                        Grid_InX_t_1,Grid_InY_t_1,Time_In_t_1=FindIndexOfMatrix_Speed(Point_t_1,Point_0,GridSize,TimeGrid,Device_info,MaxSpeed)

                        if Time_In<TimeFrameNum:
                            if Time_In-Time_In_t_1>1:
                                #print(Time_In-Time_In_t_1)
                                ## need to interpolate
                                BasedPointX=Point_t_1["location"][0]
                                BasedPointY=Point_t_1["location"][1]
                                BasedPointT=Point_t_1["timestamp"]
                                
                                for it in range(1,Time_In-Time_In_t_1):
                                    ratio=(it)/(Time_In-Time_In_t_1)

                                    interpolatePointX=Point["location"][0]*ratio+Point_t_1["location"][0]*(1-ratio)
                                    interpolatePointY=Point["location"][1]*ratio+Point_t_1["location"][1]*(1-ratio)
                                    interpolatePointT=Point["timestamp"]*ratio+Point_t_1["timestamp"]*(1-ratio)
                                    

                                    #ix,iy=InterpolationIndexOfMatrix(BasedPointX,BasedPointY,interpolatePointX,interpolatePointY,GridSize,MaxSpeed)
                                    ix,iy=InterpolationIndexOfMatrix_Speed(BasedPointX,BasedPointY,BasedPointT,interpolatePointX,interpolatePointY,interpolatePointT,GridSize,MaxSpeed)
                                    
                                    #print("Dt",Time_In-Time_In_t_1,"Interpolate?",Time_In-Time_In_t_1>1,it,ratio,"Point",interpolatePointX,interpolatePointY,"index",ix,iy)
                                    DataMatrix[ix][iy][Time_In_t_1+it][0]=DataMatrix[ix][iy][Time_In_t_1+it][0]+1
                                    BasedPointX=interpolatePointX
                                    BasedPointY=interpolatePointY
                                    BasedPointT=interpolatePointT


          
            AllDataX.append(DataMatrix)
            AllDataY.append(Task)
        Task=Task+1
    return np.array(AllDataX),np.array(AllDataY)


# Translate data to color
def array_to_color(array, cmap="Oranges"):
    s_m = plt.cm.ScalarMappable(cmap=cmap)
    return s_m.to_rgba(array)[:,:-1]

# def translate(x):
#     xx = np.ndarray((x.shape[0], 4096, 3))
#     for i in range(x.shape[0]):
#         xx[i] = array_to_color(x[i])
#         if i % 1000 == 0:
#             print(i)
#     # Free Memory
#     del x

#     return xx


# with h5py.File("3dmnist/full_dataset_vectors.h5", 'r') as h5:
#     X_train, y_train = h5["X_train"][:], h5["y_train"][:]
#     X_test, y_test = h5["X_test"][:], h5["y_test"][:]
#     print(X_test[0])

#print(FindIndexOfMatrix(550,110,2.31,22,0.1))

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

def evaluate(ValidIndex,AllTaskValidIndex,DefaultSuccessRate):
    global model

    pred = model.predict(X_test)
    pred = np.argmax(pred, axis=1)
    #print(pred)

    DetailString=""
    for i in range(len(pred)):
        DetailString+=" "+str(pred[i]) +" / "+str(One_hot_Decode(y_test[i]))
    ValidData=""
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        ValidData+=" "+str(task)
        for i in range(len(AllTaskValidIndex[task])):
            ValidData+=" "+str(AllTaskValidIndex[task][i])
    dataString=str(User)+" "+str(ValidIndex)+" Accuracy: "+str(accuracy_score(to_categorical(pred, num_classes=2),y_test))+" Grid "+str(tGrid)+" Detail: "+DetailString+" ValidData: "+ValidData
    print("Default:",DefaultSuccessRate)
    print(dataString)
    #f.write(dataString)
    #f.close()
    #print(pred)
    #print(ValidIndex,accuracy_score(to_categorical(pred, num_classes=4),y_test),)
    # Heat Map
    #array = confusion_matrix(y_test, to_categorical(pred, num_classes=4))
    #cm = pd.DataFrame(array, index = range(10), columns = range(10))
    #plt.figure(figsize=(20,20))
    #sns.heatmap(cm, annot=True)
    #plt.show()


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
        
        # if DataPointNum>1:

        #     if len(CandidateDataInFinger)>1:
        #         largestClusterFinger=np.argmax(np.bincount(np.array(CandidateDataInFinger).transpose(1,0)[0]))
                
        #         for i in range(len(CandidateDataInFinger)):
        #             CheckPoint=CandidateDataInFinger[i][1]
        #             if(CandidateDataInFinger[i][0]!=largestClusterFinger):
        #                 if DataPointNum>1:
        #                     LabelFalse(OutputData,CandidateDataInFinger[i][0],CheckPoint)
        #                     DataPointNum=DataPointNum-1
        # MaxTime=0
        # FinalFinger=0
        # FinalFingerPoint=0
        # if DataPointNum>1:
        #     for iFinger in range(len(OutputData["rawTouchTracks"])):
        #         for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):

        #              if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
        #                 #print("remain",iFinger,iPoint)
        #                 PossibleX.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
        #                 PossibleY.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])
        #                 t=OutputData["rawTouchTracks"][iFinger]["rawTouches"][len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp']- OutputData["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
        #                 if t>MaxTime:
                            
        #                     LabelFalse(OutputData,FinalFinger,FinalFingerPoint)
        #                     MaxTime=t
        #                     FinalFinger=iFinger
        #                     FinalFingerPoint=iPoint
        #                     OutputData["rawTouchTracks"][FinalFinger]["rawTouches"][FinalFingerPoint]['label']=True
        #                 else:
        #                     LabelFalse(OutputData,iFinger,iPoint)

        # for iFinger in range(len(OutputData["rawTouchTracks"])):
        #     for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
        #         if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
        #             OutPutPoint=FingerCenterDict[str(iFinger)]
        #             PossibleX.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
        #             PossibleY.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])

        # print("Final:",FinalFinger,FinalFingerPoint)
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
                if pred==1:
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

                    # if (abs( OutPutPoint[0] - TaskData["targetFrame"][0][0] -TaskData["targetFrame"][1][0]*0.5) > TaskData["targetFrame"][1][0]*0.5)|(abs( OutPutPoint[1]- TaskData["targetFrame"][0][1] - TaskData["targetFrame"][1][1]*0.5) >TaskData["targetFrame"][1][1]*0.5):
                    #         # cout << "First touch point is not correct" << endl;
                    #     print("My Prediction False")
                    # else:
                    #      OptimzerSuccess=OptimzerSuccess+1

                    # if len(OptimizedData['rawTouchTracks'])==0:
                    #     print("MyFalse Nofinger")

                    # if len(OptimizedData['rawTouchTracks'][0]['rawTouches'])==0:
                    #     print("MyFalse Nopoint")
                    # #print("MyAlgorithm OutPut:  ",OptimizedData['rawTouchTracks'][0]['rawTouches'][0])

                    # if len(FilteredOptimizedData['rawTouchTracks'])==0:
                    #     print("Nofinger")

                    if tv.TapTask_SuccessVerify(FilteredOptimizedData):
                        OptimzerSuccess=OptimzerSuccess+1


                    defaultfalse=0
                    for tapindex in range(len(TaskData['tapEvents'])):
                        print(TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex'])
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
    #f.write(dataString)
    #f.close()
    #print(pred)
    #print(ValidIndex,accuracy_score(to_categorical(pred, num_classes=4),y_test),)
    # Heat Map
    #array = confusion_matrix(y_test, to_categorical(pred, num_classes=4))
    #cm = pd.DataFrame(array, index = range(10), columns = range(10))
    #plt.figure(figsize=(20,20))
    #sns.heatmap(cm, annot=True)
    #plt.show()


    if RecognizedTapTrials!=0:
        return DefaultSuccess/RecognizedTapTrials,OptimzerSuccess/RecognizedTapTrials,accuracy_score(to_categorical(pred, num_classes=2),y_test)
    else:
        return 1234567,1234567,accuracy_score(to_categorical(pred, num_classes=2),y_test)

def save_model(User,CrossValidationIndex,tGrid):
    global model

    model_json = model.to_json()
    with open('TrainedModel/Final/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.json', 'w') as f:
        f.write(model_json)

    model.save_weights('TrainedModel/Final/'+str(User)+'/model_3DCNN_'+str(User)+'_'+str(CrossValidationIndex)+'_'+str(tGrid)+'.h5')

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

                # if DataPointNum>1:

                #     if len(CandidateDataInFinger)>1:
                #         largestClusterFinger=np.argmax(np.bincount(np.array(CandidateDataInFinger).transpose(1,0)[0]))
                        
                #         for i in range(len(CandidateDataInFinger)):
                #             CheckPoint=CandidateDataInFinger[i][1]
                #             if(CandidateDataInFinger[i][0]!=largestClusterFinger):
                #                 if DataPointNum>1:
                #                     LabelFalse(OutputData,CandidateDataInFinger[i][0],CheckPoint)
                #                     DataPointNum=DataPointNum-1
                # MaxTime=0
                # FinalFinger=0
                # FinalFingerPoint=0
                # if DataPointNum>1:
                #     for iFinger in range(len(OutputData["rawTouchTracks"])):
                #         for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):

                #              if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                #                 #print("remain",iFinger,iPoint)
                #                 PossibleX.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                #                 PossibleY.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])
                #                 t=OutputData["rawTouchTracks"][iFinger]["rawTouches"][len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp']- OutputData["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                #                 if t>MaxTime:
                                    
                #                     LabelFalse(OutputData,FinalFinger,FinalFingerPoint)
                #                     MaxTime=t
                #                     FinalFinger=iFinger
                #                     FinalFingerPoint=iPoint
                #                     OutputData["rawTouchTracks"][FinalFinger]["rawTouches"][FinalFingerPoint]['label']=True
                #                 else:
                #                     LabelFalse(OutputData,iFinger,iPoint)

                # for iFinger in range(len(OutputData["rawTouchTracks"])):
                #     for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                #         if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                #             OutPutPoint=FingerCenterDict[str(iFinger)]
                #             PossibleX.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                #             PossibleY.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])

                # print("Final:",FinalFinger,FinalFingerPoint)
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
                print(TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex'])
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
            # if task=='swipeTask' or task=='horizontalScrollTask' or task=='verticalScrollTask':
            #     if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
            #             if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
            #                     DefaultSuccessCount=DefaultSuccessCount+1
            # elif task=='tapTask':
                
            #     if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
            #             if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
            #                     DefaultSuccessCount=DefaultSuccessCount+1

            #     if CNNSuccess==True:
            #             TapAllAfterCNN=TapAllAfterCNN+1
            #             defaultTap,MyTap=VerifyTap(Validation_Data_2[task]['trials'][iTrial])
            #             TapDefaultSuccess=TapDefaultSuccess+defaultTap
            #             TapMyTapSuccess=TapMyTapSuccess+MyTap
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

                # if DataPointNum>1:

                #     if len(CandidateDataInFinger)>1:
                #         largestClusterFinger=np.argmax(np.bincount(np.array(CandidateDataInFinger).transpose(1,0)[0]))
                        
                #         for i in range(len(CandidateDataInFinger)):
                #             CheckPoint=CandidateDataInFinger[i][1]
                #             if(CandidateDataInFinger[i][0]!=largestClusterFinger):
                #                 if DataPointNum>1:
                #                     LabelFalse(OutputData,CandidateDataInFinger[i][0],CheckPoint)
                #                     DataPointNum=DataPointNum-1
                # MaxTime=0
                # FinalFinger=0
                # FinalFingerPoint=0
                # if DataPointNum>1:
                #     for iFinger in range(len(OutputData["rawTouchTracks"])):
                #         for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):

                #              if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                #                 #print("remain",iFinger,iPoint)
                #                 PossibleX.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                #                 PossibleY.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])
                #                 t=OutputData["rawTouchTracks"][iFinger]["rawTouches"][len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp']- OutputData["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                #                 if t>MaxTime:
                                    
                #                     LabelFalse(OutputData,FinalFinger,FinalFingerPoint)
                #                     MaxTime=t
                #                     FinalFinger=iFinger
                #                     FinalFingerPoint=iPoint
                #                     OutputData["rawTouchTracks"][FinalFinger]["rawTouches"][FinalFingerPoint]['label']=True
                #                 else:
                #                     LabelFalse(OutputData,iFinger,iPoint)

                # for iFinger in range(len(OutputData["rawTouchTracks"])):
                #     for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
                #         if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                #             OutPutPoint=FingerCenterDict[str(iFinger)]
                #             PossibleX.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                #             PossibleY.append(OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])

                # print("Final:",FinalFinger,FinalFingerPoint)
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
                print(TaskData['tapEvents'][tapindex]['locationOfTouchAtIndex'])
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
    def JsonToCube_NoInterpolation_DynamicTime_OnTrial(JsonDataOneTrial,task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,ModelDict):

        def AdjustPrediction(pred):
            if pred[0][0]>0.999:
                    return 0
            else:
                    return 1

        def ModelChoose(TimeGrid,ModelDict):
            return ModelDict[0.1],0.1,10

            # if TimeGrid<0.005:
            #     return ModelDict[0.005],0.005,10
            # elif (TimeGrid>=0.005 )&(TimeGrid<0.01):
            #     return ModelDict[0.01],0.01,10
            # elif (TimeGrid>=0.01) & (TimeGrid<0.02):
            #     return ModelDict[0.02],0.02,10
            # elif (TimeGrid>=0.02) & (TimeGrid<0.03):
            #     return ModelDict[0.03],0.03,10
            # elif (TimeGrid>=0.03) & (TimeGrid<0.04):
            #     return ModelDict[0.04],0.04,10
            # elif (TimeGrid>=0.04) & (TimeGrid<0.05):
            #     return ModelDict[0.05],0.05,10
            # elif (TimeGrid>=0.05) & (TimeGrid<0.06):
            #     return ModelDict[0.06],0.06,10
            # elif (TimeGrid>=0.06) & (TimeGrid<0.07):
            #     return ModelDict[0.07],0.07,10
            # elif (TimeGrid>=0.07) & (TimeGrid<0.08):
            #     return ModelDict[0.08],0.08,10
            # elif (TimeGrid>=0.08) & (TimeGrid<0.09):
            #     return ModelDict[0.09],0.09,10
            # else: 
            #     return ModelDict[0.1],0.1,5

            # if TimeGrid<0.005:
            #     return ModelDict[0.005],0.005,10
            # elif (TimeGrid>=0.005 )&(TimeGrid<0.01):
            #     return ModelDict[0.005],0.005,10
            # elif (TimeGrid>=0.01) & (TimeGrid<0.02):
            #     return ModelDict[0.01],0.01,10
            # elif (TimeGrid>=0.02) & (TimeGrid<0.03):
            #     return ModelDict[0.02],0.02,10
            # elif (TimeGrid>=0.03) & (TimeGrid<0.04):
            #     return ModelDict[0.03],0.03,10
            # elif (TimeGrid>=0.04) & (TimeGrid<0.05):
            #     return ModelDict[0.04],0.04,10
            # elif (TimeGrid>=0.05) & (TimeGrid<0.06):
            #     return ModelDict[0.05],0.05,10
            # elif (TimeGrid>=0.06) & (TimeGrid<0.07):
            #     return ModelDict[0.06],0.06,10
            # elif (TimeGrid>=0.07) & (TimeGrid<0.08):
            #     return ModelDict[0.09],0.07,10
            # elif (TimeGrid>=0.08) & (TimeGrid<0.09):
            #     return ModelDict[0.08],0.08,10
            # elif (TimeGrid>=0.09) & (TimeGrid<0.1):
            #     return ModelDict[0.09],0.09,10
            # else: 
            #     return ModelDict[0.1],0.1,10

            # if TimeGrid<0.005:
            #     return ModelDict[0.005],0.005
            # elif (TimeGrid>=0.005 )&(TimeGrid<0.01):
            #     return ModelDict[0.01],0.01
            # else: 
            #     return ModelDict[0.02],0.02

            # if TimeGrid<0.005:
            #     return ModelDict[0.005],0.005
            # else: 
            #     return ModelDict[0.01],0.01

            # if TimeGrid<0.04:
            #     return ModelDict[0.04],0.04,10
            # elif (TimeGrid>=0.04) & (TimeGrid<0.05):
            #     return ModelDict[0.05],0.05,10
            # elif (TimeGrid>=0.05) & (TimeGrid<0.06):
            #     return ModelDict[0.06],0.06,10
            # elif (TimeGrid>=0.06) & (TimeGrid<0.07):
            #     return ModelDict[0.07],0.07,10
            # else:
            #     return ModelDict[0.08],0.08,10
           
          




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
            if JsonDataOneTrial['panEvents'][panevent_t]['state']!='changed':
                #print(JsonDataOneTrial['panEvents'][panevent_t]['state'])
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
            BaseTime=began_T-TimeGrid*TimeFrameNum
            FirstTouchTime=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']

            TimeGrid=(began_T-FirstTouchTime)/10

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
            
            

            # if BaseTime<JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']:
            #     BaseTime=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
            # if began_T-JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']>1:
            #     BaseTime=began_T-TimeGrid*TimeFrameNum
            # else:
            #     BaseTime=JsonDataOneTrial["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
            BaseTime=began_T-TimeGrid*TimeFrameNum
            print("EventTime ",began_T,"BaseTime ",BaseTime,"RecognitionTime ",began_T-BaseTime)
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
        #     if TouchBeganEvent==True:
        #         # if TouchEndEvent==True:
        #         #     pred = PredictModel.predict(X_test)
        #         #         #print("pred",pred)
        #         #     prediction = np.argmax(pred, axis=1)[0]
        #         #         #print("pred1",prediction)
        #         #     touchBeganPredict=str(prediction)
        #         # else:
        #         #     pred = PredictModel.predict(X_test)
        #         #     prediction=AdjustPrediction(pred)
        #         #         #print("pred",pred)
        #         #     #prediction = np.argmax(pred, axis=1)[0]
        #         #         #print("pred1",prediction)
        #         #     touchBeganPredict=str(prediction)


        #         pred = PredictModel.predict(X_test)
        #             #print("pred",pred)
        #         prediction = np.argmax(pred, axis=1)[0]
        #             #print("pred1",prediction)
        #         touchBeganPredict=str(prediction)

        #     else:
        # #print(CNNEvent)
        #         if touchBeganPredict=='1':
        #             pred = PredictModel.predict(X_test)
        #             prediction=AdjustPrediction(pred)
        #         else:
        #             pred = PredictModel.predict(X_test)
        #             #print("pred",pred)
        #             prediction = np.argmax(pred, axis=1)[0]
        #                     #print("pred1",prediction)
        #             touchBeganPredict=str(prediction)


            CNNEvent.append(prediction)

        print(task,len(JsonDataOneTrial['tapEvents']),len(JsonDataOneTrial['panEvents'])," vs ",(0 in CNNEvent),(1 in CNNEvent),CNNEvent)
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
    PanAllAfterCNN=0
    TapTotal=0
    PanTotal=0



    #####Task 分類用 Validation_Data 因為有內差 。  Tap優化用 Validation_Data_2 因為沒有內差
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        for iTrial in range(len(Validation_Data[task]['trials'])):
            TotalCount=TotalCount+1
            
            CNNSuccess=JsonToCube_NoInterpolation_DynamicTime_OnTrial(Validation_Data[task]['trials'][iTrial],task,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,ModelDict)
            
            if task=='swipeTask' or task=='horizontalScrollTask' or task=='verticalScrollTask':
                PanTotal=PanTotal+1
                if CNNSuccess==True:
                    PanAllAfterCNN=PanAllAfterCNN+1
                if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['panEvents'])>0:
                                DefaultSuccessCount=DefaultSuccessCount+1

            elif task=='tapTask':
                TapTotal=TapTotal+1
                if len(Validation_Data[task]['trials'][iTrial]['panEvents'])==0:
                        if len(Validation_Data[task]['trials'][iTrial]['tapEvents'])>0:
                                DefaultSuccessCount=DefaultSuccessCount+1

                if CNNSuccess==True:
                    TapAllAfterCNN=TapAllAfterCNN+1
                #         # defaultTap,MyTap=VerifyTap(Validation_Data_2[task]['trials'][iTrial])
                #         # TapDefaultSuccess=TapDefaultSuccess+defaultTap
                #         # TapMyTapSuccess=TapMyTapSuccess+MyTap
            if CNNSuccess==True:

                SuccessCount=SuccessCount+1
    

    ValidData=""
   
   
    if TapAllAfterCNN!=0:
        print("SuccessRate:",DefaultSuccessCount/TotalCount," vs ",SuccessCount/TotalCount," Confusion: ", " TapTask ",TapAllAfterCNN," ",TapTotal," PanTask ", PanAllAfterCNN,"  ",PanTotal,"   After CNN Tap ", TapDefaultSuccess/TapAllAfterCNN," vs ",  TapMyTapSuccess/TapAllAfterCNN)

        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,TapDefaultSuccess/TapAllAfterCNN,TapMyTapSuccess/TapAllAfterCNN

    else:
        print("SuccessRate:",DefaultSuccessCount/TotalCount," vs ",SuccessCount/TotalCount," Confusion: ", " TapTask ",TapAllAfterCNN,"  ",TapTotal," PanTask ", PanAllAfterCNN,"  ",PanTotal,"   After CNN Tap : NO Success")
        return DefaultSuccessCount/TotalCount,SuccessCount/TotalCount,1234567,1234567


  
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
    tGrid=float(sys.argv[2])
    TrainingMode=sys.argv[3]
    startCV=int(sys.argv[4])
    endCV=int(sys.argv[5])

    FactorEventCountDict_Tap=dict()
    FactorEventCountDict_Pan=dict()
    for DictLabel in ['TrialNum','NoEvent','PanOthers','TapPanOthers','TapOthers','Others','Pan','TapPan','Tap']:

        FactorEventCountDict_Tap[DictLabel]=0
        FactorEventCountDict_Pan[DictLabel]=0


    #for User in ['3012','3014','3009','3007','3001','3005','3008','3010','3011','3015','3002','3003','3006']:
    #for User in ['3002','3003','3007','3008','3009','3010','3014','3015']: 
    #for User in ['3010']:
    #for User in ['3011','3008','3009','3010','3012','3014','3015','3001','3002','3003','3005','3006','3007']:
        FactorEventCountDict_Tap=dict()
        FactorEventCountDict_Pan=dict()
        for DictLabel in ['TrialNum','NoEvent','PanOthers','TapPanOthers','TapOthers','Others','Pan','TapPan','Tap']:

            FactorEventCountDict_Tap[DictLabel]=0
            FactorEventCountDict_Pan[DictLabel]=0
    # for User in ['3006','3007','3008','3009']
    # for User in ['3010','3011','3012','3014','3015']: 
    #for User in ['3012','3014','3007']:
    #for User in ['3014','3015','3008','3009','3005','3003']:
    
    #for User in ['3012']:
    
    #for User in ['3001','3005','3011','3012','3014']:

        AllCrossValidationSuccess=list()
        Default_AllCrossValidationSuccess=list()
                
        TapDefaultSuccessList=list()
        TapMyalgoSuccessList=list()


    for aaaaaa in range(1):
        
        #for tGrid in [10000]:
        #for tGrid in [0.005,0.01,0.02,10000]:
        #for tGrid in [0.005]:
        for xxxx in range(1):
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



            path='StudyData/NewData/'+User+'/'

            WritingFileName='Result/Classify/'+User+"_"+str(tGrid)+"_3DCNN_"+TimeNow+'.txt'
            
            #f=open(WritingFileName,'a')

            print("Open File:",WritingFileName)
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

            for cvIndex in range(startCV,endCV):
             
                
                cvIndex=cvIndex*9%100
                
                if TrainingMode!='2':
                    Training_Data,Validation_Data,ValidIndex,ValidTaskStartIndexArray,AllTaskValidIndex=CrossValidation(cvIndex,data_NoCrossValidation_RecognitionTime)
                    Training_Data_2,Validation_Data_2,ValidIndex_2,ValidTaskStartIndexArray_2,AllTaskValidIndex_2=CrossValidation(cvIndex,data_NoCrossValidation_RecognitionTime_NoInterpolation)
                    
                if TrainingMode=='2':
                    
                    Training_Data_2,Validation_Data_2,ValidIndex_2,ValidTaskStartIndexArray_2,AllTaskValidIndex_2=CrossValidation(cvIndex,data_NoCrossValidation_RecognitionTime_NoInterpolation)
                    Training_Data,Validation_Data,ValidIndex,ValidTaskStartIndexArray,AllTaskValidIndex=CrossValidation(cvIndex,data_NoCrossValidation_RecognitionTime)

               

                if tGrid==10000:   #代表訓練 touchEnd model
                    if TrainingMode=='1':
                        MaxSpeed=20
                        [TrainDataX,TrainDataY]=JsonToCube_TouchEnded(Training_Data,Device_info,1,10,MaxSpeed,tGrid)
                        [ValidDataX,ValidDataY]=JsonToCube_TouchEnded(Validation_Data,Device_info,1,10,MaxSpeed,tGrid)
                        X_train = TrainDataX.reshape(-1, TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 2)
                        X_test  = ValidDataX.reshape(-1, ValidDataX.shape[1], ValidDataX.shape[2], ValidDataX.shape[3], 2)
                        y_train = to_categorical(TrainDataY, num_classes=2)
                        y_test = to_categorical(ValidDataY, num_classes=2)

                        print(TrainDataX.shape)
                        optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
                        #optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
                        scheduler = ReduceLROnPlateau(monitor='val_acc', patience=3, verbose=1, factor=0.5, min_lr=1e-5)

                        model = ThreeDCNN((TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 2), 2)

                        print("Training...")
                        
                        train(optimizer, scheduler)
                        save_model(User,cvIndex,tGrid)



                elif tGrid==987:
                    if TrainingMode=='1':

                        MaxSpeed=4
                        [TrainDataX,TrainDataY]=JsonToCube_NoInterpolation_EventFromBegan(Training_Data,Device_info,0.25,10,MaxSpeed,tGrid)
                        [ValidDataX,ValidDataY]=JsonToCube_NoInterpolation_EventFromBegan(Training_Data,Device_info,0.25,10,MaxSpeed,tGrid)
                        X_train = TrainDataX.reshape(-1, TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1)
                        X_test  = ValidDataX.reshape(-1, ValidDataX.shape[1], ValidDataX.shape[2], ValidDataX.shape[3], 1)
                        y_train = to_categorical(TrainDataY, num_classes=2)
                        y_test = to_categorical(ValidDataY, num_classes=2)

                        print(TrainDataX.shape)
                        optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
                        #optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
                        scheduler = ReduceLROnPlateau(monitor='val_acc', patience=3, verbose=1, factor=0.5, min_lr=1e-5)

                        model = ThreeDCNN((TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1), 2)

                        print("Training...")
                        
                        train(optimizer, scheduler)
                        save_model(User,cvIndex,tGrid)
                elif tGrid==111:
                    if TrainingMode=='1':
                        #for DynamicTime in [0.005,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]:
                        #for DynamicTime in [0.04,0.05,0.06,0.07,0.08]:
                        for DynamicTime in [0.1]:
                            MaxSpeed=10
                            [TrainDataX,TrainDataY]=JsonToCube_NoInterpolation(Training_Data,Device_info,0.5,10,MaxSpeed,DynamicTime)
                            [ValidDataX,ValidDataY]=JsonToCube_NoInterpolation(Validation_Data,Device_info,0.5,10,MaxSpeed,DynamicTime)



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
                            save_model(User,cvIndex,DynamicTime)

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
                            evaluate(cvIndex,AllTaskValidIndex,DefaultSuccessCount/TrialCount)
                elif tGrid==222:
                    if TrainingMode=='1':
                        for DynamicTime in [0.005,0.01,0.02,0.03,0.04,0.05]:
                            MaxSpeed=10
                            [TrainDataX,TrainDataY]=JsonToCube_NoInterpolation_twoChannel(Training_Data,Device_info,0.25,10,MaxSpeed,DynamicTime)
                            [ValidDataX,ValidDataY]=JsonToCube_NoInterpolation_twoChannel(Validation_Data,Device_info,0.25,10,MaxSpeed,DynamicTime)

                            
                            X_train = TrainDataX.reshape(-1, TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 2)
                            X_test  = ValidDataX.reshape(-1, ValidDataX.shape[1], ValidDataX.shape[2], ValidDataX.shape[3], 2)
                            y_train = to_categorical(TrainDataY, num_classes=2)
                            y_test = to_categorical(ValidDataY, num_classes=2)

                            print(TrainDataX.shape)
                            optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
                            #optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
                            scheduler = ReduceLROnPlateau(monitor='val_acc', patience=3, verbose=1, factor=0.5, min_lr=1e-5)

                            model = ThreeDCNN((TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 2), 2)

                            print("Training...")
                            
                            train(optimizer, scheduler)
                            save_model(User,cvIndex,DynamicTime)

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
                            evaluate(cvIndex,AllTaskValidIndex,DefaultSuccessCount/TrialCount)


                elif tGrid<1:
                    if TrainingMode=='1':
                        MaxSpeed=4
                        # [TrainDataX,TrainDataY]=JsonToCube(Training_Data,Device_info,0.25,10,MaxSpeed,tGrid)
                        # [ValidDataX,ValidDataY]=JsonToCube(Validation_Data,Device_info,0.25,10,MaxSpeed,tGrid)

                        # [TrainDataX,TrainDataY]=JsonToCube_DataAugment(Training_Data,Device_info,0.25,10,MaxSpeed,tGrid)
                        # [ValidDataX,ValidDataY]=JsonToCube(Validation_Data,Device_info,0.25,10,MaxSpeed,tGrid)

                        #[TrainDataX,TrainDataY]=JsonToCube_DataAugment_NoInterpolation(Training_Data,Device_info,0.25,10,MaxSpeed,tGrid)
                        
                       

                       

                        # [TrainDataX,TrainDataY]=JsonToCube_MovedMoved(Training_Data,Device_info,0.25,10,MaxSpeed,tGrid)
                        # [ValidDataX,ValidDataY]=JsonToCube_MovedMoved(Validation_Data,Device_info,0.25,10,MaxSpeed,tGrid)


                        #Model2

                        [TrainDataX,TrainDataY]=JsonToCube_NoInterpolation(Training_Data,Device_info,0.25,10,MaxSpeed,tGrid)
                        [ValidDataX,ValidDataY]=JsonToCube_NoInterpolation(Validation_Data,Device_info,0.25,10,MaxSpeed,tGrid)


                        #Model 3
                        # [TrainDataX,TrainDataY]=JsonToCube_NoInterpolation_AllBegan(Training_Data,Device_info,0.25,10,MaxSpeed,tGrid)
                        # [ValidDataX,ValidDataY]=JsonToCube_NoInterpolation(Validation_Data,Device_info,0.25,10,MaxSpeed,tGrid)


                        X_train = TrainDataX.reshape(-1, TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1)
                        X_test  = ValidDataX.reshape(-1, ValidDataX.shape[1], ValidDataX.shape[2], ValidDataX.shape[3], 1)
                        y_train = to_categorical(TrainDataY, num_classes=2)
                        y_test = to_categorical(ValidDataY, num_classes=2)




                        # testindex=25
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                        
                        # testindex=testindex-10
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                        # testindex=testindex-10
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                        # for testindex in range(20):
                        #     testindex=testindex+19
                        #     Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                        # testindex=1
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                        # testindex=11
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                        # testindex=21
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                        # testindex=31
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])


                        #optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
                        
                        print(TrainDataX.shape)

                        # optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
                        # scheduler = ReduceLROnPlateau(monitor='val_acc', patience=3, verbose=1, factor=0.5, min_lr=1e-5)

                        # model = ThreeDCNN((TrainDataX.shape[1], TrainDataX.shape[2], TrainDataX.shape[3], 1), 2)
 
                        model=load_model(User,cvIndex,tGrid)



                        # # print("Training...")
                        
                        # # train(optimizer, scheduler)
                        # save_model(User,cvIndex,tGrid)



                ##################Evaluation##############
                ##################Evaluation##############

                #####Default Recognizer########

                #
                
                if TrainingMode!='2':
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

                #####Tap Optimizer########

            #     defaulttap,mytap,ClassifySuccess=evaluate_TapOptimizer(cvIndex,AllTaskValidIndex,DefaultSuccessCount/TrialCount,Validation_Data_2,FactorEventCountDict_Tap,FactorEventCountDict_Pan)
            #     ClassifySuccessList.append(ClassifySuccess)
            #     #evaluate(cvIndex,AllTaskValidIndex,DefaultSuccessCount/TrialCount)
           
            #     if mytap!=1234567:
            #         DefualtTap.append(defaulttap)

            #         MyTap.append(mytap)
            # print("=============================================================")  
            # print(str(User)," Clasify: ",np.mean(ClassifySuccessList)," After CNN Default ",np.mean(DefualtTap) ," MyTap: ",  np.mean(MyTap) )
            # print("-------------------------------------------------------------")
            # print(str(User), FactorEventCountDict_Tap ,FactorEventCountDict_Pan)



                #####Dynamic Response Time ########
                # if tGrid==987:
                #     GridSize=0.25
                #     MaxSpeed=4
                #     TimeFrameNum=10
                #     if TrianingMode!='1':
                #         ModelDict=dict()
                #         for t in [0.0025,0.005,0.01,0.015,0.02,0.03,0.04,0.05]:
                #             ModelDict[t]=load_model(User,cvIndex,t)

                #         a,b,c,d=evaluate_DynamicTime(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,Validation_Data_2)
                #         AllCrossValidationSuccess.append(b)
                #         Default_AllCrossValidationSuccess.append(a)
                #         if c!=1234567:
                #             TapDefaultSuccessList.append(c)
                #             TapMyalgoSuccessList.append(d)
                if tGrid==111:
                    GridSize=0.5
                    MaxSpeed=10
                    TimeFrameNum=10
                    if TrainingMode=='0':
                        ModelDict=dict()
                        print("Validation....", User," cvIndex", cvIndex)
                        #for t in [0.005,0.01,0.02,0.03,0.04,0.05]:
                        #for t in [0.005,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]:
                        for t in [0.1]:
                            ModelDict[t]=load_model(User,cvIndex,t)

                        a,b,c,d=evaluate_DynamicTime(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,Validation_Data_2)
                        AllCrossValidationSuccess.append(b)
                        Default_AllCrossValidationSuccess.append(a)
                        if c!=1234567:
                            TapDefaultSuccessList.append(c)
                            TapMyalgoSuccessList.append(d)


                    if TrainingMode=='2':
                        MaxSpeed=10
                        DynamicTime=0.06
                        [ValidDataX,ValidDataY]=JsonToCube_NoInterpolation(Validation_Data,Device_info,0.5,10,MaxSpeed,DynamicTime)

                            
                        for testindex in range(0,19):
                       
                            Visualize2(ValidDataX[testindex],ValidDataY[testindex],0)
                        
                        # testindex=testindex-10
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                        # testindex=testindex-10
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])

                if tGrid==222:
                    GridSize=0.25
                    MaxSpeed=10
                    TimeFrameNum=10
                    if TrainingMode=='0':
                        ModelDict=dict()
                        for t in [0.005,0.01,0.02,0.03,0.04,0.05]:
                            ModelDict[t]=load_model(User,cvIndex,t)

                        a,b,c,d=evaluate_DynamicTime(ValidIndex,AllTaskValidIndex,ModelDict,Validation_Data,Device_info,GridSize,TimeFrameNum,MaxSpeed,tGrid,Validation_Data_2)
                        AllCrossValidationSuccess.append(b)
                        Default_AllCrossValidationSuccess.append(a)
                        if c!=1234567:
                            TapDefaultSuccessList.append(c)
                            TapMyalgoSuccessList.append(d)
                    if TrainingMode=='2':
                        MaxSpeed=10
                        DynamicTime=0.1
                        [ValidDataX,ValidDataY]=JsonToCube_NoInterpolation_twoChannel(Validation_Data_2,Device_info,0.25,10,MaxSpeed,DynamicTime)

                            
                        for testindex in range(0,19):
                       
                            Visualize2(ValidDataX[testindex],ValidDataY[testindex],1)
                        
                        # testindex=testindex-10
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])
                        # testindex=testindex-10
                        # Visualize2(ValidDataX[testindex],ValidDataY[testindex])



            print(str(User)+" tGrid: ",tGrid,' Classify Success: ',np.mean(Default_AllCrossValidationSuccess)," vs ",np.mean(AllCrossValidationSuccess)," After CNN Tap ", np.mean(TapDefaultSuccessList)," vs ",np.mean(TapMyalgoSuccessList))       



