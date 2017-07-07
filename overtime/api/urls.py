from django.conf.urls import include, patterns, url


urlpatterns = patterns('overtime.api.views',
    url(r'^auth/', include('overtime.api.auth.urls', namespace='auth')),
    url(r'^overtimes/', include('overtime.api.overtimes.urls', namespace='overtimes')),
    url(r'^users/', include('overtime.api.users.urls', namespace='users')),
)
