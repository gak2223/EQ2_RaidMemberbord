AUTH_RESPONSE_BODY = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<title>401 Authorization Required</title>
</head>
<body>401 Authorization Required</body>
</html>"""

userDict = {'colgate':'dfl',
			'eriik':'ill',
			'dog':'manjo'
			}

def auth_required_app(environ, start_response, realm):
	start_response('401 Authorization Required', [
		('WWW-Authenticate', 'Basic realm="%s"' % realm),
		('Content-Type', 'text/html; charset=iso-8859-1'),
	])
	return AUTH_RESPONSE_BODY

class AuthMiddleware(object):
	def __init__(self, application, realm, username, password):
		self.application = application
		self.realm = realm
		self.username = username
		self.password = password

	def get_token(self):
		import base64
		return base64.b64encode('%s:%s' % (self.username, self.password))

	def get_auth_basic_header(self):
		return 'Basic %s' % self.get_token()

	def __call__(self, environ, start_response):
		auth_header = environ.get('HTTP_AUTHORIZATION')
		#if ((auth_header) and (auth_header == self.get_auth_basic_header())):
		if (auth_header):
			for key in userDict.keys():
				self.username = key
				self.password = userDict[key]
				if(auth_header == self.get_auth_basic_header()):
					return self.application(environ, start_response)
		return auth_required_app(environ, start_response, self.realm)