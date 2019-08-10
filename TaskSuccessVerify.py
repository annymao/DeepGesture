

TapMaximumDuration = 1; #paper  350 ms

#TapAllowableMovement = 14; #paper 5mm iOS 實測大約3mm (20points)
#TapAllowableMovement = 46; #paper 5mm iOS 實測大約3mm (20points)
TapAllowableMovement = 45; #paper 5mm iOS 實測大約3mm (20points)

DoubleTapTimeInterval=0.2

PanAllowableMovement=10

SwipeMaximumDuration = 0.3;

SwipeMinimumMovement = 20;

SwipeMinimumVelocity = 300
#SwipeMinimumVelocity = 200;
#SwipeMinimumVelocity = 180;

#SwipeMinimumMovement=100
#SwipeMaximumDuration=0.351

# def TaskThresholdClassification2(NewTaskData):
#     ##0 no data ,1:tap. , 2:swipe.  3:pan
#     ##數入的是單單純純的rawtouchdata
#     FingerNum=len(NewTaskData["rawTouchTracks"]);
#     if(FingerNum<1):
#         #print("No Finger")
#         return 0
#     noTouchPoint=True
#     for iFinger in range(len(NewTaskData["rawTouchTracks"])):
#         touchpointnum=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"]);    
#         if touchpointnum>0:
#             noTouchPoint=False

#     if noTouchPoint==True:
#         #print("No Touch Point")
#         return 0

#     for iFinger in range(len(NewTaskData["rawTouchTracks"])):
#         if(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])>0):
#             TimeDuration=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]
#             if TimeDuration>TapMaximumDuration:
#                 return 3   #任何一個點大於門檻都為 scroll

#     for iFinger in range(len(NewTaskData["rawTouchTracks"])):
#         if(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])>0):
#             TimeDuration=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]
#         for touchPointIndex in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
#             dx=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][0] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0];
#             dy=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][1] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1];
#             if dx*dx+dy*dy <=TapAllowableMovement*TapAllowableMovement:
#                 if TimeDuration<=TapMaximumDuration:
#                     return 1

#     WhichFingerCanSwipe=np.zeros(FingerNum)
#     Recognized=False
#     for iFinger in range(len(NewTaskData["rawTouchTracks"])):
#         for iPoint in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
#             if NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]>=SwipeMaximumDuration:
#                 if Recognized==False:
#                     finalRecognizedDirection = "none";
#                 continue
#             PointPosition=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"]
#             dx = PointPosition[0] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0];
#             dy = PointPosition[1] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1];
            
#             #print(dx * dx + dy * dy,"vs",SwipeMinimumMovement * SwipeMinimumMovement)
#             if (dx * dx + dy * dy >= SwipeMinimumMovement * SwipeMinimumMovement):    
#                 WhichFingerCanSwipe[iFinger] = True;
                    
#             if WhichFingerCanSwipe[iFinger] ==True:
#                 PointPosition=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"]
#                 prePointPosition=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"]
#                 dx=PointPosition[0] - prePointPosition[0]
#                 dy=PointPosition[1] - prePointPosition[1]
                
#                 dt=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"] -NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"];
#                 v=np.sqrt(dx * dx + dy * dy)/dt;
                
#                 if (abs(v) >= SwipeMinimumVelocity):
#                     return 2
#     return 3               

def TaskThresholdClassification(NewTaskData):
    import TaskSuccessVerify as tv
    import numpy as np
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
                    return 2   #任何一個點大於門檻都為 scroll
                elif abs(dx)<=abs(dy):
                    return 2

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
            return 2   #任何一個點大於門檻都為 scroll
        elif abs(dx)<=abs(dy):
            return 2
             


