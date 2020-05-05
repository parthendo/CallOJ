from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib import auth
# from .models import User
from django.contrib.auth.models import User
from problems.models import AllProblems
def loginView(request):
    #print(request.POST['username'],request.POST['pass'])
    # insertInProblems = 1
    # if(insertInProblems == 1):
    #     problemCode1 = "ABC"
    #     problemName1 = "Add Two Numbers"
    #     problemStatement1 = "Given two numbers a and b , print their Sum."
    #     timeLimit1 = 2.0
    #     memoryLimit1 = 65573
    #     creator1 = "Jayant0730"
    #     editorialist1 = "Jayant0730"
    #     problem1 = AllProblems(problemCode=problemCode1,problemName=problemName1,problemStatement=problemStatement1,timeLimit=timeLimit1,memoryLimit=memoryLimit1,creator=creator1,editorialist=editorialist1)
    #     problem1.save()
    #     problemCode2 = "XYZ"
    #     problemName2 = "XOR"
    #     problemStatement2 = "Perform XOR of two numbers and return the output ."
    #     timeLimit2 = 1.0
    #     memoryLimit2 = 65573
    #     creator2 = "Parth74"
    #     editorialist2 = "Parth74"
    #     problem2 = AllProblems(problemCode=problemCode2,problemName=problemName2,problemStatement=problemStatement2,timeLimit=timeLimit2,memoryLimit=memoryLimit2,creator=creator2,editorialist=editorialist2)
    #     problem2.save()
    # invalid = 1
    # userfound = 0
    username = request.POST['username']
    password = request.POST['pass']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request,user)
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/')
    # all_users = User.objects.all()
    # for user in all_users:
    #     if user.userid == username:
    #         userfound=1
    #         if user.password == password:
    #             invalid = 0
    #             break
    #         else:
    #             messages.info(request,'Password did not match')
    #             break
    # if userfound==0:
    #     messages.info(request,'Username is not valid')
    #loop through all the users in the user table
    #if username matches but password does not match
    # if invalid == 1:
    #     return HttpResponseRedirect('/')
    # else:
    #     return HttpResponseRedirect('/dashboard/')
    #else
    #render to the dashboard page

    #return HttpResponseRedirect('/thanks/')
    # if request.method == 'POST':

    #     form = NameForm(request.POST)

    #     if form.is_valid():
    #         print(form.cleaned_data['your_name'])
    #         your_name = form.cleaned_data['your_name']
    #         your_pass = form.cleaned_data['your_pass']
    #         your_code = form.cleaned_data['your_code']
    #         sender = form.cleaned_data['sender']
    #         cc_myself = form.cleaned_data['cc_myself']
    #         recipients = ['jayant.tiwari@iiitb.org']
    #         if cc_myself:
    #             recipients.append(sender)
    #        # send_mail(your_name,your_code,sender,recipients)
    #         return HttpResponseRedirect('/thanks/')
    # else:
    #     form = NameForm()
    # return render(request,'home.html',{'form':form})
# Create your views here.

#def initial_view(request):
 #   return render(request,'home.html',{'form':form})

def logoutView(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def initialView(request):
    return render(request,'index.html')

def registerView(request):
    return render(request,'registration.html')

def saveUserView(request):
    exists = 0
    username = request.POST['username']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']

    email = request.POST['mail']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    if(password1!=password2):
        messages.info(request,'Password did not match')
        exists = 1
    all_users = User.objects.all()
    for user in all_users:
        if user.username == username:
            exists = 1
            messages.info(request,'Username Taken')
            break
        if user.email == email:
            exists = 1
            messages.info(request,'Email Taken')
            break
    
    #loop through all the users if at any point username matches set exists=1 and break

    if exists == 0:
        new_user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password1)
        new_user.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/registration/')




        