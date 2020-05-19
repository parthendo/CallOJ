import yaml
import re
import os, zipfile
from .judge import Judge
from django.core.files.storage import FileSystemStorage
import shutil

class Utils:

	'''
	Reads the judge's configuration file and fetches all the directories of languages and 
	is returned to the front-end drop down menu
	'''
	def fetchAvailableLanguages(self):

		path = os.path.dirname(__file__).rsplit('/',1)[0]
		judgeConfigFilePath =  open(os.path.join(path,'media/judgeConfiguration/languageExtension.yml'))
		judgeConfigFile = yaml.load(judgeConfigFilePath, Loader = yaml.FullLoader)
		languages = []
		for configuration in judgeConfigFile:
			languages.append(configuration)
		print(languages)
		return languages

	'''
	Reads language extension yaml file for file extension as per the language
	'''
	def fetchLanguageExtension(self):

		path = os.path.dirname(__file__).rsplit('/',1)[0]
		fileExtensionFile = open(os.path.join(path,'media/judgeConfiguration/languageExtension.yml'))
		languageExtension = yaml.load(fileExtensionFile, Loader=yaml.FullLoader)
		return languageExtension

	'''
	Saves file code file in the user directory as per the username folder in media 
	'''
	def saveFile(self, user, problem, languageExtension, code):
		
		with open(("media/submittedFiles/" + user.username + "/" + problem.problemCode + ".txt"), "w") as file:
			file.write(code)
		codeFile = "media/submittedFiles/" + user.username + "/" + problem.problemCode + ".txt"
		base = os.path.splitext(codeFile)[0]
		os.rename(codeFile, base + languageExtension)
	
	'''
	Submits a problem and returns the results. 
	Input:
		User, Code (solution to the problem), Language from the drop down, Problem credentials
	'''

	def submitProblem(self, user, code, language, problem):

		# Absolute parent path i.e. ~/CallOJ/
		parentDirPath = os.path.dirname(__file__).rsplit('/',1)[0]
		print(parentDirPath)

		# Fetches language extension e.g .cpp for g++
		# Update file CallOJ/media/judgeConfiguration/languageExtension.yml for extension
		# Update file CallOJ/media/judgeConfiguration/config.yml for language directory path
		languageExtension = self.fetchLanguageExtension()
		languageExtension = languageExtension[language]
		print("Language Extension: ")
		print(languageExtension)
		self.saveFile(user, problem, languageExtension, code)

		# Updating judge configurations

		judge = Judge()
		judge.judgeConfigFile = os.path.join(parentDirPath,'media/judgeConfiguration/config.yml')
		judge.problemPath = os.path.join(parentDirPath,'media/problems/')
		judge.problemCode = str(problem.problemCode)
		judge.submittedFileDir = os.path.join(parentDirPath, 'media/submittedFiles')
		judge.solutionCode = str(os.path.join(user.username , problem.problemCode+languageExtension))
		print(judge.solutionCode)
		judge.languageCode = language
		judge.timeLimit = str(problem.timeLimit)
		judge.memoryLimit = str(problem.memoryLimit)
		judge.problemType = problem.marking

		return judge.executeJudge()

	def saveProblem(self, YAMLFile, problemCode, uploadedFiles):

		# Path of ~/CallOJ/media/problem
		parentDirPath = os.path.dirname(__file__).rsplit('/',1)[0]
		path = os.path.join(parentDirPath, 'media/problems/'+ problemCode)
		################################################
		# Creating directory media/problems/ProblemCode#
		################################################
		mode = 0o777
		os.mkdir(path, mode)
		fileSystem = FileSystemStorage()
		# Saving yaml file
		fileSystem.save(YAMLFile.name, YAMLFile)
		# Moving init.yml file inside the folder
		src = os.path.join(parentDirPath,'media/init.yml')
		shutil.move(src, path)

		# Saving the uploaded test cases file in a zip inside the folder
		# Maintaining the nomenclature of the file as per the init.yml file

		uploadedFilesCount = len(uploadedFiles)
		loop = 0
		index = 0

		while loop < uploadedFilesCount:

			# Nomenclature belongs to standard dmoj type
			# Input File
			inputTestFile = uploadedFiles[loop]
			inputTestFile.name = "tc" + str(index) + ".in"
			fileSystem.save(inputTestFile.name, inputTestFile)
			src = os.path.join(parentDirPath, 'media/'+inputTestFile.name)
			shutil.move(src, path)
			# Output File
			outputTestFile = uploadedFiles[loop+1]
			outputTestFile.name = "tc" + str(index) + ".out"
			fileSystem.save(outputTestFile.name, outputTestFile)
			src = os.path.join(parentDirPath, 'media/'+outputTestFile.name)
			shutil.move(src, path)

			loop = loop + 2
			index = index + 1

		zfName = problemCode + ".zip"
		print(zfName)
		zfPath = os.path.join(path, zfName)
		print(zfPath)
		zf = zipfile.ZipFile((zfPath),"w")
		for root, subdirs, files in os.walk(path):
			for filename in files:
				if filename!="init.yml" and filename!=zfName:
					zf.write(os.path.join(root, filename), filename, zipfile.ZIP_DEFLATED)
		zf.close()

		# Removing all the residual files
		loop = 0
		index = 0
		
		while loop < uploadedFilesCount:
			inputFile = uploadedFiles[loop] 
			src = os.path.join(path, inputFile.name)
			os.remove(src)

			outputFile = uploadedFiles[loop+1]
			src = os.path.join(path, outputFile.name)
			os.remove(src)

			loop = loop + 2