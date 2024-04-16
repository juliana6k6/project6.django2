from django.urls import path
from mail.views import MainPageView
from django.views.decorators.cache import cache_page
from django.conf.urls.static import static
from django.conf import settings


app_name = 'mailing'


urlpatterns = \
    [path('', cache_page(60)(MainPageView.as_view()), name='main_page'),
     ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



