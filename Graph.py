def ComputeJerk(Point_t,Point_t_1,Point_t_2,Point_t_3):
    ##backward
    import numpy as np
    h=100*(Point_t[2]-Point_t_3[2])/3

    JerkX=(Point_t[0]-3*Point_t_1[0]+3*Point_t_2[0]-Point_t_3[0])/(h*h*h)
    JerkY=(Point_t[1]-3*Point_t_1[1]+3*Point_t_2[1]-Point_t_3[1])/(h*h*h)

    return np.sqrt(JerkX*JerkX+JerkY*JerkY)

def ComputeJerkX(Point_t,Point_t_1,Point_t_2,Point_t_3):
    ##backward
    import numpy as np
    h=100*(Point_t[2]-Point_t_3[2])/3

    JerkX=(Point_t[0]-3*Point_t_1[0]+3*Point_t_2[0]-Point_t_3[0])/(h*h*h)
    JerkY=(Point_t[1]-3*Point_t_1[1]+3*Point_t_2[1]-Point_t_3[1])/(h*h*h)

    return JerkX
def ComputeJerkY(Point_t,Point_t_1,Point_t_2,Point_t_3):
    ##backward
    import numpy as np
    h=100*(Point_t[2]-Point_t_3[2])/3

    JerkX=(Point_t[0]-3*Point_t_1[0]+3*Point_t_2[0]-Point_t_3[0])/(h*h*h)
    JerkY=(Point_t[1]-3*Point_t_1[1]+3*Point_t_2[1]-Point_t_3[1])/(h*h*h)

    return JerkY
def ComputeAccelerate(Point_t,Point_t_1,Point_t_2):
    ##backward
    import numpy as np
    h=100*((Point_t[2]-Point_t_1[2])+(Point_t_1[2]-Point_t_2[2]))/2
    aX=(Point_t[0]-2*Point_t_1[0]+Point_t_2[0])/(h*h)
    aY=(Point_t[1]-2*Point_t_1[1]+Point_t_2[1])/(h*h)
    return np.sqrt(aX*aX+aY*aY)

def ComputeAccelerateX(Point_t,Point_t_1,Point_t_2):
    ##backward
    import numpy as np
    h=100*((Point_t[2]-Point_t_1[2])+(Point_t_1[2]-Point_t_2[2]))/2
    aX=(Point_t[0]-2*Point_t_1[0]+Point_t_2[0])/(h*h)
    aY=(Point_t[1]-2*Point_t_1[1]+Point_t_2[1])/(h*h)
    return aX

def ComputeAccelerateY(Point_t,Point_t_1,Point_t_2):
    ##backward
    import numpy as np
    h=100*((Point_t[2]-Point_t_1[2])+(Point_t_1[2]-Point_t_2[2]))/2
    aX=(Point_t[0]-2*Point_t_1[0]+Point_t_2[0])/(h*h)
    aY=(Point_t[1]-2*Point_t_1[1]+Point_t_2[1])/(h*h)
    return aY

def ComputeVelocity(Point_t,Point_t_1):
    import numpy as np
    
    vx=(Point_t[0]-Point_t_1[0])/((Point_t[2]-Point_t_1[2])*1000)
    vy=(Point_t[1]-Point_t_1[1])/((Point_t[2]-Point_t_1[2])*1000)
    return np.sqrt(vx*vx+vy*vy)
def ComputeVelocityX(Point_t,Point_t_1):
    import numpy as np
    
    vx=(Point_t[0]-Point_t_1[0])/((Point_t[2]-Point_t_1[2])*1000)
    vy=(Point_t[1]-Point_t_1[1])/((Point_t[2]-Point_t_1[2])*1000)
    return vx
def ComputeVelocityY(Point_t,Point_t_1):
    import numpy as np
    
    vx=(Point_t[0]-Point_t_1[0])/((Point_t[2]-Point_t_1[2])*1000)
    vy=(Point_t[1]-Point_t_1[1])/((Point_t[2]-Point_t_1[2])*1000)
    return vy

def ComputeDisplace(Point_t,Point_t_1):
    import numpy as np
    
    vx=(Point_t[0]-Point_t_1[0])
    vy=(Point_t[1]-Point_t_1[1])
    return np.sqrt(vx*vx+vy*vy)

def LabelAllTrue(TaskData,iTrial):
    
    for iFinger in range(len(TaskData["rawTouchTracks"])):
        for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])): 
                TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True
                  

def LabelFalse(InputTaskData,iTrial,iFinger,iPoint):
    InputTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=False


def ReadData(path_0,file_0):
    data = dict{}
    for i in range(len(file_0)):
        with open(path_0+file_0[i]) as json_file: 
            
            data_0= json.load(json_file)
            
            if file_0[i]!=file_0[0]:
                try:
                    data['horizontalScrollTask']=data_0['horizontalScrollTask']
                except:
                    a=1
                    #print("No file")
                try:
                    data['verticalScrollTask']=data_0['verticalScrollTask']
                except:
                    a=1
                    #print("No file")
                try:
                    data['tapTask']=data_0['tapTask']
                except:
                    a=1
                    #print("No file")
                try:
                    data['swipeTask']=data_0['swipeTask']
                    
                except:
                    a=1
                    #print("No file")
            elif file_0[i]==file_0[0]:
                data=data_0
                try:
                    data['horizontalScrollTask']=data_0['horizontalScrollTask']
                except:
                    a=1
                    #print("No file")
                try:
                    data['verticalScrollTask']=data_0['verticalScrollTask']
                except:
                    a=1
                    #print("No file")
                try:
                    data['tapTask']=data_0['tapTask']
                except:
                    a=1
                    #print("No file")
                try:
                    data['swipeTask']=data_0['swipeTask']
                    
                except:
                    a=1
                    #print("No file")
                
    #print(data['tapTask'])
    Device_info=data['deviceInfo']['screenSize']
    return data,Device_info

def PlotJerk_AllTask(PlotData):
    import matplotlib.pyplot as plt
    DataX=list()
    DataY=list()
    AllColor=['red','green','blue','yellow','gray','purple','pink']
    ColorCount=0
    #for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
    for task in ['verticalScrollTask']:
     
        DataX=list()
        DataY=list()
        DataZ=list()
        for iTrial in range(len(PlotData[task]['trials'])):
            EachTrialDataX=list()
            EachTrialDataY=list()
            EachTrialDataZ=list()

            if iTrial==11:
                for iFinger in range(len(PlotData[task]['trials'][iTrial]["rawTouchTracks"])):
                    #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                    #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                    
                    if len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])>2:
                        for iPoint in range(3,len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                            Point_t=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                            Point_t_1=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                            Point_t_2=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]
                            Point_t_3=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]
                            X0=Point_t['location'][0]
                            Y0=Point_t['location'][1]
                            T0=Point_t['timestamp']

                            X1=Point_t_1['location'][0]
                            Y1=Point_t_1['location'][1]
                            T1=Point_t_1['timestamp']

                            X2=Point_t_2['location'][0]
                            Y2=Point_t_2['location'][1]
                            T2=Point_t_2['timestamp']

                            X3=Point_t_3['location'][0]
                            Y3=Point_t_3['location'][1]
                            T3=Point_t_3['timestamp']

                            myV3x=(X0-X1)/(T0-T1)
                            myV2x=(X1-X2)/(T1-T2)
                            myV1x=(X2-X3)/(T2-T3)

                            myV3y=(Y0-Y1)/(T0-T1)
                            myV2y=(Y1-Y2)/(T1-T2)
                            myV1y=(Y2-Y3)/(T2-T3)

                            myV3=np.sqrt(myV3x*myV3x+myV3y*myV3y)
                            myV2=np.sqrt(myV2x*myV2x+myV2y*myV2y)

                            myA3x=(myV3x-myV2x)/((T0-T2)/2)
                            myA2x=(myV2x-myV1x)/((T1-T3)/2)
                            myA3y=(myV3x-myV2x)/((T0-T2)/2)
                            myA2y=(myV2x-myV1x)/((T1-T3)/2)

                            myA3=np.sqrt(myA3x*myA3x+myA3y*myA3y)

                            myJerkx=(myA3x-myA2x)/((T0-T3)/3)
                            myJerky=(myA3y-myA2y)/((T0-T3)/3)

                            myJerk=np.sqrt(myJerkx*myJerkx+myJerky*myJerky)


                            Jerk=ComputeJerk([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3])
                            Accelerate=ComputeAccelerate([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2])
                            Speed=ComputeVelocity([X0,Y0,T0],[X1,Y1,T1])

                            print(iFinger,iPoint,X0,Y0," : ",Speed,Accelerate,Jerk," vs ",myV3,myA3,myJerk)
                            EachTrialDataX.append(Jerk)
                            EachTrialDataY.append(Accelerate)
                            EachTrialDataZ.append(Speed)
                DataX=EachTrialDataX
                DataY=EachTrialDataY
                DataZ=EachTrialDataZ
        plt.subplot(4,1,(ColorCount)+1)
        
        #plt.plot(Scale(DataY))
        #plt.plot(Scale(DataX))
        
        plt.plot(DataX)
        plt.ylim(0,5000)
        plt.xlim(0,10)
        #plt.scatter(DataX,DataY,c=AllColor[ColorCount])
        ColorCount=ColorCount+1                
                        #plt.legend(loc='upper right')
                
                
                
                
    
    plt.show()


def Scale(Data):
    import numpy as np
    Max=np.max(Data)
    Min=np.min(Data)
    ScaledData=Data
    for i in range(len(ScaledData)):
        ScaledData[i]=(Data[i]-Min)/(Max-Min)
    return ScaledData
def myPlot_tap(PlotData):
    import matplotlib.pyplot as plt

    AllColor=['red','green','blue','yellow','gray','purple','pink',"#661111","#772222","#883333","#992222","#992222","#992222","#992222","#992222","#992222","#992222","#992222","#992222","#992222"]
    
    for i in range(len(PlotData["rawTouchTracks"])):
        #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
        #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
        DataX=list()
        DataY=list()
        
        BadDataX=list()
        BadDataY=list()
        for j in range(len(PlotData["rawTouchTracks"][i]["rawTouches"])):
           
            
            #print("Finger",(i),"X",(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0]),"Y",(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1]),"T",(PlotData["rawTouchTracks"][i]["rawTouches"][j]["timestamp"]))
            if(PlotData["rawTouchTracks"][i]["rawTouches"][j]['label']==False):
               BadDataX.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0])
               BadDataY.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1])
            else:
               DataX.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0])
               DataY.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1])
            
    #//print(j/len(TaskData["rawTouchTracks"][i]["rawTouches"]))
            # DataX.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0])
            # DataY.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1])
        plt.scatter(BadDataX,BadDataY,c='black',label='black')
        plt.scatter(DataX,DataY,c=AllColor[i],label=AllColor[i])
            
            #plt.legend(loc='upper right')
    

    import matplotlib.patches as patches
    x1=PlotData["targetFrame"][0][0]
    x2=PlotData["targetFrame"][0][0]
    x3=PlotData["targetFrame"][0][0]+PlotData["targetFrame"][1][0]
    x4=PlotData["targetFrame"][0][0]+PlotData["targetFrame"][1][0]
    y1=PlotData["targetFrame"][0][1]
    y2=PlotData["targetFrame"][0][1]+PlotData["targetFrame"][1][1]
    y3=PlotData["targetFrame"][0][1]
    y4=PlotData["targetFrame"][0][1]+PlotData["targetFrame"][1][1]
    
    TargetX=[x1,x2,x1,x3,x4,x2,x4]
    TargetY=[y1,y2,y1,y3,y4,y2,y4]
    TargetXlocation=PlotData["targetFrame"][0][0]+0.5*PlotData["targetFrame"][1][0]
    TargetYlocation=PlotData["targetFrame"][0][1]+0.5*PlotData["targetFrame"][1][1]
    plt.plot(TargetX,TargetY)
    
    #plt.axvspan(ymin=(y1-100)/200,ymax=(y2-100)/200,xmin=(x1-100)/200,xmax=(x3-100)/200)
    #plt.add_patch(patches.Rectangle((TargetXlocation,TargetYlocation),0.5,0.5))
    #plt.axvspan(ymin=0.1,ymax=0.2,xmin=0.2,xmax=0.5)
    plt.axvspan(ymin=y1,ymax=y2,xmin=x1,xmax=x3,facecolor='blue')
    plt.xlim(x1-100,x3+100)
    plt.ylim(y1-100,y3+100)
    

def myPlot_swipe(PlotData,Device_info):
    import matplotlib.pyplot as plt
    AllColor=['red','green','blue','yellow','gray','purple','pink',"#661111","#772222","#883333","#992222","#992222","#992222","#992222","#992222","#992222","#992222","#992222","#992222","#992222"]
    print(len(PlotData["rawTouchTracks"]))
    for i in range(len(PlotData["rawTouchTracks"])):
        #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
        #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
        DataX=list()
        DataY=list()
        
        BadDataX=list()
        BadDataY=list()
        for j in range(len(PlotData["rawTouchTracks"][i]["rawTouches"])):
           
            
            #print("Finger",(i),"X",(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0]),"Y",(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1]),"T",(PlotData["rawTouchTracks"][i]["rawTouches"][j]["timestamp"]))
            if(PlotData["rawTouchTracks"][i]["rawTouches"][j]['label']==False):
               BadDataX.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0])
               BadDataY.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1])
            else:
               DataX.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0])
               DataY.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1])
            
    #//print(j/len(TaskData["rawTouchTracks"][i]["rawTouches"]))
            # DataX.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0])
            # DataY.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1])
        
        plt.scatter(DataX,DataY,c=AllColor[i],label=AllColor[i])
        plt.scatter(BadDataX,BadDataY,c='black',label='black')   
            #plt.legend(loc='upper right')
    plt.xlim(0,Device_info[0])
    plt.ylim(0,Device_info[1])

    
def myPlot_scroll(PlotData,Device_info):
    import matplotlib.pyplot as plt
    AllColor=['red','green','blue','yellow','gray','purple','pink',"#661111","#772222","#883333","#992222","#992222","#992222","#992222","#992222","#992222","#992222"]
    #print(len(PlotData["rawTouchTracks"]))
    for i in range(len(PlotData["rawTouchTracks"])):
        #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
        #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
        DataX=list()
        DataY=list()
        
        BadDataX=list()
        BadDataY=list()
        for j in range(len(PlotData["rawTouchTracks"][i]["rawTouches"])):
           
            
            #print("Finger",(i),"X",(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0]),"Y",(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1]),"T",(PlotData["rawTouchTracks"][i]["rawTouches"][j]["timestamp"]))
            if(PlotData["rawTouchTracks"][i]["rawTouches"][j]['label']==False):
               BadDataX.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0])
               BadDataY.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1])
            else:
               DataX.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0])
               DataY.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1])
            
    #//print(j/len(TaskData["rawTouchTracks"][i]["rawTouches"]))
            # DataX.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][0])
            # DataY.append(PlotData["rawTouchTracks"][i]["rawTouches"][j]["location"][1])
        plt.scatter(BadDataX,BadDataY,c='black',label='black')
        plt.scatter(DataX,DataY,c=AllColor[i],label=AllColor[i])
            
            #plt.legend(loc='upper right')
    plt.xlim(0,Device_info[0])
    plt.ylim(0,Device_info[1]) 
    


