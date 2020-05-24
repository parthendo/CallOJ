from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
import os
# from .models import User

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from problems.models import AllProblems

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
import logging

log = logging.getLogger('login')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
    d = {'clientip': get_client_ip(request), 'user': request.user}
    log.warning('"GET Login started when logged in"', extra=d)
    username = request.POST['username']
    password = request.POST['pass']
    print(username," ",password)
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request,user)
        d = {'clientip': get_client_ip(request), 'user': request.user}
        log.info('"POST '+user.username+' user logged in"', extra=d)
        return HttpResponseRedirect('/dashboard/')
    else:
        allusers = User.objects.all()
        whichMessageToShow = 1
        for user in allusers:
            if user.username == username and user.password!=password:
                messages.info(request,'Password did not match')
                whichMessageToShow = 2
                break
        if whichMessageToShow == 1:
            messages.info(request,'Username does not exist')
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

# E-mail verification redirect sent from user's email
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        # Redirecting to user's dashboard
        # auth.login(request, user)
        # return HttpResponseRedirect('/dashboard/')
        
        # Redirecting to login page
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Activation link is invalid!')

def saveUserView(request):
    
    if(request.method == 'POST'):
        
        exists = False
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Confirming passwords
        if(password1 != password2):
            messages.info(request,'Password did not match')
            exists = True

        # Checking if username or e-mail is already taken
        all_users = User.objects.all()
        for user in all_users:
            # Unique username
            if user.username == username:
                exists = True
                messages.info(request,'Username Taken')
                break
            # Unique e-mail
            if user.email == email:
                exists = True
                messages.info(request,'Username with this e-mail account already exists')
                break

        #loop through all the users if at any point username matches set exists=1 and break

        if exists == False:
            mode = 0o777
            directory = username
            parentDirPath = os.path.dirname(__file__).rsplit('/',1)[0]
            parent_dir = os.path.join(parentDirPath,'media/submittedFiles')
            path = os.path.join(parent_dir, directory)
            os.mkdir(path,mode)
            new_user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password1)
            # Setting active status for the user false for the email verification
            new_user.is_active = False
            new_user.save()

            # E-mail Verfication 
            current_site = get_current_site(request)
            mail_subject = 'Activate your CallOJ account'
            message = render_to_string('verificationEmail.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                    'token':account_activation_token.make_token(new_user),
                })

            reciever_email = email
            msg = EmailMessage(mail_subject, message, to=[reciever_email])
            msg.send()
            messages.success(request, f'Your account has been created ! You are now able to log in')

            return HttpResponse('Please confirm your email address to complete the registration')
        
        else:
            # Redirects to registeration page in case of invalid inputs
            return HttpResponseRedirect('/registration/')




        