from .models import Contest,IoiMarks,IcpcMarks
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
        if timeElapsed.seconds>=contestTimePeriod:
            return "contestEnded" 

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



