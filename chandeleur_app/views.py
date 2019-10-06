import logging
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


logger = logging.getLogger('chandeleur_app.views')


# handle errors
def on_error(text, will_send_mail=True):
    logger.error(text)
    mails = [admin[1] for admin in settings.ADMINS]
    if will_send_mail:
        send_mail('Error from foyerduporteau.net', text, 'foyerduporteau@gmail.com', mails, fail_silently=False)
