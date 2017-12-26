from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', auth_views.login, kwargs={'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, kwargs={'next_page': '/'}, name='logout'),

    path('feed/', include('app.urls')),
    path('', RedirectView.as_view(permanent=False, pattern_name='list_feeds')),

    path('admin/', admin.site.urls),
]
