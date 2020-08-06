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
	
	def _transformDateStr(self):
		startHour = int(self._startTime[:2])
		startMinute = int(self._startTime[3:])
		start5min = startHour * 60/5 + startMinute/5		

		endHour = int(self._endTime[:2])
		endMinute = int(self._endTime[3:])
		end5min = endHour * 60/5 + endMinute/5		
		
		return (start5min, end5min)

	def __string__(self):
		return self._day + self._startTime + self._endTime + self._timeInterval


	#def intersect(self
	
