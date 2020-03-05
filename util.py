############################################################
# Course scheduling specifics.

# Information about a course:
# - self.cid: course ID (e.g., stats, morf3)
# - self.name: name of the course (e.g., Artificial Intelligence)
# - self.quarters: quarters without the years (e.g., Aut)
# - self.minUnits: minimum allowed units to take this course for (e.g., 3)
# - self.maxUnits: maximum allowed units to take this course for (e.g., 3)
# - self.prereqs: list of course IDs that must be taken before taking this course.
class Course:
	def __init__(self, info):
		self.__dict__.update(info)
	
	# Return whether this course is offered in |quarter| (e.g., Aut2013).
	def is_offered_in(self, quarter):
		return any(quarter.startswith(q) for q in self.quarters)
	
	def short_str(self): return '%s: %s' % (self.cid, self.name)
	
	def __str__(self):
		return 'Course{cid: %s, name: %s, quarters: %s, units: %s-%s, prereqs: %s}' % (self.cid, self.name, self.quarters, self.minUnits, self.maxUnits, self.prereqs)


# Information about all the courses
class CourseBulletin:
	def __init__(self, coursesPath):
	"""
	Initialize the bulletin.
	
	@param coursePath: Path of a file containing all the course information.
	"""  

	# Read courses (JSON format) 
	self.courses = {}
	info = json.loads(open(coursesPath).read())
	for courseInfo in list(info.values()):
		course = Course(courseInfo)
		self.courses[course.cid] = course
