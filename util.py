"""
	- Structure of Course Object: 
		(id, 
		semester, 
		sections:
			[e.g., 
			sid, 
			timeObj,
			Labs: 
				[e.g., 	
				lab1,
				timeObj, 
				etc]
			, etc]
"""

from collections import defaultdict


# Information about a course:
# - self.courseID: course ID/name (e.g., BIOQUIMICA)
# - self.semester: semester number in which course is in (e.g., [Ciclo] 4)
# - self.sections: list of Section Objects for Course (Sections are 3A, 3B, etc) 
class Course:
	def __init__(self, courseID="", semester="", sections=[]):
		self.courseID = courseID
		self.semester = semester
		self.sections = sections

	def getCourseID(self):
		return self.courseID

	def getSemester(self):
		return self.semester
	
	def getsections(self):
		return self.sections 

	def __str__(self):
		sectionStr = "CourseID: %s  \nsemester: %s\n\n" % (self.courseID, self.semester) 
		for section in self.sections:
			sectionStr += "\t" + self.sections[section].__str__() + "\n\n"
		
		return sectionStr 	


# Information about a course section:
# - self.sectionID: Section ID/name (e.g., 3A, 3B, 4O)
# - self.theorytime: a ClassTime Object for the thoery portion
# - self.labs: list of Lab Objects for Course 
class Section:
	def __init__(self, sid=None, theoryTimes=[], labs=defaultdict(list)):
		self.sid = sid 
		self.theoryTimes = theoryTimes  
		self.labs = labs

	def getSID(self):
		return self.sid
	
	def getLabs(self):
		return self.labs

	def __str__(self):
		res = "SID: %s\n" %(self.sid)
		res += "\tTheory Times:\n"
		# Print Theory Times
		for to in self.theoryTimes:
			res += "\t\t" + to.__str__() + "\n"

		# Print Lab Times
		res += "\t\tLab Times(%s): \n" % (len(self.labs))
		for lab in self.labs:
			res += "\t\t[\n\t\t\tLabID: %s\n"%(lab)
			for to in self.labs[lab]:
				res += "\t\t\t" + to.__str__() + "\n"
			res += "\t\t]\n" 

		return res



"""
        This will handle all the time related stuff
        for classes and such
"""

DAYS = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB"]


class TimeObj:
	"""
	The input, dateTuple, comes from RawSection.
	Structure is (day, start_time, end_time)
	
	The TimeObj is basically just a tuple (start5min, end5min)
	"""
	def __init__(self, dateTuple):
		self._day = dateTuple[0]
		self._startTime = dateTuple[1]
		self._endTime = dateTuple[2]
		self._timeInterval = self._transformDateStr()

	def getDay(self):
		return self._day
	
	def _transformDateStr(self):
		dayBonus = DAYS.index(self._day) * 24 * 60 / 5

		startHour = int(self._startTime[:2])
		startMinute = int(self._startTime[3:])
		start5min = startHour * 60/5 + startMinute/5 + dayBonus
		
		endHour = int(self._endTime[:2])
		endMinute = int(self._endTime[3:])
		end5min = endHour * 60/5 + endMinute/5 + dayBonus

		return (int(start5min), int(end5min))
		#NOTE: will I need end5min + 1? or not

	
	def __str__(self):	
		return "Day: %s\n\
			Start: %s\n\
			End: %s\n\
			Time Interval: %s\n" % (self._day, 
			self._startTime, 
			self._endTime, 
			self._timeInterval)
