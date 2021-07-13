"""
schedule.py holds the combined code for creating schedule.
Given a saved HTML file, the steps it takes are:
	(1) Scrape the HTML file(e.g. Beautiful Soup) 
		Create a list of Course Objects (see course.py) 
	(2) Get user requests for schedule creation
	(3) Print the schedules and store them into ./result directory
	(4) Create schedule images.

"""
from htmlParser import parseHTML 
from htmlParser import parseJSON 
from itertools import product
from collections import defaultdict#NOTE: remember right now code is not super clean
from util import ComplexEncoder

import json #NOTE: check the circularity of this, already imported in util
import os
import sys
import argparse
#import errno
from shutil import rmtree 

def makeCatalog(courseDict):
	catalog = defaultdict(list)
	for (k,v) in courseDict.items():
		catalog[v.getSemester()].append(v.getCourseID())

	# Sort it to maintain Uniformity
	for k in catalog:
		catalog[k].sort()

	return catalog


# Outputs the catalog nicely onto console
def printCatalog(catalog):
	print("\nCursos en su horario 2021-1: \n")

	counter = 0
	for c in catalog:
		ciclo = str(c) if c > 0 else "Electivo"  
		ciclo = "\t\t\t--- Ciclo " + ciclo + " --- "
		print(ciclo)

		#NOTE: not sorted yet
		for co in catalog[c]:
			space = "" if counter >= 10 else " "
			print("\t" + str(counter) + space + "  => " + co)
			counter += 1
		print()

def getRequestList(catalog):
	print("\n\nIngresa los digitos de los cursos que quieres: ")
	numbers = list(filter(None, input().split(" ")))
	numbers = list(map(int, numbers))

	allCourses = []
	for (k, v) in catalog.items():
		for e in v:
			allCourses.append(e)

	print("\nEscogistes: ")
	print("----------------")

	reqCourses = []
	for n in numbers:
		print(str(n) + ":" + allCourses[n])
		reqCourses.append(allCourses[n])	

	return reqCourses


def findAllSchedComb(requestList, courseDict):
	results = []
	#Create a list of (cid, sid, labid) for each course
	#TODO: maybe make a courseMap so that only numbers are stored not the entire cid  
	cids = [cn for cn in requestList]	

	# List for closed section in the request courses
	closed = []
	cOpen = []
                                                                                   
	for cid in cids:
		courseCombinations = []
		sections = courseDict[cid].sections
		for sid in sections:
			section = sections[sid]	
			# Course may not have Lab
			#NOTE: being modified
			if not section.labs: 
				courseCombinations.append((cid, sid, None))
			for labid in section.labs:
				courseCombinations.append((cid, sid, labid))	
		results.append(courseCombinations)

	#print("\n\n$$$$$$$$$$$$$$$$$$$$  Cerradas $$$$$$$$$$$$$$$$$$$$$")
	closed.sort()
	for p in closed:
		print(p)

	#print("\n\n$$$$$$$$$$$$$$$$$$$$  Abiertas $$$$$$$$$$$$$$$$$$$$$")
	cOpen.sort()
	for p in cOpen:
		print(p)
                                        
	# itertools.product	
	all_combinations = list(product(*results))
	return all_combinations


def getTimeIntervals(courseDict, sched):
	timeIntervals = []
	for period in sched:
		course = courseDict[period[0]]
		section = course.sections[period[1]]
		for to in section.theoryTimes:
			ti = to._timeInterval
			timeIntervals.append(ti)

		labs = section.labs[period[2]]
		for lab in labs:
			ti = lab._timeInterval
			timeIntervals.append(ti)

	return timeIntervals



# SCHEDTI is a list of intervals sorted by the first index 
def tiIntersects(schedTI):
	intersects = False
	for i in range(1, len(schedTI)):
		prev = schedTI[i-1]
		cur = schedTI[i]
		if cur[0] < prev[1]:
			intersects = True	
			break
	return intersects	


"""
TEMP
"""
def startsBefore(schedTI, hour):
	for ti in schedTI:
		startHour = ti[0] % 288
		if startHour < (hour * 12):
			return True
	return False


def endsAfter(schedTI, hour):
	for ti in schedTI:
		endHour = ti[1] % 288
		if endHour > (hour * 12):
			return True
	return False


def tempHasBadDay(schedTI):
	#for ti in schedTI:
		#Monday
	#	if ti[0] < 288:
	#		return True 
		##TUE
		#if ti[0] > 288 and ti[0] < 576:
		#	return True 
		##WED
		#if ti[0] > 576 and ti[0] < 864:
		#	return True 
		##THU
		#if ti[0] > 864 and ti[0] < 1152:
		#	return True 
		#FRI
		#if ti[0] > 1152 and ti[0] < 1440:
		#	return True 
		#SAT
		#if ti[0] >1440 and ti[0] < 1728:
			#return True 

	return False


dayIndexSet = {0, 1, 2, 3, 4, 5}		
def findDaysWithout(schedTI):
	days = set()
	for ti in schedTI:
		dayIndex = int(ti[0]/288)
		days.add(dayIndex)

	daysWithout = []
	for d in dayIndexSet: 
		if d not in days:
			daysWithout.append(DAYS[d])	

	return " ".join(daysWithout) 