def SimulationGestureRecognizer(NewTaskData):
    import TaskSuccessVerify as tv
    import numpy as np
    TapMaximumDuration = tv.TapMaximumDuration; #paper  350 ms

    TapAllowableMovement = tv.TapAllowableMovement; #paper 5mm iOS 實測大約3mm (20points)




    SwipeMaximumDuration = tv.SwipeMaximumDuration;

    SwipeMinimumMovement = tv.SwipeMinimumMovement;

    SwipeMinimumVelocity = tv.SwipeMinimumVelocity;
    

    #Gesture Recognizer state: "possible", "began","changed","ended","cancelled","failed","recognized"

    TapState="possible"
    PanState="possible"
    SwipeState="possible"

    EachTrialUniquetimeStamp=set()
    FingerStartTime=list()
    FingerEndTime=list()
    FingerStartPointX=list();
    FingerStartPointY=list();

    TimeData=list()
    FingerIndex=list()
    PointIndex=list()
    dX=0
    dY=0
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):

        for iPoint in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
            t=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
            dX=dX+NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]-NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['previousLocation'][0]
            dY=dY+NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]-NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['previousLocation'][1]
            
            if iPoint==0:
                FingerStartTime.append(t)
                FingerStartPointX.append(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0])
                FingerStartPointY.append(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1])
                if len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])==1:
                     FingerEndTime.append(t)
            elif iPoint>=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1:
                FingerEndTime.append(t)
            TimeData.append(t)
            FingerIndex.append(iFinger)
            PointIndex.append(iPoint)

            EachTrialUniquetimeStamp.add(t)
    
    #print("test",FingerEndTime)
    SortedAllTimeStamp=sorted(list(EachTrialUniquetimeStamp))
    
    for t in SortedAllTimeStamp:
        # if t in FingerStartTime: #TouchBegan
    
        #     ##Touch Began
            
        #     # TapState="possible"
        #     # PanState="possible"
        #     # SwipeState="possible"  
            
        # if t in FingerEndTime:  #TouchEnded
        #     if TapState=="possible":
        #         if SwipeState!="recognized":
        #             TapState="recognized"
        #             return 1
        #     if SwipeState!="recognized":
        #         SwipeState="failed"

        if t == min(FingerEndTime):  #TouchEnded
            
            FingerArray=list()
            PointArray=list()
            #print(TimeData," vs ",t," in ",np.where(t==np.array(TimeData))[0])
            Findindex=np.where(t==np.array(TimeData))[0]
            for i in Findindex:
                #print(i,Findindex)
                FingerArray.append(FingerIndex[i])
                PointArray.append(PointIndex[i])

            for checkdataindex in range(len(FingerArray)):
                iFinger=FingerArray[checkdataindex]
                iPoint=PointArray[checkdataindex]
                PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
                PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                PresentT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
                StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
                StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
                StartT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['timestamp']
                if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>TapAllowableMovement*TapAllowableMovement:
                    TapState="failed"
                if (PresentT-StartT)>TapMaximumDuration:
                    TapState="failed"

                if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>SwipeMinimumMovement * SwipeMinimumMovement:    
                    
                    if (PresentT-StartT)<SwipeMaximumDuration:
                        if iPoint!=0:
                            prePointPosition=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"]
                            # dx=PresentX - prePointPosition[0]
                            # dy=PresentY - prePointPosition[1]
                            # dt=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"] -NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"];
                            
                            dx=PresentX -StartX
                            dy=PresentY-StartY
                            dt=PresentT-StartT
                            v=np.sqrt(dx * dx + dy * dy)/dt;
                            
                            if (abs(v) >= SwipeMinimumVelocity):
                                if TapState!="recognized":
                                    if SwipeState=="possible":
                                        SwipeState="recognized"
                                        #print(v)
                                        return 2
                if TapState=="possible":
                    if SwipeState!="recognized":
                        if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))<TapAllowableMovement*TapAllowableMovement:
                               
                            if (PresentT-StartT)<TapMaximumDuration:
                                #if iPoint+1>=len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches']):
                                if NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['phase']=='ended':
                                    TapState="recognized"
                                    #print("Tap recognized")
                                    return 1
                if SwipeState!="recognized":
                    SwipeState="failed"

        if t not in FingerStartTime:                      #TouchMoved
            FingerArray=list()
            PointArray=list()
            #print(TimeData," vs ",t," in ",np.where(t==np.array(TimeData))[0])
            Findindex=np.where(t==np.array(TimeData))[0]
            for i in Findindex:
                #print(i,Findindex)
                FingerArray.append(FingerIndex[i])
                PointArray.append(PointIndex[i])

            for checkdataindex in range(len(FingerArray)):
                iFinger=FingerArray[checkdataindex]
                iPoint=PointArray[checkdataindex]
                PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
                PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                PresentT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
                StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
                StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
                StartT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['timestamp']
                if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>TapAllowableMovement*TapAllowableMovement:
                    TapState="failed"
                if (PresentT-StartT)>TapMaximumDuration:
                    TapState="failed"

                # if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>SwipeMinimumMovement * SwipeMinimumMovement:    
                #     if (PresentT-StartT)<SwipeMaximumDuration:
                #         prePointPosition=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"]
                #         dx=PresentX - prePointPosition[0]
                #         dy=PresentY - prePointPosition[1]
                #         dt=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"] -NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint-1]["timestamp"];
                #         v=np.sqrt(dx * dx + dy * dy)/dt;
                        
                #         if (abs(v) >= SwipeMinimumVelocity):
                #             if TapState!="recognized":
                #                 if SwipeState=="possible":
                #                     SwipeState="recognized"
                #                     print(v)
                #                     return 2
    #print("Pan recognized")
    if abs(dX)>=abs(dY):
        return 3
    else:
        return 4 
        
    # if SwipeState!="recognized":
    #     if TapState!="recognized":
    #         return 3


