#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import json

from TouchAccommodations import TouchAccommodations
import MyTouchTask


if __name__ == "__main__":

	touchAccommodations = TouchAccommodations()

	filename = sys.argv[1]

	with open(filename, 'r') as jsonFile:
		dataStr = jsonFile.read()
	#print dataStr

	data = json.loads(dataStr)

	##### rawTouchData format #####
	#rawTouchData = [[[TOUCHPOINTS1, TOUCHPOINTS2, TOUCHPOINTS3], [TOUCHPOINTS1, TOUCHPOINTS2], TRACK3], [TRIAL2]]

	'''
	##### VERSION 1 #####
	## data["trials"][0]["tracks"][0]["touchPoints"][0]["timestamp"]
	rawTouchData = []
	for trial in data["trials"]:
		trialTmp = []
		for track in trial["tracks"]:
			trackTmp = []
			for touchPoint in track["touchPoints"]:
				trackTmp.append({"timestamp": touchPoint["timestamp"], "x": touchPoint["x"], "y": touchPoint["y"]})
			trialTmp.append(trackTmp)
		rawTouchData.append(trialTmp)
	#print(rawTouchData)

	OptimizeParameter(rawTouchData)
	'''

	##### VERSION 2 #####
	rawTouchData = []
	for taskName, taskData in data.items():
		if "tapTask" in taskName:
			rawTouchData = []
			for trial in taskData["trials"]:
				trialTmp = []
				for track in trial["rawTouchTracks"]:
					trackTmp = []
					for touchPoint in track["rawTouches"]:
						trackTmp.append(touchPoint)
						#trackTmp.append({"timestamp": touchPoint["timestamp"], "x": touchPoint["location"][0], "y": touchPoint["location"][1]}) 
						#print touchPoint
					trialTmp.append(trackTmp)
				rawTouchData.append(trialTmp)

			rawTouchDataMod = touchAccommodations.FindBestParameter(rawTouchData, "Task")
			#print rawTouchDataMod
			'''
			for trialIndex in range(len(rawTouchDataMod)):
				for trackIndex in range(len(rawTouchDataMod[trialIndex])):
					taskData["trials"][trialIndex]["rawTouchTracks"][trackIndex] = []
					for touchPoint in rawTouchDataMod[trialIndex][trackIndex]:
						taskData["trials"][trialIndex]["rawTouchTracks"][trackIndex].append(touchPoint)
			'''
			




	
				




