
from django.conf import settings 
from django.core.mail import send_mail, send_mass_mail
import OJ.settings
from django.core.mail import EmailMessage


class alertEmail:
	
	def alertMassUsers(self, userList, subject, message):
		msg = []
		sender_email = OJ.settings.EMAIL_HOST_USER
		for user in userList:
			temp = (subject, message, sender_email, [user])
			msg.append(temp)
		send_mass_mail((msg), fail_silently=False)

	def alertSingleUser(self, user, subject, message):
		send_mail = OJ.settings.EMAIL_HOST_USER
		msg = EmailMessage(subject, message, send_mail, [user])
		msg.send()