def LabelByHuman_TapGraph(myTask,Device_info,TestTrial):
    import sklearn
    from sklearn import cluster
    import numpy as np
    import TaskSuccessVerify as tv

    def ClusterBetweenFingers(BeforeClusterData,AfterClusterData):

        ClusterData=np.array(BeforeClusterData).transpose(1,0)[2:3].transpose(1,0)
        if len(BeforeClusterData)>1:
           
            maxScore=0
            #print("len(BeforeClusterData)",len(BeforeClusterData))
            ChooseLabel=list(np.zeros(len(BeforeClusterData)))
            if len(BeforeClusterData)>2:
                #print("test")
                for nCluster in range(2,len(BeforeClusterData)):
                    #print(nCluster)
                    kmeans_fit = cluster.KMeans(n_clusters = nCluster).fit(np.array(ClusterData))
                    cluster_labels = kmeans_fit.labels_
                    #print(cluster_labels)
                    #print("KmeanScore: ",sklearn.metrics.silhouette_score(CandidateData,cluster_labels))
                    #print(len(list(set(cluster_labels))))
                    if len(list(set(cluster_labels)))>1:
                        if maxScore<=sklearn.metrics.silhouette_score(ClusterData,cluster_labels):
                            maxScore=sklearn.metrics.silhouette_score(ClusterData,cluster_labels)
                            
                            ChooseLabel=cluster_labels
                            #print("Choose",nCluster,ChooseLabel)
            elif len(BeforeClusterData)==2:
                kmeans_fit = cluster.KMeans(n_clusters = 2).fit(np.array(ClusterData))
                cluster_labels = kmeans_fit.labels_
                ChooseLabel=cluster_labels
            #print(chooseNcluster)
            
            
            #kmeans_fit = cluster.KMeans(n_clusters = chooseNcluster).fit(np.array(CandidateData))
            #cluster_labels = kmeans_fit.labels_
            #print(ChooseLabel)
            #print(CandidateData,len(CandidateData))
            #print("ChooseLabel",ChooseLabel)
            ###如果fisrt touch 也是最大值用first touch
            largestCluster=np.argmax(np.bincount(ChooseLabel))

            for i in range(len(BeforeClusterData)):
                if BeforeClusterData[i][0]==0:
                    #print("FistTouch len: ",np.where(ChooseLabel==ChooseLabel[i])[0])
                    if len(np.where(ChooseLabel==ChooseLabel[i])[0])>=max(np.bincount(ChooseLabel)):
                        largestCluster=ChooseLabel[i]

            ###如果fisrt touch 也是最大值用first touch first touch 優先選用
            ThisClusterFinalPoint=list()
            
            for i in range(len(BeforeClusterData)):
                
                if(ChooseLabel[i]==largestCluster):
                    AppendPoint=[BeforeClusterData[i][0],BeforeClusterData[i][1],BeforeClusterData[i][2],BeforeClusterData[i][3]]
                    #print("Larget: ",AppendPoint)
                    ThisClusterFinalPoint.append(AppendPoint)
                    #print("ThisClusterFinalPoint",ThisClusterFinalPoint)
            #print(ThisClusterFinalPoint[0])
            ##找出離該劇類中心最近點為代表
            #print("FinalCluster:",np.array(ThisClusterFinalPoint[0]).shape)
            Xave=np.mean(np.array(ThisClusterFinalPoint).transpose(1,0)[2])
            Yave=np.mean(np.array(ThisClusterFinalPoint).transpose(1,0)[3])
            Distance=9999999999999999999999999
            
            SelectedPoint=ThisClusterFinalPoint[0]
            #print("AfterClusterData",AfterClusterData)
            #print("ThisClusterFinalPoint",ThisClusterFinalPoint)
            for i in range(len(ThisClusterFinalPoint)):
                ThisClusterFinalPoint_InAfterCluserData=False
                for AfterCluserIndex in range(len(AfterClusterData)):
                    if AfterClusterData[AfterCluserIndex][0]==ThisClusterFinalPoint[i][0]:
                        if  AfterClusterData[AfterCluserIndex][1]==ThisClusterFinalPoint[i][1]:
                            ThisClusterFinalPoint_InAfterCluserData=True

                
               
                if (ThisClusterFinalPoint_InAfterCluserData):
                    
                    distance=np.sqrt((ThisClusterFinalPoint[i][2]-Xave)*(ThisClusterFinalPoint[i][2]-Xave)+(ThisClusterFinalPoint[i][3]-Yave)*(ThisClusterFinalPoint[i][3]-Yave))
                    #LabelFalse(OutputData,TestTrial,iFinger,ThisClusterFinalPoint[i][0])
                    #print(ThisClusterFinalPoint[i],"distance",distance)

                    if (distance<Distance) & (Distance!=0.0) & (distance!=0.0):
                        #print(ThisClusterFinalPoint[i])
                        Distance=distance
                        SelectedPoint=ThisClusterFinalPoint[i]

            return SelectedPoint
           

    OutputData=myTask
    TapAllowableMovement=tv.TapAllowableMovement
    
    iTrial=TestTrial
    ReferFingerIndex=0
    PointsAfterCluster=0;
    CandidateDataInFinger=list()
    AllCandidateDataBeforeCluster=list()

    AllFingerLargestCluster=list()
    for iFinger in range(len(OutputData["rawTouchTracks"])):
        
        CandidateData=list()
        for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
             
            TargetX=OutputData["targetFrame"][0][0]+ OutputData["targetFrame"][1][0]*0.5
            TargetY=OutputData["targetFrame"][0][1]+ OutputData["targetFrame"][1][1]*0.5
             
            # if (abs(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0] - TargetX) > myTask[iTrial]["targetFrame"][1][0]*0.5)|(abs(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1] - TargetY) > myTask[iTrial]["targetFrame"][1][1]*0.5):
            #     LabelFalse(myTask,TestTrial,iFinger,iPoint)
                
             
            if iPoint==0 or iPoint==1:
                accelerate=0
            else:
                positionX1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                positionY1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                positionT1=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]

                positionX2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                positionY2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                positionT2=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]

                positionX3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                positionY3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                positionT3=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]

                V1=np.sqrt((positionX2-positionX1)*(positionX2-positionX1)+(positionY2-positionY1)*(positionY2-positionY1))/(positionT2-positionT1)
                V2=np.sqrt((positionX3-positionX2)*(positionX3-positionX2)+(positionY3-positionY2)*(positionY3-positionY2))/(positionT3-positionT2)

                accelerate=V2-V1
             #print((TestTrial),(iFinger),(iPoint),(accelerate))
            if accelerate>0:
                LabelFalse(OutputData,TestTrial,iFinger,iPoint)
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
                    LabelFalse(OutputData,TestTrial,iFinger,iPoint-2)

                if (AverageX2-positionX3)*(AverageX2-positionX3)+(AverageY2-positionY3)*(AverageY2-positionY3)>TapAllowableMovement*TapAllowableMovement:
                    LabelFalse(OutputData,TestTrial,iFinger,iPoint) 
            if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                positionx=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]
                positiony=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]
                time=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]-OutputData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]
                dx=positionx-OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"][0]
                dy=positiony-OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"][1]
                dS=dx*dx+dy*dy
                  #AllData.append([timestamp,previousLocationX,previousLocationY,majorRadius,locationX,locationY])

                CandidateData.append([iPoint,positionx,positiony,time,dS])
        for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
            if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                px=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]
                py=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]
                CandidateDataInFinger.append([iFinger,iPoint])
                AllCandidateDataBeforeCluster.append([iFinger,iPoint,px,py])

        ##聚類開始
        if len(CandidateData)>1:
            maxScore=0
            ClusterData=np.array(CandidateData).transpose(1,0)[1:4].transpose(1,0)

            if len(CandidateData)>2:
                for nCluster in range(2,len(CandidateData)):
                    kmeans_fit = cluster.KMeans(n_clusters = nCluster).fit(np.array(ClusterData))
                    cluster_labels = kmeans_fit.labels_
                    #print(cluster_labels)
                    #print("KmeanScore: ",sklearn.metrics.silhouette_score(CandidateData,cluster_labels))
                    if maxScore<=sklearn.metrics.silhouette_score(ClusterData,cluster_labels):
                        maxScore=sklearn.metrics.silhouette_score(ClusterData,cluster_labels)
                        
                        ChooseLabel=cluster_labels
                        #print("Choose",nCluster,ChooseLabel)
            elif len(CandidateData)==2:
                kmeans_fit = cluster.KMeans(n_clusters = 2).fit(np.array(ClusterData))
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
                #print("Other cluster",[iFinger,CandidateData[i][0],CandidateData[i][1],CandidateData[i][2]])
                if(ChooseLabel[i]!=largestCluster):
                    LabelFalse(OutputData,TestTrial,iFinger,CheckPoint)
                else:
                    ThisClusterFinalPoint.append(CandidateData[i])
                    AllFingerLargestCluster.append([iFinger,CandidateData[i][0],CandidateData[i][1],CandidateData[i][2]])
            ##找出離該劇類中心最近點為代表
            Xave=np.mean(np.array(ThisClusterFinalPoint).transpose(1,0)[1])
            Yave=np.mean(np.array(ThisClusterFinalPoint).transpose(1,0)[2])
            Distance=9999999999999999999999999
            SelectedPoint=0
            #print("ThisClusterFinalPoint INFinger:",iFinger,ThisClusterFinalPoint)
            for i in range(len(ThisClusterFinalPoint)):
                distance=np.sqrt((ThisClusterFinalPoint[i][1]-Xave)*(ThisClusterFinalPoint[i][1]-Xave)+(ThisClusterFinalPoint[i][2]-Yave)*(ThisClusterFinalPoint[i][2]-Yave))
                #print(ThisClusterFinalPoint,"ThisClusterFinalPoint distance",distance)
                LabelFalse(OutputData,TestTrial,iFinger,ThisClusterFinalPoint[i][0])
                if distance<=Distance:
                    Distance=distance
                    SelectedPoint=ThisClusterFinalPoint[i][0]

            OutputData["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['label']=True
            OutputData["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['location'][0]=Xave
            OutputData["rawTouchTracks"][iFinger]["rawTouches"][SelectedPoint]['location'][1]=Yave
            #print("Finger",iFinger," Center",Xave,Yave)
    #in Finger end

    ####最後解決ｍｕlti fingers
   
    #print("FingerNum",len(OutputData["rawTouchTracks"]))
    # if len(OutputData["rawTouchTracks"])>0:
    #     AfterCluster_Data=list()
    #     DataPointNum=0
    #     for iFinger in range(len(OutputData["rawTouchTracks"])):
    #         for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
    #              if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
    #                 px=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]
    #                 py=OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]
    #                 AfterCluster_Data.append([iFinger,iPoint,px,py])
    #                 DataPointNum=DataPointNum+1
    #     #print("AllFingerLargestCluster",AllFingerLargestCluster)
    #     #print("AllFingerLargestCluster shape",np.array(AllFingerLargestCluster).shape)
    #     #print(AllCandidateDataBeforeCluster)  
    #     #print("After Cluster: ",len(AfterCluster_Data)) 
    #     #print("Cluster....")
    #     #print("AllFingerLargestCluster",AllFingerLargestCluster)
    #     #print(AfterCluster_Data)
    #     FinalChoosePoint=ClusterBetweenFingers(AllFingerLargestCluster,AfterCluster_Data)
    #     #FinalChoosePoint=ClusterBetweenFingers(AllCandidateDataBeforeCluster,AfterCluster_Data)
        
    #     #print("Final Point",FinalChoosePoint)
    #     if len(AfterCluster_Data)>1:
    #         for i in range(len(AfterCluster_Data)):
    #             if AfterCluster_Data[i][0]!=FinalChoosePoint[0]:
    #                 LabelFalse(OutputData,iTrial,AfterCluster_Data[i][0],AfterCluster_Data[i][1])

    #     # if len(AfterCluster_Data)>1:
    #     #     largestClusterFinger=np.argmax(np.bincount(np.array(AllCandidateDataBeforeCluster).transpose(1,0)[0]))
    #     #     print("Largest is ",largestClusterFinger)


    #     #     for i in range(len(AfterCluster_Data)):
    #     #         CheckPoint=AfterCluster_Data[i][1]
    #     #         if(AfterCluster_Data[i][0]!=largestClusterFinger):
    #     #             if DataPointNum>0:
    #     #                 #LabelFalse(OutputData,iTrial,AfterCluster_Data[i][0],CheckPoint)
    #     #                 DataPointNum=DataPointNum-1

    #     DataPointNum=0
    #     for iFinger in range(len(OutputData["rawTouchTracks"])):
    #         for iPoint in range(len(OutputData["rawTouchTracks"][iFinger]["rawTouches"])):
    #              if OutputData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
    #                 DataPointNum=DataPointNum+1
    #     #print("After Handle Multitouch: ",DataPointNum)     
    return OutputData

def LabelByHuman_PanGraph(myTask,Device_info,Accelerate_Threshold):
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

    import sklearn
    from sklearn import cluster
    import numpy as np
    iTrial=0
    
    for iFinger in range(len(myTask["rawTouchTracks"])):
        
        CandidateData=list()
        for iPoint in range(len(myTask["rawTouchTracks"][iFinger]["rawTouches"])):
             
            
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
                 positionX1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                 positionY1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                 positionT1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["timestamp"]
                 positionRadius1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["majorRadius"]
                 
                 positionX2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                 positionY2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                 positionT2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"]
                 positionRadius2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["majorRadius"]
                 
                 positionX3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                 positionY3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                 positionT3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                 positionRadius3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["majorRadius"]
                 
                 V1=np.sqrt((positionX2-positionX1)*(positionX2-positionX1)+(positionY2-positionY1)*(positionY2-positionY1))/(positionT2-positionT1)
                 V2=np.sqrt((positionX3-positionX2)*(positionX3-positionX2)+(positionY3-positionY2)*(positionY3-positionY2))/(positionT3-positionT2)
                 
                 PointTheta_t=ComputeTheta(positionX2,positionY2,positionX3,positionY3)
                 PointTheta_t_1=ComputeTheta(positionX1,positionY1,positionX2,positionY2)
                
                 #accelerate=(V2-V1)/((positionT3-positionT1)/2)
                 accelerate=(V2-V1)
                 
                 if iPoint>3:
                     positionX0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][0]/Device_info[0]
                     positionY0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][1]/Device_info[1]
                     positionT0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["timestamp"]
                     positionRadius0=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["majorRadius"]
                     
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
                             LabelFalse(myTask,iTrial,iFinger,iPoint)
                         #if iPoint>3:
                            
                             #if (myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]['label']==True)&(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]['label']==True)&(myTask[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]['label']==True):
                             #  LabelFalse(myTask,TestTrial,iFinger,iPoint)
    return myTask



def LabelAllFalse(TaskData):
    
    for iFinger in range(len(TaskData["rawTouchTracks"])):
        for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])): 
                TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=False
    return TaskData


def LabelByHuman_SwipeGraph(myTask,Device_info,TestTrial):
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


    import sklearn
    from sklearn import cluster
    import numpy as np
    
    iTrial=TestTrial
    for iFinger in range(len(myTask["rawTouchTracks"])):
        
        CandidateData=list()
        for iPoint in range(len(myTask["rawTouchTracks"][iFinger]["rawTouches"])):
             
            
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

                 positionX0=myTask["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0]/Device_info[0]
                 positionY0=myTask["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1]/Device_info[1]
                 

                 positionX1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][0]/Device_info[0]
                 positionY1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]["location"][1]/Device_info[1]
                 
                 positionX2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][0]/Device_info[0]
                 positionY2=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]["location"][1]/Device_info[1]
                 
                 positionX3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][0]/Device_info[0]
                 positionY3=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["location"][1]/Device_info[1]
                 
                 positionX4=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                 positionY4=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]
                 
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

    for iFinger in range(len(myTask["rawTouchTracks"])):
            
            AllPoint_dx=list()
            AllPoint_dy=list()

            for iPoint in range(len(myTask["rawTouchTracks"][iFinger]["rawTouches"])):
                if myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    positionX_t_1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"][0]/Device_info[0]
                    positionY_t_1=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"][1]/Device_info[1]

                  

                    positionX=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]/Device_info[0]
                    positionY=myTask["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]/Device_info[1]

                    AllPoint_dx.append(positionX-positionX_t_1)
                    AllPoint_dy.append(positionY-positionY_t_1)

            Ave_dx=np.mean(AllPoint_dx)
            Ave_dy=np.mean(AllPoint_dy)
            NewX=Ave_dx*100000
            NewY=Ave_dy*100000

            print(NewX,NewY)
            myTask["rawTouchTracks"][iFinger]["rawTouches"][1]["location"][0]=myTask["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0]+NewX
            myTask["rawTouchTracks"][iFinger]["rawTouches"][1]["location"][1]=myTask["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1]+NewY
    
    LabelAllFalse(myTask)

    for iFinger in range(len(myTask["rawTouchTracks"])):
        if len(myTask["rawTouchTracks"][iFinger]["rawTouches"])>1:
            myTask["rawTouchTracks"][iFinger]["rawTouches"][0]['label']=True
            myTask["rawTouchTracks"][iFinger]["rawTouches"][1]['label']=True
                
                


    return myTask






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

def FilteredJson2(InputTaskData):
    FinalTaskData=list()
    
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
    FinalTaskData.append(FilterDataDict) 

    return FinalTaskData

def PlotTap(data,TestTrial,Device_info):
    import TaskSuccessVerify as tv
    #TaskData=data['tapTask']['trials']
    #Device_info=data['deviceInfo']['screenSize']
    LabelAllTrue(data,TestTrial)
    OriTrue=0
    NewTrue=0
    HD=0.05
    TA=0.7
    IG=0.05
    IG_state=2

    #plt.subplot(2,1,1)
    #myPlot_tap(data)
    OptimizedData=LabelByHuman_TapGraph(data,Device_info,TestTrial)
    #LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state)


    OptimizedData=FilteredJson2(OptimizedData)
    
    #plt.subplot(2,1,2)
    myPlot_tap(data)
    

    # if tv.TapTask(OptimizedData[0],TestTrial)==False:
    #     #myPlot_tap(OptimizedData[0])
    #     myPlot_tap(data)

    #
    #myPlot_tap(data['tapTask']['trials'][TestTrial])
    #myPlot_tap(FilteredJson(data['tapTask']['trials'])[TestTrial])

   
   
    
    
    
    
   

    return tv.TapTask(OptimizedData[0],TestTrial)

def PlotJerk_AllVelocity(PlotData,User):
    import matplotlib.pyplot as plt
    DataX=list()
    DataY=list()

    DataX=list()
    DataY=list()
    DataZ=list()
    AllColor=['red','green','blue','yellow','gray','purple','pink']
    ColorCount=0
    for task in ['swipeTask','horizontalScrollTask','verticalScrollTask','tapTask']:
    #for task in ['verticalScrollTask']:
        EachTrialDataX=list()
        EachTrialDataY=list()
        EachTrialDataZ=list()
        
        for iTrial in range(len(PlotData[task]['trials'])):
            

            
            for iFinger in range(len(PlotData[task]['trials'][iTrial]["rawTouchTracks"])):
                #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                
                if len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])>2:
                    for iPoint in range(3,len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                        Point_t=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                        Point_t_1=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                        Point_t_2=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]
                        Point_t_3=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]
                        X0=Point_t['location'][0]
                        Y0=Point_t['location'][1]
                        T0=Point_t['timestamp']

                        X1=Point_t_1['location'][0]
                        Y1=Point_t_1['location'][1]
                        T1=Point_t_1['timestamp']

                        X2=Point_t_2['location'][0]
                        Y2=Point_t_2['location'][1]
                        T2=Point_t_2['timestamp']

                        X3=Point_t_3['location'][0]
                        Y3=Point_t_3['location'][1]
                        T3=Point_t_3['timestamp']

                        myV3x=(X0-X1)/(T0-T1)
                        myV2x=(X1-X2)/(T1-T2)
                        myV1x=(X2-X3)/(T2-T3)

                        myV3y=(Y0-Y1)/(T0-T1)
                        myV2y=(Y1-Y2)/(T1-T2)
                        myV1y=(Y2-Y3)/(T2-T3)

                        myV3=np.sqrt(myV3x*myV3x+myV3y*myV3y)
                        myV2=np.sqrt(myV2x*myV2x+myV2y*myV2y)

                        myA3x=(myV3x-myV2x)/((T0-T2)/2)
                        myA2x=(myV2x-myV1x)/((T1-T3)/2)
                        myA3y=(myV3x-myV2x)/((T0-T2)/2)
                        myA2y=(myV2x-myV1x)/((T1-T3)/2)

                        myA3=np.sqrt(myA3x*myA3x+myA3y*myA3y)

                        myJerkx=(myA3x-myA2x)/((T0-T3)/3)
                        myJerky=(myA3y-myA2y)/((T0-T3)/3)

                        myJerk=np.sqrt(myJerkx*myJerkx+myJerky*myJerky)


                        Jerk=ComputeJerk([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3])
                        Accelerate=ComputeAccelerate([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2])
                        Speed=ComputeVelocity([X0,Y0,T0],[X1,Y1,T1])

                        print(iFinger,iPoint,X0,Y0," : ",Speed,Accelerate,Jerk," vs ",myV3,myA3,myJerk)
                        EachTrialDataX.append(ComputeVelocityX([X0,Y0,T0],[X1,Y1,T1]))
                        EachTrialDataY.append(ComputeVelocityY([X0,Y0,T0],[X1,Y1,T1]))
                        EachTrialDataZ.append(Speed)
            DataX.append(EachTrialDataX)
            DataY.append(EachTrialDataY)
            DataZ.append(EachTrialDataZ)

    #plt.subplot(4,1,(ColorCount)+1)
        
        #plt.plot(Scale(DataY))
        #plt.plot(Scale(DataX))
        
        #plt.plot(DataX)
        
        plt.scatter(EachTrialDataX,EachTrialDataY,c=AllColor[ColorCount],label=task)
        ColorCount=ColorCount+1 
        plt.ylim(-10,10)
        plt.xlim(-10,10)               
        plt.legend(loc='upper right')
        
        # if User=='3001':
        #     a="P1"
        # elif User=="3002":
        #     a="P2"
        # elif User=="3012":
        #     a="P11"
        # plt.title(str(a))
        plt.xlabel("Horizontal Velocity (points/ms)")
        plt.ylabel("Vertical Velocity (points/ms)")    
                
                
    
    # plt.show()
