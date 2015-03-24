#!/usr/local/bin/python

import splice

#Create object
sp = splice.SpliceClient()

#Connect
sp.connect('username', 'password')

#Retrieve the list of the users projects
projectList = sp.listProjects()

for project in projectList:	
	print project

#Let's work with this project
projectURL = 'https://splice.com/haywyre/wip'

#Get the project UUID for a projectURL
projectUUID = sp.getURLToUUID(projectURL)

#Get the entire project JSON if you want 
# print(sp.getProjectJSON(projectURL))

#Splice the projectURL and get the userProjectUUID
#Remember that the userProjectUUID corresponds to the project in your studio
userProjectUUID = sp.spliceProject(projectURL)
print userProjectUUID

#Retrieve the list of the users projects again
projectList = sp.listProjects()

for project in projectList:	
	print project

#You can download and open it with this
sp.openProject(userProjectUUID)

#You can delete it with this call
sp.deleteProject(userProjectUUID)




