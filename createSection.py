import os
import sys
import constants

template = "<tr _ngcontent-ggn-c1=\"\" class=\"text-center text-s ng-tns-c"+ constants._VAR + "-0 ng-star-inserted\"><td _ngcontent-ggn-c1=\"\" class=\"px-2 py-1 text-left\">{}</td><td _ngcontent-ggn-c1=\"\" class=\"px-2 py-1\">{}</td><td _ngcontent-ggn-c1=\"\" class=\"px-2 py-1\">{}</td><td _ngcontent-ggn-c1=\"\" class=\"px-2 py-1\"> </td><td _ngcontent-ggn-c1=\"\" class=\"px-2 py-1\">2020-08-24</td><td _ngcontent-ggn-c1=\"\" class=\"px-2 py-1\">{}:{}</td><td _ngcontent-ggn-c1=\"\" class=\"px-2 py-1\">{}:{}</td><td _ngcontent-ggn-c1=\"\" class=\"px-2 py-1\"></td></tr>"

def main():
	# User inputs HTML file as option
	
	sectionType = sys.argv[1]
	_id = sys.argv[2]
	day = sys.argv[3] 
	start_hour = sys.argv[4]
	if (len(start_hour) < 2):
		start_hour = "0" + start_hour 
	start_min = sys.argv[5] 
	end_hour = sys.argv[6] 
	if (len(end_hour) < 2):
		end_hour = "0" + end_hour 
	end_min = sys.argv[7]  

	print("Day :%s\nType:%s\nTime:%s:%s %s:%s"%(day, 
												sectionType,
												start_hour,
												start_min,
												end_hour,
												end_min))


	print(template.format(sectionType, _id, day, start_hour, start_min, end_hour, end_min))
	



if __name__ == '__main__':
	main()
