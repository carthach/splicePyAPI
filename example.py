#!/usr/local/bin/python

import splice
import AbletonParser

#Create object
sp = splice.SpliceClient()

#Connect
sp.connect('username', 'password')

#Retrieve the list of the users projects
projectList = sp.listUserProjects()

for project in projectList:	
	print project

#Let's work with this project
projectURL = 'https://splice.com/haywyre/wip'

#Get the project UUID for a projectURL
projectUUID = sp.getURLToUUID(projectURL)

#Get the entire project JSON if you want 
print(sp.getSpliceProjectJSON(projectURL))

#You can download the preview mp3
sp.getPreviewMP3(projectURL)

#The HTML embed code for the DNA player
print(sp.getDNAPlayerEmbedCode('https://splice.com/haywyre/wip'))

#Splice the projectURL and get the userProjectUUID
#Remember that the userProjectUUID corresponds to the project in your studio
userProjectUUID = sp.spliceProject(projectURL)
print userProjectUUID

#Retrieve the list of the users projects again
projectList = sp.listUserProjects()

for project in projectList:	
	print project

#You can download and open it with this
sp.openProject(userProjectUUID)

#You can delete it with this call
# sp.deleteProject(userProjectUUID)

#Get the local project path for a userProjectUUID
localProjectPath = getLocalProjectPath(self, userProjectUUID)

#Finally you can use the Ableton Parser and get the marker info from the Ableton file!

ap = AbletonParser.AbletonParser()

ap.loadProject(localProjectPath)

print(ap.getAbletonMarkers())