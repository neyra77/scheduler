"""
The functions for pruning.
	Main control function:  parseHTML(htmlFile)
	Steps:
		scrapeHTMLFile: get a bs4 object of the HTML
		prune: discard the rest, keep only schedule part
		splitSemesters: put the html for each semester in a list
		
		for each semester:
			get a list of course html
			create the Course Objects
			add it to a list
	
		return the list.
"""

from bs4 import BeautifulSoup
from util import Course
from util import Section
from util import TimeObj
from collections import defaultdict
import re
import constants
import json


def scrapeHTMLFile(htmlFile):
	# Return a BeautifulSoup Object of the HTML for easier parsing
	return BeautifulSoup(open(htmlFile), "html.parser")


def prune(soup): 
	#Keep only the part where the schedule is
	return soup.find(constants.MAIN_TAG
		, attrs = {'class': constants.MAIN_CLASS})

	

def splitSemesters(prunedSoup):
	#Return a list of Semester divs	
	return prunedSoup.find_all(constants.SEMESTER_TAG
		, attrs = {'class': constants.SEMESTER_CLASS})


def getRawCourseList(semesterHTMLList):
	rawCourseList = [] 
	for semesterHTML in semesterHTMLList:
		# Get Ciclo:
		ciclo = semesterHTML.find(constants.CICLO_TAG
			, {'class': constants.CICLO_NAME})	
		#TODO: make this regex prob + this is fast solution
		ciclo = ciclo.text.strip()[6:]
		if ciclo == "Electivo":
			ciclo = 0
		else:
			ciclo = int(ciclo)	
	
		courseHTMLList = semesterHTML.find_all(constants.COURSE_TAG
			, {'class': constants.COURSE_CLASS})
		for courseHTML in courseHTMLList:
			rawCourse = RawCourse(courseHTML, ciclo)

			#NOTE: putting the filter here for now

			rawCourseList.append(rawCourse)
	return rawCourseList


#NOTE: 3/14/21 this might be a test method (unneeded) 
def printSectionsDict(sd):
	if len(sd) == 0:
		print("Dictionary Empty")
	else:
		for k in sd:
			print(sd[k])



#Fills section dictionary for each rawSection (i.e. row)
def parseRawSection(sectionsDict, rs):
	sid = rs.findSID()
	timeObj = rs.createTimeObj() 

	#TODO: check this,  In case there wasn't a day
	#if timeObj is None:
	#	return

	#print(rs)	
	
	if sid not in sectionsDict:
		#TODO: look at constructor with NONE if(pacman.py has some) 
		section = Section(sid, [], defaultdict(list))
		sectionsDict[sid] = section

	if rs.isTheory():
		# Update the sid if necessary (Used when PRA came before TEO) 
		if not sectionsDict[sid].getSID():
			sectionsDict[sid].sid = sid

		# Update Time (NOTE watch out for repeats)
		if timeObj not in sectionsDict[sid].getTheoryTimes():
			sectionsDict[sid].getTheoryTimes().append(timeObj)

	#Labs are added Here
	else:	
		labID = rs.getFullID()

		if timeObj not in sectionsDict[sid].getLabs()[labID]:	
			sectionsDict[sid].getLabs()[labID].append(timeObj)


# Returns a defaultdict of Section Objects to fill Course with. 
def fillSections(rawCourse):
	sectionsDict = defaultdict(Section) 
	
	rawSections = rawCourse.findRawSections()
	
	# Iterate through each rawSection or row parse  
	for rs in rawSections:
		parseRawSection(sectionsDict, rs)

	return sectionsDict


