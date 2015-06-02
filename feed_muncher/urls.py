from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
import app

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', kwargs={'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', kwargs={'next_page': '/'}, name='logout'),

    url(r'^feed', include(app.urlpatterns)),
    url(r'^$', RedirectView.as_view(permanent=False, pattern_name='list_feeds')),

    url(r'^admin/', include(admin.site.urls)),
]
