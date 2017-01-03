from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_feeds, name='list_feeds'),
    url(r'^new/$', views.new_feed, name='new_feed'),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.edit_feed, name='edit_feed'),
    url(r'^preview/$', views.preview_feed, name='preview_feed'),
    url(r'^update/(?P<slug>[-\w]+)/$', views.update_feed, name='update_feed'),
    url(r'^really-update/(?P<slug>[-\w]+)/$', views.really_update_feed, name='really_update_feed'),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.delete_feed, name='delete_feed'),
    url(r'^serve/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', views.serve_feed, name='serve_feed'),
    url(r'^mass-update', views.mass_update, name='mass_update'),
]