def Plot_FingerTime(PlotData,User,iUser):
    import matplotlib.pyplot as plt
    DataX=list()
    DataY=list()

    DataX=list()
    DataY=list()
    DataZ=list()
    AllColor=['red','green','blue','yellow','gray','purple','pink']
    ColorCount=0
    for task in ['tapTask','swipeTask']:
    #for task in ['verticalScrollTask','horizontalScrollTask']:
        EachTrialDataX=list()
        EachTrialDataY=list()
        EachTrialDataZ=list()
        
        for iTrial in range(len(PlotData[task]['trials'])):
            
            for iFinger in range(len(PlotData[task]['trials'][iTrial]["rawTouchTracks"])):
                #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                
                Finaldt=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][-1]['timestamp']-PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                
                EachTrialDataX.append(Finaldt)
                
        DataX.append(EachTrialDataX)
            

    #plt.subplot(4,1,(ColorCount)+1)
        
        #plt.plot(Scale(DataY))
        #plt.plot(Scale(DataX))
        
        #plt.plot(DataX)

    print(User+" VS1% "+str(np.percentile(DataX[0],1))+" VS5% "+str(np.percentile(DataX[0],5))+" VS10% "+str(np.percentile(DataX[0],10))+" HS1% "+str(np.percentile(DataX[1],1))+" HS5% "+str(np.percentile(DataX[1],5))+" HS10% "+str(np.percentile(DataX[1],10)))
    


    #print(User+" Tap90% "+str(np.percentile(DataX[0],90))+" Tap95% "+str(np.percentile(DataX[0],95))+" Tap97.5% "+str(np.percentile(DataX[0],97.5))+" Tap99% "+str(np.percentile(DataX[0],99))+" Tap100% "+str(np.percentile(DataX[0],100))+"Tap3sigma"+str(np.mean(DataX[0])+3*np.std(DataX[0])))
    #print(User+" Tap95% "+str(np.percentile(DataX[0],95))+" Tap97.5% "+str(np.percentile(DataX[0],97.5))+" Tap99% "+str(np.percentile(DataX[0],99))+" Tap2sigma"+str(np.mean(DataX[0])+2*np.std(DataX[0]))+" 97.5%+2sigma: "+str(np.mean([np.percentile(DataX[0],97.5),np.mean(DataX[0])+2*np.std(DataX[0])])))
    
    #print(User+"Tap Max"+str(np.max(DataX[0]))+" Tap90% "+str(np.percentile(DataX[0],90))+" Tap95% "+str(np.percentile(DataX[0],95))+" Tap100% "+str(np.percentile(DataX[0],100))+"Swipe Max"+str(np.max(DataX[1]))+" 90% "+str(np.percentile(DataX[1],90)))
    #
    #print(User+"Tap Max"+str(np.mean(DataX[0])+3*np.std(DataX[0]))+" 3/4"+str(np.median(DataX[0]))+"Swipe Max"+str(np.mean(DataX[1])+3*np.std(DataX[1]))+" 3/4"+str(np.median(DataX[1])))
    #print(User+"Tap Max"+str(np.max(DataX[0]))+" Median"+str(np.median(DataX[0]))+"Swipe Max"+str(np.max(DataX[1]))+" Median"+str(np.median(DataX[1])))
        

    plt.boxplot(DataX)
    plt.xticks([1,2],['tap','swipe'])
    plt.ylim([0,2])
    plt.title("P"+str(iUser))
    #plt.boxplot(DataX,EachTrialDataY,c=AllColor[ColorCount],label=task)
    ColorCount=ColorCount+1 
              
    
    plt.ylabel("Duration (sec)")    
                
    
    #plt.show()

def PlotJerk_Accelerate(PlotData,User):
    import matplotlib.pyplot as plt
    DataX=list()
    DataY=list()

    DataX=list()
    DataY=list()
    DataZ=list()
    AllColor=['red','green','blue','yellow','gray','purple','pink']
    ColorCount=0
    for task in ['swipeTask','horizontalScrollTask','verticalScrollTask','tapTask']:
    #for task in ['verticalScrollTask']:
        EachTrialDataX=list()
        EachTrialDataY=list()
        EachTrialDataZ=list()
        
        for iTrial in range(len(PlotData[task]['trials'])):
            

            
            for iFinger in range(len(PlotData[task]['trials'][iTrial]["rawTouchTracks"])):
                #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                
                if len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])>2:
                    for iPoint in range(3,len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                        Point_t=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                        Point_t_1=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                        Point_t_2=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]
                        Point_t_3=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]
                        X0=Point_t['location'][0]
                        Y0=Point_t['location'][1]
                        T0=Point_t['timestamp']

                        X1=Point_t_1['location'][0]
                        Y1=Point_t_1['location'][1]
                        T1=Point_t_1['timestamp']

                        X2=Point_t_2['location'][0]
                        Y2=Point_t_2['location'][1]
                        T2=Point_t_2['timestamp']

                        X3=Point_t_3['location'][0]
                        Y3=Point_t_3['location'][1]
                        T3=Point_t_3['timestamp']

                        myV3x=(X0-X1)/(T0-T1)
                        myV2x=(X1-X2)/(T1-T2)
                        myV1x=(X2-X3)/(T2-T3)

                        myV3y=(Y0-Y1)/(T0-T1)
                        myV2y=(Y1-Y2)/(T1-T2)
                        myV1y=(Y2-Y3)/(T2-T3)

                        myV3=np.sqrt(myV3x*myV3x+myV3y*myV3y)
                        myV2=np.sqrt(myV2x*myV2x+myV2y*myV2y)

                        myA3x=(myV3x-myV2x)/((T0-T2)/2)
                        myA2x=(myV2x-myV1x)/((T1-T3)/2)
                        myA3y=(myV3x-myV2x)/((T0-T2)/2)
                        myA2y=(myV2x-myV1x)/((T1-T3)/2)

                        myA3=np.sqrt(myA3x*myA3x+myA3y*myA3y)

                        myJerkx=(myA3x-myA2x)/((T0-T3)/3)
                        myJerky=(myA3y-myA2y)/((T0-T3)/3)

                        myJerk=np.sqrt(myJerkx*myJerkx+myJerky*myJerky)


                        Jerk=ComputeJerk([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3])
                        Accelerate=ComputeAccelerate([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2])
                        Speed=ComputeVelocity([X0,Y0,T0],[X1,Y1,T1])

                        print(iFinger,iPoint,X0,Y0," : ",Speed,Accelerate,Jerk," vs ",myV3,myA3,myJerk)
                        # EachTrialDataX.append(ComputeAccelerateX([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2]))
                        # EachTrialDataY.append(ComputeAccelerateY([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2]))
                        # EachTrialDataZ.append(Speed)
                        EachTrialDataX.append(ComputeJerkX([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3]))
                        EachTrialDataY.append(ComputeJerkY([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3]))
                        EachTrialDataZ.append(Speed)




            DataX.append(EachTrialDataX)
            DataY.append(EachTrialDataY)
            DataZ.append(EachTrialDataZ)

    #plt.subplot(4,1,(ColorCount)+1)
        
        #plt.plot(Scale(DataY))
        #plt.plot(Scale(DataX))
        
        #plt.plot(DataX)
        
        plt.scatter(EachTrialDataX,EachTrialDataY,c=AllColor[ColorCount],label=task)
        ColorCount=ColorCount+1 
        plt.ylim(-10,10)
        plt.xlim(-10,10)               
        plt.legend(loc='upper right')
        
        if User=='3001':
            a="P1"
        elif User=="3002":
            a="P2"
        elif User=="3012":
            a="P11"
        plt.title(str(a))
        plt.xlabel("Horizontal Velocity (points/ms)")
        plt.ylabel("Vertical Velocity (points/ms)")    
                
                
    

def PlotSwipe(data,TestTrial,Device_info):
    
    #TaskData=data['tapTask']['trials']
    #Device_info=data['deviceInfo']['screenSize']
    LabelAllTrue(data,TestTrial)
    OriTrue=0
    NewTrue=0
    HD=0.05
    TA=0.7
    IG=0.05
    IG_state=2

    LabelByHuman_SwipeGraph(data,Device_info,TestTrial)
    #LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state)
    myPlot_swipe(data,Device_info)
    #
    #myPlot_tap(data['tapTask']['trials'][TestTrial])
    #myPlot_tap(FilteredJson(data['tapTask']['trials'])[TestTrial])
    return data

def PlotHScroll(data,TestTrial,Device_info):
    
    #TaskData=data['tapTask']['trials']
    #Device_info=data['deviceInfo']['screenSize']
    LabelAllTrue(data,TestTrial)
    OriTrue=0
    NewTrue=0
    HD=0.05
    TA=0.7
    IG=0.05
    IG_state=2
    LabelByHuman_PanGraph(data,Device_info,0)
    
    #LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state)
    myPlot_scroll(data,Device_info)
    #
    #myPlot_tap(data['tapTask']['trials'][TestTrial])
    #myPlot_tap(FilteredJson(data['tapTask']['trials'])[TestTrial])
    return data

def PlotVScroll(data,TestTrial,Device_info):
    
    #TaskData=data['tapTask']['trials']
    #Device_info=data['deviceInfo']['screenSize']
    LabelAllTrue(data,TestTrial)
    OriTrue=0
    NewTrue=0
    HD=0.05
    TA=0.7
    IG=0.05
    IG_state=2

    
    #LabelByPersonalTouch(TaskData,Device_info,HD,TA,IG,IG_state)
    myPlot_scroll(data,Device_info)
    #
    #myPlot_tap(data['tapTask']['trials'][TestTrial])
    #myPlot_tap(FilteredJson(data['tapTask']['trials'])[TestTrial])
    return data

def PlotJerk(PlotData):
    import matplotlib.pyplot as plt
    DataX=list()
    DataY=list()
      
    for iFinger in range(len(PlotData["rawTouchTracks"])):
        #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
        #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
        
        if len(PlotData["rawTouchTracks"][iFinger]["rawTouches"])>2:
            for iPoint in range(3,len(PlotData["rawTouchTracks"][iFinger]["rawTouches"])):
                Point_t=PlotData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                Point_t_1=PlotData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                Point_t_2=PlotData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]
                Point_t_3=PlotData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]
                X0=Point_t['location'][0]
                Y0=Point_t['location'][1]
                T0=Point_t['timestamp']

                X1=Point_t_1['location'][0]
                Y1=Point_t_1['location'][1]
                T1=Point_t_1['timestamp']

                X2=Point_t_2['location'][0]
                Y2=Point_t_2['location'][1]
                T2=Point_t_2['timestamp']

                X3=Point_t_3['location'][0]
                Y3=Point_t_3['location'][1]
                T3=Point_t_3['timestamp']


                Jerk=ComputeJerk([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3])
                Accelerate=ComputeAccelerate([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2])
                DataX.append(Jerk)
                DataY.append(Accelerate)
                plt.scatter(DataX,DataY)
                
                #plt.legend(loc='upper right')
        
        
        
        
    
    plt.show()



def PlotAllJerk(PlotData):
    import matplotlib.pyplot as plt
    

    AllDataX=list()
    AllDataY=list()
    AllDataZ=list()
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        DataX=list()
        DataY=list()
        DataZ=list()
        for iTrial in range(len(PlotData[task]['trials'])):
            DataX_IneachTrial=list()
            DataY_IneachTrial=list()
            DataZ_IneachTrial=list()
            for iFinger in range(len(PlotData[task]['trials'][iTrial]["rawTouchTracks"])):
                #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                if len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])>2:
                    for iPoint in range(3,len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                        Point_t=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                        Point_t_1=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                        Point_t_2=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]
                        Point_t_3=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]
                        X0=Point_t['location'][0]
                        Y0=Point_t['location'][1]
                        T0=Point_t['timestamp']

                        X1=Point_t_1['location'][0]
                        Y1=Point_t_1['location'][1]
                        T1=Point_t_1['timestamp']

                        X2=Point_t_2['location'][0]
                        Y2=Point_t_2['location'][1]
                        T2=Point_t_2['timestamp']

                        X3=Point_t_3['location'][0]
                        Y3=Point_t_3['location'][1]
                        T3=Point_t_3['timestamp']

                        Velocity=ComputeVelocity([X0,Y0,T0],[X1,Y1,T1])
                        Velocity_t_1=ComputeVelocity([X1,Y1,T1],[X2,Y2,T2])

                        
                        
                        Accelerate=ComputeAccelerate([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2])
                        #Accelerate=Velocity-Velocity_t_1

                        A1=ComputeAccelerate([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2])
                        A2=ComputeAccelerate([X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3])

                        Jerk=ComputeJerk([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3])
                        #Jerk=A1-A2
                        

                        if ~np.isnan(Jerk):
                            DataX_IneachTrial.append(Jerk)
                        if ~np.isnan(Accelerate):
                            DataY_IneachTrial.append(Accelerate)
                        if ~np.isnan(Velocity):
                            DataZ_IneachTrial.append(Velocity)
                        #plt.scatter(DataX,DataY)
                        
                        #plt.legend(loc='upper right')
            if len(DataX_IneachTrial)>0:
                DataX.append(np.mean(DataX_IneachTrial))
            if len(DataY_IneachTrial)>0:
                DataY.append(np.mean(DataY_IneachTrial))
            if len(DataZ_IneachTrial)>0:
                DataZ.append(np.mean(DataZ_IneachTrial))

            
        AllDataX.append(DataX)   
        AllDataY.append(DataY)
        AllDataZ.append(DataZ) 
    #print(AllDataY)
    plt.subplot(3,1,1)
    plt.boxplot(AllDataZ)
    plt.subplot(3,1,2)
    plt.boxplot(AllDataY)
    plt.subplot(3,1,3)
    plt.boxplot(AllDataX)
    plt.show()



def DurationDiscreteGesture_v1():


    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014']

    #AllUser=['3007','3008','3009','3010','3011','3012','3014']

    for iUser in range(12):
        User=AllUser[iUser]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        plt.subplots_adjust(wspace=0.5,hspace=0.5)
        plt.subplot(4,3,iUser+1)
        #PlotJerk_AllVelocity(GraphData[0],User)
        #PlotJerk_Accelerate(GraphData[0],User)
        Plot_FingerTime(GraphData[0],User,iUser+1)

    plt.savefig('DurationDiscreteGesture.png')
    plt.show()

def TapMovement():
    import numpy as np
    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']
    AllUserLabel=['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13']
    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt
    for iUser in range(13):
        User=AllUser[iUser]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        TapMovement=list()
        


        for iTrial in range(len(Tap_GraphData)):
            #for tapEvent in range(len(Tap_GraphData[iTrial]['tapEvents'])):
            
            for iFinger in range(len(Tap_GraphData[iTrial]["rawTouchTracks"])):
                FingerLargestMovement=0
                for iPoint in range(len(Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):

                    dx=Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]-Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['location'][0]
                    dy=Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]-Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['location'][1]
                
                    if np.sqrt(dx*dx+dy*dy)>FingerLargestMovement:
                        FingerLargestMovement=np.sqrt(dx*dx+dy*dy)

                
                TapMovement.append(FingerLargestMovement)
            
        
        AllUserTap.append(TapMovement) 

        # 
    import matplotlib.pyplot as plt
    import numpy as np
     
    import seaborn as sns
    sns.set_style('whitegrid')
    # plt.subplot(2,1,1)
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    
    all_data = AllUserTap
     
    # fig = plt.figure(figsize=(8,6))
     
    bplot = plt.boxplot(all_data,
                notch=False,  # notch shape
                   # vertical box aligmnent
                patch_artist=True)   # fill with color
    plt.title("Movement in tap task (pt)")
    colors = ['pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
     
        # plt.xticks([y+1 for y in range(len(all_data))], ['x1', 'x2', 'x3'])
        # plt.xlabel('measurement x')
        # t = plt.title('Box plot')
    plt.xlabel=AllUserLabel
    plt.ylabel='pt'
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13],AllUserLabel)
    plt.yticks(np.arange(0,100,5))
    plt.ylim([0,100])



    # plt.subplot(2,1,2)
    # plt.subplots_adjust(wspace=0.3,hspace=0.3)
    
    # all_data = AllUserPan
     
    # # fig = plt.figure(figsize=(8,6))
     
    # bplot = plt.boxplot(all_data,
    #             notch=False,  # notch shape
    #             vert=True,   # vertical box aligmnent
    #             patch_artist=True)   # fill with color
     
    # colors = ['lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue']
    # for patch, color in zip(bplot['boxes'], colors):
    #     patch.set_facecolor(color)
    # plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13],AllUser)
    # plt.title("Duration in swipe(fast pan) task (sec)")
    # plt.ylabel='sec'

    # plt.yticks(np.arange(0,2.3,0.1))
    # plt.ylim([0,2.3])
        # plt.xticks([y+1 for y in range(len(all_data))], ['x1', 'x2', 'x3'])
        # plt.xlabel('measurement x')
        # t = plt.title('Box plot')


    plt.show()

