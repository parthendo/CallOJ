import logging


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def registerLog(level, method, username, function, activity, IP):

	log = logging.getLogger('CallOJLogs')
	staticLogInfo = {'clientip': IP, 'user': username}
	if level == "INFO":
		log.info('"'+ method + ' '+ username + ' '+ function +' '+ activity +'"', extra = staticLogInfo)
	elif level == "ERROR":
		log.error('"'+ method + ' '+ username + ' '+ function +' '+ activity +'"', extra = staticLogInfo)
	else:
		log.debug('"'+ method + ' '+ username + ' '+ function +' '+ activity +'"', extra = staticLogInfo)