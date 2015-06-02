from django.conf.urls import url

urlpatterns = [
    url(r'^/$', 'app.views.list_feeds', name='list_feeds'),
    url(r'^/new/$', 'app.views.new_feed', name='new_feed'),
    url(r'^/edit/(?P<slug>[-\w]+)/$', 'app.views.edit_feed', name='edit_feed'),
    url(r'^/preview/$', 'app.views.preview_feed', name='preview_feed'),
    url(r'^/update/(?P<slug>[-\w]+)/$', 'app.views.update_feed', name='update_feed'),
    url(r'^/really-update/(?P<slug>[-\w]+)/$', 'app.views.really_update_feed', name='really_update_feed'),
    url(r'^/delete/(?P<slug>[-\w]+)/$', 'app.views.delete_feed', name='delete_feed'),
    url(r'^/serve/(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$', 'app.views.serve_feed', name='serve_feed'),
    url(r'^/mass-update', 'app.views.mass_update', name='mass_update'),
]