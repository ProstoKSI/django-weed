django-weed
===========

This project provides `Weed-FS <https://code.google.com/p/weed-fs/>`_ integration with Django by giving model field. Works with Python 2 and Python 3 with Django 1.8+

Dependencies
============

This project is built on top of `pyweed <https://github.com/utek/pyweed>`_ project which provides Python implementation of API to Weed-FS.

Thus dependencies are:

* configured Weed-fS
* pyseaweed module
* django (tested only with 1.6 now, but should work with early releases as well)


Installation
============

    pip install django-weed

or

    pip install https://github.com/ProstoKSI/django-weed/archive/master.zip

How to use
==========

Add `django-weed` specific constants to your `settings.py`

.. code:: python

    # django-weed
    WEEDFS_MASTER_HOST = 'localhost'  # replace with your SeaweedFS master host
    WEEDFS_MASTER_PORT = 9333  # replace with your SeaweedFS master port
    ALLOW_NGINX_X_ACCEL_REDIRECT = True

`django-weed` provides `WeedFSFileField` model field, so if you have regular `FileField` in your models:

.. code:: python

    class Book(models.Model):
        name = models.CharField(_("Name"), max_length=255)
        content = models.FileField(_("Content"), upload_to=settings.CONTENT_URL)

you can easily convert this `FileField` to `WeedFSFileField`:

.. code:: python

    from djweed.db_fields import WeedFSFileField

    class Book(models.Model):
        name = models.CharField(_("Name"), max_length=255)
        content = WeedFSFileField(_("Content"))

Note: there is no sense in `upload_to` keyword for Weed-FS as it uses flat file id structure.

After that you can use content almost as before.

.. code:: python

    >>> book = Book.objects.get(id=1)
    >>> from django.core.files import File
    >>> book.content = File(open('/tmp/book_content_1.txt'))
    >>> book.save()
    >>> Book.objects.filter(id=1).update(content=File(open('/tmp/book_content_2.txt')))
    >>> book.content.size
    100
    >>> book.content.storage_url
    http://127.0.0.1:9300/3,1f23101a
    >>> book.content.name
    u"3,1f23101a:book_content_2.txt"
    >>> book.content.verbose_name
    u"book_content_2.txt"
    >>> book.content.content[:41]
    u"These are first words in the book content"

Furthermore, `django-weed` has integration with Nginx's X-Accel-Redirect so you can safely serve data from Weed-FS. You have to add `djweed` to your INSTALLED_APPS in settings.py and assign url in urls.py to `djweed.urls`, i.e.:

.. code:: python

    (r'^media/', include('djweed.urls')),

There is no special Nginx configuration as it supports X-Accel-Redirect out of the box and the link will point to the Weed-FS volume.

Once you configured `djweed` you could get url from content:

.. code:: python

    >>> book.content.url
    "/media/15/1/content/book_content_2.txt"
