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
from course import Course
from course import Section
from timeHandler import TimeObj
from collections import defaultdict
import re
import constants



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
		courseHTMLList = semesterHTML.find_all(constants.COURSE_TAG
			, {'class': constants.COURSE_CLASS})
		for courseHTML in courseHTMLList:
			rawCourse = RawCourse(courseHTML)
			rawCourseList.append(rawCourse)
	return rawCourseList




#Fills section dictionary for each rawSectiong(i.e. row)
def parseRawSection(sectionsDict, rs):
	sid = rs.findSID()
	timeObj = rs.createTimeObj() 
	
	if rs.isTheory():
		# Create new only if doesn't exist 
		if sid not in sectionsDict:
			labs = defaultdict(str) 
			section = Section(sid, timeObj, labs)
			sectionsDict[sid] = section
		# Otherwise just update it	
		else:
			if not sectionsDict[sid].getSID():
				sectionsDict[sid].sid = sid
			else: 
				# TODO: Update Time Obj
				sectionsDict[sid].theoryTime += timeObj 

	else:
		labID = rs.getFullID()

		if not sectionsDict[sid].getLabs():
			sectionsDict[sid].labs = defaultdict(str)

		if labID in sectionsDict[sid].getLabs():
			#TODO: Update Time Obj
			sectionsDict[sid].getLabs()[labID] += timeObj 
			pass
		else:
			#TODO Put the TimeObj
			sectionsDict[sid].getLabs()[labID] = timeObj 



def fillSections(rawCourse):
	sectionsDict = defaultdict(Section) 
	
	rawSections = rawCourse.findRawSections()
	
	# Iterate through each rawSection or row parse  
	for rs in rawSections:
		parseRawSection(sectionsDict, rs)

	#for s in sectionsDict:
	#	print(sectionsDict[s])
	#	print()
	return sectionsDict


class RawSection:
	"""
	Placeholder object for the Section HTML
	with methods to extract necessary info
	to create a Section
	"""
	TYPE_PATTERN = re.compile(constants.TYPE_REGEX)


	def __init__(self, columns):
		self.columns = columns

	def isTheory(self):
		sectionType = self.columns[constants.TYPE_INDEX]	
		return True if sectionType == constants.THEORY else False

	def createTimeObj(self):
		day = self.columns[constants.DAY_INDEX]
		startTime = self.columns[constants.START_HOUR_INDEX]
		endTime = self.columns[constants.END_HOUR_INDEX]	
	
		dateTuple = (day, startTime, endTime)
		return TimeObj(dateTuple) 

	def getFullID(self):
		fullID = None	
		if not self.isTheory():
			fullID = self.columns[constants.SECTION_INDEX]
		return fullID


	def findSID(self):
		sid = self.columns[constants.SECTION_INDEX]
		if not self.isTheory():
			regex_search = re.search(self.TYPE_PATTERN, sid)
			sid = regex_search.group(1)
		return sid
	
				 

	def __string__(self):
		print(self.columns) 



class RawCourse:
	"""
	Placeholder object for the course HTML
	with methods to extract the necessary info
	to create a Course object.  
	"""
	def __init__(self, html):
		self.html = html

	def getHTML(self):
		return self.html
	
	def findCID(self):
		fulltag = self.html.find(constants.CN_TAG
			, {'class': constants.CN_CLASS})
		return fulltag.text

	# Might need to fix this
	def findSemester(self):
		return "N/A"

	# Returns a list of rawsection objects
	def findRawSections(self):
		rawSections = []
		sections = self.html.find_all('tr')
		for section in sections:
			columns = section.find_all('td')
			columns = [c.text for c in columns]
			if columns:
				rawSection = RawSection(columns)		
				rawSections.append(rawSection)
		return rawSections



def getCourseList(htmlCourseList):
	courseList = []
	
	# For each course
	for rc in htmlCourseList:
		courseID = rc.findCID() 
		semester = rc.findSemester()  
		sections = fillSections(rc)
		
		course = Course(courseID, semester, sections)
		courseList.append(course)	
	
		#NOTE: take this out when 	
		#break
	
	return courseList



def parseHTML(htmlFile):
	"""
	Main Control loop of function
	"""
	soup = scrapeHTMLFile(htmlFile)
	prunedSoup = prune(soup)
	semesterHTMLList = splitSemesters(prunedSoup)
	rawCourseList = getRawCourseList(semesterHTMLList)
	
	courseList = getCourseList(rawCourseList) 
	return courseList














 
		

