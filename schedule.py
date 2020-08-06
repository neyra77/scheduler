"""
schedule.py holds the combined code for creating schedule.
Given a saved HTML file, the steps it takes are:
	(1) Scrape the HTML file(e.g. Beautiful Soup) 
		Create a list of Course Objects (see course.py) 
	(3) Get user requests for schedule creation
	(4) Print the schedules and store them into ./result directory
	(5) Create schedule images.

"""
from htmlParser import parseHTML 

def printCatalogue(courseList):

def main():
	#htmlFile = '/mnt/c/Users/framo/OneDrive/Desktop/Control de eventos UCSUR.html'
	htmlFile = '/mnt/c/Users/framo/OneDrive/Desktop/Alumno.html'

	""" (1). Scrape, return a list of courses """
	courseList = parseHTML(htmlFile)
	""" (2). Print catalogue & get User requests """
	printCatalogue(courseList)






	#_printCourseList(courseList)





def _printCourseList(cl):
	"helper function for debugging"
	print("$$$$$$$$")
	for c in cl:
		print(c)


if __name__ == '__main__':
	main()
