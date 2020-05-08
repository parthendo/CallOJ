import subprocess
import re

class Judge:

    def trimResult(self, input):
        # removing all byte encodings
        # tried reg-ex but failed
        input = input.replace(b'\x1b[0m',b'')
        input = input.replace(b'\x1b[1m',b'')
        input = input.replace(b'\x1b[4m',b'')
        input = input.replace(b'\x1b[31m',b'')
        input = input.replace(b'\x1b[32m',b'')
        input = input.replace(b'\x1b[33m',b'')
        input = input.replace(b'\x1b[36m',b'')
        input = input.replace(b'\x1b[35m',b'')
        output = str(input,'utf-8')
        return output

    def executeJudge(self, judgeConfigFile, solutionCode, problemCode, languageCode, timeLimit, memoryLimit):
        # initializes the process to query dmoj-cli
        process = subprocess.Popen(["dmoj-cli","-c",judgeConfigFile], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # query for dmoj-cli
        query = "submit -tl "+ timeLimit + " -ml " + memoryLimit + " " + problemCode + " " + languageCode + " " + "CallOJ/media/submittedFiles/" + solutionCode
        print("Query is ",query)
        query = bytes(query, 'utf-8') 
        stdout, stderr = process.communicate(input=query)
        return stdout


if __name__ == "__main__":
    judgeConfigFile =  b"CallOJ/media/judgeConfiguration/config.yml"
    solutionCode = "1.cpp"
    problemCode = "XYZ"
    languageCode = "CPP14" 
    timeLimit = "1"
    memoryLimit = "65000"
    output = Judge.executeJudge(None, judgeConfigFile, solutionCode, problemCode, languageCode, timeLimit, memoryLimit)
    output = Judge.trimResult(None, output)
    list = output.split("dmoj> ")
    print(list[1])
    list = list[1].split('\n')
    #print(list[1])