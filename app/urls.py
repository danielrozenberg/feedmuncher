from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_feeds, name='list_feeds'),
    path('new/', views.new_feed, name='new_feed'),
    path('edit/<slug:slug>/', views.edit_feed, name='edit_feed'),
    path('preview/', views.preview_feed, name='preview_feed'),
    path('update/<slug:slug>/', views.update_feed, name='update_feed'),
    path('really-update/<slug:slug>/', views.really_update_feed, name='really_update_feed'),
    path('delete/<slug:slug>/', views.delete_feed, name='delete_feed'),
    path('serve/<slug:user>/<slug:slug>/', views.serve_feed, name='serve_feed'),
    path('mass-update/', views.mass_update, name='mass_update'),
]
