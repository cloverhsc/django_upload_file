# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
import hashlib


# Create your models here.
class BookManager(models.Manager):
    def create_book(self, **extra_field):
        md5obj = hashlib.md5()
        md5obj.update(extra_field['title'])
        md5 = md5obj.hexdigest()

        bk = self.model(
            md5=md5,
            **extra_field
        )
        bk.save()
        return bk


class Book(models.Model):
    objects = BookManager()
    title = models.CharField(max_length=64, unique=True)
    author = models.CharField(max_length=128, null=True, blank=True)
    md5 = models.CharField(max_length=64)
    date = models.DateField(auto_now=True)

    REQUIRED_TITLE = ['title']
    USERNAME_FIELD = 'title'

    class Meta:
        db_table = 'Book'
        ordering = ['title']


class Device(models.Model):
    AUTH_TYPE_NONE = 0
    AUTH_TYPE_PLAIN = 1
    AUTH_TYPE_MD5 = 2
    AUTH_TYPE_SHA1 = 3

    AUTH_TYPE_CHOICES = (
        (AUTH_TYPE_NONE, 'None'),
        (AUTH_TYPE_PLAIN, 'Plain'),
        (AUTH_TYPE_MD5, 'MD5'),
        (AUTH_TYPE_SHA1, 'SHA1'),
    )

    device_id = models.CharField(max_length=50, primary_key=True, unique=True)
    auth_type = models.IntegerField(
        choices=AUTH_TYPE_CHOICES, default=AUTH_TYPE_NONE)
    version = models.CharField(max_length=250)
    modified_date = models.DateTimeField(auto_now=True)

    REQUIRED_TITLE = ['device_id']
    USERNAME_FIELD = 'device_id'

    def __str__(self):
        return self.device_id


# The FW path and filename
def generate_fw_path(instance, filename):
    return "uploaded_files/{0}".format(filename)


class FilesManager(models.Manager):
    def up_save(self, fw, **extra_filed):
        md5obj = hashlib.md5()
        for chunk in fw.chunks():
            md5obj.update(chunk)
        md5 = md5obj.hexdigest()
        size = fw.size

        print('----md5: {0}'.format(md5))
        print('----size: {0}'.format(size))
        file = self.model(
            fw=fw,
            md5=md5,
            size=size,
            **extra_filed
        )
        file.save()
        return file


class Files(models.Model):
    objects = FilesManager()
    md5 = models.CharField(max_length=128, primary_key=True, unique=True)
    fw = models.FileField(upload_to=generate_fw_path)
    size = models.IntegerField()
    date = models.DateField(auto_now=True)

    REQUIRED_FIELD = ['fw']

    def __str__(self):
        return self.fw


class TempUrl(models.Model):
    url_token = models.CharField(
        max_length=128, blank=False, null=False,
        primary_key=True, unique=True)
    expire_time = models.DateTimeField(blank=True)
    target_file = models.ForeignKey(Files)

    class Meta:
        db_table = "TempUrl"

    def __str__(self):
        return self.url_token

    def expiretime(self):
        return unicode(self.expire_time)

    def path(self):
        return self.target_file
