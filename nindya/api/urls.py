from django.conf.urls import include, patterns, url


urlpatterns = patterns('nindya.api.views',
    url(r'^auth/', include('nindya.api.auth.urls', namespace='auth')),
    url(r'^overtimes/', include('nindya.api.overtimes.urls', namespace='overtimes')),
)
