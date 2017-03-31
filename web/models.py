# -*- coding: utf-8 -*-
from django.db import models
import hashlib


# Create your models here.
class Model(models.Model):
    '''
        Production model name. EX: Babycam, Personal Cloud, ....etc
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    desc = models.CharField(blank=True, max_length=256, null=True)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELD = ['name']

    class Meta:
        db_table = 'Model'
        ordering = ['name']

    def __str__(self):
        return self.name

    def raw_data(self):
        return (self.id, self.name, self.desc)

    def description(self):
        return self.desc


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
    title = models.CharField(max_length=64, unique=True, primary_key=True)
    author = models.CharField(max_length=128, null=True, blank=True)
    md5 = models.CharField(max_length=64)
    date = models.DateField(auto_now=True)

    REQUIRED_TITLE = ['title']
    USERNAME_FIELD = 'title'

    class Meta:
        db_table = 'Book'
        ordering = ['title']


class DeviceManager(models.Manager):
    def create_dev(self, device_id, auth_type, model, **kwargs):
        AUTH_TYPE_NONE = 0
        AUTH_TYPE_PLAIN = 1
        AUTH_TYPE_MD5 = 2
        AUTH_TYPE_SHA1 = 3
        if auth_type == AUTH_TYPE_PLAIN:
            passwd = device_id + model.name
        elif auth_type == AUTH_TYPE_MD5:
            passwd = hashlib.md5(device_id + model.name).hexdigest()
        elif auth_type == AUTH_TYPE_SHA1:
            print(model.name)
            passwd = hashlib.sha1(device_id + model.name).hexdigest()
        else:
            passwd = ''

        dev = self.model(
            device_id=device_id,
            auth_type=auth_type,
            model=model,
            passwd=passwd,
            **kwargs
        )
        dev.save(using=self._db)
        return dev


class Device(models.Model):
    objects = DeviceManager()
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
    model = models.ForeignKey(Model)
    passwd = models.CharField(max_length=256, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.auth_type == self.AUTH_TYPE_PLAIN:
            self.passwd = self.device_id + self.model.name
        elif self.auth_type == self.AUTH_TYPE_MD5:
            print('------- here -----')
            self.passwd = hashlib.md5(self.device_id + self.model.name).hexdigest()
            print(self.model.name)

        elif self.auth_type == self.AUTH_TYPE_SHA1:
            self.passwd = hashlib.sha1(self.device_id + self.model.name).hexdigest()
        else:
            self.passwd = ''
        super(Device, self).save(*args, **kwargs)

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


class Session(models.Model):
    RESULT_UNKNOWN = 0
    RESULT_SUCCESSFUL = 200
    RESULT_CLIENT_ERROR = 400
    RESULT_USER_CANCELED = 401
    RESULT_PACKAGE_CORRUPT = 402
    RESULT_PACKAGE_MISMATCH = 403
    RESULT_SIGNATURE_FAILED = 404
    RESULT_NOT_ACCEPTABLE = 405
    RESULT_AUTH_FAILED = 406
    RESULT_REQUEST_TIMEOUT = 407
    RESULT_NOT_IMPLEMENTED = 408
    RESULT_UNDEFINED_ERROR = 409
    RESULT_UPDATE_FAILED = 410
    RESULT_BAD_URL = 411
    RESULT_DOWNLOAD_SERVER_UNAVAILABLE = 412
    RESULT_DOWNLOAD_SERVER_ERROR = 500
    RESULT_OUT_OF_MEMORY_FOR_DOWNLOAD = 501
    RESULT_OUT_OF_MEMORY_FOR_UPDATE = 502

    RESULT_CHOICES = (
        (RESULT_UNKNOWN, 'RESULT_UNKNOWN'),
        (RESULT_SUCCESSFUL, 'RESULT_SUCCESSFUL'),
        (RESULT_CLIENT_ERROR, 'RESULT_CLIENT_ERROR'),
        (RESULT_USER_CANCELED, 'RESULT_USER_CANCELED'),
        (RESULT_PACKAGE_CORRUPT, 'RESULT_PACKAGE_CORRUPT'),
        (RESULT_PACKAGE_MISMATCH, 'RESULT_PACKAGE_MISMATCH'),
        (RESULT_SIGNATURE_FAILED, 'RESULT_SIGNATURE_FAILED'),
        (RESULT_NOT_ACCEPTABLE, 'RESULT_NOT_ACCEPTABLE'),
        (RESULT_AUTH_FAILED, 'RESULT_AUTH_FAILED'),
        (RESULT_REQUEST_TIMEOUT, 'RESULT_REQUEST_TIMEOUT'),
        (RESULT_NOT_IMPLEMENTED, 'RESULT_NOT_IMPLEMENTED'),
        (RESULT_UNDEFINED_ERROR, 'RESULT_UNDEFINED_ERROR'),
        (RESULT_UPDATE_FAILED, 'RESULT_UPDATE_FAILED'),
        (RESULT_BAD_URL, 'RESULT_BAD_URL'),
        (RESULT_DOWNLOAD_SERVER_UNAVAILABLE,
         'RESULT_DOWNLOAD_SERVER_UNAVAILABLE'),
        (RESULT_DOWNLOAD_SERVER_ERROR, 'RESULT_DOWNLOAD_SERVER_ERROR'),
        (RESULT_OUT_OF_MEMORY_FOR_DOWNLOAD,
         'RESULT_OUT_OF_MEMORY_FOR_DOWNLOAD'),
        (RESULT_OUT_OF_MEMORY_FOR_UPDATE, 'RESULT_OUT_OF_MEMORY_FOR_UPDATE'),
    )

    device = models.ForeignKey(Device)
    session_id = models.AutoField(primary_key=True, unique=True)
    result = models.IntegerField(
        choices=RESULT_CHOICES, default=RESULT_UNKNOWN)
    time = models.DateTimeField(auto_now=True)

    REQUIRED_FIELD = ['device']

    def __str__(self):
        return self.session_id

    class Meta:
        db_table = 'Session'


class SessionEvent(models.Model):
    EVENT_UNKNOWN = 0
    EVENT_PUSH_NOTIFICATION = 1
    EVENT_FOTA_CHECK = 2
    EVENT_FOTA_REQUEST = 3
    EVENT_FOTA_DOWNLOAD = 4
    EVENT_FOTA_RESULT = 5

    EVENT_CHOICES = (
        (EVENT_UNKNOWN, 'EVENT_UNKNOWN'),
        (EVENT_PUSH_NOTIFICATION, 'EVENT_PUSH_NOTIFICATION'),
        (EVENT_FOTA_CHECK, 'EVENT_FOTA_CHECK'),
        (EVENT_FOTA_REQUEST, 'EVENT_FOTA_REQUEST'),
        (EVENT_FOTA_DOWNLOAD, 'EVENT_FOTA_DOWNLOAD'),
        (EVENT_FOTA_RESULT, 'EVENT_FOTA_RESULT')
    )

    session = models.ForeignKey(Session)
    time = models.DateTimeField(auto_now=True)
    event = models.IntegerField(choices=EVENT_CHOICES, default=EVENT_UNKNOWN)

    REQUIRED_FIELD = ['SESSION']

    def __str__(self):
        return self.EVENT_CHOICES[self.event]

    class Meta:
        db_table = 'SessionEvent'
