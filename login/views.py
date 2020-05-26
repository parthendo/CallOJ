from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
import os
import shutil

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
from OJ.loggingUtils import get_client_ip
from OJ.loggingUtils import registerLog

def loginView(request):
    
    username = request.POST['username']
    password = request.POST['pass']
    
    print(username," ",password)
    user = auth.authenticate(username = username, password = password)
    if user is not None and user.is_active:
        auth.login(request,user)
        registerLog('INFO','POST',user.username,'Login','LoginSuccessful',get_client_ip(request))
        return HttpResponseRedirect('/dashboard/')
    else:
        allusers = User.objects.all()
        whichMessageToShow = 1
        for user in allusers:
            if user.username == username and user.password!=password:
                messages.info(request,'Password did not match')
                whichMessageToShow = 2
                registerLog('ERROR','POST',user.username,'Login','IncorrectPassword',get_client_ip(request))
                break
        if whichMessageToShow == 1:
            registerLog('ERROR','POST',username,'Login','UsernameDoesNotExist',get_client_ip(request))
            messages.info(request,'Username does not exist')
        return HttpResponseRedirect('/')

def logoutView(request):
    registerLog('INFO','GET',request.user.username,'Login','UserLogsOut',get_client_ip(request))
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
        registerLog('INFO','GET',user.username,'Login','AccountActivated',get_client_ip(request))
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
            registerLog('ERROR','POST',username,'Login','RegisterationPasswordMismatch',get_client_ip(request))

        # Checking if username or e-mail is already taken
        all_users = User.objects.all()
        for user in all_users:
            # Unique username
            if user.username == username:
                exists = True
                messages.info(request,'Username Taken')
                registerLog('ERROR','POST',username,'Login','RegisterationUsernameTaken',get_client_ip(request))
                break
            # Unique e-mail
            if user.email == email:
                exists = True
                registerLog('ERROR','POST',username,'Login','RegisterationEMailTaken',get_client_ip(request))
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
            shutil.copy("static/images/f.jpg",path)
            renamedPath = path + "/" + username + ".jpg"
            path=path + "/f.jpg"
            os.rename(path,renamedPath)
            new_user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password1)
            registerLog('INFO','POST',username,'Login','NewUserCreated',get_client_ip(request))
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




        