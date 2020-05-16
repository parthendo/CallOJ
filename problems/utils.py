import yaml
import re
import os

class Utils:

	def fetchAvailableLanguages(self):
		path = os.path.dirname(__file__).rsplit('/',1)[0]
		judgeConfigFilePath =  open(os.path.join(path,'media/judgeConfiguration/config.yml'))
		judgeConfigFile = yaml.load(judgeConfigFilePath, Loader = yaml.FullLoader)
		configurations = judgeConfigFile.get("runtime")
		languages = []
		flag = False
		for configuration in configurations:
			if flag == True:
				languages.append(configuration)
			elif configuration == "gcc":
				flag = True
				languages.append(configuration)
		return languages
