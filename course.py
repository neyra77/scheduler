"""
courseParser puts the information in the bs4 soup into a list of Course objects.
Steps:
	- Find the correct place in the webpage html (e.g. just the schedule)
	- Reads the tables with schedules and adds Course object to list
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
	- Returns the list of Course Objects
"""

# Information about a course:
# - self.courseID: course ID/name (e.g., BIOQUIMICA)
# - self.semester: semester number in which course is in (e.g., [Ciclo] 4)
# - self.sections: list of Section Objects for Course (Sections are 3A, 3B, etc) 
class Course:
	def __init__(self, courseID, semester, sections):
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
			sectionStr += self.sections[section].__str__() + "\n\n"
		
		return sectionStr 	


# Information about a course section:
# - self.sectionID: Section ID/name (e.g., 3A, 3B, 4O)
# - self.theorytime: a ClassTime Object for the thoery portion
# - self.labs: list of Lab Objects for Course 
class Section:
	def __init__(self, sid=None, theoryTime=None, labs=None):
		self.sid = sid 
		self.theoryTime = theoryTime 
		self.labs = labs

	def getSID(self):
		return self.sid

	def getLabs(self):
		return self.labs

	def __str__(self):
		return "SID: %s \ntimeObj: %s \nlabs: %s" % (self.sid,
			self.theoryTime, self.labs)




	
