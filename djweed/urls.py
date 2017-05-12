from django.conf.urls import url
from .views import get_file

urlpatterns = [
    url('^(?P<content_type_id>\d+)/(?P<object_id>\d+)/(?P<field_name>[\w\_]+)/(?P<file_name>[\w\.\_\-]*)$', get_file, name='weedfs_get_file')
]