def SimulationGestureRecognizer_NoSwipe(NewTaskData):
    import TaskSuccessVerify as tv
    import numpy as np
    TapMaximumDuration = tv.TapMaximumDuration; #paper  350 ms

    TapAllowableMovement = tv.TapAllowableMovement; #paper 5mm iOS 實測大約3mm (20points)

    SwipeMaximumDuration = tv.SwipeMaximumDuration;

    SwipeMinimumMovement = tv.SwipeMinimumMovement;

    SwipeMinimumVelocity = tv.SwipeMinimumVelocity;
    

    #Gesture Recognizer state: "possible", "began","changed","ended","cancelled","failed","recognized"

    TapState="possible"
    PanState="possible"
    SwipeState="possible"

    EachTrialUniquetimeStamp=set()
    FingerStartTime=list()
    FingerEndTime=list()
    FingerStartPointX=list();
    FingerStartPointY=list();

    TimeData=list()
    FingerIndex=list()
    PointIndex=list()
    dX=0
    dY=0
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):

        for iPoint in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
            t=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
            dX=dX+NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]-NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['previousLocation'][0]
            dY=dY+NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]-NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['previousLocation'][1]
            
            if iPoint==0:
                FingerStartTime.append(t)
                FingerStartPointX.append(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0])
                FingerStartPointY.append(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1])
                if len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])==1:
                     FingerEndTime.append(t)
            elif iPoint>=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1:
                FingerEndTime.append(t)
            if NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='ended':
                FingerEndTime.append(t)
            TimeData.append(t)
            FingerIndex.append(iFinger)
            PointIndex.append(iPoint)

            EachTrialUniquetimeStamp.add(t)
    
    #print("test",FingerEndTime)
    SortedAllTimeStamp=sorted(list(EachTrialUniquetimeStamp))
    FingerEndTime=list(set(FingerEndTime))

    AllEvent=list()




    #####Begin to simulate the touch data
    for tindex in range(len(SortedAllTimeStamp)):
        t=SortedAllTimeStamp[tindex]
        ThisTimeFingerCount=0
        for iFinger in range(len(NewTaskData["rawTouchTracks"])):
            fingerstarttime=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['timestamp']
            fingerendtime=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])-1]['timestamp']
            if (t>=fingerstarttime) & (t<=fingerendtime):
                ThisTimeFingerCount=ThisTimeFingerCount+1

        #if t == min(FingerEndTime):  #TouchEnded
        if t in FingerStartTime:    
            FingerArray=list()
            PointArray=list()
            #print(TimeData," vs ",t," in ",np.where(t==np.array(TimeData))[0])
            Findindex=np.where(t==np.array(TimeData))[0]
            for i in Findindex:
                #print(i,Findindex)
                FingerArray.append(FingerIndex[i])
                PointArray.append(PointIndex[i])

            for checkdataindex in range(len(FingerArray)):
                iFinger=FingerArray[checkdataindex]
                iPoint=PointArray[checkdataindex]
                PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
                PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                PresentT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
                StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
                StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
                StartT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['timestamp']
                # if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>TapAllowableMovement*TapAllowableMovement:
                #     TapState="failed"
                # if (PresentT-StartT)>TapMaximumDuration:
                #     TapState="failed"

                # if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>TapAllowableMovement*TapAllowableMovement:
                #     TapState="failed"
                #     PanState=="changed"

        if t not in FingerStartTime:                      #TouchMoved
            if t not in FingerEndTime:
                FingerArray=list()
                PointArray=list()
                #print(TimeData," vs ",t," in ",np.where(t==np.array(TimeData))[0])
                Findindex=np.where(t==np.array(TimeData))[0]
                for i in Findindex:
                    #print(i,Findindex)
                    FingerArray.append(FingerIndex[i])
                    PointArray.append(PointIndex[i])

                for checkdataindex in range(len(FingerArray)):
                    iFinger=FingerArray[checkdataindex]
                    iPoint=PointArray[checkdataindex]
                    PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
                    PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                    PresentT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
                    StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
                    StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
                    StartT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['timestamp']

                    #if (((PresentX-StartX)*(PresentX-StartX))>PanAllowableMovement)|(((PresentY-StartY)*(PresentY-StartY))>PanAllowableMovement):

                    if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>PanAllowableMovement*PanAllowableMovement:
                        #TapState="failed"
                        if ThisTimeFingerCount==1:
                            PanState=="changed"
                            AllEvent.append(2)
                        AllEvent.append(2)

                    # if (PresentT-StartT)>TapMaximumDuration:
                    #     TapState="failed"
            else:
                FingerArray=list()
                PointArray=list()
                #print(TimeData," vs ",t," in ",np.where(t==np.array(TimeData))[0])
                Findindex=np.where(t==np.array(TimeData))[0]
                for i in Findindex:
                    #print(i,Findindex)
                    FingerArray.append(FingerIndex[i])
                    PointArray.append(PointIndex[i])

                for checkdataindex in range(len(FingerArray)):
                    iFinger=FingerArray[checkdataindex]
                    iPoint=PointArray[checkdataindex]
                    CanTap=1
                    for iFinger in range(len(NewTaskData['rawTouchTracks'])):
                        for iPoint in range(len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])):
                            PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
                            PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                            PresentT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
                            StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
                            StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
                            StartT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['timestamp']
                            if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>TapAllowableMovement*TapAllowableMovement:
                                CanTap=0

                    
                    # if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>TapAllowableMovement*TapAllowableMovement:
                    #     TapState="failed"
                    # if (PresentT-StartT)>TapMaximumDuration:
                    #     TapState="failed"

                                
                    # if TapState=="possible":

                        
                    #     # if PanState=="possible":
                    #         if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))<TapAllowableMovement*TapAllowableMovement:
                                   
                    #             # if (PresentT-StartT)<TapMaximumDuration:
                    #                 #if iPoint+1>=len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches']):
                    #             # if NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['phase']=='ended':
                    #             TapState="recognized"
                    #             #print("Tap recognized")
                    #             # return 1
                    #             PanState='possible'
                    #             TapState='possible'
                    #             AllEvent.append(1)
                    iFinger=FingerArray[checkdataindex]
                    iPoint=PointArray[checkdataindex]
                    PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
                    PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                    PresentT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
                    StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
                    StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
                    StartT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['timestamp']
               
                    # if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))<TapAllowableMovement*TapAllowableMovement:
                    #     if (PresentT-StartT)<TapMaximumDuration:
                    #         #if ThisTimeFingerCount==1:
                    #     # if (PresentT-StartT)<TapMaximumDuration:
                    #         #if iPoint+1>=len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches']):
                    #     # if NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['phase']=='ended':
                    #             TapState="recognized"
                    #             #print("Tap recognized")
                    #             # return 1
                    #             PanState='possible'
                    #             TapState='possible'
                    #             if CanTap==1:
                    #                 if tindex+1<len(SortedAllTimeStamp):
                    #                     if SortedAllTimeStamp[tindex+1]-SortedAllTimeStamp[tindex]>0.1:
                    #                         AllEvent.append(1)
                                    
                    # PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
                    # PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                    
                    # StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['previousLocation'][0]
                    # StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['previousLocation'][1]
            
                    if PanState=='changed':
                        #if (((PresentX-StartX)*(PresentX-StartX))>PanAllowableMovement)|(((PresentY-StartY)*(PresentY-StartY))>PanAllowableMovement):

                        if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>PanAllowableMovement*PanAllowableMovement:
                            if ThisTimeFingerCount==1:
                                AllEvent.append(2)
                                PanState='possible'
                                TapState='possible'
                    #if (((PresentX-StartX)*(PresentX-StartX))>PanAllowableMovement)|(((PresentY-StartY)*(PresentY-StartY))>PanAllowableMovement):

                    if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>PanAllowableMovement*PanAllowableMovement:
                            if ThisTimeFingerCount==1:
                                AllEvent.append(2)
                                PanState='possible'
                                TapState='possible'
                            AllEvent.append(2)
        if t in FingerEndTime:
            FingerArray=list()
            PointArray=list()
            #print(TimeData," vs ",t," in ",np.where(t==np.array(TimeData))[0])
            Findindex=np.where(t==np.array(TimeData))[0]
            for i in Findindex:
                #print(i,Findindex)
                FingerArray.append(FingerIndex[i])
                PointArray.append(PointIndex[i])

            for checkdataindex in range(len(FingerArray)):
                iFinger=FingerArray[checkdataindex]
                iPoint=PointArray[checkdataindex]

                CanTap=1
                
                for iPoint in range(len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])):
                    PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
                    PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                    PresentT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
                    StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
                    StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
                    StartT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['timestamp']
                    # if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))>TapAllowableMovement*TapAllowableMovement:
                    #     CanTap=0
                    if (np.sqrt((PresentX-StartX)*(PresentX-StartX))>TapAllowableMovement )|(np.sqrt((PresentY-StartY)*(PresentY-StartY))>TapAllowableMovement ):
                        CanTap=0
                # PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
                # PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                # PresentT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
                # StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
                # StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
                # StartT=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['timestamp']

                # if ((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))<TapAllowableMovement*TapAllowableMovement:
                #     # if ThisTimeFingerCount==1:
                    
                #         # if (PresentT-StartT)<TapMaximumDuration:
                #             #if iPoint+1>=len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches']):
                #         # if NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['phase']=='ended':
                #         TapState="recognized"
                #         #print("Tap recognized")
                #         # return 1
                #         PanState='possible'
                #         TapState='possible'
                #         if tindex+1<len(SortedAllTimeStamp):
                #             if CanTap==1:
                #                     #if SortedAllTimeStamp[tindex+1]-SortedAllTimeStamp[tindex]>0.15:
                #                         AllEvent.append(1)



                if CanTap==1:
                    if (PresentT-StartT)<TapMaximumDuration:
                        #if SortedAllTimeStamp[tindex+1]-SortedAllTimeStamp[tindex]>0.15:
                            AllEvent.append(1)


    # if len(NewTaskData['tapEvents'])>0:
    #     if 1 not in AllEvent:
    #         print("TapError")
    #         #print(NewTaskData['tapEvents'],AllEvent)
    #         AllLocation=list()
    #         for iFinger in range(len(NewTaskData['rawTouchTracks'])):
    #             #if len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])<20:
    #                 # print(NewTaskData['tapEvents'])
    #                 # print(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])
                        
                    
    #                 MaxDis=list()
    #                 for iPoint in range(len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])):
    #                     PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
    #                     PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                        
    #                     StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
    #                     StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
    #                     AllLocation.append([iFinger,PresentX,PresentY])
    #                     distance=np.sqrt((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))
    #                     MaxDis.append(distance)
    #                 print("MaxDis and MinDis",np.max(MaxDis),np.min(MaxDis))
            #if np.max(MaxDis)>TapAllowableMovement:
            #print(NewTaskData['tapEvents'],AllEvent,AllLocation)
            #print("---------")

    # if len(NewTaskData['panEvents'])>0:
    #     if 2 not in AllEvent:

    #         print("PanError")
    #         #print(NewTaskData['tapEvents'],AllEvent)
    #         AllLocation=list()
    #         for iFinger in range(len(NewTaskData['rawTouchTracks'])):
    #             #if len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])<20:
    #                 # print(NewTaskData['tapEvents'])
    #                 # print(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])
                        
                    
    #                 MaxDis=list()
    #                 for iPoint in range(len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])):
    #                     PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
    #                     PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
                        
    #                     StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['previousLocation'][0]
    #                     StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['previousLocation'][1]
    #                     AllLocation.append([iFinger,PresentX,PresentY])
    #                     distance=np.sqrt((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY))
    #                     MaxDis.append(distance)
    #                 print("MaxDis",np.max(MaxDis))
            #if np.max(MaxDis)>PanAllowableMovement:
            #print(AllEvent,AllLocation)
            #print("---------")

    # if len(NewTaskData['tapEvents'])>0:
    #     if 1 not in AllEvent:
    #         print(len(NewTaskData['tapEvents']),len(NewTaskData['panEvents'])," vs ",AllEvent)
    # if len(NewTaskData['tapEvents'])>0:
    #     MinMax=list()
    #     for iFinger in range(len(NewTaskData['rawTouchTracks'])):
    #         Dis=list()
    #         for iPoint in range(len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])):
    #             PresentX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][0]
    #             PresentY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['location'][1]
    #             StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
    #             StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
    #             Dis.append(np.sqrt((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY)))
    #         #print(iFinger,np.max(Dis))
    #         MinMax.append(np.max(Dis))
    #     if np.min(MinMax)>0:
    #         print("**",np.min(MinMax),"**")
    #         print("---------------------------")


    # if len(NewTaskData['panEvents'])>0:
    #     MinMax=list()
    #     for ipan in range(len(NewTaskData['panEvents'])):
            
    #         if NewTaskData['panEvents'][ipan]['state']=='began':
    #             Dis=list()
    #             for iFinger in range(len(NewTaskData['rawTouchTracks'])):
                    
                    
    #                 PresentX=NewTaskData['panEvents'][ipan]['location'][0]
    #                 PresentY=NewTaskData['panEvents'][ipan]['location'][1]
    #                 StartX=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][0]
    #                 StartY=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][0]['location'][1]
    #                 Dis.append(np.sqrt((PresentX-StartX)*(PresentX-StartX)+(PresentY-StartY)*(PresentY-StartY)))
    #                 #print(iFinger,np.max(Dis))
    #             MinMax.append(np.min(Dis))
    #     if np.min(MinMax)>0:
    #         print("**",MinMax,"**")
    #         print("---------------------------")


    if 2 not in AllEvent:
        if 1 in AllEvent:
            return 1 
    if 1 not in AllEvent:
        if 2 in AllEvent:
            return 2 
    return 0   
    #print("Pan recognized")
    
   
