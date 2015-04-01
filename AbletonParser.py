"""
A simple parser for Ableton als files

At the moment just use it to extract the users' locators
"""
from bs4 import BeautifulSoup

class AbletonParser:	
	abletonProjectData = ""

	def loadProject(self, abletonProjectPath):
		if abletonProjectPath == "":
			return "Project is empty"
		else:			
			import gzip			
			f = gzip.open(abletonProjectPath, 'r')		
			self.abletonProjectData = f.read()			

	#Output the Ableton markers given the project uuid
	def getAbletonMarkers(self):						   		  	 
		soup = BeautifulSoup(self.abletonProjectData)

		markers = []

		locators = soup.ableton.liveset.locators.locators.find_all('locator')
		endTime = soup.ableton.liveset.transport.looplength['value']	   

		for locator in locators:
			marker = {}
			marker['time'] = float(locator.time['value'])

			name = locator.find_all('name')
			marker['name'] = name[0]['value']

			markers.append(marker)

		markers = sorted(markers, key=lambda marker: marker['time'])

		endMarker = {}
		endMarker['time'] = float(endTime)
		endMarker['name'] = 'loopEnd'

		# markers.append(endMarker)

		return markers, endMarker


