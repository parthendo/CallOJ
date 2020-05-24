from .models import Contest,IoiMarks,IcpcMarks
from problems.models import Question
from datetime import datetime, timedelta
from django.contrib.auth.models import User
import time
class ContestUtilities:
    def contestFinished(self,contest_id):
        datetimeFormat = '%Y-%m-%d %H:%M:%S'
        now = datetime.now()
        current = str(now)
        current = current[0:19]
        contest = Contest.objects.get(id=contest_id)
        print('Ho',contest_id)
        startYear = contest.startYear
        startMonth = contest.startMonth
        startDay = contest.startDay
        startHours = contest.startHours
        startMinutes = contest.startMinutes
        durationHours = contest.durationHours
        durationMinutes = contest.durationMinutes
        contestStart = str(startYear)+ "-" + str(startMonth)+ "-" + str(startDay)+" "+str(startHours)+ ":"+str(startMinutes)+":"+ "00"
        timeElapsed = datetime.strptime(current, datetimeFormat)-datetime.strptime(contestStart, datetimeFormat)
        contestTimePeriod = (durationHours*60*60) + (durationMinutes*60)
        print(contestTimePeriod)
        print(timeElapsed.seconds)
        if timeElapsed.seconds>=contestTimePeriod:
            return "contestEnded" 
    
    # Tells the state of a cotest i.e.
    # 0 for contest is in past
    # 1 for contest is in future
    # 2 for contest is running
    def contestState(self,contest_id):
        currentTimeStamp = datetime.now()
        contest = Contest.objects.get(id=contest_id)
        startYear = contest.startYear
        startMonth = contest.startMonth
        startDay = contest.startDay
        startHours = contest.startHours
        startMinutes = contest.startMinutes
        durationHours = contest.durationHours
        durationMinutes = contest.durationMinutes
        contestTimeStamp = datetime(int(startYear), int(startMonth), int(startDay), int(startHours), int(startMinutes),int(0))
        startMinutes = int(startMinutes) + int(durationMinutes)
        if(startMinutes >= 60):
            startHours = startHours + 1
            startMinutes = startMinutes % 60
        startHours = int(startHours) + int(durationHours)
        if(startHours >= 24):
            startDay = startDay + 1
            startHours = startHours % 24
        contestEndTimeStamp = datetime(int(startYear), int(startMonth), int(startDay), int(startHours), int(startMinutes),int(0))
        if(currentTimeStamp<contestTimeStamp):
            return 1
        elif(currentTimeStamp>=contestTimeStamp and currentTimeStamp<contestEndTimeStamp):
            return 2
        else:
            return 0

    def ioiRanklist(self,contest_id):
        print('Kadam')
        currentContestEntries = []
        final_list = []
        contestants = []
        mydict = {}
        currentContest = Contest.objects.get(id=contest_id)
        contestEntries = IoiMarks.objects.all()
        print(contestEntries)
        for contest in contestEntries:
            if contest.contestId_id == contest_id and contest.marksAlloted!=0:
                currentContestEntries.append(contest)
                participant = User.objects.get(id=contest.userId_id)
                contestants.append(participant.username)
        contestants = list(set(contestants))
        for contestant in contestants:
            mydict[contestant] = [0,0]
    
        for entry in currentContestEntries:
            participant = User.objects.get(id=entry.userId_id)
            if entry.marksAlloted != 0:
                mydict[participant.username][1] = mydict[participant.username][1] + entry.marksAlloted

        for item in mydict:
	        print(item,mydict[item][0],mydict[item][1])
	        temp=[mydict[item][0],item,mydict[item][1]]
	        final_list.append(temp)
        print(final_list)
        final_list.sort(key=lambda x: (-x[2]))
        rank = 1
        for count in range(len(final_list)):
            skiprank = 1
            if count==0:
                final_list[0][0]=rank
                continue
            if final_list[count][2] == final_list[count-1][2]:
                index=count
                for newcount in range(index,len(final_list)):
                    if final_list[newcount][2] == final_list[newcount-1][2]:
                        final_list[newcount][0] = final_list[newcount-1][0]
                        skiprank = skiprank+1
                    else:
                        count = newcount-1
                        rank = final_list[newcount-1][0]+skiprank
                        break
            else:
                final_list[count][0] = rank
        return final_list
    
    def icpcRanklist(self,contest_id):
        print('Kabutar')
        currentContestEntries = []
        final_list = []
        contestants = []
        mydict = {}
        contestEntries = IcpcMarks.objects.all()
        print(contestEntries)
        for contest in contestEntries:
            if contest.contestId_id == contest_id and contest.verdict==1:
                currentContestEntries.append(contest)
                participant = User.objects.get(id=contest.userId_id)
                contestants.append(participant.username)
        contestants = list(set(contestants))
        for contestant in contestants:
            mydict[contestant] = [0,0]
    
        for entry in currentContestEntries:
            participant = User.objects.get(id=entry.userId_id)
            if entry.verdict == 1:
                mydict[participant.username][0] = mydict[participant.username][0] + 1
                mydict[participant.username][1] = mydict[participant.username][1] + entry.totalTime

        for item in mydict:
	        print(item,mydict[item][0],mydict[item][1])
	        temp=[item,mydict[item][0],mydict[item][1]]
	        final_list.append(temp)
        print(final_list)
        final_list.sort(key=lambda x: (-x[1], x[2]))
        print('Udd')
        return final_list

    def getContests(self):
        all_contests = Contest.objects.all()
        present_contests = []
        future_contests = []
        past_contests = []
        now = datetime.now()
        current = str(now)
        server_year = current[:4]
        server_month = current[5:7]
        server_day = current[8:10]
        server_hours = current[11:13]
        server_minutes = current[14:16]
        print('Hi',server_year,server_month,server_day,server_hours,server_minutes)
        print('Holla',int(server_year),int(server_month),int(server_day),int(server_hours),int(server_minutes))
        for contest in all_contests:
            if contest.startYear>int(server_year):
                future_contests.append(contest)
                continue
            if contest.startYear==int(server_year) and contest.startMonth>int(server_month):
                future_contests.append(contest)
                continue
            if contest.startYear==int(server_year) and contest.startMonth==int(server_month) and contest.startDay>int(server_day):
                future_contests.append(contest)
                continue
            if contest.startYear==int(server_year) and contest.startMonth==int(server_month) and contest.startDay==int(server_day) and contest.startHours>int(server_hours):
                future_contests.append(contest)
                continue
            if contest.startYear==int(server_year) and contest.startMonth==int(server_month) and contest.startDay==int(server_day) and contest.startHours==int(server_hours) and contest.startMinutes>int(server_minutes):
                future_contests.append(contest)
                continue
            present_contests.append(contest)
    
        return present_contests,future_contests

    def submitProblem(self,x,contest_id,problem_id,request):
        final_verdict = x[len(x)-1][0]
        marks_obtained = x[len(x)-1][1]
        #Add Code to check whether contest finished or not , if not finished then only update in Icpc_Marks

        contest = Contest.objects.get(id=contest_id)
        print('Ho',contest_id)
        startYear = contest.startYear
        startMonth = contest.startMonth
        startDay = contest.startDay
        startHours = contest.startHours
        startMinutes = contest.startMinutes
        entries = IcpcMarks.objects.all()
        entries_ioi = IoiMarks.objects.all()
        print(entries)
        entry = ()
        entry_ioi = ()
        for item in entries:
            if item.userId_id == request.user.id and item.contestId_id == contest_id and item.questionId_id==problem_id:
                entry = item
                break
        for item in entries_ioi:
            if item.userId_id == request.user.id and item.contestId_id == contest_id and item.questionId_id==problem_id:
                entry_ioi = item
                break
        #1 is for Icpc
        if contest.rankingStyle == 2:
            # entry = IcpcMarks.objects.get(userId_id=request.user.id,contestId_id=contest_id,questionId_id=problem_id)
            if entry:
                if final_verdict == "AC":
                    entry.verdict = 1
                    datetimeFormat = '%Y-%m-%d %H:%M:%S'
                    now = datetime.now()
                    current = str(now)
                    current = current[0:19]
                    # server_year = current[:4]
                    # server_month = current[5:7]
                    # server_day = current[8:10]
                    # server_hours = current[11:13]
                    # server_minutes = current[14:16]
                    # server_seconds = current[17:19]
                    contestStart = str(startYear)+ "-" + str(startMonth)+ "-" + str(startDay)+" "+str(startHours)+ ":"+str(startMinutes)+":"+ "00"
                    timeToSolve = datetime.strptime(current, datetimeFormat)-datetime.strptime(contestStart, datetimeFormat)
                    print("contestStart:",contestStart)
                    entry.totalTime = entry.totalTime + timeToSolve.seconds
                    entry.save()
                else:
                    entry.totalTime = entry.totalTime + 1200
                    entry.save()
            else:
                if final_verdict == "AC":
                    verdict = 1
                    datetimeFormat = '%Y-%m-%d %H:%M:%S'
                    now = datetime.now()
                    current = str(now)
                    current = current[0:19]
                    contestStart = str(startYear) + "-" + str(startMonth) + "-" + str(startDay) + " " + str(startHours) + ":" + str(startMinutes) + ":" + "00"
                    print('HelloJayant')
                    print(contestStart)
                    timeToSolve = datetime.strptime(current, datetimeFormat)-datetime.strptime(contestStart, datetimeFormat)
                    # contest_object = Contest.objects.get(id=contest_id)
                    # problem_object = Question.objects.get(id=problem_id)
                    # user_object = User.objects.get(id=request.user.id)
                    newItem = IcpcMarks(userId_id=request.user.id,contestId_id=contest_id,questionId_id=problem_id,totalTime=timeToSolve.seconds,verdict=verdict)
                    newItem.save()
                else:
                    verdict = 0
                    contest_object = Contest.objects.get(id=contest_id)
                    problem_object = Question.objects.get(id=problem_id)
                    user_object = User.objects.get(id=request.user.id)
                    newItem = IcpcMarks(userId_id=request.user.id,contestId_id=contest_id,questionId_id=problem_id,totalTime=1200,verdict=verdict)
                    newItem.save()
        else:
            if entry_ioi:
                entry_ioi.marksAlloted = max(entry_ioi.marksAlloted,marks_obtained)
                entry_ioi.save()
            else:
                newItem = IoiMarks(userId_id=request.user.id,contestId_id=contest_id,questionId_id=problem_id,marksAlloted=marks_obtained)
                newItem.save()



