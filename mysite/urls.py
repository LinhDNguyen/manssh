from django.conf.urls import patterns, include, url
from manssh import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name='index'),
    url(r'^manssh/?$', views.index, name='index'),
    url(r'^manssh/getKeyByIndex.*$', views.getKeyByIndex, name='index'),
    url(r'^manssh/getKeys.*$', views.getKeys, name='index'),
    url(r'^manssh/saveKey.*$', views.saveKey, name='index'),
    url(r'^manssh/deleteKey.*$', views.deleteKey, name='index'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': '/home/linh/temp/mysite/static',
          'show_indexes': True }),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': '/home/linh/temp/mysite/media',
          'show_indexes': True }),
)