def DurationDiscreteGesture_v2():
    import numpy as np
    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']
    AllUserLabel=['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13']
    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt
    for iUser in range(13):
        User=AllUser[iUser]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        TapDuration=list()
        SwipeDuration=list()


        for iTrial in range(len(Tap_GraphData)):
            #for tapEvent in range(len(Tap_GraphData[iTrial]['tapEvents'])):
            
            for iFinger in range(len(Tap_GraphData[iTrial]["rawTouchTracks"])):
                t=Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][len(Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp']-Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                if t>0:
                    TapDuration.append(t)
            
        SwipeTaskResponseTime=list()
        for iTrial in range(len(Swipe_GraphData)):
            #for tapEvent in range(len(Swipe_GraphData[iTrial]['tapEvents'])):
           
            for iFinger in range(len(Swipe_GraphData[iTrial]["rawTouchTracks"])):
                t=Swipe_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][len(Swipe_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])-1]['timestamp']-Swipe_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                if t>0:
                    SwipeDuration.append(t)
            
       
        AllUserPan.append(SwipeDuration)  
        AllUserTap.append(TapDuration) 

        # 
    import matplotlib.pyplot as plt
    import numpy as np
     
    import seaborn as sns
    sns.set_style('whitegrid')
    plt.subplot(2,1,1)
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    
    all_data = AllUserTap
     
    # fig = plt.figure(figsize=(8,6))
     
    bplot = plt.boxplot(all_data,
                notch=False,  # notch shape
                   # vertical box aligmnent
                patch_artist=True)   # fill with color
    plt.title("Duration in tap task (sec)")
    colors = ['pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
     
        # plt.xticks([y+1 for y in range(len(all_data))], ['x1', 'x2', 'x3'])
        # plt.xlabel('measurement x')
        # t = plt.title('Box plot')
    plt.xlabel=AllUserLabel
    plt.ylabel='sec'
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13],AllUserLabel)
    plt.yticks(np.arange(0,1.3,0.1))
    plt.ylim([0,1.3])



    plt.subplot(2,1,2)
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    
    all_data = AllUserPan
     
    # fig = plt.figure(figsize=(8,6))
     
    bplot = plt.boxplot(all_data,
                notch=False,  # notch shape
                vert=True,   # vertical box aligmnent
                patch_artist=True)   # fill with color
     
    colors = ['lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13],AllUserLabel)
    plt.title("Duration in swipe(fast pan) task (sec)")
    plt.ylabel='sec'

    plt.yticks(np.arange(0,2.3,0.1))
    plt.ylim([0,2.3])
        # plt.xticks([y+1 for y in range(len(all_data))], ['x1', 'x2', 'x3'])
        # plt.xlabel('measurement x')
        # t = plt.title('Box plot')


    plt.show()




def SurveyThreshold():
    AllUser=['2008']

    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    import matplotlib.pyplot as plt
    for iUser in range(1):
        User=AllUser[iUser]
        #path='StudyData/NewData/'+User+'/'
        path='StudyData/OldData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        TapTaskResponseTime=list()
        for iTrial in range(len(Tap_GraphData)):
            AllDisplace=list()
            if len(Tap_GraphData[iTrial]['tapEvents'])>0:
                if Tap_GraphData[iTrial]['success']==True:
                    for panevent in range(len(Tap_GraphData[iTrial]['tapEvents'])):
                        if Tap_GraphData[iTrial]['tapEvents'][panevent]['state']=='ended':
                            if len(Tap_GraphData[iTrial]["rawTouchTracks"])==1:
                                for iPoint in range(len(Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"])):

                                    dX=Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][iPoint]['location'][0]-Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['location'][0]
                                    dY=Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][iPoint]['location'][1]-Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['location'][1]
                                    
                                    AllDisplace.append(np.sqrt(dX*dX+dY*dY))
            if len(AllDisplace)>=1:
                print(np.max(AllDisplace))



def Draw_RecognizerSponseTime():
    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014']

    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    import matplotlib.pyplot as plt
    for iUser in range(12):
        User=AllUser[iUser]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        TapTaskResponseTime=list()
        for iTrial in range(len(Tap_GraphData)):
            #for tapEvent in range(len(Tap_GraphData[iTrial]['tapEvents'])):
            for tapEvent in range(1):
                if len(Tap_GraphData[iTrial]['tapEvents'])>0:
                    TapTaskResponseTime.append(Tap_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp'])
            

            #TapTaskResponseTime.append(Tap_GraphData[iTrial]['tapEvents'][0]['timestamp']-Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp'])
            



            #for panEvent in range(len(Tap_GraphData[iTrial]['panEvents'])):
            for panEvent in range(1):
                if len(Tap_GraphData[iTrial]['panEvents'])>0:
                    Min=list()
                    for iFinger in range(len(Tap_GraphData[iTrial]["rawTouchTracks"])):
                        t=Tap_GraphData[iTrial]['panEvents'][panEvent]['timestamp']-Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    TapTaskResponseTime.append(np.min(Min))
                
        SwipeTaskResponseTime=list()
        for iTrial in range(len(Swipe_GraphData)):
            #for tapEvent in range(len(Swipe_GraphData[iTrial]['tapEvents'])):
            for tapEvent in range(1):
                if len(Swipe_GraphData[iTrial]['tapEvents'])>0:
                    SwipeTaskResponseTime.append(Swipe_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-Swipe_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp'])
            #for panEvent in range(len(Swipe_GraphData[iTrial]['panEvents'])):
            for panEvent in range(1):
                if len(Swipe_GraphData[iTrial]['panEvents'])>0:
                    Min=list()
                    for iFinger in range(len(Swipe_GraphData[iTrial]["rawTouchTracks"])):
                        t=Swipe_GraphData[iTrial]['panEvents'][panEvent]['timestamp']-Swipe_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    SwipeTaskResponseTime.append(np.min(Min))
            
        HPanTaskResponseTime=list()
        for iTrial in range(len(HScroll_GraphData)):
            #for tapEvent in range(len(HScroll_GraphData[iTrial]['tapEvents'])):
            for tapEvent in range(1):
                if len(HScroll_GraphData[iTrial]['tapEvents'])>0:
                    HPanTaskResponseTime.append(HScroll_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-HScroll_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp'])
            #for panEvent in range(len(HScroll_GraphData[iTrial]['panEvents'])):
            for panEvent in range(1):
                if len(HScroll_GraphData[iTrial]['panEvents'])>0:
                    Min=list()
                    for iFinger in range(len(HScroll_GraphData[iTrial]["rawTouchTracks"])):
                        t=HScroll_GraphData[iTrial]['panEvents'][panEvent]['timestamp']-HScroll_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    HPanTaskResponseTime.append(np.min(Min))
        
        VPanTaskResponseTime=list()
        for iTrial in range(len(VScroll_GraphData)):
            #for tapEvent in range(len(VScroll_GraphData[iTrial]['tapEvents'])):
            for tapEvent in range(1):
                if len(VScroll_GraphData[iTrial]['tapEvents'])>0:
                    VPanTaskResponseTime.append(VScroll_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-VScroll_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp'])
            #for panEvent in range(len(VScroll_GraphData[iTrial]['panEvents'])):
            for panEvent in range(1):
                if len(VScroll_GraphData[iTrial]['panEvents'])>0:
                    Min=list()
                    for iFinger in range(len(HScroll_GraphData[iTrial]["rawTouchTracks"])):
                        t=VScroll_GraphData[iTrial]['panEvents'][panEvent]['timestamp']-VScroll_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    VPanTaskResponseTime.append(np.min(Min))
            
        Alllist.append(np.min(TapTaskResponseTime))
        Alllist.append(np.min(SwipeTaskResponseTime))
        Alllist.append(np.min(HPanTaskResponseTime))
        Alllist.append(np.min(VPanTaskResponseTime))
        print(np.min(TapTaskResponseTime),np.min(SwipeTaskResponseTime),np.min(HPanTaskResponseTime),np.min(VPanTaskResponseTime))



        import matplotlib.pyplot as plt
        import numpy as np
         
        all_data = [TapTaskResponseTime,SwipeTaskResponseTime,HPanTaskResponseTime,VPanTaskResponseTime]
         
        fig = plt.figure(figsize=(8,6))
         
        bplot = plt.boxplot(all_data,
                    notch=False,  # notch shape
                    vert=True,   # vertical box aligmnent
                    patch_artist=True)   # fill with color
         
        colors = ['pink', 'lightblue', 'lightgreen']
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
         
        plt.xticks([y+1 for y in range(len(all_data))], ['x1', 'x2', 'x3'])
        plt.xlabel('measurement x')
        t = plt.title('Box plot')
        plt.show()

        # plt.subplot(2,2,1)
        # plt.hist(TapTaskResponseTime,bins='auto')

        # plt.xlim(0,10)
        # plt.title('tap')
        # plt.subplot(2,2,2)
        # plt.hist(SwipeTaskResponseTime,bins='auto')
        # plt.xlim(0,10)
        # plt.title('swipe')
        # plt.subplot(2,2,3)
        # plt.hist(HPanTaskResponseTime,bins='auto')
        # plt.xlim(0,10)
        # plt.title('horizontalscroll')
        # plt.subplot(2,2,4)
        # plt.hist(VPanTaskResponseTime,bins='auto')
        # plt.xlim(0,10)
        # plt.title('verticalscroll')
        # plt.show()


def DefaultSystemRecognitionTime():
    import numpy as np
    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']
    AllUserLabel=['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13']
    Alllist=list()
    
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt
    for iUser in range(13):
        User=AllUser[iUser]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        TapResponseTime=list()
        PanResponseTime=list()


        for iTrial in range(len(Tap_GraphData)):
            if len(Tap_GraphData[iTrial]["rawTouchTracks"])>0:
                FirstFingerTime=Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
                if len(Tap_GraphData[iTrial]['tapEvents'])>0: #有tap
                    TapResponseTime.append(Tap_GraphData[iTrial]['tapEvents'][0]['timestamp']-FirstFingerTime)

                if len(Tap_GraphData[iTrial]['panEvents'])>0: #有pan 
                    PanResponseTime.append(Tap_GraphData[iTrial]['panEvents'][0]['timestamp']-FirstFingerTime)

        for iTrial in range(len(Swipe_GraphData)):
            if len(Swipe_GraphData[iTrial]["rawTouchTracks"])>0:
                FirstFingerTime=Swipe_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
                if len(Swipe_GraphData[iTrial]['tapEvents'])>0: #有tap
                    TapResponseTime.append(Swipe_GraphData[iTrial]['tapEvents'][0]['timestamp']-FirstFingerTime)

                if len(Swipe_GraphData[iTrial]['panEvents'])>0: #有pan 
                    PanResponseTime.append(Swipe_GraphData[iTrial]['panEvents'][0]['timestamp']-FirstFingerTime)

        for iTrial in range(len(HScroll_GraphData)):
            if len(HScroll_GraphData[iTrial]["rawTouchTracks"])>0:
                FirstFingerTime=HScroll_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
                if len(HScroll_GraphData[iTrial]['tapEvents'])>0: #有tap
                    TapResponseTime.append(HScroll_GraphData[iTrial]['tapEvents'][0]['timestamp']-FirstFingerTime)

                if len(HScroll_GraphData[iTrial]['panEvents'])>0: #有pan 
                    PanResponseTime.append(HScroll_GraphData[iTrial]['panEvents'][0]['timestamp']-FirstFingerTime)

        for iTrial in range(len(VScroll_GraphData)):
            if len(VScroll_GraphData[iTrial]["rawTouchTracks"])>0:
                FirstFingerTime=VScroll_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']
                if len(VScroll_GraphData[iTrial]['tapEvents'])>0: #有tap
                    TapResponseTime.append(VScroll_GraphData[iTrial]['tapEvents'][0]['timestamp']-FirstFingerTime)

                if len(VScroll_GraphData[iTrial]['panEvents'])>0: #有pan 
                    PanResponseTime.append(VScroll_GraphData[iTrial]['panEvents'][0]['timestamp']-FirstFingerTime)

        print(User," Tap Recognition Time ",np.mean(TapResponseTime)," Pan Recognition Time ",np.mean(PanResponseTime)," Average ",(np.mean(TapResponseTime)+np.mean(PanResponseTime))/2)



def RecognizerSponseTime():
    import numpy as np
    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']
    AllUserLabel=['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13']
    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt
    for iUser in range(13):
        User=AllUser[iUser]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        TapResponseTime=list()
        PanResponseTime=list()


        for iTrial in range(len(Tap_GraphData)):
            #for tapEvent in range(len(Tap_GraphData[iTrial]['tapEvents'])):
            for tapEvent in range(1):
                if len(Tap_GraphData[iTrial]['tapEvents'])>0:
                    Min=list()
                    for iFinger in range(len(Tap_GraphData[iTrial]["rawTouchTracks"])):
                        t=Tap_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    if len(Min)>0:
                        TapResponseTime.append(np.min(Min))


                    # if Tap_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp']>0:
                    #     TapResponseTime.append(Tap_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp'])
            

            #TapTaskResponseTime.append(Tap_GraphData[iTrial]['tapEvents'][0]['timestamp']-Tap_GraphData[iTrial]["rawTouchTracks"][0]["rawTouches"][0]['timestamp'])
            



            #for panEvent in range(len(Tap_GraphData[iTrial]['panEvents'])):
            for panEvent in range(1):
                if len(Tap_GraphData[iTrial]['panEvents'])>0:
                    Min=list()
                    for iFinger in range(len(Tap_GraphData[iTrial]["rawTouchTracks"])):
                        t=Tap_GraphData[iTrial]['panEvents'][panEvent]['timestamp']-Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    if len(Min)>0:
                        PanResponseTime.append(np.min(Min))
                
        SwipeTaskResponseTime=list()
        for iTrial in range(len(Swipe_GraphData)):
            #for tapEvent in range(len(Swipe_GraphData[iTrial]['tapEvents'])):
            for tapEvent in range(1):

                if len(Swipe_GraphData[iTrial]['tapEvents'])>0:
                    Min=list()
                    for iFinger in range(len(Swipe_GraphData[iTrial]["rawTouchTracks"])):
                        t=Swipe_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-Swipe_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    if len(Min)>0:
                        TapResponseTime.append(np.min(Min))

            #for panEvent in range(len(Swipe_GraphData[iTrial]['panEvents'])):
            for panEvent in range(1):
                if len(Swipe_GraphData[iTrial]['panEvents'])>0:
                    Min=list()
                    for iFinger in range(len(Swipe_GraphData[iTrial]["rawTouchTracks"])):
                        t=Swipe_GraphData[iTrial]['panEvents'][panEvent]['timestamp']-Swipe_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    if len(Min)>0:
                        PanResponseTime.append(np.min(Min))
            
       
        for iTrial in range(len(HScroll_GraphData)):
            #for tapEvent in range(len(HScroll_GraphData[iTrial]['tapEvents'])):
            for tapEvent in range(1):
                if len(HScroll_GraphData[iTrial]['tapEvents'])>0:
                    Min=list()
                    for iFinger in range(len(HScroll_GraphData[iTrial]["rawTouchTracks"])):
                        t=HScroll_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-HScroll_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    if len(Min)>0:
                        TapResponseTime.append(np.min(Min))

                    #for panEvent in range(len(HScroll_GraphData[iTrial]['panEvents'])):
            for panEvent in range(1):
                if len(HScroll_GraphData[iTrial]['panEvents'])>0:
                    Min=list()
                    for iFinger in range(len(HScroll_GraphData[iTrial]["rawTouchTracks"])):

                        t=HScroll_GraphData[iTrial]['panEvents'][panEvent]['timestamp']-HScroll_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    if len(Min)>0:
                        PanResponseTime.append(np.min(Min))

        
        
        for iTrial in range(len(VScroll_GraphData)):
            #for tapEvent in range(len(VScroll_GraphData[iTrial]['tapEvents'])):
            for tapEvent in range(1):
                if len(VScroll_GraphData[iTrial]['tapEvents'])>0:
                    Min=list()
                    for iFinger in range(len(VScroll_GraphData[iTrial]["rawTouchTracks"])):
                        t=VScroll_GraphData[iTrial]['tapEvents'][tapEvent]['timestamp']-VScroll_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    if len(Min)>0:
                        TapResponseTime.append(np.min(Min))

            for panEvent in range(1):
                if len(VScroll_GraphData[iTrial]['panEvents'])>0:
                    Min=list()
                    for iFinger in range(len(VScroll_GraphData[iTrial]["rawTouchTracks"])):
                        t=VScroll_GraphData[iTrial]['panEvents'][panEvent]['timestamp']-VScroll_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]['timestamp']
                        if t>0:
                            Min.append(t)
                    if len(Min)>0:
                        PanResponseTime.append(np.min(Min))
        AllUserPan.append(PanResponseTime)  
        AllUserTap.append(TapResponseTime) 

        # 
    import matplotlib.pyplot as plt
    import numpy as np
     
    import seaborn as sns
    sns.set_style('whitegrid')
    plt.subplot(2,1,1)
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    
    all_data = AllUserTap
     
    # fig = plt.figure(figsize=(8,6))
     
    bplot = plt.boxplot(all_data,
                notch=False,  # notch shape
                   # vertical box aligmnent
                patch_artist=True)   # fill with color
    plt.title("First Tap Event Recognition Time (sec)")
    colors = ['pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink','pink']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
     
        # plt.xticks([y+1 for y in range(len(all_data))], ['x1', 'x2', 'x3'])
        # plt.xlabel('measurement x')
        # t = plt.title('Box plot')
    plt.xlabel= AllUserLabel
    plt.ylabel='sec'
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13], AllUserLabel)
    plt.yticks(np.arange(0,1.3,0.1))
    plt.ylim([0,1.3])



    plt.subplot(2,1,2)
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    
    all_data = AllUserPan
     
    # fig = plt.figure(figsize=(8,6))
     
    bplot = plt.boxplot(all_data,
                notch=False,  # notch shape
                vert=True,   # vertical box aligmnent
                patch_artist=True)   # fill with color
     
    colors = ['lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue','lightblue']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13], AllUserLabel)
    plt.title("First Pan Event Recognition Time (sec)")
    plt.ylabel='sec'

    plt.yticks(np.arange(0,1,0.1))
    plt.ylim([0,1])
        # plt.xticks([y+1 for y in range(len(all_data))], ['x1', 'x2', 'x3'])
        # plt.xlabel('measurement x')
        # t = plt.title('Box plot')


    plt.show()


