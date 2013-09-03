from django.conf.urls import patterns, include, url
from manssh import views
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name='index'),
    url(r'^manssh/?$', views.index, name='index'),
    url(r'^manssh/getKeyByIndex.*$', views.getKeyByIndex, name='index'),
    url(r'^manssh/getKeys.*$', views.getKeys, name='index'),
    url(r'^manssh/saveKey.*$', views.saveKey, name='index'),
    url(r'^manssh/deleteKey.*$', views.deleteKey, name='index'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': settings.STATIC_ROOT,
          'show_indexes': True }),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': settings.MEDIA_ROOT,
          'show_indexes': True }),
)