def printDaysWithoutDict(missingDaysDict):
	tracker = defaultdict(int)

	for dw in missingDaysDict:
		ndays = len(DAYS) - int(len(dw)/3) 
		tracker[ndays] += len(missingDaysDict[dw])

	#print("\nHorarios posibles con 'n' dias de clase:")
	#resList = []
	#for d in range(6, -1, -1):
	#	res = "\t" + str(d) + " dias: "
	#	if d not in tracker:
	#		res += "0"
	#	else:
	#		res += str(tracker[d]) 
	#	print(res)

	#print("\n# Horarios sin dia:")
	#for d in missingDaysDict:
	#	print("\t%s\t: %s"%(d, missingDaysDict[d]))

	#print("\n# Horarios con dias de semana:\n")

	print("\nEscoge cual horarios ver: \n")
	counter = 0
	for k, v in sorted(missingDaysDict.items(), key=lambda x: x[0]):
		dayList = k.split()
		#TODO: print out day if in dayList else leave a space
		weekStr = "\t" + str(counter) + ")\t"
		for day in DAYS:
			if day not in dayList:
				weekStr += day
			else:
				weekStr += "---"
			weekStr += "|"
		weekStr += "    ->\t" + str(len(v)) + "\n"
		counter += 1
		print(weekStr)

# This function is where user requests for specific 
def passFilter(sched):
	avoid = {
				
			}
	requested = {
			"Medicina Legal": ["10C1"],
			"Psiquiatría Clínica": ["8D1"],
			"Medicina I": ["6B1"], 
			"Anatomía Patológica II": ["6B3"],
			"Imagenología Médica": ["6A1"],
			"Diagnóstico por Laboratorio": ["7C1"]
			}

	#NOTE, if the requested doesn't have a lab, this doesn't work
	for sec in sched:
		(cid, sid, labid) = sec
		if cid in requested and labid not in requested[cid]:
			return False
		if cid in avoid and labid in avoid[cid]:
			return False	
	return True	
 

def findViableSchedules(requestList, courseDict):
	viable = []

	#NOTE: can make the removal of unwanted or closed courses here or below
	#		after checking for tiIntersects 
	possible = findAllSchedComb(requestList, courseDict)
	
	goodCounter = 0
	badCounter = 0		


	# Creates a count for number of possible schedules w/ certain days 
	# 3/16 Now adding the actual schedules too
	missingDaysDict = defaultdict(list)
	
	#TODO: make this an item too instead of a tuple?	
	for sched in possible:
	
		# TODO NOTE: putting filter here for the moment	
		if not passFilter(sched):
			continue

		#print("sched")	
		#print(sched)				
			
		schedTI = getTimeIntervals(courseDict, sched) 
		schedTI.sort(key=lambda tup:tup[0])

		# If the schedule is viable	
		if not tiIntersects(schedTI):
			# TODO: make it multiply iteratable probably by saving this result
			# 	or see the note above 
			daysWithout = findDaysWithout(schedTI)
			missingDaysDict[daysWithout].append(sched)	

			# Here is where the filter for days is done. 
			#if not tempHasBadDay(schedTI):
			goodCounter += 1
			viable.append(sched)
			#else:
			#	badCounter += 1
		else:
			#print(schedTI)
			badCounter += 1


	#printDaysWithoutDict(missingDaysDict)	
	#NOTE: might add conditionallyViable along with viable to tuple result
	return (goodCounter, badCounter, viable, missingDaysDict)	


def getFileSched(day, startTime, endTime):
	resStr = ""
	resStr += str(DAYS.index(day) + 1) + "\t"
	resStr += startTime[:2] + "\t"
	resStr += startTime[3:] + "\t"           	
	resStr += endTime[:2] + "\t"
	resStr += endTime[3:] + "\t"
	return resStr


#TODO: packge this DAYS somewhere 
#DAYS = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB"]	
#NOTE: This is for 2021-2 version
DAYS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sábado"]

# Print human readable schedule
def getSchedString(courseDict, coursetuple, course_counter):
	#print(coursetuple)
	(cid, sid, labid) = coursetuple

	# Section might not have labtimes or even theotimes thus no sid
	if not labid:
		labid = ""
	if not sid:
		sid = "" #TODO prob regex is better
	
	print("\tCurso " + str(course_counter) + ".\t------------- " +
		cid + " [" + sid +
		"|" + labid + "]")	
	sections = courseDict[cid].sections
	section = sections[sid]	
	theoryTimes = []
	for tt in section.theoryTimes:
		theoryTimes.append(tt)

	labTimes = []
	labs = section.labs[labid]
	for lto in labs:
		labTimes.append(lto)

	resStr = ""	
	for to in theoryTimes:
		(day, startTime, endTime) = to.dateTuple 
		print("\t\tTEO\t%s %s - %s"%(day, startTime, endTime))
		resStr += getFileSched(day, startTime, endTime) 
		courseStr = cid + "\t" + sid + "\t(TEO)"
		resStr += courseStr.replace(" ", "") + "\n"
				
	
	#NOTE: somehow combine this an the thing above 
	for lt in labTimes:
		(day, startTime, endTime) = lt.dateTuple 
		print("\t\tPRA\t%s %s - %s"%(day, startTime, endTime))
		resStr += getFileSched(day, startTime, endTime) 
		courseStr = cid + "\t" + labid + "\t(PRA)"
		resStr += courseStr.replace(" ", "") + "\n"

	return resStr 