def OverView():
    import numpy as np
    import matplotlib.patches as patches
    import matplotlib.gridspec as gridspec
    def LabelAllTrue(TaskData):
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])): 
                    TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True

        return TaskData
    def DrawScroll(TaskData):
        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        AllFinger_PositionX_Dropout=list()
        AllFinger_PositionY_Dropout=list()

        AllColor=['red','blue','green','yellow','pink','orange','purple','gray','black','red','blue','green','yellow','pink','orange','purple','gray','black']

        firstPointX=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][0]
        firstPointY=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][1]
        #TargetX=TaskData["targetFrame"][0][0]+ TaskData["targetFrame"][1][0]*0.5
        #TargetY=TaskData["targetFrame"][0][1]+ TaskData["targetFrame"][1][1]*0.5
        
      



                

               
        #############################
        # plt.subplot(4,1,1)
        fig1,ax1=plt.subplots(1)
        #fig1,ax1=plt.subplots(4,1,1)
        # inner1 = gridspec.GridSpecFromSubplotSpec(1, 1,
        #                 subplot_spec=outer[0], wspace=0.0, hspace=0.0)
        # ax1 = plt.Subplot(fig, inner1[0])

        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        #rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        #ax1.add_patch(rect)
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            AllFinger_PositionX.append([])
            AllFinger_PositionY.append([])
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
                # if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    AllFinger_PositionX[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                    AllFinger_PositionY[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])


        for iFinger in range(len(AllFinger_PositionX)):
            ax1.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color=AllColor[iFinger])

        plt.xlim(firstPointX-200,firstPointX+200)
        plt.ylim(firstPointY-200,firstPointY+200)


    def DrawTap(TaskData):
        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        AllFinger_PositionX_Dropout=list()
        AllFinger_PositionY_Dropout=list()

        AllColor=['red','blue','green','yellow','pink','orange','purple','gray','black','red','blue','green','yellow','pink','orange','purple','gray','black']

        firstPointX=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][0]
        firstPointY=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][1]
        TargetX=TaskData["targetFrame"][0][0]+ TaskData["targetFrame"][1][0]*0.5
        TargetY=TaskData["targetFrame"][0][1]+ TaskData["targetFrame"][1][1]*0.5
        
        X1=TaskData["targetFrame"][0][0]
        Y1=TaskData["targetFrame"][0][1]   



        fig = plt.figure(figsize=(10, 8))
        outer = gridspec.GridSpec(3, 2, wspace=0.1, hspace=0.1)
        
                

               
        ##############################
        # # plt.subplot(4,1,1)
        # fig1,ax1=plt.subplots(1)
        # #fig1,ax1=plt.subplots(4,1,1)
        # # inner1 = gridspec.GridSpecFromSubplotSpec(1, 1,
        # #                 subplot_spec=outer[0], wspace=0.0, hspace=0.0)
        # # ax1 = plt.Subplot(fig, inner1[0])

        # AllFinger_PositionX=list()
        # AllFinger_PositionY=list()
        # rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        # ax1.add_patch(rect)
        # for iFinger in range(len(TaskData["rawTouchTracks"])):
        #     AllFinger_PositionX.append([])
        #     AllFinger_PositionY.append([])
        #     for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
        #         # if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
        #             AllFinger_PositionX[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
        #             AllFinger_PositionY[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])


        # for iFinger in range(len(AllFinger_PositionX)):
        #     ax1.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color=AllColor[iFinger])

        # plt.xlim(TargetX-100,TargetX+100)
        # plt.ylim(TargetY-100,TargetY+100)


        ######################################
        #plt.subplot(4,1,2)
        # fig2,ax2=plt.subplots(1)
        # #fig2,ax2=plt.subplots(4,1,2)
        
        # # inner2 = gridspec.GridSpecFromSubplotSpec(1, 1,
        # #                 subplot_spec=outer[1], wspace=0.0, hspace=0.0)
        # # ax2 = plt.Subplot(fig, inner2[0])
        # AllFinger_PositionX=list()
        # AllFinger_PositionY=list()
        # print(TargetX,TargetY,firstPointX,firstPointY)
        # rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        # ax2.add_patch(rect)


        # for iFinger in range(len(TaskData["rawTouchTracks"])):
            
        #     for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
        #         if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==False:
        #             #print(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
        #             AllFinger_PositionX_Dropout.append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
        #             AllFinger_PositionY_Dropout.append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])

       
        # # plt.scatter(AllFinger_PositionX_Dropout,AllFinger_PositionY_Dropout,color='black')
       

        
        
        # # ax.xlim(firstPointX-50,firstPointX+50)
        # # ax.ylim(firstPointY-50,firstPointY+50)


        
        # ax2.scatter(AllFinger_PositionX_Dropout,AllFinger_PositionY_Dropout,color='black')





        # plt.xlim(TargetX-100,TargetX+100)
        # plt.ylim(TargetY-100,TargetY+100)

        # ###################################
        #plt.subplot(4,1,3)
        fig3,ax3=plt.subplots(1)
        #fig3,ax3=plt.subplots(4,1,3)
        # inner3 = gridspec.GridSpecFromSubplotSpec(1, 1,
        #                 subplot_spec=outer[2], wspace=0.0, hspace=0.0)
        # ax3 = plt.Subplot(fig, inner3[0])


        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        ax3.add_patch(rect)
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            AllFinger_PositionX.append([])
            AllFinger_PositionY.append([])
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
                if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    AllFinger_PositionX[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                    AllFinger_PositionY[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])


        for iFinger in range(len(AllFinger_PositionX)):
            ax3.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color=AllColor[iFinger])

        plt.xlim(TargetX-100,TargetX+100)
        plt.ylim(TargetY-100,TargetY+100)



        



    AllUser=['3012']

    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt

    User='3011'
    path='StudyData/NewData/'+User+'/'

    files=listdir(path)
    file=list()
    for i in range(len(files)):
        if files[i][-4:]=='json':
            file.append(files[i])

    GraphData=ReadData(path,file)

    Device_info=GraphData[0]['deviceInfo']['screenSize']
    Tap_GraphData=GraphData[0]['tapTask']['trials']
    Swipe_GraphData=GraphData[0]['swipeTask']['trials']
    HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
    VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

    
    task='pan'
    for test in range(15,16):
       
        if task=='tap':
            TaskData=Tap_GraphData[test]

           


            LabelAllTrue(TaskData)
            

            AfterFilterData,Success=tapopt.TapOptimizer_Graph(TaskData)
            DrawTap(TaskData)
            
            print(Success)
           
            plt.show()
        else:
            TaskData=Swipe_GraphData[test]
            DrawScroll(TaskData)
            plt.show()

def ModelArchitecture(User,CrossValidationIndex,tGrid,Mode):
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

    
    from keras.utils import plot_model

    model=load_model(User,CrossValidationIndex,tGrid,Mode)
    #plot_model(model, to_file='ModelwithPhase.png',show_shapes=True,show_layer_names=False,rankdir='LR')
    plot_model(model, to_file=str(User)+"_"+str(CrossValidationIndex)+"_"+str(Mode)+"_"+str(tGrid)+'_Model.png',show_shapes=True,show_layer_names=False,rankdir='TB')

    



def AnalysisOfFingerNum():


    import numpy as np
    #AllUser=['3001']
    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']

    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt
    AllUserCount=list()
    for iUser in range(13):
        User=AllUser[iUser]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        TapSingle=0
        TapMulti=0

        SwipeSingle=0
        SwipeMulti=0
        
        HPanSingle=0
        HPanMulti=0
        
        VPanSingle=0
        VPanMulti=0

        for iTrial in range(len(Tap_GraphData)):
            
            if len(Tap_GraphData[iTrial]["rawTouchTracks"])==1:
                TapSingle=TapSingle+1
            elif len(Tap_GraphData[iTrial]["rawTouchTracks"])>1:
                TapMulti=TapMulti+1

        for iTrial in range(len(Swipe_GraphData)):
            
            if len(Swipe_GraphData[iTrial]["rawTouchTracks"])==1:
                SwipeSingle=SwipeSingle+1
            elif len(Swipe_GraphData[iTrial]["rawTouchTracks"])>1:
                SwipeMulti=SwipeMulti+1

        for iTrial in range(len(HScroll_GraphData)):
            
            if len(HScroll_GraphData[iTrial]["rawTouchTracks"])==1:
                HPanSingle=HPanSingle+1
            elif len(HScroll_GraphData[iTrial]["rawTouchTracks"])>1:
                HPanMulti=HPanMulti+1

        for iTrial in range(len(VScroll_GraphData)):
            
            if len(VScroll_GraphData[iTrial]["rawTouchTracks"])==1:
                VPanSingle=VPanSingle+1
            elif len(VScroll_GraphData[iTrial]["rawTouchTracks"])>1:
                VPanMulti=VPanMulti+1


        print(User," Tap ",TapSingle,TapMulti," Swipe ",SwipeSingle,SwipeMulti," HPan ",HPanSingle,HPanMulti," VPan ",VPanSingle,VPanMulti)


        