def SimulationGestureRecognizer_Android(NewTaskData):
    
    
    mAlwaysInTapRegion = True;
    mAlwaysInBiggerTapRegion = True;
    mStillDown = True;
    mInLongPress = False;
    mDeferConfirmSingleTap = False;
    def SimulateEvent(NewTaskData,t,FingerArray,PointArray,BeganEvent,EndEvent,mAlwaysInTapRegion):
        

        if BeganEvent==True & EndEvent==True:

            mAlwaysInTapRegion=True
            mAlwaysInTapRegion = True;
            mAlwaysInBiggerTapRegion = True;
            mStillDown = True;
            mInLongPress = False;
            mDeferConfirmSingleTap = False;
            if mAlwaysInTapRegion==True:
                for indexFinger in range(len(FingerArray)):
                    iFinger=FingerArray[indexFinger]
                    iPoint=PointArray[indexFinger]
                    PresentT=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                    StartT=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]
                    if PresentT-StartT>0:
                        TimeInterval=PresentT-StartT
                if (TimeInterval)>TapMaximumDuration:
                    return 1,mAlwaysInTapRegion
        elif BeganEvent==False & EndEvent==True:
            
            if mAlwaysInTapRegion==True:
                for indexFinger in range(len(FingerArray)):
                    iFinger=FingerArray[indexFinger]
                    iPoint=PointArray[indexFinger]
                    PresentT=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]
                    StartT=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]
                if (PresentT-StartT)>TapMaximumDuration:
                    return 1,mAlwaysInTapRegion
        elif BeganEvent==True & EndEvent==False:
            mAlwaysInTapRegion=True
            mAlwaysInTapRegion = True;
            mAlwaysInBiggerTapRegion = True;
            mStillDown = True;
            mInLongPress = False;
            mDeferConfirmSingleTap = False;
        else:
            for indexFinger in range(len(FingerArray)):
                iFinger=FingerArray[indexFinger]
                iPoint=PointArray[indexFinger]

                dX=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"][0]
                dY=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"][1]
                DeltaX=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["previousLocation"][0]
                DeltaY=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["previousLocation"][1]
                if mAlwaysInTapRegion==True:
                    distance=DeltaX*DeltaX+DeltaY*DeltaY
                    if distance>TapAllowableMovement*TapAllowableMovement:
                        mAlwaysInTapRegion=False
                        return 2,mAlwaysInTapRegion
                elif (dX>=1)|(dY>=1):

                    #print("Pan")
                    return 2,mAlwaysInTapRegion

        return 0,mAlwaysInTapRegion


    import TaskSuccessVerify as tv
    import numpy as np
    TapMaximumDuration = tv.TapMaximumDuration; #paper  350 ms

    TapAllowableMovement = tv.TapAllowableMovement; #paper 5mm iOS 實測大約3mm (20points)

    SwipeMaximumDuration = tv.SwipeMaximumDuration;

    SwipeMinimumMovement = tv.SwipeMinimumMovement;

    SwipeMinimumVelocity = tv.SwipeMinimumVelocity;
    



    #Gesture Recognizer state: "possible", "began","changed","ended","cancelled","failed","recognized"
    EachTrialUniquetimeStamp=list()

    AllTimeTouchphase=dict()
    FingerEndTime=list()
    FingerBeganTime=list()

    FingerBeganFingerIndex=list()
    FingerEndedFingerIndex=list()

    TimeData=list()
    FingerIndex=list()
    PointIndex=list() 
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        for iPoint in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
            t=NewTaskData['rawTouchTracks'][iFinger]['rawTouches'][iPoint]['timestamp']
            TimeData.append(t)
            FingerIndex.append(iFinger)
            PointIndex.append(iPoint)      
            if NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='ended':
                FingerEndTime.append(t)
                FingerEndedFingerIndex.append(iFinger)
            if NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]['phase']=='began':
                FingerBeganTime.append(t)
                FingerBeganFingerIndex.append(iFinger)



            EachTrialUniquetimeStamp.append(t)
    
    #print("test",FingerEndTime)
    SortedAllTimeStamp=sorted(list(EachTrialUniquetimeStamp))
    

    AllEvent=list()
    
    for t in SortedAllTimeStamp:
        FingerArray=list()
        PointArray=list()    
        Findindex=np.where(t==np.array(TimeData))[0]
        EndEvent=False
        BeganEvent=False
        if t in FingerEndTime:
            EndEvent=True
        if t in FingerBeganTime:
            BeganEvent=True

        for i in Findindex:
            #print(i,Findindex)
            FingerArray.append(FingerIndex[i])
            PointArray.append(PointIndex[i])

        [Event,mAlwaysInTapRegion]=SimulateEvent(NewTaskData,t,FingerArray,PointArray,BeganEvent,EndEvent,mAlwaysInTapRegion)
        if Event!=0:
            AllEvent.append(Event)
        

    #print(len(NewTaskData['tapEvents']),len(NewTaskData['panEvents'])," vs ",AllEvent)
    if 2 not in AllEvent:
        if 1 in AllEvent:
            return 1 
    if 1 not in AllEvent:
        if 2 in AllEvent:
            return 2 

    return 0 



