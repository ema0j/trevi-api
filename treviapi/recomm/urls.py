from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from recomm import views

urlpatterns = [
    url(r'^$', views.MusicList.as_view(context_object_name="music_list"), name='view_music_list'),
    url(r'^recomm/$', views.RecommList.as_view()),
    url(r'^recomm/get/(?P<playlist_id>[-\w+&*=% ]+)/(?P<limit>\d+)/$', views.RecommGetLimit.as_view()),
    url(r'^recomm/update/(?P<playlist_id>[-\w+&*=% ]+)/(?P<track>[\w\W]+)/(?P<limit>\d+)/$', views.RecommUpdateLimit.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