def TappingMultiTouch():


    def Analyzing2(GraphData):
        labels=['Only Tap ,No Other Event','OtherEvents With Tap','Only Scroll ,No Other Event','OtherEvents With Scroll','Tap Scroll ,No Other Event','OtherEvents With Scroll and Tap','Only OtherEvents','NoEvent']
        OnlyTap_Count=0
        
        TapScroll_Count=0
        OnlyScroll_Count=0

        
        NoEvent_Count=0
        OtherEventCount_Tap=0
        OtherEventCount_Scroll=0
        OtherEventCount_Tap_Scroll=0

        OnlyOtherEvent=0
        

        for iTrial in range(len(GraphData)):
            OtherEvent=OtherEventFuc(GraphData,iTrial)
            if len(GraphData['tapEvents'])==1:
                if len(GraphData['panEvents'])==0:
                    if OtherEvent==0:
                        OnlyTap_Count=OnlyTap_Count+1
            
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        TapScroll_Count=TapScroll_Count+1



            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        OnlyScroll_Count=OnlyScroll_Count+1
                       
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0: 
                    if OtherEvent>0:
                        OnlyOtherEvent=OnlyOtherEvent+1

            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        OtherEventCount_Tap_Scroll=OtherEventCount_Tap_Scroll+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OtherEventCount_Scroll=OtherEventCount_Scroll+1
                        elif NumberOfPanBegan>1:
                            OtherEventCount_Scroll=OtherEventCount_Scroll+1

        
        return [OnlyTap_Count,OtherEventCount_Tap,OnlyScroll_Count,OtherEventCount_Scroll,TapScroll_Count,OtherEventCount_Tap_Scroll,OnlyOtherEvent,NoEvent_Count],labels
            


    import numpy as np
    #AllUser=['3001']
    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']

    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt
    AllUserCount=list()
    for iUser in range(13):
        User=AllUser[iUser]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        MultiTouchCount=0
        for iTrial in range(len(Tap_GraphData)):
            Alltimestamp=list()
            BeganTime=list()
            EndedTime=list()
            for iFinger in range(len(Tap_GraphData[iTrial]["rawTouchTracks"])):
            
                for iPoint in range(len(Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                    t=Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['timestamp']
                    phase=Tap_GraphData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']
                    if phase=='began':
                        BeganTime.append(t)
                        Alltimestamp.append(t+0.00002)
                    if phase=='ended':
                        EndedTime.append(t)


                    if t not in Alltimestamp:
                        Alltimestamp.append(t)
            SortedAllTimeStamp=sorted(Alltimestamp)

            FingerCount=list()
            if len(SortedAllTimeStamp)>0:
                fingerthisthime=0
                for t in SortedAllTimeStamp:
                    
                    if t in BeganTime:
                        fingerthisthime=fingerthisthime+1
                    if t in EndedTime:
                        fingerthisthime=fingerthisthime-1
                    FingerCount.append(fingerthisthime)
                    #print(t,fingerthisthime)


                if np.max(FingerCount)>1:
                    MultiTouchCount=MultiTouchCount+1
        AllUserCount.append(MultiTouchCount)
    print(AllUserCount)
    plt.bar(AllUserCount,0.5)
    plt.show()
    
            

def AnalyzeError():

    def OtherEventFuc(GraphData,iTrial):
        OtherEvent=0
        if len(GraphData[iTrial]['rotationEvents'])>0:
            OtherEvent=1
        if len(GraphData[iTrial]['pinchEvents'])>0:
            OtherEvent=1
        if len(GraphData[iTrial]['longPressEvents'])>0:
            OtherEvent=1
        return OtherEvent

    def Analyzing2(GraphData):
        labels=['Only Tap ,No Other Event','OtherEvents With Tap','Only Scroll ,No Other Event','OtherEvents With Scroll','Tap Scroll ,No Other Event','OtherEvents With Scroll and Tap','Only OtherEvents','NoEvent']
        OnlyTap_Count=0
        
        TapScroll_Count=0
        OnlyScroll_Count=0

        
        NoEvent_Count=0
        OtherEventCount_Tap=0
        OtherEventCount_Scroll=0
        OtherEventCount_Tap_Scroll=0

        OnlyOtherEvent=0
        

        for iTrial in range(len(GraphData)):
            OtherEvent=OtherEventFuc(GraphData,iTrial)
            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        OnlyTap_Count=OnlyTap_Count+1
            
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        TapScroll_Count=TapScroll_Count+1



            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        OnlyScroll_Count=OnlyScroll_Count+1
                       
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0: 
                    if OtherEvent>0:
                        OnlyOtherEvent=OnlyOtherEvent+1

            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        OtherEventCount_Tap_Scroll=OtherEventCount_Tap_Scroll+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OtherEventCount_Scroll=OtherEventCount_Scroll+1
                        elif NumberOfPanBegan>1:
                            OtherEventCount_Scroll=OtherEventCount_Scroll+1

        
        return [OnlyTap_Count,OtherEventCount_Tap,OnlyScroll_Count,OtherEventCount_Scroll,TapScroll_Count,OtherEventCount_Tap_Scroll,OnlyOtherEvent,NoEvent_Count],labels
            

    def Analyzing(GraphData):
        labels=['OneTap','TwoTap','ThreeMoreTap','TapScroll','OneScroll','TwoMoreScroll','NoEvent','OtherEvents']
        OneTap_Count=0
        TwoTap_Count=0
        ThreeMoreTap_Count=0
        TapScroll_Count=0
        OneScroll_Count=0
        TwoMoreScroll_Count=0
        NoEvent_Count=0
        OtherEventCount=0
        

        for iTrial in range(len(GraphData)):
            OtherEvent=OtherEventFuc(GraphData,iTrial)
            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        OneTap_Count=OneTap_Count+1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        TwoTap_Count=TwoTap_Count+1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        ThreeMoreTap_Count=ThreeMoreTap_Count+1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        TapScroll_Count=TapScroll_Count+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OneScroll_Count=OneScroll_Count+1
                        elif NumberOfPanBegan>1:
                            TwoMoreScroll_Count=TwoMoreScroll_Count+1

            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0: 
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1

            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OtherEventCount=OtherEventCount+1
                        elif NumberOfPanBegan>1:
                            OtherEventCount=OtherEventCount+1

           
                        

        return [OneTap_Count,TwoTap_Count,ThreeMoreTap_Count,TapScroll_Count,OneScroll_Count,TwoMoreScroll_Count,NoEvent_Count,OtherEventCount],labels

    def plot_func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        if pct>0.2:
            
            return "{:.1f}%\n({:d} trials)".format(pct, absolute)
        else:
            return ""



                   


    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']
    UserName=['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13']

    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    import matplotlib.pyplot as plt
    
    import matplotlib.gridspec as gridspec

    fig = plt.figure(figsize=(14, 12))
    #outer = gridspec.GridSpec(4, 4, wspace=0.05, hspace=0.05)
    outer = gridspec.GridSpec(4, 4)

    inner = gridspec.GridSpecFromSubplotSpec(1, 2,
                        subplot_spec=outer[14], wspace=0.0, hspace=0.0)
        
      
    labels=['Only Tap ,No Other Event','OtherEvents With Tap','Only Scroll ,No Other Event','OtherEvents With Scroll','Tap Scroll ,No Other Event','OtherEvents With Scroll and Tap','Only OtherEvents','NoEvent']
        
    axLegend = plt.Subplot(fig, inner[1])
    axLegend.pie(np.zeros(len(labels)))
    axLegend.legend(labels=labels,prop={'size':8},loc='center')
    fig.add_subplot(axLegend)

    for iUser in range(13):
        User=AllUser[iUser ]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        TapError,labels=Analyzing2(Tap_GraphData)

        Tapvals = np.array([[TapError[0], TapError[1],0,0,0,0,0,0],[0,0,TapError[2], TapError[3],TapError[4], TapError[5],TapError[6], TapError[7]]])


        SwipeError,labels=Analyzing2(Swipe_GraphData)
        HScrollError,labels=Analyzing2(HScroll_GraphData)
        VScrollError,labels=Analyzing2(VScroll_GraphData)

        AllPanError=np.zeros(len(TapError))
        for i in range(len(TapError)):
            AllPanError[i]=SwipeError[i]+HScrollError[i]+VScrollError[i]

        Panvals = np.array([[0,0,AllPanError[2], AllPanError[3],0,0,0,0],[AllPanError[0], AllPanError[1],0,0,AllPanError[4], AllPanError[5],AllPanError[6],AllPanError[7]]])

        #labels=['OneTap','TwoTap','ThreeMoreTap','TapScroll','OneScroll','TwoMoreScroll','NoEvent','OtherEvents']
        explode_Tap=np.zeros(len(TapError))
        explode_Pan=np.zeros(len(TapError))


        

       

        
        inner = gridspec.GridSpecFromSubplotSpec(1, 2,
                        subplot_spec=outer[iUser], wspace=0.0, hspace=0.0)
        
        size=0.5
        for j in range(2):
            if j==0:
                

                ax = plt.Subplot(fig, inner[j])
                #ax.pie(TapError,labels=labels)
                ax.pie(TapError,explode=explode_Tap,autopct=lambda pct: plot_func(pct, TapError),
                                  textprops=dict(color="black"))
                ax.set_title("P"+str(iUser+1)+" Tap")
                if iUser==15:
                    if j==0:
                        ax.legend(labels=labels,bbox_to_anchor=[-1,0.7,-1,0.7],prop={'size':8})
                fig.add_subplot(ax)


                # ax = plt.Subplot(fig, inner[j])
                # ax.set_title("User"+str(iUser)+" Tap")
                
                # cmap = plt.get_cmap("tab20c")

                # outer_colors = cmap([0,3])
                # inner_colors = cmap(np.array([9, 10, 11, 12, 13, 14,15,16]))
                # if iUser==0:
                #     if j==0:
                #         ax.legend(labels=labels)

                # ax.pie(Tapvals.sum(axis=1), radius=1, colors=outer_colors,
                #        wedgeprops=dict(width=size, edgecolor='w'))

                # ax.pie(Tapvals.flatten(), radius=1-size, colors=inner_colors,
                #        wedgeprops=dict(width=size, edgecolor='w'))

                # #ax.set(aspect="equal", title='Pie plot with `ax.pie`')
                # fig.add_subplot(ax)

            elif j==1:



                ax = plt.Subplot(fig, inner[j])
                ax.set_title("P"+str(iUser+1)+" Pan")
                #ax.pie(AllPanError,labels=labels)
                ax.pie(AllPanError,explode=explode_Pan,autopct=lambda pct: plot_func(pct, TapError),
                                  textprops=dict(color="black"))

                
                fig.add_subplot(ax)


                # ax = plt.Subplot(fig, inner[j])
                # ax.set_title("User"+str(iUser)+" Pan")
               
                # cmap = plt.get_cmap("tab20c")
                # outer_colors = cmap([0,3])
                # inner_colors = cmap(np.array([9, 10, 11, 12, 13, 14,15,16]))

                # ax.pie(Panvals.sum(axis=1), radius=1, colors=outer_colors,
                #        wedgeprops=dict(width=size, edgecolor='w'))

                # ax.pie(Panvals.flatten(), radius=1-size, colors=inner_colors,
                #        wedgeprops=dict(width=size, edgecolor='w'))

                # #ax.set(aspect="equal", title='Pie plot with `ax.pie`')
                # fig.add_subplot(ax)


        #plt.pie(TapError,explode=explode_Tap,labels=labels)

    plt.show()



def AnalyzeErrorOneTask(task):

    def OtherEventFuc(GraphData,iTrial):
        OtherEvent=0
        if len(GraphData[iTrial]['rotationEvents'])>0:
            OtherEvent=1
        if len(GraphData[iTrial]['pinchEvents'])>0:
            OtherEvent=1
        if len(GraphData[iTrial]['longPressEvents'])>0:
            OtherEvent=1
        return OtherEvent

    def Analyzing2(GraphData):
        labels=['Only Tap ,No Other Event','OtherEvents With Tap','Only Scroll ,No Other Event','OtherEvents With Scroll','Tap Scroll ,No Other Event','OtherEvents With Scroll and Tap','Only OtherEvents','NoEvent']
        OnlyTap_Count=0
        
        TapScroll_Count=0
        OnlyScroll_Count=0

        
        NoEvent_Count=0
        OtherEventCount_Tap=0
        OtherEventCount_Scroll=0
        OtherEventCount_Tap_Scroll=0

        OnlyOtherEvent=0
        

        for iTrial in range(len(GraphData)):
            AssignedClass=0
            OtherEvent=OtherEventFuc(GraphData,iTrial)
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        OnlyTap_Count=OnlyTap_Count+1
                        AssignedClass=1
            
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        TapScroll_Count=TapScroll_Count+1
                        AssignedClass=1


            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        OnlyScroll_Count=OnlyScroll_Count+1
                        AssignedClass=1
                       
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0: 
                    if OtherEvent>0:
                        OnlyOtherEvent=OnlyOtherEvent+1
                        AssignedClass=1

            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
                        AssignedClass=1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
                        AssignedClass=1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
                        AssignedClass=1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        OtherEventCount_Tap_Scroll=OtherEventCount_Tap_Scroll+1
                        AssignedClass=1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OtherEventCount_Scroll=OtherEventCount_Scroll+1
                            AssignedClass=1
                        elif NumberOfPanBegan>1:
                            OtherEventCount_Scroll=OtherEventCount_Scroll+1
                            AssignedClass=1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        NoEvent_Count=NoEvent_Count+1
                        AssignedClass=1

            if AssignedClass==0:
                print("Trial ",iTrial,"Events: ",len(GraphData[iTrial]['tapEvents']),len(GraphData[iTrial]['panEvents']),len(GraphData[iTrial]['longPressEvents']),len(GraphData[iTrial]['rotationEvents']),len(GraphData[iTrial]['pinchEvents']),len(GraphData[iTrial]['swipeEvents']))
        
        return [OnlyTap_Count,OtherEventCount_Tap,OnlyScroll_Count,OtherEventCount_Scroll,TapScroll_Count,OtherEventCount_Tap_Scroll,OnlyOtherEvent,NoEvent_Count],labels
            

    def Analyzing(GraphData):
        labels=['OneTap','TwoTap','ThreeMoreTap','TapScroll','OneScroll','TwoMoreScroll','NoEvent','OtherEvents']
        OneTap_Count=0
        TwoTap_Count=0
        ThreeMoreTap_Count=0
        TapScroll_Count=0
        OneScroll_Count=0
        TwoMoreScroll_Count=0
        NoEvent_Count=0
        OtherEventCount=0
        

        for iTrial in range(len(GraphData)):
            OtherEvent=OtherEventFuc(GraphData,iTrial)
            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        OneTap_Count=OneTap_Count+1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        TwoTap_Count=TwoTap_Count+1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        ThreeMoreTap_Count=ThreeMoreTap_Count+1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        TapScroll_Count=TapScroll_Count+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OneScroll_Count=OneScroll_Count+1
                        elif NumberOfPanBegan>1:
                            TwoMoreScroll_Count=TwoMoreScroll_Count+1

            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0: 
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1

            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OtherEventCount=OtherEventCount+1
                        elif NumberOfPanBegan>1:
                            OtherEventCount=OtherEventCount+1

            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        NoEvent_Count=NoEvent_Count+1

                        

        return [OneTap_Count,TwoTap_Count,ThreeMoreTap_Count,TapScroll_Count,OneScroll_Count,TwoMoreScroll_Count,NoEvent_Count,OtherEventCount,NoEvent_Count],labels

    def plot_func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        if pct/100>0.025:
            
            return "{:.1f}% ({:d} trials)".format(pct, absolute)
        else:
            return ""


    def plot_label(pct):
        if pct>0.1:
            return float(0.6)
        else: 
            return float(1.3)
                   


    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']
    UserName=['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13']

    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    import matplotlib.pyplot as plt
    
    import matplotlib.gridspec as gridspec

    fig = plt.figure(figsize=(14, 12))
    #outer = gridspec.GridSpec(4, 4, wspace=0.05, hspace=0.05)
    outer = gridspec.GridSpec(4, 4)

    inner = gridspec.GridSpecFromSubplotSpec(1, 2,
                        subplot_spec=outer[14], wspace=0.0, hspace=0.0)
        
      
    labels=['Only Tap ,No Other Event','OtherEvents With Tap','Only Scroll ,No Other Event','OtherEvents With Scroll','Tap Scroll ,No Other Event','OtherEvents With Scroll and Tap','Only OtherEvents','NoEvent']
        
    

    for iUser in range(13):
        User=AllUser[iUser ]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        if task=='tapTask':
            TapError,labels=Analyzing2(Tap_GraphData)
        elif task=='swipeTask':
            TapError,labels=Analyzing2(Swipe_GraphData)
        elif task=='horizontalScrollTask':
            TapError,labels=Analyzing2(HScroll_GraphData)
        elif task=='verticalScrollTask':
            TapError,labels=Analyzing2(VScroll_GraphData)

        # #TapError,labels=Analyzing2(Tap_GraphData)
        # TapError,labels=Analyzing2(VScroll_GraphData)

        # Tapvals = np.array([[TapError[0], TapError[1],0,0,0,0,0,0],[0,0,TapError[2], TapError[3],TapError[4], TapError[5],TapError[6], TapError[7]]])


        
        # print("User",User," Tap Trial ",len(Tap_GraphData))
        # AllPanError=np.zeros(len(TapError))
        # # for i in range(len(TapError)):
        # #     AllPanError[i]=SwipeError[i]+HScrollError[i]+VScrollError[i]

        # Panvals = np.array([[0,0,AllPanError[2], AllPanError[3],0,0,0,0],[AllPanError[0], AllPanError[1],0,0,AllPanError[4], AllPanError[5],AllPanError[6],AllPanError[7]]])

        #labels=['OneTap','TwoTap','ThreeMoreTap','TapScroll','OneScroll','TwoMoreScroll','NoEvent','OtherEvents']
        explode_Tap=np.zeros(len(TapError))
        explode_Pan=np.zeros(len(TapError))

        colors = ['red','blue','orange','yellow','green', 'pink',  'purple','lightskyblue','black']


        plt.subplot(3,5,iUser+1)
           
        plt.pie(TapError,colors=colors,explode=explode_Tap,autopct=lambda pct: plot_func(pct, TapError),pctdistance= 1.1)
        plt.title("P"+str(iUser+1)+" "+task)
        if iUser==12:  
            plt.legend(labels=labels,bbox_to_anchor=[0,1,3.5,0],prop={'size':12})
            

    
        

    plt.show()


def AnalyzeError_AllUser():

    def OtherEventFuc(GraphData,iTrial):
        OtherEvent=0
        if len(GraphData[iTrial]['rotationEvents'])>0:
            OtherEvent=1
        if len(GraphData[iTrial]['pinchEvents'])>0:
            OtherEvent=1
        if len(GraphData[iTrial]['longPressEvents'])>0:
            OtherEvent=1
        return OtherEvent

    def Analyzing2(GraphData):
        labels=['Only Tap ,No Other Event','OtherEvents With Tap','Only Pan ,No Other Event','OtherEvents With Pan','Tap Pan ,No Other Event','OtherEvents With Pan and Tap','Only OtherEvents','NoEvent']
        OnlyTap_Count=0
        
        TapScroll_Count=0
        OnlyScroll_Count=0

        
        NoEvent_Count=0
        OtherEventCount_Tap=0
        OtherEventCount_Scroll=0
        OtherEventCount_Tap_Scroll=0

        OnlyOtherEvent=0
        

        for iTrial in range(len(GraphData)):
            OtherEvent=OtherEventFuc(GraphData,iTrial)
            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        OnlyTap_Count=OnlyTap_Count+1
            
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        TapScroll_Count=TapScroll_Count+1



            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        OnlyScroll_Count=OnlyScroll_Count+1
                       
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0: 
                    if OtherEvent>0:
                        OnlyOtherEvent=OnlyOtherEvent+1

            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount_Tap=OtherEventCount_Tap+1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        OtherEventCount_Tap_Scroll=OtherEventCount_Tap_Scroll+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OtherEventCount_Scroll=OtherEventCount_Scroll+1
                        elif NumberOfPanBegan>1:
                            OtherEventCount_Scroll=OtherEventCount_Scroll+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        NoEvent_Count=NoEvent_Count+1
        
        return [OnlyTap_Count,OtherEventCount_Tap,OnlyScroll_Count,OtherEventCount_Scroll,TapScroll_Count,OtherEventCount_Tap_Scroll,OnlyOtherEvent,NoEvent_Count],labels
            

    def Analyzing(GraphData):
        labels=['OneTap','TwoTap','ThreeMoreTap','TapScroll','OneScroll','TwoMoreScroll','NoEvent','OtherEvents']
        OneTap_Count=0
        TwoTap_Count=0
        ThreeMoreTap_Count=0
        TapScroll_Count=0
        OneScroll_Count=0
        TwoMoreScroll_Count=0
        NoEvent_Count=0
        OtherEventCount=0
        

        for iTrial in range(len(GraphData)):
            OtherEvent=OtherEventFuc(GraphData,iTrial)
            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        OneTap_Count=OneTap_Count+1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        TwoTap_Count=TwoTap_Count+1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        ThreeMoreTap_Count=ThreeMoreTap_Count+1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        TapScroll_Count=TapScroll_Count+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent==0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OneScroll_Count=OneScroll_Count+1
                        elif NumberOfPanBegan>1:
                            TwoMoreScroll_Count=TwoMoreScroll_Count+1

            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0: 
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1

            if len(GraphData[iTrial]['tapEvents'])==1:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])==2:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])>=3:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])>0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])>0:
                    if OtherEvent>0:
                        NumberOfPanBegan=0
                        for i in range(len(GraphData[iTrial]['panEvents'])):
                            if GraphData[iTrial]['panEvents'][i]['state']=='began':
                                NumberOfPanBegan=NumberOfPanBegan+1
                        if NumberOfPanBegan==1:

                            OtherEventCount=OtherEventCount+1
                        elif NumberOfPanBegan>1:
                            OtherEventCount=OtherEventCount+1
            if len(GraphData[iTrial]['tapEvents'])==0:
                if len(GraphData[iTrial]['panEvents'])==0:
                    if OtherEvent==0:
                        NoEvent_Count=NoEvent_Count+1
           
                        

        return [OneTap_Count,TwoTap_Count,ThreeMoreTap_Count,TapScroll_Count,OneScroll_Count,TwoMoreScroll_Count,NoEvent_Count,OtherEventCount,NoEvent_Count],labels

    def plot_func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        print(pct)
        if pct/100>0.1:
            
            return "{:.1f}%\n({:d} trials)".format(pct, absolute)
        else:
            return ""

    def plot_label(pct):
        if pct >0.03:
            return 0.5
        else:
            return 1


                   


    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']


    #UserName=['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13']

    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    import matplotlib.pyplot as plt
    
    import matplotlib.gridspec as gridspec

    fig = plt.figure(figsize=(10, 8))
    #outer = gridspec.GridSpec(4, 4, wspace=0.05, hspace=0.05)
    
      
    labels=['Only Tap ,No Other Event','OtherEvents With Tap','Only Scroll ,No Other Event','OtherEvents With Scroll','Tap Scroll ,No Other Event','OtherEvents With Scroll and Tap','Only OtherEvents','NoEvent']
        
 


    AllUserTapError=[0,0,0,0,0,0,0,0]
    AllUserPanError=[0,0,0,0,0,0,0,0]

    for iUser in range(len(AllUser)):
        User=AllUser[iUser]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        TapError,labels=Analyzing2(Tap_GraphData)

        Tapvals = np.array([[TapError[0], TapError[1],0,0,0,0,0,0],[0,0,TapError[2], TapError[3],TapError[4], TapError[5],TapError[6], TapError[7]]])



        SwipeError,labels=Analyzing2(Swipe_GraphData)
        HScrollError,labels=Analyzing2(HScroll_GraphData)
        VScrollError,labels=Analyzing2(VScroll_GraphData)

        AllPanError=np.zeros(len(TapError))


        for i in range(len(TapError)):
            

            AllPanError[i]=SwipeError[i]+HScrollError[i]+VScrollError[i]
            AllUserTapError[i]=AllUserTapError[i]+TapError[i]
            AllUserPanError[i]=AllUserPanError[i]+AllPanError[i]

        Panvals = np.array([[0,0,AllPanError[2], AllPanError[3],0,0,0,0],[AllPanError[0], AllPanError[1],0,0,AllPanError[4], AllPanError[5],AllPanError[6],AllPanError[7]]])

        #labels=['OneTap','TwoTap','ThreeMoreTap','TapScroll','OneScroll','TwoMoreScroll','NoEvent','OtherEvents']
        explode_Tap=np.zeros(len(TapError))
        explode_Pan=np.zeros(len(TapError))


        

       
    ######

    colors = ['red','blue','orange','yellow','green', 'pink',  'purple','lightskyblue','black']


    # print(labels)
    # print(AllUserTapError)
    # print(AllUserPanError)
    plt.subplot(2,1,1)
    plt.pie(AllUserTapError,colors=colors,autopct=lambda pct: plot_func(pct, AllUserTapError),
                                  textprops=dict(color="black"))

    plt.title("Default system events in tap task for all users")
              
    plt.legend(labels=labels,bbox_to_anchor=[0,0.5,0,0.5],prop={'size':12})

    plt.subplot(2,1,2)
    # plt.pie(AllUserPanError,colors=colors,autopct=lambda pct: plot_func(pct, AllUserPanError),pctdistance=lambda pct: plot_label(pct),
    #                               textprops=dict(color="black"))
    plt.pie(AllUserPanError,colors=colors,autopct=lambda pct: plot_func(pct, AllUserPanError))

    plt.title("Default system events in pan task for all users")
              
    #plt.legend(labels=labels,bbox_to_anchor=[-1,-1,-1,],prop={'size':16})

    plt.show()




            
