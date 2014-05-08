from django.conf.urls import patterns, url

urlpatterns = patterns('djweed.views',
    url('^(?P<content_type_id>\d+)/(?P<object_id>\d+)/(?P<field_name>[\w\_]+)/(?P<file_name>[\w\.\_\-]*)$', 'get_file', name='weedfs_get_file'),
) 