def TapTask2(NewTaskData,iTrial):
    import numpy as np
    #TapMaximumDuration=100;
    #TapAllowableMovement=15;
    # FingerNum=len(NewTaskData["rawTouchTracks"]);
    # if(FingerNum<1):
    #     #print("No Finger")
    #     return False
    # noTouchPoint=True
    # for iFinger in range(len(NewTaskData["rawTouchTracks"])):
    #     touchpointnum=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"]);    
    #     if touchpointnum>0:
    #         noTouchPoint=False

    # if noTouchPoint==True:
    #     #print("No Touch Point")
    #     return False
    
    # for iFinger in range(len(NewTaskData["rawTouchTracks"])):
    #     #print(iFinger)
    #     #print("Fingers Len",(len(TaskData["rawTouchTracks"])))
    #     #print("TouchPoint",(touchpointnum))
    #     #print("Point Size",(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])))
    #     if(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])>0):
    #         if NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]>TapMaximumDuration:
    #             #print("Tapping too long")
    #             return False
    #第幾個手指要再判定
#    for iFinger in range(FingerNum):
#        if (abs(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0] - TaskData[iTrial]["targetFrame"][0][0] - TaskData[iTrial]["targetFrame"][1][0]*0.5) > TaskData[iTrial]["targetFrame"][1][0]*0.5)|(abs(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] - TaskData[iTrial]["targetFrame"][0][1] - TaskData[iTrial]["targetFrame"][1][1]*0.5) > TaskData[iTrial]["targetFrame"][1][1]*0.5):
#               #//cout << "First touch point is not correct" << endl;
#            print("First Touch")
#            return False
    iFinger=0
    
    if (abs(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0] - NewTaskData["targetFrame"][0][0] - NewTaskData["targetFrame"][1][0]*0.5) > NewTaskData["targetFrame"][1][0]*0.5)|(abs(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] - NewTaskData["targetFrame"][0][1] - NewTaskData["targetFrame"][1][1]*0.5) > NewTaskData["targetFrame"][1][1]*0.5):
        #//cout << "First touch point is not correct" << endl;
        
        #print((NewTaskData["targetFrame"][0][0]),(NewTaskData["targetFrame"][0][1]),(NewTaskData["targetFrame"][1][0]),(NewTaskData["targetFrame"][1][1]),NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0],NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] )
        #print("First Touch")
        return False
    isInAllowableMovement=True;
    for touchPointIndex in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
        
        dx=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][0] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0];
        dy=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][1] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1];
        
        dxx=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][0]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["previousLocation"][0]
        dyy=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][1]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["previousLocation"][1]
        
        v=0
        if touchPointIndex >0:
            dt=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex-1]["timestamp"]
            v=np.sqrt(dxx*dxx+dyy*dyy)/dt


        # if v>300:
        #     return False
        if dx*dx+dy*dy >= TapAllowableMovement*TapAllowableMovement:
            return False;
            
    # if isInAllowableMovement==False:
    #     #print("Moving")
    #     return False
    
    EachFingerBeganTime=list()
    EachFingerEndedTime=list()
    AllFingerBeganEndTime=list()
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        if len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])==1:
            EachFingerBeganTime.append(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"])
            EachFingerEndedTime.append(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"])
            AllFingerBeganEndTime.append(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"])
            AllFingerBeganEndTime.append(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"])
        else:
            EachFingerBeganTime.append(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"])
            EachFingerEndedTime.append(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][-1]["timestamp"])


            AllFingerBeganEndTime.append(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"])
            AllFingerBeganEndTime.append(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][-1]["timestamp"])
    

    
    #print("test",FingerEndTime)
    SortedAllTimeStamp=sorted(list(set(AllFingerBeganEndTime)))

    # if len(EachFingerBeganTime)%2==0:   #偶數的finger數
    if True==True:
        # print("======")
        # print(SortedAllTimeStamp)
        Fingerlist=list()
        CanTriggerTap=list()

        hint=list()
        FingeronScreen=0
        PossibleList=list(range(len(EachFingerBeganTime)))
        for t in SortedAllTimeStamp:

            Beganindex=np.where(t==np.array(EachFingerBeganTime))[0]
            Endindex=np.where(t==np.array(EachFingerEndedTime))[0]

            #print(t,Beganindex,Endindex,EachFingerBeganTime,EachFingerEndedTime)
            if len(Beganindex)>0:
                for begini in range(len(Beganindex)):

                    FingeronScreen=FingeronScreen+1
                    CanTriggerTap.append(Beganindex)
                    Fingerlist.append(Beganindex[begini])
            if len(Endindex)>0:
                
                FingeronScreen=FingeronScreen-1
                if FingeronScreen==1:
                    for endi in range(len(Endindex)):
                        PossibleList.remove(Endindex[endi])
                        try :
                            PossibleList.remove(Fingerlist[0])
                        except:
                            pass
                    
                # elif FingeronScreen==0:
                #     return True

                #print(Endindex,"in",Fingerlist)
                for endi in range(len(Endindex)):
                    #Fingerlist.remove(Endindex)
                    Fingerlist=list(filter((Endindex[endi]).__ne__,Fingerlist))
                    #Fingerlist=list(filter(lambda a:a != Endindex,Fingerlist))
        #print(len(PossibleList))
        if len(PossibleList)>0:
            return True
        else:
            return False



           

           





    return True
    





def TapTask_SuccessVerify(NewTaskData):
    
    #TapMaximumDuration=100;
    #TapAllowableMovement=15;
    FingerNum=len(NewTaskData["rawTouchTracks"]);
    if(FingerNum<1):
        print("False: No Finger")
        return False
    noTouchPoint=True
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        touchpointnum=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"]);    
        if touchpointnum>0:
            noTouchPoint=False

    if noTouchPoint==True:
        print("False:No Touch Point")
        return False
    
    # for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        
    #第幾個手指要再判定
#    for iFinger in range(FingerNum):
#        if (abs(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0] - TaskData[iTrial]["targetFrame"][0][0] - TaskData[iTrial]["targetFrame"][1][0]*0.5) > TaskData[iTrial]["targetFrame"][1][0]*0.5)|(abs(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] - TaskData[iTrial]["targetFrame"][0][1] - TaskData[iTrial]["targetFrame"][1][1]*0.5) > TaskData[iTrial]["targetFrame"][1][1]*0.5):
#               #//cout << "First touch point is not correct" << endl;
#            print("First Touch")
#            return False
    iFinger=0
    
    if (abs(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0] - NewTaskData["targetFrame"][0][0] - NewTaskData["targetFrame"][1][0]*0.5) > NewTaskData["targetFrame"][1][0]*0.5)|(abs(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] - NewTaskData["targetFrame"][0][1] - NewTaskData["targetFrame"][1][1]*0.5) > NewTaskData["targetFrame"][1][1]*0.5):
                # cout << "First touch point is not correct" << endl;
        
        #print((NewTaskData["targetFrame"][0][0]),(NewTaskData["targetFrame"][0][1]),(NewTaskData["targetFrame"][1][0]),(NewTaskData["targetFrame"][1][1]),NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0],NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] )
        print("False: wrong Position")
        return False
    
    
    return True



def TapTaskOneTrial(NewTaskData):
    
    #TapMaximumDuration=100;
    #TapAllowableMovement=15;
    FingerNum=len(NewTaskData["rawTouchTracks"]);
    if(FingerNum<1):
        #print("No Finger")
        return False
    noTouchPoint=True
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        touchpointnum=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"]);    
        if touchpointnum>0:
            noTouchPoint=False

    if noTouchPoint==True:
        #print("No Touch Point")
        return False
    
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        #print(iFinger)
        #print("Fingers Len",(len(TaskData["rawTouchTracks"])))
        #print("TouchPoint",(touchpointnum))
        #print("Point Size",(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])))
        if(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])>0):
            if NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]>TapMaximumDuration:
                #print("Tapping too long")
                return False
    #第幾個手指要再判定
