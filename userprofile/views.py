from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib import auth
# Create your views here.
def profileView(request):
    return render(request,'profilepage.html')

def updateProfileView(request):
    return render(request,'updateProfile.html')

def changesToProfileView(request):
    current_user=request.user
    username = request.POST["username"]
    firstName = request.POST["firstName"]
    lastName = request.POST["lastName"]
    email = request.POST["email"]
    password1 = request.POST["password1"]
    password2 = request.POST["password2"]
    all_users = User.objects.all()
    credentials_exist = 0
    password_ok = 0
    if password1 != password2:
        messages.info(request,'Password did not match')
        return HttpResponseRedirect('/userprofile/updateProfile/')
    if request.user.username != username:
        for user in all_users:
            if user.username!=request.user.username and user.username == username:
                messages.info(request,'Username already exist')
                return HttpResponseRedirect('/userprofile/updateProfile/')
    password_length = len(password1)
    current_user.username = username
    current_user.first_name = firstName
    current_user.last_name = lastName
    if password_length!=0:
        print("Change Hogaya Bhyii")
        current_user.set_password(password1)
    current_user.save()
    if password_length!=0:
        auth.logout(request)
        messages.info(request,'Password successfully changed please login again')
        return HttpResponseRedirect('/')
    return render(request,'profilepage.html')
    







