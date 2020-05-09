from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
# Create your views here.
def profileView(request):
    return render(request,'profilepage.html')

def updateProfileView(request):
    return render(request,'updateProfile.html')

def changesToProfileView(request):
    logoutAfterChange = 0
    username = request.POST["username"]
    firstName = request.POST["firstName"]
    lastName = request.POST["lastName"]
    email = request.POST["email"]
    password1 = request.POST["password1"]
    password2 = request.POST["password2"]
    all_users = User.objects.all()
    credentials_exist = 0
    password_ok = 0
    if request.user.username == username:
        logoutAfterChange=0
    else:
        logoutAfterChange=1

    for instance in all_users:
        if instance.username == username and username!=request.user.username:
            credentials_exist=1
            break
        if instance.username != request.user.username and instance.email == email:
            credentials_exist=1
            break
            
    
    if password1 == password2:
        password_ok = 1

    print(credentials_exist," ",password_ok)
    if credentials_exist==0 and password_ok==1:
        User.objects.filter(username=request.user.username).update(username=username,first_name=firstName,last_name=lastName,email=email,password=password1)
        auth.logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/userprofile/updateProfile/')






