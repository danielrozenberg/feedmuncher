from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from app import urls as app_urls

urlpatterns = [
    url(r'^login/$', auth_views.login, kwargs={'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, kwargs={'next_page': '/'}, name='logout'),

    url(r'^feed/', include(app_urls.urlpatterns)),
    url(r'^$', RedirectView.as_view(permanent=False, pattern_name='list_feeds')),

    url(r'^admin/', include(admin.site.urls)),
]