#    for iFinger in range(FingerNum):
#        if (abs(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0] - TaskData[iTrial]["targetFrame"][0][0] - TaskData[iTrial]["targetFrame"][1][0]*0.5) > TaskData[iTrial]["targetFrame"][1][0]*0.5)|(abs(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] - TaskData[iTrial]["targetFrame"][0][1] - TaskData[iTrial]["targetFrame"][1][1]*0.5) > TaskData[iTrial]["targetFrame"][1][1]*0.5):
#               #//cout << "First touch point is not correct" << endl;
#            print("First Touch")
#            return False
    iFinger=0
    
    if (abs(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0] - NewTaskData["targetFrame"][0][0] - NewTaskData["targetFrame"][1][0]*0.5) > NewTaskData["targetFrame"][1][0]*0.5)|(abs(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] - NewTaskData["targetFrame"][0][1] - NewTaskData["targetFrame"][1][1]*0.5) > NewTaskData["targetFrame"][1][1]*0.5):
                #//cout << "First touch point is not correct" << endl;
        
        #print((NewTaskData["targetFrame"][0][0]),(NewTaskData["targetFrame"][0][1]),(NewTaskData["targetFrame"][1][0]),(NewTaskData["targetFrame"][1][1]),NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0],NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] )
        #print("First Touch")
        return False
    isInAllowableMovement=True;
    for touchPointIndex in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
        
        dx=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][0] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0];
        dy=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][1] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1];
        
        
        if dx*dx+dy*dy >= TapAllowableMovement*TapAllowableMovement:
            
            isInAllowableMovement = False;
            break;
    if isInAllowableMovement==False:
        #print("Moving")
        return False
    
    return True


