"""
	Some code for interacting with Splice.com using Python.

	There is no official API (yet), but with some snooping we can find out some of the 
	API calls.
"""
import requests, json
from urlparse import urlparse

class SpliceClient:
	cookies = ""
	connected = False
	spliceAPIRoot = 'https://api.splice.com'

	#Login and set the session cookie
	def connect(self, username, password):
		credentials = {'login': username, 'password': password}
		r = requests.post('https://api.splice.com/www/sign_in',data=credentials)

		if r.status_code == 401:
			return "401 Error: check your login details"
		else:
			self.cookies = r.cookies
			self.connected = True

	def listSpliceProjects(self, daw="ableton", number=100):
		if not self.connected:
			return "Not connected"
			

		apiCallURL = self.spliceAPIRoot + '/www/releases?'
		apiCallURL = apiCallURL + 'daw=' + daw
		apiCallURL = apiCallURL + '&page=' + str(1)
		apiCallURL = apiCallURL + '&per_page=' + str(number)
		apiCallURL = apiCallURL + '&sort=trending'

		r = requests.get(apiCallURL,cookies=self.cookies)

		jsonData = json.loads(r.text)

		return jsonData

	#List the project uuid, name and latest revision in JSON format
	def listUserProjects(self):
		if not self.connected:
			return "Not connected"			

		apiCallURL = self.spliceAPIRoot + '/studio/projects'
		r = requests.get(apiCallURL,cookies=self.cookies)
		jsonData = json.loads(r.text)

		your_keys = ['uuid', 'name', 'revision_uuid']
		projectsOut = []

		#Strip out the data we want - could be faster?
		for project in jsonData['projects']:
			newProjectData = { your_key: project[your_key] for your_key in your_keys }
			projectsOut.append(newProjectData)

		return projectsOut

	def getURLToUUID(self, projectURL):
		projectJSON = self.getSpliceProjectJSON(projectURL)

		return projectJSON['uuid']

	#Splice the project given the URL and return its uuid
	def spliceProject(self, projectURL):
		if not self.connected:
			return "Not connected"

		projectJSON = self.getSpliceProjectJSON(projectURL)			

		title = projectJSON['title']
		uuid = projectJSON['uuid']
		revision_uuid = projectJSON['related_sources'][0]['revision_uuid']

		apiCallURL = self.spliceAPIRoot + '/www/releases/' + uuid + '/splice'
		apiCallURL = apiCallURL + "?project_name=" + title + "&" + "revision_uuid=" + revision_uuid

		r = requests.post(apiCallURL,cookies=self.cookies)
		spliceJSON = json.loads(r.text)

		if r.status_code != requests.codes.ok:
		    return "Request error: " + str(r.status_code)
		    
		userProjectID = spliceJSON['project_uuid']
		userRevID = spliceJSON['revision_uuid']

		return userProjectID

	#Open the splice project given the userProjectUUID, download if it hasn't been already
	def openProject(self, userProjectUUID):
		if not self.connected:
			return "Not connected"

		userProjectJSON = self.getUserProjectJSON(userProjectUUID)			

		userProjectID = userProjectJSON['uuid']
		userRevID = userProjectJSON['revision_uuid']		

		apiCallURL = self.spliceAPIRoot + '/studio/projects/' + userProjectUUID + '/revisions/' + userRevID + '/open'
		
		r = requests.post(apiCallURL,cookies=self.cookies)

		if r.status_code != 204:
		    return "Request error: " + str(r.status_code)

	#Delete the splice project for the given userProjectUUID
	def deleteProject(self, userProjectUUID):
		if not self.connected:
			return "Not connected"

		apiCallURL = self.spliceAPIRoot + '/studio/projects/' + userProjectUUID

		r = requests.options(apiCallURL, cookies=self.cookies)

		if r.status_code != requests.codes.ok:
		    return "Request error: " + str(r.status_code)

		r = requests.delete(apiCallURL,cookies=self.cookies)

		# if r.status_code != requests.code.ok:
		#     print "Request error: " + str(r.status_code)

	#Given a URL, get the project JSON and return as an object
	def getSpliceProjectJSON(self, projectURL):
		if not self.connected:			
			return "Not connected"

		if projectURL == "":
		    return "Project URL is empty"

		o = urlparse(projectURL)
		details = o.path
		details = details.split('/')
		username = details[1]
		projectName = details[2]

		apiCallURL = self.spliceAPIRoot + '/www/users/' + username + '/releases/' + projectName

		r = requests.get(apiCallURL,cookies=self.cookies)

		if r.status_code != requests.codes.ok:
		    return "Request error: " + str(r.status_code)

		jsonResults = json.loads(r.text)

		return jsonResults

	#Given a userProjectUUID, get the project JSON and return as an object
	def getUserProjectJSON(self, userProjectUUID):
		if not self.connected:			
			return "Not connected"

		if userProjectUUID == "":
		    return "userProjectUUID is empty"

		apiCallURL = self.spliceAPIRoot + '/studio/projects/' + userProjectUUID

		r = requests.get(apiCallURL,cookies=self.cookies)

		if r.status_code != requests.codes.ok:
		    return "Request error: " + str(r.status_code)
		
		jsonResults = json.loads(r.text)

		return jsonResults		


	#Write the preview mp3 for the project at the url, you can specify an optional filename
	def getPreviewMP3(self, projectURL, filename=""):
		if projectURL == "":
			return "projectURL is empty"
		
		spliceProjectJSON = self.getSpliceProjectJSON(projectURL)

		if filename == "":
			filename = spliceProjectJSON['preview_url']
			filename = filename.rsplit('/',1)[1]
		
		#Write the preview mp3 to the filesystem
		mp3Out = file(filename, 'wb')

		r = requests.get(spliceProjectJSON['preview_url'])

		if r.status_code != requests.codes.ok:
		    return "Request error: " + str(r.status_code)

		mp3Out.write(r.content)

		return filename

	#Do some hack and slash to get the project name for a userProjectUUID
	def getProjectPath(self, userProjectUUID):
		import os, shutil, subprocess, signal, sys
		import fnmatch, getpass

		localUsername = getpass.getuser()
		localSpliceRoot = '/Users/' + localUsername + '/Splice'

		matches = []
		for root, dirnames, filenames in os.walk(localSpliceRoot):
		  for filename in fnmatch.filter(filenames, 'project_cache.json'):
		    matches.append(os.path.join(root, filename))

		path = ""
		for file in matches:
		    f = open(file, 'r')
		    projectDataJSON = json.loads(f.read())
		      
		    if projectDataJSON['project_uuid'] == userProjectUUID:
		        path = localSpliceRoot + "/" + projectDataJSON['original_path'] + "/" + projectDataJSON['als'][0]['original_path']
		        
		if path == "":
		    return "No path found has it downloaded yet?"
		else:
			return path
		


		