class RawSection:
	"""
	Placeholder object for the Section HTML
	with methods to extract necessary info
	to create a Section
	"""
	_TYPE_PATTERN = re.compile(constants.TYPE_REGEX)


	def __init__(self, columns):
		self.columns = columns

	def isTheory(self):
		sectionType = self.columns[constants.TYPE_INDEX]	
		return True if sectionType == constants.THEORY else False

	#NOTE hours have [:5] due to change 2021-2
	def createTimeObj(self):
		day = self.columns[constants.DAY_INDEX]
		startTime = self.columns[constants.START_HOUR_INDEX][:5]
		endTime = self.columns[constants.END_HOUR_INDEX][:5]
	
		dateTuple = (day, startTime, endTime)

		# NOTE: Returning None for empty days
		if day == "":
			return None
		return TimeObj(dateTuple) 

	def getFullID(self):
		fullID = None	
		if not self.isTheory():
			fullID = self.columns[constants.SECTION_INDEX]
		return fullID

	def findSID(self):
		sid = self.columns[constants.SECTION_INDEX]
		if not self.isTheory():
			regex_search = re.search(self._TYPE_PATTERN, sid)
			sid = regex_search.group(1)
		return sid
	
	def __string__(self):
		return self.columns



class RawCourse:
	"""
	Placeholder object for the course HTML
	with methods to extract the necessary info
	to create a Course object.  
	"""
	_CID_PATTERN = re.compile(constants.CID_REGEX)

	def __init__(self, html, ciclo):
		self.html = html
		self.ciclo = ciclo

	def getHTML(self):
		return self.html

	#def getCiclo(self):
	#	return self.ciclo
	
	def findCID(self):
		fulltag = self.html.find(constants.CN_TAG
			, {'class': constants.CN_CLASS})
		text = fulltag.text
		regexSearch = re.search(self._CID_PATTERN, text)
		cid = regexSearch.group(1)	
		cid = cid.strip()

		return cid

	# Might need to fix this: NOTE: should do it but prob call it getSemester
	def findSemester(self): 
		return self.ciclo

	# Returns a list of rawsection objects
	def findRawSections(self):
		rawSections = []
		sections = self.html.find_all('tr')
		for section in sections:
			columns = section.find_all('td')
			columns = [c.text for c in columns]
			if columns:
				#NOTE: 2021-2 change
				if len(columns) < 2: 
					continue	
	
				if columns[constants.DAY_INDEX] == "":
					continue
	
				rawSection = RawSection(columns)	
				rawSections.append(rawSection)
		return rawSections



def getCourseDict(rawCourseList):
	courseDict = defaultdict(Course)
	
	# For each course
	for rc in rawCourseList:
		courseID = rc.findCID() 
		semester = rc.findSemester()  
		sections = fillSections(rc)

		#TEMP
		#print(courseID)
		#print(sections)
		#for s in sections:
		#	print(sections[s])
		
		course = Course(courseID, semester, sections)
		courseDict[courseID] = course
		
		#NOTE: take this out when 	
		#break

	return courseDict



def parseHTML(htmlFile):
	"""
	Main Control loop for HTML parser
	"""
	soup = scrapeHTMLFile(htmlFile)

	prunedSoup = prune(soup)
	semesterHTMLList = splitSemesters(prunedSoup)
	rawCourseList = getRawCourseList(semesterHTMLList)
	
	courseDict = getCourseDict(rawCourseList) 
	return courseDict



# Now the JSON parser
def parseJSON(jsonFile):
	"""
	Main Control loop for JSON parser
	"""
	courseDict = defaultdict(Course)

	with open(jsonFile) as f:
		cdict = json.load(f)

	# Fill in each course
	for k in cdict:
		courseID = cdict[k]["CourseID"]  #NOTE: Maybe this should be in CONSTANTS as json parameters
		semester = cdict[k]["semester"]
	
		# Fill in sections	
		sectionsDict = defaultdict(Section) 
		for s in cdict[k]["sections"]:
			sid = cdict[k]["sections"][s]["SectionID"]
			rawTtimes = cdict[k]["sections"][s]["theoryTimes"]
			tTimes = [TimeObj(x) for x in rawTtimes]
			labs = cdict[k]["sections"][s]["labTimes"]

			# Fill in lab Times 
			labDict = defaultdict(list)
			for l in labs:
				labDict[l] = [TimeObj(x) for x in labs[l]]

			# Create the section
			section = Section(sid, tTimes, labDict)
			sectionsDict[sid] = section 

		course = Course(courseID, semester, sectionsDict)
		courseDict[courseID] = course
	
	# Here return the courseDict
	return courseDict
	
	








 
		

