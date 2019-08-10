import MyTouchTask
import numpy as np
from enum import Enum

class HoldDuration(Enum):
	off = 0
	on = 1

class IgnoreRepeat(Enum):
	off = 0
	on = 1

class TapAssistance(Enum):
	off = 0
	init = 1
	final = 2

class TouchAccommodations():
	def __init__(self):
		pass
	def FindBestParameter(self, rawTouchData, Task):
		# Hold Duration
		# 0.10 - 4.00
		# delta = 0.05
		holdDurationType = [HoldDuration.off, HoldDuration.on]
		# Ignore Repeat
		# 0.10 - 4.00
		# delta = 0.05
		ignoreRepeatType = [IgnoreRepeat.off, IgnoreRepeat.on]
		# Tap assistance
		# 0.10 - 4.00
		# delta = 0.05
		tapAssistanceType = [TapAssistance.off, TapAssistance.init, TapAssistance.final]
		count = 0
		successRateMax = 0
		bestParameter = []
		for holdDuration in holdDurationType:
			for ignoreRepeat in ignoreRepeatType:
				for tapAssistance in tapAssistanceType:
					for holdDurationTimer in np.arange(0.10, 4.05, 0.05):
						for ignoreRepeatTimer in np.arange(0.10, 4.05, 0.05):
							for tapAssistanceTimer in np.arange(0.10, 4.05, 0.05):
								#########
								for trial in rawTouchData:
									trialMod = self.FilterOneTrial(trial, holdDuration, holdDurationTimer, ignoreRepeat, ignoreRepeatTimer, tapAssistance, tapAssistanceTimer)
									count = count + 1
									print count
									break
								successRate = MyTouchTask.TaskTesting(trialMod)
								#########
								if successRate > successRateMax:
									successRateMax = successRate
									bestParameter = [{"HoldDuration": holdDuration, "IgnoreRepeat": ignoreRepeat, "TapAssistance": tapAssistance, "HoldDurationTimer": holdDurationTimer, "IgnoreRepeatTimer": ignoreRepeatTimer, "TapAssistanceTimer": tapAssistanceTimer}]
								elif successRate == successRateMax:
									bestParameter.append({"HoldDuration": holdDuration, "IgnoreRepeat": ignoreRepeat, "TapAssistance": tapAssistance, "HoldDurationTimer": holdDurationTimer, "IgnoreRepeatTimer": ignoreRepeatTimer, "TapAssistanceTimer": tapAssistanceTimer})

								if tapAssistance == TapAssistance.off:
									break
							if ignoreRepeat == IgnoreRepeat.off:
								break
						if holdDuration == HoldDuration.off:
							break
		return bestParameter
	def FilterOneTrial(self, trial, holdDuration, holdDurationTimer, ignoreRepeat, ignoreRepeatTimer, tapAssistance, tapAssistanceTimer):
		trialMod = []
		for i in range(len(trial)):
			trialMod.append([])
		
		# There may be more than one track within a trial
		trackIndexArr = [0] * len(trial)
		trackEndedArr = [False] * len(trial)
		trackTouchedArr = [False] * len(trial)

		# Constant
		TapAssistanceFinalLocationThreshold = 42 #pt

		# Initialization
		isTouched = False
		timestampReferenceForHoldDuration = 0.0
		flagInitForTapAssistance = False
		timestampReferenceForTapAssistance = 0.0
		locationReferenceForInitTapAssistnace = [0, 0]
		locationReferenceForFinalTapAssistance = [0, 0]
		timestampReferenceForIgnoreRepeat = float("-inf")

		while False in trackEndedArr:
			timestampNext = float("inf")
			trackNext = -1
			for i in range(len(trial)):
				if not trackEndedArr[i] and trial[i][trackIndexArr[i]]["timestamp"] < timestampNext:
					timestampNext = trial[i][trackIndexArr[i]]["timestamp"]
					trackNext = i

			assert trackNext >= 0
			#print(trackNext)
			#print(trial[trackNext][trackIndexArr[trackNext]])
			touchPoint = trial[trackNext][trackIndexArr[trackNext]].copy()
			#print(trackNext, touchPoint["timestamp"], touchPoint["location"][0], touchPoint["location"][0])

			####### IMPORTANT ######
			## IGNORE REPEAT ##
			if ignoreRepeat == IgnoreRepeat.on:
				if touchPoint["timestamp"] < timestampReferenceForIgnoreRepeat + ignoreRepeatTimer:
					trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1
					if trackIndexArr[trackNext] >= len(trial[trackNext]):
						trackEndedArr[trackNext] = True
					continue

			## HOLD DURATION ##
			if not isTouched:
				isTouched = True
				timestampReferenceForHoldDuration = touchPoint["timestamp"]
				locationReferenceForInitTapAssistnace[0] = touchPoint["location"][0]
				locationReferenceForInitTapAssistnace[1] = touchPoint["location"][1]

			trackIndexArr[trackNext] = trackIndexArr[trackNext] + 1
			if trackIndexArr[trackNext] >= len(trial[trackNext]):
				trackEndedArr[trackNext] = True
				trackTouchedArr[trackNext] = False
			else:
				trackTouchedArr[trackNext] = True

			if holdDuration == HoldDuration.on:
				if touchPoint["timestamp"] < timestampReferenceForHoldDuration + holdDurationTimer:
					# DO NOTHING
					if not True in trackTouchedArr:
						isTouched = False
					continue

			## TAP ASSISTANCE ##
			if not flagInitForTapAssistance:
				flagInitForTapAssistance = True
				timestampReferenceForTapAssistance = touchPoint["timestamp"]
				locationReferenceForFinalTapAssistance[0] = touchPoint["location"][0]
				locationReferenceForFinalTapAssistance[1] = touchPoint["location"][1]
			
			if tapAssistance == TapAssistance.init:
				if touchPoint["timestamp"] < timestampReferenceForTapAssistance + tapAssistanceTimer:
					# It would send touch event if there is no touch
					if not True in trackTouchedArr:
						touchPoint["location"][0] = locationReferenceForInitTapAssistnace[0]
						touchPoint["location"][1] = locationReferenceForInitTapAssistnace[1]
						trialMod[trackNext].append(touchPoint)
				else:
					trialMod[trackNext].append(touchPoint)
			elif tapAssistance == TapAssistance.final:
				if touchPoint["timestamp"] < timestampReferenceForTapAssistance + tapAssistanceTimer:
					if ((locationReferenceForFinalTapAssistance[0]-touchPoint["location"][0])**2 + (locationReferenceForFinalTapAssistance[1]-touchPoint["location"][1])**2) >= TapAssistanceFinalLocationThreshold**2:
						timestampReferenceForTapAssistance = touchPoint["timestamp"]
						locationReferenceForFinalTapAssistance[0] = touchPoint["location"][0]
						locationReferenceForFinalTapAssistance[1] = touchPoint["location"][1]
					# It would send touch event if there is no touch
					if not True in trackTouchedArr:
						trialMod[trackNext].append(touchPoint)
				else:
					trialMod[trackNext].append(touchPoint)
			elif tapAssistance == TapAssistance.off:
				trialMod[trackNext].append(touchPoint)

			if not True in trackTouchedArr:
				isTouched = False
				flagInitForTapAssistance = False
				timestampReferenceForIgnoreRepeat = touchPoint["timestamp"]

			####### IMPORTANT ######

		### TODO:
		# Set the phase of touchPoint

		return trialMod