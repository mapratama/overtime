from django.conf.urls import patterns, url

from .views import Get


urlpatterns = patterns('',
    url(r'^$', Get.as_view(), name='get')
)
