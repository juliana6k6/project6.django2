from django.contrib import admin

from mail.models import Client, MailAttempt, Mailing, Message

admin.site.register(Client)

admin.site.register(Mailing)

admin.site.register(MailAttempt)

admin.site.register(Message)