def TapTask(NewTaskData,iTrial):
    
    #TapMaximumDuration=100;
    #TapAllowableMovement=15;
    FingerNum=len(NewTaskData["rawTouchTracks"]);
    if(FingerNum<1):
        #print("No Finger")
        return False
    noTouchPoint=True
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        touchpointnum=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"]);    
        if touchpointnum>0:
            noTouchPoint=False

    if noTouchPoint==True:
        #print("No Touch Point")
        return False
    
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        #print(iFinger)
        #print("Fingers Len",(len(TaskData["rawTouchTracks"])))
        #print("TouchPoint",(touchpointnum))
        #print("Point Size",(len(TaskData["rawTouchTracks"][iFinger]["rawTouches"])))
        if(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])>0):
            if NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])-1]["timestamp"]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["timestamp"]>TapMaximumDuration:
                #print("Tapping too long")
                return False
    #第幾個手指要再判定
#    for iFinger in range(FingerNum):
#        if (abs(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0] - TaskData[iTrial]["targetFrame"][0][0] - TaskData[iTrial]["targetFrame"][1][0]*0.5) > TaskData[iTrial]["targetFrame"][1][0]*0.5)|(abs(TaskData[iTrial]["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] - TaskData[iTrial]["targetFrame"][0][1] - TaskData[iTrial]["targetFrame"][1][1]*0.5) > TaskData[iTrial]["targetFrame"][1][1]*0.5):
#				#//cout << "First touch point is not correct" << endl;
#            print("First Touch")
#            return False
    iFinger=0
    
    if (abs(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0] - NewTaskData["targetFrame"][0][0] - NewTaskData["targetFrame"][1][0]*0.5) > NewTaskData["targetFrame"][1][0]*0.5)|(abs(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] - NewTaskData["targetFrame"][0][1] - NewTaskData["targetFrame"][1][1]*0.5) > NewTaskData["targetFrame"][1][1]*0.5):
				#//cout << "First touch point is not correct" << endl;
        
        #print((NewTaskData["targetFrame"][0][0]),(NewTaskData["targetFrame"][0][1]),(NewTaskData["targetFrame"][1][0]),(NewTaskData["targetFrame"][1][1]),NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0],NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1] )
        #print("First Touch")
        return False
    isInAllowableMovement=True;
    for touchPointIndex in range(len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"])):
        
        dx=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][0] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0];
        dy=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][touchPointIndex]["location"][1] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1];
        
        
        if dx*dx+dy*dy >= TapAllowableMovement*TapAllowableMovement:
            
            isInAllowableMovement = False;
            break;
    if isInAllowableMovement==False:
        #print("Moving")
        return False
    
    return True
    

