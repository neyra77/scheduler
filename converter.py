DAYS = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB"]

while(True):
	time = int(input("Enter a num: "))

	totalperday = 24 * 12
	day = DAYS[int(time /(totalperday))]
	currday = time % (totalperday)


	hour = int(currday / 12)
	minute = (currday % 12) * 5
	print(str(day) + " " + str(hour) + ":" + str(minute))
