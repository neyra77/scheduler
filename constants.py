"""
Hard Coded Constants to find the attributes
        SEMESTER_TAG (e.g. 'Ciclo 3')

NOTE: probably will have to be changed every semester

"""
#_VAR = str(1)
_VAR = str(3)


_VAR2 = str(0)
#_VAR2 = str(1)


# For pruning just schedule
MAIN_TAG = 'div'
MAIN_CLASS = 'ng-tns-c' + _VAR + "-" + _VAR2 + ' ng-star-inserted'

# For pruning a list of the semester HTML
SEMESTER_TAG = 'div'
SEMESTER_CLASS = 'rounded-s bd-1 mb-3 overflow-hidden bd-ucs ng-star-inserted'

# 3/14/21 For pruning just the Semester Num
CICLO_TAG = "div"
CICLO_NAME = "bg-ucs p-2 text-white pointer"


# For pruning just the Courses
COURSE_TAG = 'div'
COURSE_CLASS = 'rounded-s bd-1 mb-3 overflow-hidden bd-gray ng-tns-c' + _VAR + "-" + _VAR2 + ' ng-star-inserted'

# For getting just the Course Name
#TODO: rename CID_TAG
CN_TAG = 'strong'
CN_CLASS = 'ng-tns-c' + _VAR + "-" + _VAR2


#THEORY = "TEO"
#LAB = "PRA"
#NOTE: changed for 2021-2
THEORY = "Teoria"
LAB = "Prácticas"

# REGEX Expressions:
TYPE_REGEX = '(\d+[a-zA-Z]+)(.*)'
CID_REGEX = 'Curso:(.+?)-.*'




#TODO: probably do this programmatically
# Headers (straight up copied from website)
HEADER_DICT = {'TIPO': 0, 'SECCIÓN': 1, 'DÍA':2, 'AULA - LOCAL':3, 
	'FECHA INICIO': 4, 'HORA INICIO': 5, 'HORA FIN': 6, 'DOCENTE': 7}

#NOTE: Needs change if table changes
TYPE_INDEX = 0
SECTION_INDEX = 1
DAY_INDEX = 2
START_HOUR_INDEX = 5
END_HOUR_INDEX = 6


# Directory names
JSON_DIRECTORY = "JSON"



