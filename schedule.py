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
from itertools import product

import os
from shutil import rmtree 

def makeCatalog(courseDict):
	courses = []
	for (k,v) in courseDict.items():
		courses.append(v.getCourseID())		

	courses.sort()
	catalog = list(enumerate(courses))
	return catalog


def printCatalog(catalog):
	print("Cursos en su horario 2020-2: \n")
	for c in catalog:
		print(c)


def getRequestList(catalog):
	print("\n\nIngresa los digitos de los cursos que quieres: ")
	numbers = list(filter(None, input().split(" ")))
	numbers = list(map(int, numbers))

	print("\n\nEscogistes: ")
	print("----------------")
	for n in numbers:
		print(str(catalog[n][0]) + ":" + catalog[n][1])

	return numbers


def findPossibleSchedules(requestList, catalog, courseDict):
	results = []
	#Create a list of (cid, sid, labid) for each course
	#TODO: maybe make a courseMap so that only numbers are stored not the entire cid  
	cids = [catalog[cn][1] for cn in requestList]
	                                                                                   
	for cid in cids:
		courseCombinations = []
		sections = courseDict[cid].getSections()	
		for sid in sections:
			section = sections[sid]	
			# Course may not have Lab
			if not section.getLabs(): 
				courseCombinations.append((cid, sid, None))
			for labid in section.getLabs():
				courseCombinations.append((cid, sid, labid))	
		results.append(courseCombinations)	
	                                                                                  	
	# itertools.product	
	all_combinations = list(product(*results))	
	return all_combinations


def getTimeIntervals(courseDict, sched):
	timeIntervals = []
	for period in sched:
		course = courseDict[period[0]]
		section = course.getSections()[period[1]]
		for to in section.theoryTimes:
			ti = to.getTimeInterval()
			timeIntervals.append(ti)

		labs = section.getLabs()[period[2]]
		for lab in labs:
			ti = lab.getTimeInterval()
			timeIntervals.append(ti)

	return timeIntervals



# SCHEDTI is a list of intervals sorted by the first index 
def tiIntersects(schedTI):
	intersects = False
	for i in range(1, len(schedTI)):
		prev = schedTI[i-1]
		cur = schedTI[i]
		if cur[0] < prev[1]:
			return True
	return intersects	




def findViableSchedules(requestList, catalog, courseDict):
	viable = []
	possible = findPossibleSchedules(requestList, catalog, courseDict)
	
	#TODO: possibly don't need these
	possibleCounter = len(possible)
	goodCounter = 0
	badCounter = 0		
	
	#TODO: make this an item too instead of a tubple?	
	for sched in possible:
		schedTI = getTimeIntervals(courseDict, sched) 
		schedTI.sort(key=lambda tup:tup[0])	
		if not tiIntersects(schedTI):
			goodCounter += 1
			viable.append(sched)
		else:
			badCounter += 1


	#TODO: remove
	print("\n\nPossible: %s \t Good: %s \t Bad: %s\n"%(possibleCounter, goodCounter, badCounter))
	return (goodCounter, badCounter, viable)	


def getFileSched(day, startTime, endTime):
	resStr = ""
	resStr += str(DAYS.index(day) + 1) + "\t"
	resStr += startTime[:2] + "\t"
	resStr += startTime[3:] + "\t"           	
	resStr += endTime[:2] + "\t"
	resStr += endTime[3:] + "\t"
	return resStr

#TODO: packge this DAYS somewhere 
DAYS = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB"]	
# Print human readable schedule
def getSchedString(courseDict, coursetuple, course_counter):
	(cid, sid, labid) = coursetuple
	
	print("\tCurso " + str(course_counter) + ".\t------------- " +
		cid + " [" + sid +
		"|" + labid + "] -------------")
	
	sections = courseDict[cid].getSections()	
	section = sections[sid]	
	theoryTimes = []
	for tt in section.theoryTimes:
		theoryTimes.append(tt)

	labTimes = []
	labs = section.getLabs()[labid]
	for lto in labs:
		labTimes.append(lto)

	resStr = ""	
	for to in theoryTimes:
		(day, startTime, endTime) = to.dateTuple 
		print("\t\tTEO\t%s %s - %s"%(day, startTime, endTime))
		resStr += getFileSched(day, startTime, endTime) 
		courseStr = cid + sid + labid
		resStr += courseStr.replace(" ", "") + "\n"
				
	
	#NOTE: somehow combine this an the thing above 
	for lt in labTimes:
		(day, startTime, endTime) = lt.dateTuple 
		print("\t\tPRA\t%s %s - %s"%(day, startTime, endTime))
		resStr += getFileSched(day, startTime, endTime) 
		courseStr = cid + sid + labid
		resStr += courseStr.replace(" ", "") + "\n"

	return resStr 



def printSchedules(courseDict, resultTuple):
	(goodCounter, badCounter, viable) = resultTuple
	total = goodCounter + badCounter
	print("\n\nBuscando combinaciones viables entre " + str(total) + " posibilidades...........")
	#print("Condiciones: No clase [\'Martes\', \'Sabado\']")
	print ("\nHorarios viables: " + str(goodCounter))
	print("Horarios NO viables: " + str(badCounter))
	
	# Create the directory
	dname = "results"
	if os.path.exists(dname):
		rmtree(dname) #shutil.rmtree
	os.makedirs(dname)
	
	MAXTOPRINT = 10
	counter = 1
	
	#TODO: revise everything after this, I have just copied 
	for v in viable:
		if counter >= MAXTOPRINT: break
		
		print("\n\nHorario Final: " + str(counter) + "/" + str(goodCounter))
		course_counter = 1
		
		# Open a file
		f_name = dname + "/schedule" + str(counter) + "of" + str(goodCounter)
		f = open(f_name, "w+")
		data_string = ""
		for coursetuple in v:
			data_string += getSchedString(courseDict, coursetuple, course_counter)
			course_counter += 1
			f.write(data_string)
		f.close()
		
		counter += 1
		print("\n")
	print("\n")
		

	

def main():
	#htmlFile = '/mnt/c/Users/framo/OneDrive/Desktop/Control de eventos UCSUR.html'
	htmlFile = '/mnt/c/Users/framo/OneDrive/Desktop/Alumno.html'

	""" (1). Scrape, return a list of courses """
	courseDict = parseHTML(htmlFile)
	
	""" (2). Print catalogue & get User requests """
	catalog = makeCatalog(courseDict)
	printCatalog(catalog)
	requestList = getRequestList(catalog)
	#_printCourseDict(courseDict)		

	""" (3). Get the viable schedules """
	resultTuple = findViableSchedules(requestList, catalog, courseDict)

	""" (4). Printing top (n) schedules + Store into File """
	printSchedules(courseDict, resultTuple)	
 
		



def _printCourseDict(cl):
	"helper function for debugging"
	print("$$$$$$$$")
	for c in cl:
		print(cl[c])


if __name__ == '__main__':
	main()
