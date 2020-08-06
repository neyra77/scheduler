"""
	This will handle all the time related stuff
	for classes and such
"""

DAYS = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB"]


class TimeObj:
	"""
	The input, dateTuple, comes from RawSection. 
	Structure is (day, start_time, end_time)
	"""	
	def __init__(self, dateTuple): 
		self.day = dateTuple[0]
		self.start_time = dateTuple[1]
		self.end_time = dateTuple[2]
		self.timeSet = self._transformDateStr()
	
	def _transformDateStr(self):
		start_hour = int(self.start_time[:2])
		start_minute = int(self.start_time[3:])
		start_5min = start_hour * 60/5 + start_minute/5		

		end_hour = int(self.end_time[:2])
		end_minute = int(self.end_time[3:])
		end_5min = end_hour * 60/5 + end_minute/5		
		
		addend = DAYS.index(self.day) * 24 * 60 / 5
		start_5min += int(addend) #NOTE: Is this calculation fine?
		end_5min += int(end_5min)
		
		return list(range(start_5min, end_5min + 1))	
	
	#def extract







