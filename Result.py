import numpy as np
import sys
from os import listdir
#from os.path import isfile,isdir,join
User=sys.argv[1]
#path='Result/Classify/TwoChannel/'+User+'/'
path='Result/Classify/OneChannel/007/'
files=listdir(path)
file=list()
for i in range(len(files)):
    
    file.append(files[i])



# for thisfile in file:
# 	filename=path+thisfile

# 	Accuracylist=list()
# 	with open (filename,'r') as f:
# 		for line in f:
# 			A=line.split(' ')
# 			#print(A[3])
# 			Accuracylist.append(float(A[3]))
# 	print(thisfile,np.mean(Accuracylist))
		


for thisfile in file:
	filename=path+thisfile

	Accuracylist=list()
	with open (filename,'r') as f:
		TapTotalCount=0
		TapSuccessCount=0
		SwipeTotalCount=0
		SwipeSuccessCount=0
		HScrollTotalCount=0
		HScrollSuccessCount=0
		VScrollTotalCount=0
		VScrollSuccessCount=0

		for line in f:
			A=line.split(' ')
			#print(A[173])
			for j in range(5):
				#223

				for i in range(40):
					#print(A[j*173+8+3*i],"/",A[j*173+10+3*i],A[j*173+8+3*i]==A[j*173+10+3*i])

					if int(A[j*173+10+3*i])==0:
						TapTotalCount=TapTotalCount+1
						if int(A[j*173+8+3*i])==0:
							TapSuccessCount=TapSuccessCount+1
						
					elif int(A[j*173+10+3*i])==1:
						SwipeTotalCount=SwipeTotalCount+1
						if int(A[j*173+8+3*i])==1:
							SwipeSuccessCount=SwipeSuccessCount+1

					elif int(A[j*173+10+3*i])==2:
						HScrollTotalCount=HScrollTotalCount+1
						if int(A[j*173+8+3*i])==2:
							HScrollSuccessCount=HScrollSuccessCount+1

					elif int(A[j*173+10+3*i])==3:
						VScrollTotalCount=VScrollTotalCount+1
						if int(A[j*173+8+3*i])==3:
							VScrollSuccessCount=VScrollSuccessCount+1





			# 	print(A[8+3*i])
			# 	print(A[9+3*i])
			# 	print(A[10+3*i])

			# print("A8",A[8])
			# print("A9",A[9])
			# print("A10",A[10])
			#print(A[3])
			#Accuracylist.append(float(A[3]))
			#print(filename,TapSuccessCount," / ",TapTotalCount,"=",float(float(TapSuccessCount)/float(TapTotalCount)),SwipeSuccessCount," / ",SwipeTotalCount,"=",float(float(SwipeSuccessCount)/float(SwipeTotalCount)))
			print(filename,"Tap",float(float(TapSuccessCount)/float(TapTotalCount)),"Swipe",float(float(SwipeSuccessCount)/float(SwipeTotalCount)),"HS",float(float(HScrollSuccessCount)/float(HScrollTotalCount)),"VS",float(float(VScrollSuccessCount)/float(VScrollTotalCount)))

	#print(thisfile,np.mean(Accuracylist))
		

