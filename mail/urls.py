from django.urls import path
from mail.views import MainPageView, MailingListView
from django.views.decorators.cache import cache_page
from django.conf.urls.static import static
from django.conf import settings


app_name = 'mailing'


urlpatterns = [path('', cache_page(60)(MainPageView.as_view()), name='main_page'),
               path('mailinglist/', MailingListView.as_view(), name='mailing_list'),
               path('details/<int:pk>/', MailingDetailView.as_view(), name='mailing_details'),
     ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



