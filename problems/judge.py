import subprocess
import re
import yaml

class Judge:

    def runQuery(self):
        # initializes the process to query dmoj-cli
        process = subprocess.Popen(["dmoj-cli","-c",self.judgeConfigFile], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # query for dmoj-cli
        query = "submit -tl "+ self.timeLimit + " -ml " + self.memoryLimit + " " + self.problemCode + " " + self.languageCode + " " + "/home/jayant/CallOJ/media/submittedFiles/" + self.solutionCode
        print("Query is ",query)
        query = bytes(query, 'utf-8') 
        stdout, stderr = process.communicate(input=query)
        # Saving the terminal output
        self.terminalOutput = stdout
        self.terminalExecutionError = stderr 

    def trimResult(self):
        ASCIICodes = [b'\x1b[0m',b'\x1b[1m',b'\x1b[4m',b'\x1b[31m',b'\x1b[32m',b'\x1b[33m',b'\x1b[36m',b'\x1b[35m',b'\x1b[01m\x1b[K',b'\x1b[m\x1b[K',b'\x1b[01;31m\x1b[K',b'\x1b[01;32m\x1b[K']
        # removing all byte encodings
        # tried reg-ex but failed
        
        for code in ASCIICodes:
            self.terminalOutput = (self.terminalOutput).replace(code,b'')

        self.processedOutput = str(self.terminalOutput,'utf-8')
        self.result = (self.processedOutput).split("dmoj> ")[1]
    
    def processResultPerTC(self, itr):
        verdict = []
        tempVerdict = ((self.result[itr]).split("  ")[1]).split(" ")
        if(tempVerdict[1] == 'IR'):
            verdict.append("RTE")
        else:
            verdict.append(tempVerdict[1])
        # Marks (grades further)
        verdict.append(0)
        # Time taken for this test case
        verdict.append(tempVerdict[2][1:])
        # Memory taken by this test case
        verdict.append(tempVerdict[5][:-1])
        # Remarks
        verdict.append(tempVerdict[6:])
        self.tcverdict = verdict

    def fetchResult(self):
        self.verdict = []
        self.result = (self.result).split("\n")
        resultLen = len(self.result)
        if self.result[1] == "Failed compiling submission!":
            self.verdict.append("CE")
            self.verdict.append("NA")
            self.verdict.append("NA")
            self.verdict.append("NA")
            # NOTETOSELF: Remember to typecaste to string while using
            self.verdict.append(list(self.result[1:resultLen-2]))
        else:
            for itr in range(1,resultLen-3): 
                self.processResultPerTC(itr)
                self.verdict.append(self.tcverdict)

    def grade(self):
        
        problemConfigurationFile = open("/home/jayant/CallOJ/media/problems/" + self.problemCode + "/init.yml")
        problemConfigurationFile = yaml.load(problemConfigurationFile, Loader=yaml.FullLoader)

        testCases = problemConfigurationFile.get("test_cases")
        testCasesLen = len(testCases)
        
        '''
        Temporary flagging variables for scoring
        '''
        finalVerdict = []
        allAC = True
        maxTime = -float('inf')
        maxSpace = -float('inf')
        score = 0

        for tc in range(0, testCasesLen):
            verdict = self.verdict[tc]
            if (verdict[0] == "AC"):
                timeTaken = float(verdict[2][:-1])
                memory = float(verdict[3][:-2])
                maxTime = max(timeTaken, maxTime)
                maxSpace = max(memory, maxSpace)
                score = score + testCases[tc]['points']
            else:
                allAC = False
        
        if(allAC == False):
            finalVerdict.append("WA")
        else:
            finalVerdict.append("AC")
        
        finalVerdict.append(score)
        finalVerdict.append(str(maxTime)+"s")
        finalVerdict.append(str(maxSpace)+"kb")
        finalVerdict.append(list)

        if(self.problemType == 2 and allAC == False):
            finalVerdict[1] = 0
        
        self.verdict.append(finalVerdict)

    """
    For each test case file, generating result i.e. this method returns a matrix on (N+1)x5, where N is the number of testcases
    
    [Verdict, Score, Time Taken, Memory Taken, Remarks]

    The last row of the matrix returns the final output of the problem
    """
    def executeJudge(self):
        
        self.runQuery()
        self.trimResult()
        self.fetchResult()
        self.grade()
        return self.verdict

if __name__ == "__main__":
    
    # judge = Judge()
    count=0
    # judge.judgeConfigFile =  b"CallOJ/media/judgeConfiguration/config.yml"
    # judge.solutionCode = "1.java"
    # judge.problemCode = "XYZ"
    # judge.languageCode = "JAVA8" 
    # judge.timeLimit = "1"
    # judge.memoryLimit = "65000"
    # judge.problemType = 2 #ICPC type
    
    # x = judge.executeJudge()
    # print(x)
    #output = Judge.trimResult(None, output)
    
    #print(list[1])