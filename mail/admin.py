from django.contrib import admin

from mail.models import Client, Mailing, Message, Mail_attempt


admin.site.register(Client)

admin.site.register(Mailing)

admin.site.register(Mail_attempt)

admin.site.register(Message)
