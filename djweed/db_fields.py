from django.contrib.contenttypes.models import ContentType
try:
    from django.core.urlresolvers import reverse
except ImportError:  # Django 2.0
    from django.urls import reverse
from django.db.models.fields.files import FieldFile, FileField
from django.utils import six

from .storage import WeedFSStorage


class WeedFSFieldFile(FieldFile):

    def _split_name(self):
        splitted_name = self.name.split(':', 1)
        if len(splitted_name) == 2:
            return splitted_name
        return splitted_name[0], ''

    def _get_storage_fid(self):
        return self._split_name()[0]
    storage_fid = property(_get_storage_fid)

    def _get_verbose_name(self):
        return self._split_name()[1]
    verbose_name = property(_get_verbose_name)

    def _get_content(self):
        self._require_file()
        return self.storage.content(self.storage_fid)
    content = property(_get_content)

    def _get_url(self):
        self._require_file()
        content_type = ContentType.objects.get_for_model(self.instance._meta.model)
        return reverse('weedfs_get_file', kwargs={
            'content_type_id': content_type.id,
            'object_id': self.instance.id,
            'field_name': self.field.name,
            'file_name': self.verbose_name,
        })
    url = property(_get_url)

    def _get_storage_url(self):
        self._require_file()
        return self.storage.url(self.storage_fid)
    storage_url = property(_get_storage_url)


class WeedFSFileField(FileField):

    # The class to wrap instance attributes in. Accessing the file object off
    # the instance will always return an instance of attr_class.
    attr_class = WeedFSFieldFile

    def __init__(self, verbose_name=None, name=None, storage=None, **kwargs):
        kwargs.pop('upload_to', None)
        storage = kwargs.pop('storage', None)
        if storage is None:
            storage = WeedFSStorage()

        super(WeedFSFileField, self).__init__(verbose_name, name,
            storage=storage, **kwargs)

    def get_prep_value(self, value):
        "Returns field's value prepared for saving into a database."
        # Need to convert File objects provided via a form to unicode for database insertion
        if value is None:
            return None
        if isinstance(value, six.string_types):
            return six.text_type(value)
        if value.name == '':
            return ''
        if isinstance(value, WeedFSFieldFile):
            return value.name
        return self.storage.save(None, value)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