def printSchedules(courseDict, resultTuple):
	(goodCounter, badCounter, viable, missingDaysDict) = resultTuple
	total = goodCounter + badCounter
	print("\n\n\nBuscando combinaciones viables entre " + str(total) + " posibilidades...........")
	print ("\tHorarios viables: " + str(goodCounter))
	print("\tHorarios NO viables: " + str(badCounter))
	print()	
	printDaysWithoutDict(missingDaysDict)

	#NOTE: temporary put into while loop	
	while(True):	
		#NOTE: package better later
		dayChoice = int(input()) # Ask for specific schedules
		# Create the directory
		dname = "results"
		if os.path.exists(dname):
			rmtree(dname) #shutil.rmtree
		os.makedirs(dname)
		
		MAXTOPRINT = 400
		counter = 1
		
		#TODO: revise everything after this, I have just copied 
		
		keys = missingDaysDict.keys()
		keys = sorted(keys)
		newViable = missingDaysDict[keys[dayChoice]]

		for v in newViable: 
		#for v in viable:
			if counter > MAXTOPRINT: break
			
			print("\n\nHorario Final: " + str(counter) + "/" + str(goodCounter))
			course_counter = 1
			
			# Open a file
			f_name = dname + "/horario" + str(counter) + "de" + str(goodCounter)
			f = open(f_name, "w+")
			data_string = ""
			for coursetuple in v:
				data_string += getSchedString(courseDict, coursetuple, course_counter)
				course_counter += 1
				f.write(data_string)
			f.close()
			
			counter += 1
	#		print("\n")
		print("\n")

		#NOTE: fix later, saying confusing stuff
		# Write ellipsis if there are more courses
		#if counter < goodCounter:
		#	print("\t\t\t\t\t--------- %s horarios mas -----------\n\n\n\n\n"%
		#		(str(goodCounter-counter + 1)))


# This function transforms the final Course Dictionary into JSON
def turnToJSON(courseDict, jsonFile):
	#dname = constants.JSON_DIRECTORY 	
	dname = "JSON"
	#Open file
	with open(dname + "/" + jsonFile, 'w', encoding='utf8') as json_file:
		json.dump(courseDict, 
						json_file,
						cls=ComplexEncoder, 
						ensure_ascii=False, 
						sort_keys=True,
						indent=4)


# Reads Command line Arguments and creates the Course Dictionary from them
def createCourseDict():
	parser = argparse.ArgumentParser(description="Find the schedules")
	parser.add_argument('-H', '--htmlFile', type=str, help="Name of HTML schedule File")
	parser.add_argument('-J', '--jsonFile', type=str, help="Name of JSON schedule File",
											required=True)	
	args = parser.parse_args()

	courseDict = None	
	if args.htmlFile:
		htmlFile = os.getcwd() + "/" + args.htmlFile
		jsonFile = os.getcwd() + "/JSON/" + args.jsonFile
		cDictH = parseHTML(htmlFile)
		cDictJ = {}
		if os.path.isfile(jsonFile):	
			cDictJ = parseJSON(jsonFile) 
		cDictH.update(cDictJ) 
		courseDict = cDictH	
	else: 	
		jsonFile = os.getcwd() + "/JSON/" + args.jsonFile
		courseDict = parseJSON(jsonFile)
	
	""" Save the courseDict to JSON """  
	turnToJSON(courseDict, args.jsonFile)	
	return courseDict



def main():	

	""" (1). Scrape, return a dict of courses (also updates the JSON) """
	courseDict = createCourseDict()		
	#_printCourseDict(courseDict)
	
	""" (2). Print catalogue & get User requests """
	catalog = makeCatalog(courseDict)
	printCatalog(catalog)
	requestList = getRequestList(catalog)

	""" (2b). Implement user constraints on schedule """
	#TODO: eventually, rn just hack something otgether just like last time
	#NOTE(3/6/20): look at the TODO after step 3 below, that seems like
	# 			a better place to put the constraints.  

	""" (3). Get the viable schedules """
	resultTuple = findViableSchedules(requestList, courseDict)

	""" (3b). Implement user constraints on Viable Schedules """
	#TODO: constraints can be here instead
	# Benefits: can do a while loop for user constraints & printing Schedules
	#						& don't have to redo calculation for further requests (closed/baddays)
	# Negatives: Will need more calculation up front 
	# Final: This proably makes sence 

	""" (4). Printing top (n) schedules + Store into File """
	printSchedules(courseDict, resultTuple)	


# helper function for debugging"
def _printCourseDict(cl):
	for c in cl:
		print(cl[c])

if __name__ == '__main__':
	main()
