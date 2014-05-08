from datetime import datetime
import os

from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage

from pyweed import WeedFS


DATE_IS_NOT_AVAILABLE = datetime.min


class WeedFSStorage(Storage):
    """
    Weed-FS storage.
    Weed-FS is a simple and highly scalable distributed file system.
    """

    def __init__(self, master_host=None, master_port=None):
        if master_host is None:
            master_host = settings.WEEDFS_MASTER_HOST
        self.master_host = master_host
        if master_port is None:
            master_port = settings.WEEDFS_MASTER_PORT
        self.master_port = master_port
        self.fs = WeedFS(master_host, master_port)

    def get_available_name(self, name):
        return os.path.basename(name)

    def content(self, name):
        return self.fs.get_file(name)

    def _save(self, name, content):
        fid = self.fs.upload_file(stream=content.file, name=name)
        content.close()
        if hasattr(content, 'temporary_file_path'):
            os.remove(content.temporary_file_path())
        return '%s:%s' % (fid, name)

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        self.fs.delete_file(name)

    def exists(self, name):
        return self.fs.file_exists(name)

    def size(self, name):
        return self.fs.get_file_size(name) or 0

    def url(self, name):
        return self.fs.get_file_url(name)

    def accessed_time(self, name):
        return DATE_IS_NOT_AVAILABLE

    def created_time(self, name):
        return DATE_IS_NOT_AVAILABLE

    def modified_time(self, name):
        return DATE_IS_NOT_AVAILABLE