def AnalysisTapTask(Trial):
    def DrawTap(TaskData,iUser,EventString):
        import numpy as np
        import matplotlib.patches as patches
        import matplotlib.gridspec as gridspec

        UserLabel=['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13']
        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        AllFinger_PositionX_Dropout=list()
        AllFinger_PositionY_Dropout=list()

        AllColor=['red','blue','green','yellow','pink','orange','purple','gray','black','red','blue','green','yellow','pink','orange','purple','gray','black']

        firstPointX=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][0]
        firstPointY=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][1]
        TargetX=TaskData["targetFrame"][0][0]+ TaskData["targetFrame"][1][0]*0.5
        TargetY=TaskData["targetFrame"][0][1]+ TaskData["targetFrame"][1][1]*0.5
        
        X1=TaskData["targetFrame"][0][0]
        Y1=TaskData["targetFrame"][0][1]   



        fig = plt.figure(figsize=(10, 8))
        
        fig3,ax3=plt.subplots(1)
        
        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        ax3.add_patch(rect)
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            AllFinger_PositionX.append([])
            AllFinger_PositionY.append([])
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
                #if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                AllFinger_PositionX[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                AllFinger_PositionY[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])


        for iFinger in range(len(AllFinger_PositionX)):
            plt.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color=AllColor[iFinger])

        plt.xlim(TargetX-100,TargetX+100)
        plt.ylim(TargetY-100,TargetY+100)
        plt.title(str(UserLabel[iUser])+' one trial in Tap Task ')
        #plt.text(0,0,s=EventString)
        plt.text(TargetX-75, TargetY-75, EventString, horizontalalignment='center',verticalalignment='center')

        plt.show()

    def OtherEventFuc(GraphData):
        OtherEvent=0
        if len(GraphData['rotationEvents'])>0:
            OtherEvent=1
        if len(GraphData['pinchEvents'])>0:
            OtherEvent=1
        if len(GraphData['longPressEvents'])>0:
            OtherEvent=1
        return OtherEvent
    iUser=9
    Userlist=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']
    path='StudyData/NewData/'+Userlist[iUser]+'/'

    files=listdir(path)
    file=list()
    for i in range(len(files)):
        if files[i][-4:]=='json':
            file.append(files[i])

    GraphData=ReadData(path,file)
    trial=1
    Device_info=GraphData[0]['deviceInfo']['screenSize']
    GraphData=GraphData[0]['tapTask']['trials'][trial]


    ####


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
    if len(GraphData['tapEvents'])==1:
        if len(GraphData['panEvents'])==0:
            if OtherEvent==0:
                OnlyTap_Count=OnlyTap_Count+1
                EventString='One Tap'
                print('OnlyTap_Count')
    
    if len(GraphData['tapEvents'])>0:
        if len(GraphData['panEvents'])>0:
            if OtherEvent==0:
                TapScroll_Count=TapScroll_Count+1
                EventString='Tap and Pan '
                print('TapScroll_Count')


    if len(GraphData['tapEvents'])==0:
        if len(GraphData['panEvents'])>0:
            if OtherEvent==0:
                NumberOfPanBegan=0
                for i in range(len(GraphData['panEvents'])):
                    if GraphData['panEvents'][i]['state']=='began':
                        NumberOfPanBegan=NumberOfPanBegan+1
                OnlyScroll_Count=OnlyScroll_Count+1
                EventString='Pan'
                print('OnlyScroll_Count')
               
    if len(GraphData['tapEvents'])==0:
        if len(GraphData['panEvents'])==0: 
            if OtherEvent>0:
                OnlyOtherEvent=OnlyOtherEvent+1
                EventString='Other Event (Rotation,Longpress,Pinch)'
                print('OnlyOtherEvent')

    if len(GraphData['tapEvents'])==1:
        if len(GraphData['panEvents'])==0:
            if OtherEvent>0:
                OtherEventCount_Tap=OtherEventCount_Tap+1
                EventString='Tap and Other Event (Rotation,Longpress,Pinch)'
                print('OtherEventCount_Tap')
    if len(GraphData['tapEvents'])==2:
        if len(GraphData['panEvents'])==0:
            if OtherEvent>0:
                OtherEventCount_Tap=OtherEventCount_Tap+1
                EventString='Tap and Other Event (Rotation,Longpress,Pinch)'
                print('OtherEventCount_Tap')
    if len(GraphData['tapEvents'])>=3:
        if len(GraphData['panEvents'])==0:
            if OtherEvent>0:
                OtherEventCount_Tap=OtherEventCount_Tap+1
                EventString='Tap and Other Event (Rotation,Longpress,Pinch)'
                print(' OtherEventCount_Tap')
    if len(GraphData['tapEvents'])>0:
        if len(GraphData['panEvents'])>0:
            if OtherEvent>0:
                OtherEventCount_Tap_Scroll=OtherEventCount_Tap_Scroll+1
                EventString='Tap ,Pan and Other Event (Rotation,Longpress,Pinch)'
                print('OtherEventCount_Tap_Scroll')
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
                EventString='Pan and Other Event (Rotation,Longpress,Pinch)'
                print('OtherEventCount_Scroll')

    if len(GraphData['tapEvents'])==3:
        if len(GraphData['panEvents'])==0:
            if OtherEvent==0:
                NoEvent_Count=NoEvent_Count+1
                EventString='No Event'



    DrawTap(GraphData,iUser,EventString)


def PanTapOneFinger():
    AllUser=['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012','3014','3015']
    UserName=['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13']

    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    import matplotlib.pyplot as plt
    
    import matplotlib.gridspec as gridspec

    fig = plt.figure(figsize=(10, 8))
    #outer = gridspec.GridSpec(4, 4, wspace=0.05, hspace=0.05)
    
      
    labels=['Only Tap ,No Other Event','OtherEvents With Tap','Only Scroll ,No Other Event','OtherEvents With Scroll','Tap Scroll ,No Other Event','OtherEvents With Scroll and Tap','Only OtherEvents','NoEvent']
        
 


    AllUserTapError=[0,0,0,0,0,0,0,0]
    AllUserPanError=[0,0,0,0,0,0,0,0]

    for iUser in range(13):
        User=AllUser[iUser ]
        path='StudyData/NewData/'+User+'/'

        files=listdir(path)
        file=list()
        for i in range(len(files)):
            if files[i][-4:]=='json':
                file.append(files[i])

        GraphData=ReadData(path,file)

        Device_info=GraphData[0]['deviceInfo']['screenSize']
        Tap_GraphData=GraphData[0]['tapTask']['trials']
        Swipe_GraphData=GraphData[0]['swipeTask']['trials']
        HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
        VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

        for iTrial in range(len(Tap_GraphData)):
            if (len(Tap_GraphData[iTrial]["rawTouchTracks"]))==1:
                if len(Tap_GraphData[iTrial]['tapEvents'])>0:
                    if Tap_GraphData[iTrial]['tapEvents'][len(Tap_GraphData[iTrial]['tapEvents'])-1]['state']=='ended':
                        if len(Tap_GraphData[iTrial]['panEvents'])>0:
                            if Tap_GraphData[iTrial]['panEvents'][len(Tap_GraphData[iTrial]['panEvents'])-1]['state']=='ended':
                                print(User,iTrial,len(Tap_GraphData[iTrial]["rawTouchTracks"]),len(Tap_GraphData[iTrial]['tapEvents']),len(Tap_GraphData[iTrial]['panEvents']),"Tap and Pan")



def ImproveFactor():
    def OtherEventFuc(GraphData):
        OtherEvent=0
        if len(GraphData['rotationEvents'])>0:
            OtherEvent=1
        if len(GraphData['pinchEvents'])>0:
            OtherEvent=1
        if len(GraphData['longPressEvents'])>0:
            OtherEvent=1
        return OtherEvent

    def plot_func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        print(pct)
        if pct/100>0.1:
            
            return "{:.1f}%\n".format(pct)
        else:
            return ""


    Tap=[0.2786435786, 0.02070707071 ,0.05930735931  ,0 ,  0.005050505051 , 0.03775077969  , 0.5985407066  ,  0]
    Pan=[0  ,0  , 0.3755484682  ,  0.001538461538  ,0.0009496676163 ,0   ,0.6188864795  ,  0.003076923077]
    All=[0.1393217893 ,  0.01035353535   ,0.2174279138  ,  0.0007692307692, 0.003000086333 , 0.01887538984 ,  0.6087135931  ,  0.001538461538]
    colors = ['red','blue','orange','yellow','green', 'pink',  'purple','black','lightskyblue']

    labels=['Trial with No Event ' ,'Trial with Pan+Other events'   ,'Trial with Tap+Pan+Other events'   , 'Trial with Tap+Other events'  , 'Trial with Other events' , 'Trial with Pan events ','Trial with Tap+Pan events' , 'Trial with Tap events']
    plt.subplot(2,1,1)
    plt.pie(Tap,colors=colors,autopct=lambda pct: plot_func(pct, Tap),
                                  textprops=dict(color="black"))

    plt.title("Improvement Trial in Tap Task")
              
    plt.legend(labels=labels,bbox_to_anchor=[0,0.5,0,0.5],prop={'size':12})

    plt.subplot(2,1,2)
    plt.pie(Pan,colors=colors,autopct=lambda pct: plot_func(pct, Pan),
                                  textprops=dict(color="black"))

    plt.title("Improvement Trial in Pan Task")
              
    #plt.legend(labels=labels,bbox_to_anchor=[-1,-1,-1,],prop={'size':16})

    plt.show()



def PanTaskFailure(User,task ,Trial):
    def DrawScroll(TaskData,User,Trial,task):

        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        AllFinger_PositionX_Dropout=list()
        AllFinger_PositionY_Dropout=list()

        AllColor=['red','blue','green','yellow','pink','orange','purple','gray','black','red','blue','green','yellow','pink','orange','purple','gray']

        firstPointX=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][0]
        firstPointY=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][1]
        #TargetX=TaskData["targetFrame"][0][0]+ TaskData["targetFrame"][1][0]*0.5
        #TargetY=TaskData["targetFrame"][0][1]+ TaskData["targetFrame"][1][1]*0.5
        
      

        print(len(TaskData['tapEvents']),len(TaskData['panEvents']))

                

               
        #############################
        # plt.subplot(4,1,1)
        fig1,ax1=plt.subplots(1)
        #fig1,ax1=plt.subplots(4,1,1)
        # inner1 = gridspec.GridSpecFromSubplotSpec(1, 1,
        #                 subplot_spec=outer[0], wspace=0.0, hspace=0.0)
        # ax1 = plt.Subplot(fig, inner1[0])

        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        #rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        #ax1.add_patch(rect)

        MaxX=-1000000000000
        MinX=1000000000000
        MaxY=-1000000000000
        MinY=1000000000000
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            AllFinger_PositionX.append([])
            AllFinger_PositionY.append([])
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
                # if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    AllFinger_PositionX[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                    AllFinger_PositionY[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])

                    if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]<MinX:
                        MinX=TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]
                    if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]>MaxX:
                        MaxX=TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0]

                    if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]<MinY:
                        MinY=TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]
                    if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]>MaxY:
                        MaxY=TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1]



        
        for iFinger in range(len(AllFinger_PositionX)):
            if iFinger>len(AllColor)-1:
                TouchPoint=ax1.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color='gray',alpha=0.5,s=100)
            else:
                TouchPoint=ax1.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color=AllColor[iFinger],alpha=0.5,s=100)


        if len(TaskData['pinchEvents'])>0:
            Arrow=ax1.scatter(100000,1000000,color='lightblue',marker=r" ${}$ ".format(chr(8592)),label='pinch event',s=150)
        else:
            Arrow=None

        PinchXlist=list()
        PinchYlist=list()
        RotationXlist=list()
        RotationYlist=list()
        for i in range(len(TaskData['pinchEvents'])):
            #print(TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['0'])
            if True:
                try:
                    #ax1.scatter(TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['0'][0],TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['0'][1],color='purple',marker=r" ${}$ ".format(chr(10548)),label='pinch event',s=100)
                    #ax1.scatter(TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['1'][0],TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['1'][1],color='yellow',marker=r" ${}$ ".format(chr(10549)),label='pinch event',s=100)
                    startPointX=TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['0'][0]
                    startPointY=TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['0'][1]
                    CenterPointX=TaskData['pinchEvents'][i]['location'][0]
                    CenterPointY=TaskData['pinchEvents'][i]['location'][1]
                    startPointX2=TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['1'][0]
                    startPointY2=TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['1'][1]
                    
                    Distance=np.sqrt((CenterPointX-startPointX)*(CenterPointX-startPointX)+(CenterPointY-startPointY)*(CenterPointY-startPointY))
                    Distance2=np.sqrt((CenterPointX-startPointX2)*(CenterPointX-startPointX2)+(CenterPointY-startPointY2)*(CenterPointY-startPointY2))


                    # if i ==0:
                    #     Arrow=plt.arrow(startPointX,startPointY,3*(CenterPointX-startPointX)/ Distance,3*(CenterPointY-startPointY)/ Distance,width=0.3,label='Pinch')
                    #     Arrow=plt.arrow(startPointX2,startPointY2,3*(CenterPointX-startPointX2)/ Distance2,3*(CenterPointY-startPointY2)/ Distance2,width=0.3,label='Pinch')
                    #     #ax1.legend([Arrow,],['Pinch',])

                    plt.arrow(startPointX,startPointY,3*(CenterPointX-startPointX)/ Distance,3*(CenterPointY-startPointY)/ Distance,width=1,label='Pinch',color='lightblue')
                    plt.arrow(startPointX2,startPointY2,3*(CenterPointX-startPointX2)/ Distance2,3*(CenterPointY-startPointY2)/ Distance2,width=1,label='Pinch',color='lightblue')

                    
                except:
                    pass

        rotation1=None
        rotation2=None
        for i in range(len(TaskData['rotationEvents'])):
            #print(TaskData['pinchEvents'][i]['locationOfTouchAtIndex']['0'])
            if True:
                try:
                    rotation1=ax1.scatter(TaskData['rotationEvents'][i]['locationOfTouchAtIndex']['0'][0],TaskData['rotationEvents'][i]['locationOfTouchAtIndex']['0'][1],color='purple',marker=r" ${}$ ".format(chr(10558)),label='rotation event',s=150)
                    rotation2=ax1.scatter(TaskData['rotationEvents'][i]['locationOfTouchAtIndex']['1'][0],TaskData['rotationEvents'][i]['locationOfTouchAtIndex']['1'][1],color='gray',marker=r" ${}$ ".format(chr(10559)),label='rotation event',s=150)
                    
                    
                       

                    
                except:
                    pass
            
        if len(TaskData['tapEvents'])>0:
            Y=TaskData['tapEvents'][0]['location'][0]
            X=Device_info[0]-TaskData['tapEvents'][0]['location'][1]

            # Y=TaskData['tapEvents'][0]['location'][0]
            # X=TaskData['tapEvents'][0]['location'][1]

            tap=ax1.scatter(X,Y,color='black',marker="X",s=200)
        else:

            tap=None
        ax1.legend([rotation1,Arrow,tap,TouchPoint],['Rotation Event','Pinch Event','Tap Event','Touch Point'])


        ax1.set_title(str(User)+" "+str(task)+" Trial "+str(Trial))
        plt.xlim(MinX-25,MaxX+25)
        plt.ylim(MinY-25,MaxY+25)

    #AllUser=['3012']
    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    AllUser=User
    UserLabel=User
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt

   
    path='StudyData/NewData/'+User+'/'

    files=listdir(path)
    file=list()
    for i in range(len(files)):
        if files[i][-4:]=='json':
            file.append(files[i])

    GraphData=ReadData(path,file)

    Device_info=GraphData[0]['deviceInfo']['screenSize']
    Tap_GraphData=GraphData[0]['tapTask']['trials']
    Swipe_GraphData=GraphData[0]['swipeTask']['trials']
    HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
    VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']


   
   

    if task=='swipeTask':
        TaskData=Swipe_GraphData[Trial]

    elif task=='verticalScrollTask':

        TaskData=VScroll_GraphData[Trial]
    elif task=='horizontalScrollTask':

        TaskData=HScroll_GraphData[Trial]

    DrawScroll(TaskData,UserLabel,Trial,task)
    plt.show()      



