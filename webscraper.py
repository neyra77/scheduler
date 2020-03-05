import urllib.request
import requests
import itertools
import json
import re
from collections import defaultdict
from bs4 import BeautifulSoup


# NOTE: move to a constantsfile?
DAYS = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB"]
COMP_PATTERN = re.compile('(\d+[a-zA-Z]+)(.*)')


# Returns a name of the Courses (i.e Stats, Econ, Math, etc)
def getCourseNames(soup):
	names_obj = soup.find_all('td', attrs={'class':'tg-c3ow', 'valign':'middle'})
	names = [name_obj.text for name_obj in names_obj]
	#print ("\n".join(names))
	return set(names)

# Returns a name of headers (i.e Ciclo, Curso, seccion, etc)
def getTableHeaders(table):
	headers = table.findAll('th')	
	return [hd.text for hd in headers]

# Should give all categories of the table
def printTableCategories(soup):
	jsonkeys_obj = soup.find_all('th', attrs={'class':'tg-sckj'})
	jsonkeys = [key.text for key in jsonkeys_obj]
	#jsonkeys = set(jsonkeys)
	print ("\n".join(jsonkeys)) 

# TODO: Create a JSON file? 



# Nice print the dict 
def printDict(courseDict):
	# Put it into json string
	for k, v in courseDict.items():
		json_string = json.dumps(v.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
		print(json_string)


	#json_string = json.dumps(courseDict, indent=4, sort_keys=True, ensure_ascii=False)
	##parsed = json.loads(json_format)
	#print ("\n$$$$$$$$$$\n")
	#print(json_string)
	#print ("\n$$$$$$$$$$\n")


# Structure the table nicely, return a list of lists 
def preprocessTable(numheaders, headerDict, table):
	output_rows = []
	currCiclo = ""
	currCurso = ""
	currTipo = ""
	for table_row in table.findAll('tr'):
	                                                               
		columns = table_row.findAll('td')
		output_row = []
		
		if (len(columns) == 0): continue
		if len(columns) == numheaders:     # Semester row (11)
			currCiclo = columns[headerDict['CICLO']]
			currCurso = columns[headerDict['CURSO']]
			currTemp = columns[headerDict['TIPO']]
		elif len(columns) == numheaders - 1: # Course row (10)
			currCurso = columns[headerDict['CURSO'] - 1]
			output_row.append(currCiclo.text)	
		elif len(columns) == numheaders - 3: # Regular row (8)
			output_row.append(currCiclo.text)	
			output_row.append(currCurso.text)
	                                                               
		# Add the info
		for column in columns:
			output_row.append(column.text)
		
		# Equalize the size
		if len(output_row) < numheaders:
			output_row.append(currTemp.text)	
	                                                               
		output_rows.append(output_row)	
	
	return output_rows



class CourseInfo:
	def __init__(self, cid=None, sections=None, ciclo=None):
		if cid is None:
			cid = ""
		if sections is None:
			sections = defaultdict(list)
		if ciclo is None:
			ciclo = "" 
		self.cid = cid
		self.sections = sections
		self.ciclo = ciclo

	def getcid(self):
		return(self.cid)

	def getsections(self):
		return(self.sections)

	def getciclo(self):
		return(self.ciclo)

	def printCourseInfo(self):
		print("CID: " + self.getcid() + "\nSECTIONS: ")
		print(self.getsections())
		print("CICLO: " + self.getciclo())


# Parse a table
def parseTable(soup):
	courseDict = defaultdict(CourseInfo) 
	coursetimeMap = defaultdict(list)

	tables = soup.find_all("table")
	
	# We have a list of courses -> dict
	courses = getCourseNames(soup)

	#Printing coursedict	
	for key in courseDict.keys():
		courseDict[key].printCourseInfo()

	# For each table get the info
	for table in tables:
		# We have a list of headers
		headers = getTableHeaders(table)
		headerDict = {k:v for v, k in enumerate(headers)}
		numheaders = len(headers)
		
		# Preprocess the table and clean the data	
		output_rows = preprocessTable(numheaders, headerDict, table)

		table_dict = defaultdict(CourseInfo) 
		
		del_list = set()
		# Add every item from output_rows to courseDict
		for row in output_rows:
			currCourse = row[headerDict["CURSO"]]
			
			if currCourse not in table_dict:
				table_dict[currCourse]	

			currSemester= row[headerDict["CICLO"]]
			section = row[headerDict["SECCION"]]

			# Add any section to the delete list that has this as theory
			# only if this is practice
			regex_search = re.search(COMP_PATTERN, section)
			mainsection = regex_search.group(1)
			subsection = regex_search.group(2)
			if subsection and (currCourse, mainsection) in del_list:
				del_list.add((currCourse, section))	
	
			# TOMATO 
			if currCourse == "MORF. SIST.CAR.RES.DIG.EXC.REP" and (section == "3D1" or section[1] != "D"):
				del_list.add((currCourse, section))	
			#
			# Get the Time	
			day = row[headerDict["DIA"]]
			start_hour = row[headerDict["HORA INICIO"]]
			end_hour = row[headerDict["HORA FIN"]]
			date_str = day + start_hour + end_hour

			#TOMATO
			human_date_str = day + " " + start_hour + " - " + end_hour 
		
			#TOMATO	
			#if day == "SAB" or day == "MAR" or day == "JUE" or day == "LUN":
			if day == "SAB" or day == "MAR":
			#if day == "SAB":
				del_list.add((currCourse, section))	
			#TOMATO
			#newst_hour = start_hour.replace(":", ".") 
			#newst_hour = float(newst_hour)
	
			# Fill details (CID, CICLO_	
			if not table_dict[currCourse].getcid():
				table_dict[currCourse].cid = currCourse	
			if not table_dict[currCourse].getciclo():
				table_dict[currCourse].ciclo = currSemester
		
			# Fill the section's hours
			currsched = table_dict[currCourse].getsections()[section]
			newsched = translateDate(date_str)
			updatedsched = currsched + newsched 
			table_dict[currCourse].sections[section] = updatedsched 

			# TOMATO update the coursetimeMap
			comp = row[headerDict["COMP"]]	
			coursetimeMap[(currCourse, section)].append((human_date_str, comp, section))
			

		# COmbine theory and practice hours 
		for course in table_dict.keys():
			allcoursesecs = table_dict[course].getsections().keys()
			for sec1 in allcoursesecs: 
				regex_search = re.search(COMP_PATTERN, sec1)
				mainsection = regex_search.group(1)
				subsection = regex_search.group(2)

				# If course is a theory course
				if not subsection: 	
					haspractice = False 
					# Again go through all keys
					for sec2 in allcoursesecs: 
						ne_regex_search = re.search(COMP_PATTERN, sec2)
						ne_mainsection = ne_regex_search.group(1)
						ne_subsection = ne_regex_search.group(2)

						# Now check that it is a practice one belonging		
						if mainsection == ne_mainsection and ne_subsection:
							haspractice = True
							currsched = table_dict[course].getsections()[sec2]
							addsched = table_dict[course].getsections()[sec1]	
							updatedsched = currsched + addsched
							table_dict[course].sections[sec2] = updatedsched 
						
							# TOMATO update the coursetimeMap
							c = coursetimeMap[(course, sec2)] 
							a = coursetimeMap[(course, sec1)] 
							u = c + a
							coursetimeMap[(course, sec2)] = u
		
						# Add the theory to delete
						if haspractice:
							del_list.add((course, sec1))
	

		# Delete the unneeded ones	
		for (course, sec) in del_list:
			table_dict[course].getsections().pop(sec)	

		courseDict.update(table_dict)
	
	return (courseDict, coursetimeMap)


def printCourseInfoDict(d):
	for key,val in d.items():
		print("key: " + key)
		d[key].printCourseInfo()
		print("\n")


# Helper method
def print_list(l):
	for e in l:
		print(e)

# Ask user to choose what courses they want
def getrequestlist(catalog):
	print_list(catalog)
	
	print ("\n\nIngresa los digitos de los cursos que quieres: ") 
	numbers = list(filter(None, input().split(" ")))
	numbers = list(map(int, numbers)) # Transforms str -> int apparently


	print ("\n\nEscogistes: ")
	print ("------------")
	for n in numbers:
		print(str(catalog[n][0]) + " : " + catalog[n][1])
		
	return numbers 


# Compares two tuples dates to make sure there is no overlap
def checkOverlap(tup1, tup2):
	# NOTE: Assumes no incorrect data (hours are backwards)
	if tup1[1] <= tup2[0] or tup1[0] >= tup2[1]:
		return true

	return false	




#TODO: prob make a date a class
#TODO: assumes that classes take whole hours (i.e no 30 min class start)
#TODO: Use regex later too?
def translateDate(datestr):
	day = datestr[:3]
	
	start_time = datestr[3:8]
	start_hour = int(start_time[:2])
	start_minute = int(start_time[3:])
	start_5min = start_hour * 60/5 + start_minute/5


	end_time = datestr[8:]
	end_hour = int(end_time[:2])
	end_minute = int(end_time[3:])
	end_5min = end_hour * 60/5 + end_minute/5
	#TODO: perhaps add a check for if start > end time

	#Translation math:
	# 5 minute periods list 
	addend = DAYS.index(day) * 24 * 60 / 5	#TODO: make 24 a constant
	start_5min += addend
	start_5min = int(start_5min) 
	end_5min += addend 		
	end_5min = int(end_5min)

	return list(range(start_5min, end_5min + 1)) 


# Method to find the combinations
def findCombinations (request_list, catalog, courseDict, coursetimeMap):
	res_list = []	

	# Create a list of lists with each element having all 
	# sections of one course
	for catid in request_list:
		course = catalog[catid][1]
		course_reslist = []

		sections = courseDict[course].getsections()
		for secname, seclist in sections.items():
			course_reslist.append((catid, secname))
	                                                                        
		res_list.append(course_reslist)
	                                                                        
	good_counter = 0
	bad_counter = 0

	# Count the combinations & determine viability 	
	all_combinations = list(itertools.product(*res_list))	

	comb_counter = 1
	viable_list = []
	for comb in all_combinations:
		viable = True
		overall_time = set()
		for c in comb:
			courseName = catalog[c[0]][1]
			section = c[1]			
			section_time = courseDict[courseName].getsections()[section]
	
			# TODO: perhaps should be set as set from beginngn to tdetect errors	
			# Transform to set in order to take intersection
			section_time = set(section_time)
			if(section_time & overall_time):
				viable = False
				break
			else: 
				overall_time = overall_time | section_time 
	                                                                        
		if not viable:
			bad_counter += 1
			continue
		else:
			viable_list.append(comb)
			good_counter += 1	

	total = 1
	for res in res_list:
		total *= len(res)


		
	print("\n\nBuscando combinaciones viables entre " + str(total) + " posibilidades...........")
	#print("Condiciones: No clase [\'Martes\', \'Sabado\']")	
	print ("\nHorarios viables: " + str(good_counter))
	print("Horarios NO viables: " + str(bad_counter))

	comb_counter = 1
	for viable in viable_list: 
		print("\n\nHorario Final: " + str(comb_counter) + "/" + str(good_counter))	
		counter = 1
		for c in viable:
			courseName = catalog[c[0]][1]
			secName = c[1]
			
			regex_search = re.search(COMP_PATTERN, secName)
			grupo = regex_search.group(1)
			seccion = regex_search.group(2)
				
			print("\tCurso " + str(counter) + ".\t------------- " + 
				courseName + " [" + grupo + 
				"|" + seccion + "] -------------")
			time = coursetimeMap[(courseName, secName)]
			#time.sort()
			for t in time: 
				#output_str = t[0] + "  (" + t[1] + " , " + t[2] + ")"
				output_str = t[1] + "\t" + t[0] + "\t"
				spacer = "" if len(t[2]) > 2 else " " 
				#output_str = t[1] + " " + spacer + t[2] + "\t   " + t[0]
				print("\t\t{0}".format(output_str))


			counter += 1
		comb_counter += 1
		print("\n")
	print("\n")
	                                                                        
 
def main():
	# Parses the html
	url = '/mnt/c/Users/framo/OneDrive/Desktop/Control de eventos UCSUR.html'
	#url = '/mnt/c/Users/framo/OneDrive/Desktop/Control de eventos UCSUR2'
	soup = BeautifulSoup(open(url), "html.parser")
	
	(courseDict, coursetimeMap) = parseTable(soup)	

	#for key in coursetimeMap.keys():
	#	print( key)
	#	print( coursetimeMap[key])
	
	# Prints the dictionary in nice version	
	#printDict(courseDict)

	catalog = list(enumerate(sorted(courseDict.keys())))	

	print("Catalogo de cursos 2020-1:\n")
	request_list = getrequestlist(catalog)
	findCombinations (request_list, catalog, courseDict, coursetimeMap)
	
	#printDict(courseDict)


if __name__ == '__main__':
	main()




