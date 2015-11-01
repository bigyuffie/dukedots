from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
	url(r'^v1/playerdata', views.handle_post, name='handle_post')
)