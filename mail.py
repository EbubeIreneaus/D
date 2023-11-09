from django.core.mail import send_mail
class Mail:
	recipient = []
	html_message = None
	message = ''

	def __init__(self, subject, silent_fail=False):
		self.silent_fail = silent_fail
		self.subject = subject

	def send_mail(self):
		send_mail(
			subject= self.subject,
			message= self.message,
			from_email='springfieldinvest<springfieldinvesment@gmail.com>',
			recipient_list= self.recipient,
			fail_silently=self.silent_fail,
			html_message=self.html_message
		)