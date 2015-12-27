from django.conf.urls import url
import catatan.views

urlpatterns = [
    url(r'^$', catatan.views.post_list, name='post_list'),
]