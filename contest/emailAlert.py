
from django.conf import settings 
from django.core.mail import send_mail, send_mass_mail
import OJ.settings
from django.core.mail import EmailMessage


class alertEmail:
	
	def alertMassUsers(self, userList, subject, message):
		msg = []
		sender_email = 'mike.dent9@gmail.com'
		for user in userList:
			temp = (subject, message, sender_email, [user])
			msg.append(temp)
		send_mass_mail((msg), fail_silently=False)

	def alertSingleUser(self, user, subject, message):
		send_mail = 'mike.dent9@gmail.com'
		msg = EmailMessage(subject, message, send_mail, [user])
		msg.send()
