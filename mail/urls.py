from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from mail.apps import MailConfig
from mail.views import (ClientCreateView, ClientDeleteView, ClientListView,
                        ClientUpdateView, MailAttemptListView,
                        MailingCreateView, MailingDeleteView,
                        MailingDetailView, MailingListView, MailingUpdateView,
                        MainPageView, MessageCreateView, MessageListView, ClientDetailView, toggle_activity_status)


app_name = MailConfig.name


urlpatterns = [
    path("mainpage/", cache_page(60)(MainPageView.as_view()), name="main_page"),
    path("mailingdetails/<int:pk>/", MailingDetailView.as_view(), name="mailing_details"),
    path("mailingcreate/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailingupdate/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailingdelete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("messagelist/", MessageListView.as_view(), name="message_list"),
    path("messagecreate/", MessageCreateView.as_view(), name="message_create"),
    path("mailattemptlist/", MailAttemptListView.as_view(), name="mailattempt_list"),
    path("clientlist/", ClientListView.as_view(), name="client_list"),
    path("clientcreate/", ClientCreateView.as_view(), name="client_create"),
    path("clientdetails/<int:pk>/", ClientDetailView.as_view(), name="client_details"),
    path("clientupdate<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("clientdelete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path('mailingactivity/<int:pk>/', toggle_activity_status, name='mailing_activity'),
    path("", MailingListView.as_view(), name="mailing_list")]
