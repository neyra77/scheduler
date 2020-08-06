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

def scrapeHTMLFile(htmlFile):
	"""
	Return a BeautifulSoup Object of the HTML for easier parsing 
	"""
	return BeautifulSoup(open(htmlFile), "html.parser")

def main():
	#htmlFile = '/mnt/c/Users/framo/OneDrive/Desktop/Control de eventos UCSUR.html'
	htmlFile = '/mnt/c/Users/framo/OneDrive/Desktop/Alumno.html'

	""" (1). Scrape, return a list of courses """
	courseList = parseHTML(htmlFile)


	print("$$$$$$$$")
	for c in courseList:
		print(c)


if __name__ == '__main__':
	main()
