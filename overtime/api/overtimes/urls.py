from django.conf.urls import patterns, url

from .views import Add, Index, Details, ApprovedCoordinator, ApprovedManager


urlpatterns = patterns('',
    url(r'^add$', Add.as_view(), name='add'),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^(?P<id>\d+)$', Details.as_view(), name='details'),
    url(r'^approved_coordinator$',
        ApprovedCoordinator.as_view(), name='approved_coordinator'),
    url(r'^approved_manager$',
        ApprovedManager.as_view(), name='approved_manager'),
)