def SwipeTask(NewTaskData,iTrial):
    import numpy as np
    TargetDirection=NewTaskData['targetDirection']
    recognizedDirection=NewTaskData['recognizedDirection']
    FingerNum=len(NewTaskData["rawTouchTracks"]);
    if(FingerNum<1):
        print("No Finger")
        return False
    noTouchPoint=True
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        touchpointnum=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"]);    
        if touchpointnum>0:
            noTouchPoint=False

    if noTouchPoint==True:
        print("No Touch Point")
        return False
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
                #print(v,"vs ",SwipeMinimumVelocity,abs(v) >= SwipeMinimumVelocity)
                if (abs(v) >= SwipeMinimumVelocity):
                    #print("dx",dx,"dy",dy)
                    if (abs(dy) >= abs(dx)):
                        if dy>0:
                            #print("Down")
                            Recognized=True
                            finalRecognizedDirection = "down"
                        else:
                            #print("Up")
                            Recognized=True
                            finalRecognizedDirection = "up"		
                    else:
                        if dx>0:
                            Recognized=True
                            finalRecognizedDirection = "right"
                        else:
                            Recognized=True
                            finalRecognizedDirection = "left"
    if WhichFingerCanSwipe.all() ==False:
        print("Less than SwipeMinimumMovement") 
    else:
        if finalRecognizedDirection == "none":
            print("too slow")
                     
    print("Target:",TargetDirection,"iOS:",recognizedDirection,"My:",finalRecognizedDirection)
    if finalRecognizedDirection ==TargetDirection:
        return True
    else:
        return False
    

def PanTask(NewTaskData,iTrial,ScreenSize,direction):
    import numpy as np
    InitialTarget=NewTaskData['initialPosition'][direction]
    
    
    FingerNum=len(NewTaskData["rawTouchTracks"]);
    if(FingerNum<1):
        #print("No Finger")
        return 1
    noTouchPoint=True
    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
        touchpointnum=len(NewTaskData["rawTouchTracks"][iFinger]["rawTouches"]);    
        if touchpointnum>0:
            noTouchPoint=False
    
    if noTouchPoint==True:
        #print("No Touch Point")
        return 1
    
    EachTrialUniquetimeStamp=list()
    for iTrack in range(len(NewTaskData['rawTouchTracks'])):
        for iPoint in range(len(NewTaskData['rawTouchTracks'][iTrack]['rawTouches'])):
            EachTrialUniquetimeStamp.append(NewTaskData['rawTouchTracks'][iTrack]['rawTouches'][iPoint]['timestamp'])
    EachTrialUniquetimeStamp=list(set(EachTrialUniquetimeStamp))
    
    movement=0
    for Timestamp in EachTrialUniquetimeStamp:
        Largest_dx_inAllFinger=0
        Largest_dy_inAllFinger=0
        ThisFinger_dx=0
        ThisFinger_dy=0
        for iFinger in range(len(NewTaskData["rawTouchTracks"])):
            for iPoint in range(len(NewTaskData['rawTouchTracks'][iFinger]['rawTouches'])):
                if NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["timestamp"]==Timestamp:
                    ThisFinger_dx=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][0]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"][0]
                    ThisFinger_dy=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["location"][1]-NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][iPoint]["previousLocation"][1]
                    break
            if abs(Largest_dx_inAllFinger)<abs(ThisFinger_dx):
                Largest_dx_inAllFinger=ThisFinger_dx
            if abs(Largest_dy_inAllFinger)<abs(ThisFinger_dy):
                Largest_dy_inAllFinger=ThisFinger_dy
        if direction==0:
            movement=movement+Largest_dx_inAllFinger
        else:
            movement=movement+Largest_dy_inAllFinger
                
#    movement=0
#    preFingerStart=NewTaskData["rawTouchTracks"][0]["rawTouches"][0]["timestamp"]
#    preFingerEnd=NewTaskData["rawTouchTracks"][0]["rawTouches"][0]["timestamp"]
#    for iFinger in range(len(NewTaskData["rawTouchTracks"])):
#        
#        dx=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][-1]["location"][0] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][0];
#        dy=NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][-1]["location"][1] - NewTaskData["rawTouchTracks"][iFinger]["rawTouches"][0]["location"][1];
#        #print("dx",dx)
#        if direction==0:
#            if abs(movement)<abs(dx):
#                movement=dx
#        else:
#            if abs(movement)<abs(dy):
#                movement=dy
#                


    performance=abs(ScreenSize[direction]/2-(InitialTarget+movement))
    #performance=abs(ScreenSize[direction]/2-(InitialTarget+movement))/ScreenSize[direction]
    #print(InitialTarget,"to",InitialTarget+movement,"Target",ScreenSize[direction]/2,"performance:",performance)
    return performance      










# 3003/2019-03-13_07-40-40  
##3001/2019-03-06_05-51-18
#with open('StudyData/NewData/3001/2019-03-06_05-51-18.json') as json_file: 
#    import json
#    data = json.load(json_file)
#    
#    #Task='horizontalScrollTask'
#    Task='swipeTask'
#    TaskData=data[Task]['trials']
#    for i in range(len(TaskData)):
#        trial=i
#        SwipeTask(TaskData[trial],trial)
#        #PanTask(TaskData[trial],trial,data['deviceInfo']['screenSize'],0)
#        