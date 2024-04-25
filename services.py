from datetime import datetime, timedelta
from smtplib import SMTPException

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mail.models import Mailing, MailAttempt


class StyleFormMixin:
    """Стилизация форм."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


def change_status(mailing, time) -> None:
    if mailing.mailing_status == 'created':
        mailing.mailing_status = 'started'
        print('started')
    elif mailing.mailing_status == 'started' and mailing.stop_datetime_mailing <= time:
        mailing.mailing_status = 'finished'
        print('finished')
    mailing.save()


def change_start_datetime_mailing(mailing, time):
    if mailing.start_datetime_mailing < time:
        if mailing.mailing_period == 'every_day':
            mailing.start_datetime_mailing += timedelta(days=1)
        elif mailing.mailing_period == 'every_week':
            mailing.start_datetime_mailing += timedelta(days=7)
        elif mailing.mailing_period == 'every_month':
            mailing.start_datetime_mailing += timedelta(days=30)
        mailing.save()


def my_job():
    print('my_job работает')
    now = datetime.now()
    timenow = timezone.make_aware(now, timezone.get_current_timezone())
    mailings = Mailing.objects.filter(is_active=True)
    if mailings:
        for mailing in mailings:
            change_status(mailing, timenow)
            if mailing.start_datetime_mailing <= timenow <= mailing.stop_datetime_mailing:
                for client in mailing.clients.all():
                    try:
                        response = send_mail(
                            subject=mailing.message.title,
                            message=mailing.message.body,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[client.contact_email],
                            fail_silently=False
                        )
                        mailing_log = MailAttempt.objects.create(
                            attempt_time=mailing.start_datetime_mailing,
                            attempt_status="Success",
                            server_response=True,
                            mailing=mailing,
                            client=client
                        )
                        mailing_log.save()
                        change_start_datetime_mailing(mailing, timenow)
                        print("mailing_log сохранен")
                    except SMTPException as error:
                        mailing_log = MailAttempt.objects.create(
                            attempt_time=mailing.start_datetime_mailing,
                            attempt_status="Non-success",
                            server_response=False,
                            mailing=mailing,
                            client=client
                        )
                        mailing_log.save()
                        print(error)
    else:
        print('no mailings')


