from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from mail.views import (ClientCreateView, ClientDeleteView, ClientListView,
                        ClientUpdateView, MailAttemptListView,
                        MailingCreateView, MailingDeleteView,
                        MailingDetailView, MailingListView, MailingUpdateView,
                        MainPageView, MessageCreateView, MessageListView)

app_name = "mailing"


urlpatterns = [
    path("", cache_page(60)(MainPageView.as_view()), name="main_page"),
    path("mailinglist/", MailingListView.as_view(), name="mailing_list"),
    path(
        "mailingdetails/<int:pk>/", MailingDetailView.as_view(), name="mailing_details"
    ),
    path("mailingcreate/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailingupdate/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailingdelete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("messagelist/", MessageListView.as_view(), name="message_list"),
    path("messagecreate/", MessageCreateView.as_view(), name="message_create"),
    path("mailattemptlist/", MailAttemptListView.as_view(), name="mailattempt_list"),
    path("clientlist/", ClientListView.as_view(), name="client_list"),
    path("clientcreate/", ClientCreateView.as_view(), name="client_create"),
    path("clientupdate<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("clientdelete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
