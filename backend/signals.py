from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver, Signal


liked_user_signal = Signal()

@receiver(liked_user_signal)
def liked_signal(emails, names, **kwargs):

    # send an e-mail to the user
    send_mail(
        # title:
        'Взаимная симпатия',
        # message:
        f'«Вы понравились {names[1]}! Почта участника: {emails[1]}».',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [emails[0]]
    )


    send_mail(
        # title:
        'Взаимная симпатия',
        # message:
        f'«Вы понравились {names[0]}! Почта участника: {emails[0]}».',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [emails[1]]
    )