def TapOptimizer_Analysis(User,Trial,stage):
    import numpy as np
    import matplotlib.patches as patches
    import matplotlib.gridspec as gridspec
    def LabelAllTrue(TaskData):
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])): 
                    TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True

        return TaskData
    def DrawScroll(TaskData):
        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        AllFinger_PositionX_Dropout=list()
        AllFinger_PositionY_Dropout=list()

        AllColor=['red','blue','green','yellow','pink','orange','purple','gray','black','red','blue','green','yellow','pink','orange','purple','gray','black']

        firstPointX=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][0]
        firstPointY=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][1]
        #TargetX=TaskData["targetFrame"][0][0]+ TaskData["targetFrame"][1][0]*0.5
        #TargetY=TaskData["targetFrame"][0][1]+ TaskData["targetFrame"][1][1]*0.5
        
      



                

               
        #############################
        # plt.subplot(4,1,1)
        fig1,ax1=plt.subplots(1)
        #fig1,ax1=plt.subplots(4,1,1)
        # inner1 = gridspec.GridSpecFromSubplotSpec(1, 1,
        #                 subplot_spec=outer[0], wspace=0.0, hspace=0.0)
        # ax1 = plt.Subplot(fig, inner1[0])

        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        #rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        #ax1.add_patch(rect)
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            AllFinger_PositionX.append([])
            AllFinger_PositionY.append([])
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
                # if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    AllFinger_PositionX[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                    AllFinger_PositionY[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])


        for iFinger in range(len(AllFinger_PositionX)):
            ax1.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color=AllColor[iFinger])

        plt.xlim(firstPointX-200,firstPointX+200)
        plt.ylim(firstPointY-200,firstPointY+200)


    def DrawTap(TaskData,User,test,task):
        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        AllFinger_PositionX_Dropout=list()
        AllFinger_PositionY_Dropout=list()

        AllColor=['red','blue','green','yellow','pink','orange','purple','gray','black','red','blue','green','yellow','pink','orange','purple','gray','black']

        firstPointX=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][0]
        firstPointY=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][1]
        TargetX=TaskData["targetFrame"][0][0]+ TaskData["targetFrame"][1][0]*0.5
        TargetY=TaskData["targetFrame"][0][1]+ TaskData["targetFrame"][1][1]*0.5
        
        X1=TaskData["targetFrame"][0][0]
        Y1=TaskData["targetFrame"][0][1]   



        fig = plt.figure(figsize=(10, 8))
        outer = gridspec.GridSpec(3, 2, wspace=0.1, hspace=0.1)
        
                

               
  
        fig3,ax3=plt.subplots(1)
   

        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        ax3.add_patch(rect)
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            AllFinger_PositionX.append([])
            AllFinger_PositionY.append([])
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
                if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    AllFinger_PositionX[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                    AllFinger_PositionY[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])


        for iFinger in range(len(AllFinger_PositionX)):
            TouchPoint=ax3.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color=AllColor[iFinger])

        pan=None
        for panevent in range(len(TaskData['panEvents'])):

            # if panevent%3==0:
            if True:
                pan=ax3.scatter(TaskData['panEvents'][panevent]['location'][0],TaskData['panEvents'][panevent]['location'][1],color='purple',marker=r" ${}$ ".format(chr(10230)),label='pan event',s=150)
                
                
        if pan!=None:

            ax3.legend([TouchPoint,rect,pan],['Touch Point','target button','Pan Event'])
        else:
            ax3.legend([TouchPoint,rect],['Touch Point','target button'])
        
        ax3.set_title(str(User) +" "+str(task)+"Task"+" Trial "+str(test))
        plt.xlim(TargetX-100,TargetX+100)
        plt.ylim(TargetY-100,TargetY+100)



        



    AllUser=User
    UserLabel=User
    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt
   

    path='StudyData/NewData/'+User+'/'

    files=listdir(path)
    file=list()
    for i in range(len(files)):
        if files[i][-4:]=='json':
            file.append(files[i])

    GraphData=ReadData(path,file)

    Device_info=GraphData[0]['deviceInfo']['screenSize']
    Tap_GraphData=GraphData[0]['tapTask']['trials']
    Swipe_GraphData=GraphData[0]['swipeTask']['trials']
    HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
    VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

    
    task='tap'
    if Trial<=len(Tap_GraphData)-1:
        test=Trial
       
 
        TaskData=Tap_GraphData[Trial]
        LabelAllTrue(TaskData)
        

        AfterFilterData,Success=tapopt.TapOptimizer_Graph(TaskData,stage)
        DrawTap(TaskData,UserLabel,Trial,task)
        
        #print(Success)
    
        plt.show()
    else:
        print("Exceeded Index of Trial")
  

def TapTaskFailure(User,Trial):
    import numpy as np
    import matplotlib.patches as patches
    import matplotlib.gridspec as gridspec
    def LabelAllTrue(TaskData):
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])): 
                    TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']=True

        return TaskData
    def DrawScroll(TaskData):
        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        AllFinger_PositionX_Dropout=list()
        AllFinger_PositionY_Dropout=list()

        AllColor=['red','blue','green','yellow','pink','orange','purple','gray','black','red','blue','green','yellow','pink','orange','purple','gray','black']

        firstPointX=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][0]
        firstPointY=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][1]
        #TargetX=TaskData["targetFrame"][0][0]+ TaskData["targetFrame"][1][0]*0.5
        #TargetY=TaskData["targetFrame"][0][1]+ TaskData["targetFrame"][1][1]*0.5
        
      



                

               
        #############################
        # plt.subplot(4,1,1)
        fig1,ax1=plt.subplots(1)
        #fig1,ax1=plt.subplots(4,1,1)
        # inner1 = gridspec.GridSpecFromSubplotSpec(1, 1,
        #                 subplot_spec=outer[0], wspace=0.0, hspace=0.0)
        # ax1 = plt.Subplot(fig, inner1[0])

        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        #rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        #ax1.add_patch(rect)
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            AllFinger_PositionX.append([])
            AllFinger_PositionY.append([])
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
                # if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    AllFinger_PositionX[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                    AllFinger_PositionY[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])


        for iFinger in range(len(AllFinger_PositionX)):
            ax1.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color=AllColor[iFinger])

        plt.xlim(firstPointX-200,firstPointX+200)
        plt.ylim(firstPointY-200,firstPointY+200)


    def DrawTap(TaskData,User,test,task):
        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        AllFinger_PositionX_Dropout=list()
        AllFinger_PositionY_Dropout=list()

        AllColor=['red','blue','green','yellow','pink','orange','purple','gray','black','red','blue','green','yellow','pink','orange','purple','gray','black']

        firstPointX=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][0]
        firstPointY=TaskData["rawTouchTracks"][0]["rawTouches"][0]['location'][1]
        TargetX=TaskData["targetFrame"][0][0]+ TaskData["targetFrame"][1][0]*0.5
        TargetY=TaskData["targetFrame"][0][1]+ TaskData["targetFrame"][1][1]*0.5
        
        X1=TaskData["targetFrame"][0][0]
        Y1=TaskData["targetFrame"][0][1]   



        fig = plt.figure(figsize=(10, 8))
        outer = gridspec.GridSpec(3, 2, wspace=0.1, hspace=0.1)
        
                

               
  
        fig3,ax3=plt.subplots(1)
   

        AllFinger_PositionX=list()
        AllFinger_PositionY=list()
        rect=patches.Rectangle((TaskData["targetFrame"][0][0],TaskData["targetFrame"][0][1]),TaskData["targetFrame"][1][0],TaskData["targetFrame"][1][1],edgecolor='red',facecolor='None')
        ax3.add_patch(rect)
        for iFinger in range(len(TaskData["rawTouchTracks"])):
            AllFinger_PositionX.append([])
            AllFinger_PositionY.append([])
            for iPoint in range(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])):
                if TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['label']==True:
                    AllFinger_PositionX[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][0])
                    AllFinger_PositionY[iFinger].append(TaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['location'][1])


        for iFinger in range(len(AllFinger_PositionX)):
            TouchPoint=ax3.scatter(AllFinger_PositionX[iFinger],AllFinger_PositionY[iFinger],color=AllColor[iFinger])

        pan=None
        for panevent in range(len(TaskData['panEvents'])):

            # if panevent%3==0:
            if True:
                pan=ax3.scatter(TaskData['panEvents'][panevent]['location'][0],TaskData['panEvents'][panevent]['location'][1],color='purple',marker=r" ${}$ ".format(chr(10230)),label='pan event',s=150)
                
                
        if pan!=None:

            ax3.legend([TouchPoint,rect,pan],['Touch Point','target button','Pan Event'])
        else:
            ax3.legend([TouchPoint,rect],['Touch Point','target button'])
        
        ax3.set_title(str(User) +" "+str(task)+"Task"+" Trial "+str(test))
        plt.xlim(TargetX-100,TargetX+100)
        plt.ylim(TargetY-100,TargetY+100)



        



    AllUser=User
    UserLabel=User
    Alllist=list()
    #AllUser=['3007','3008','3009','3010','3011','3012','3014']
    AllUserPan=list()
    AllUserTap=list()
    import matplotlib.pyplot as plt
   

    path='StudyData/NewData/'+User+'/'

    files=listdir(path)
    file=list()
    for i in range(len(files)):
        if files[i][-4:]=='json':
            file.append(files[i])

    GraphData=ReadData(path,file)

    Device_info=GraphData[0]['deviceInfo']['screenSize']
    Tap_GraphData=GraphData[0]['tapTask']['trials']
    Swipe_GraphData=GraphData[0]['swipeTask']['trials']
    HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
    VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

    
    task='tap'
    if Trial<=len(Tap_GraphData)-1:
        test=Trial
       
 
        TaskData=Tap_GraphData[Trial]
        LabelAllTrue(TaskData)
        

        #AfterFilterData,Success=tapopt.TapOptimizer_Graph(TaskData,5)
        DrawTap(TaskData,UserLabel,Trial,task)
        
        #print(Success)
    
        plt.show()
    else:
        print("Exceeded Index of Trial")
  
def KinematicsFeatures():

    AllUserX=list()
    AllUserY=list()
    AllUserZ=list()
    #for User in ['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012']:
    for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:


       

        AllDataX=list()
        AllDataY=list()
        AllDataZ=list()
        #for task in ['tapTask','swipeTask','horizontalScrollTask','verticalScrollTask']:
        for User in ['3001','3002','3003','3005','3006','3007','3008','3009','3010','3011','3012']:
            path='StudyData/NewData/'+User+'/'

            files=listdir(path)
            file=list()
            for i in range(len(files)):
                if files[i][-4:]=='json':
                    file.append(files[i])

            GraphData=ReadData(path,file)

            Device_info=GraphData[0]['deviceInfo']['screenSize']
            Tap_GraphData=GraphData[0]['tapTask']['trials']
            Swipe_GraphData=GraphData[0]['swipeTask']['trials']
            HScroll_GraphData=GraphData[0]['horizontalScrollTask']['trials']
            VScroll_GraphData=GraphData[0]['verticalScrollTask']['trials']

            import matplotlib.pyplot as plt
            PlotData=GraphData[0]
            DataX=list()
            DataY=list()
            DataZ=list()
            for iTrial in range(len(PlotData[task]['trials'])):
                DataX_IneachTrial=list()
                DataY_IneachTrial=list()
                DataZ_IneachTrial=list()
                for iFinger in range(len(PlotData[task]['trials'][iTrial]["rawTouchTracks"])):
                    #DataX=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                    #DataY=np.zeros(len(TaskData["rawTouchTracks"][i]["rawTouches"]))
                    if len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])>2:
                        for iPoint in range(3,len(PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"])):
                            Point_t=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint]
                            Point_t_1=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]
                            Point_t_2=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-2]
                            Point_t_3=PlotData[task]['trials'][iTrial]["rawTouchTracks"][iFinger]["rawTouches"][iPoint-3]
                            X0=Point_t['location'][0]
                            Y0=Point_t['location'][1]
                            T0=Point_t['timestamp']

                            X1=Point_t_1['location'][0]
                            Y1=Point_t_1['location'][1]
                            T1=Point_t_1['timestamp']

                            X2=Point_t_2['location'][0]
                            Y2=Point_t_2['location'][1]
                            T2=Point_t_2['timestamp']

                            X3=Point_t_3['location'][0]
                            Y3=Point_t_3['location'][1]
                            T3=Point_t_3['timestamp']

                            #Velocity=ComputeVelocity([X0,Y0,T0],[X1,Y1,T1])
                            Velocity=ComputeDisplace([X0,Y0,T0],[X1,Y1,T1])
                            Velocity_t_1=ComputeVelocity([X1,Y1,T1],[X2,Y2,T2])

                            
                            
                            Accelerate=ComputeAccelerate([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2])
                            #Accelerate=Velocity-Velocity_t_1

                            A1=ComputeAccelerate([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2])
                            A2=ComputeAccelerate([X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3])

                            Jerk=ComputeJerk([X0,Y0,T0],[X1,Y1,T1],[X2,Y2,T2],[X3,Y3,T3])
                            #Jerk=A1-A2
                            

                            if ~np.isnan(Jerk):
                                DataX_IneachTrial.append(Jerk)
                            if ~np.isnan(Accelerate):
                                DataY_IneachTrial.append(Accelerate)
                            if ~np.isnan(Velocity):
                                DataZ_IneachTrial.append(Velocity)
                            #plt.scatter(DataX,DataY)
                            
                            #plt.legend(loc='upper right')
                if len(DataX_IneachTrial)>0:
                    DataX.append(np.mean(DataX_IneachTrial))
                if len(DataY_IneachTrial)>0:
                    DataY.append(np.mean(DataY_IneachTrial))
                if len(DataZ_IneachTrial)>0:
                    DataZ.append(np.mean(DataZ_IneachTrial))

                
            AllDataX.append(DataX)   
            AllDataY.append(DataY)
            AllDataZ.append(DataZ) 

        AllUserX.append(AllDataX)
        AllUserY.append(AllDataY)
        AllUserZ.append(AllDataZ)


    #print(AllDataY)

    Task=['tapping','swiping','horizontalscroll','verticalscroll']
    for iUser in range(len(AllUserX)):
        plt.subplot(3,len(AllUserX),iUser+1)
        plt.subplots_adjust(wspace=0.3,hspace=0.3)
        plt.boxplot(AllUserZ[iUser])
        plt.title(Task[iUser])
        if iUser==0:
            plt.ylabel("Velocity (points/ms)")
        #plt.xlabel("User Number")
        plt.ylim(0,50)
        plt.subplot(3,len(AllUserX),iUser+1+len(AllUserX))
        plt.subplots_adjust(wspace=0.3,hspace=0.3)
        plt.boxplot(AllUserY[iUser])
        plt.title(Task[iUser])
        #plt.xlabel("User Number")
        if iUser==0:
            plt.ylabel("Accelerate (points/ms^2)")
        plt.ylim(0,25)
        plt.subplot(3,len(AllUserX),iUser+1+2*len(AllUserX))
        plt.subplots_adjust(wspace=0.3,hspace=0.3)
        plt.boxplot(AllUserX[iUser])
        plt.title(Task[iUser])
        plt.xlabel("User Number")
        if iUser==0:
            plt.ylabel("Jerk (points/ms^3)")
        plt.ylim(0,20)
    plt.show()
    #print(len(GraphData[0]['tapTask']['trials']))
    #PlotAllJerk(GraphData[0])








import random
#import tensorflow as tf
#from tensorflow.contrib import rnn
#import DataPreProcess_Final as dp
import numpy as np
from os import listdir
from os.path import isfile,isdir,join
import json
import Optimizer.TapOptimizer as tapopt
import Optimizer.ScrollOptimizer as scrollopt
import Optimizer.SwipeOptimizer as swipeopt
import sys
import TaskSuccessVerify as tv
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.models import Sequential, model_from_json


#####
#AnalyzeError_AllUser()
#AnalyzeErrorOneTask('horizontalScrollTask')
#TapTaskFailure('3010',10)

#TapOptimizer_Analysis('3010',10,6)

#PanTaskFailure('3011','verticalScrollTask' ,2)


#DurationDiscreteGesture_v1()
#DurationDiscreteGesture_v2()
#DefaultSystemRecognitionTime()
#ModelArchitecture('3001',0,0.05,'Dynamic')
#KinematicsFeatures()











####Main Funciton ######

#Draw_RecognizerSponseTime()
#AnalyzeError()

#RecognizerSponseTime()


#AnalysisTapTask(3)




#AnalysisOfFingerNum()




#ImproveFactor()



#Test()

#PanTapOneFinger()
#Oveload_modelrView()

#TappingMultiTouch()


#TapMovement()

#SurveyThreshold()
# print(len(GraphData[0]['tapTask']['trials']))
# PlotAllJerk(GraphData[0])

# #Tap
# Success=0
# FalseResult=0
# for iTrial in range(0,1):
#     import matplotlib.pyplot as plt

#     plt.subplot(1,1,iTrial+1)
#     #plt.subplot(6,6,FalseResult+1)
#     Test=iTrial+67
#     Result=PlotTap(Tap_GraphData[Test],Test,Device_info)
#     if Resevaluate_ult==False:
#         FalseResult=FalseResult+1
#     #print("Trial:",Test,"Result",Result)
#     Success=Success+Result

# print(Success)


#Swipe
# for iTrial in range(0,10):
#     import matplotlib.pyplot as plt
#     plt.subplot(2,5,iTrial+1)
#     Test=iTrial+50
#     A=PlotSwipe(Swipe_GraphData[Test],Test,Device_info)
# plt.show()

# ##HScroll
# for iTrial in range(0,20):
#     import matplotlib.pyplot as plt
#     plt.subplot(4,5,iTrial+1)
#     Test=iTrial+10
#     A=PlotHScroll(HScroll_GraphData[Test],Test,Device_info)


# ###VScroll
# for iTrial in range(0,20):
#     import matplotlib.pyplot as plt
#     plt.subplot(4,5,iTrial+1)
#     Test=iTrial
#     A=PlotVScroll(VScroll_GraphData[Test],Test,Device_info)




#PlotJerk_AllTask(GraphData[0])
#print(len(Tap_GraphData),len(Swipe_GraphData),len(HScroll_GraphData),len(VScroll_GraphData))





##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk##PlotAll Jerk

