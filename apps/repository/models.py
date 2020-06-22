from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from base.interface import BaseModel
from django.utils import timezone
import os
import datetime
from uuid import uuid4
from django.core.exceptions import ValidationError
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User


def validate_file_size(value):
    file_size = value.size

    if file_size > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value


def re_path(instance, filename, bucket):
    now = datetime.datetime.now()
    upload_to = '{}/guess/{}/'.format(bucket, str(now.year) + str(now.month) + str(now.day))
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


def path_and_rename(instance, filename):
    return re_path(instance, filename, 'git-analytic/images')


# Create your models here.

class Media(BaseModel):
    title = models.CharField(max_length=120, blank=True)
    description = models.CharField(max_length=200, blank=True)
    path = ImageField(upload_to=path_and_rename, max_length=500, validators=[validate_file_size])
    user = models.ForeignKey(User, related_name='medias', on_delete=models.SET_NULL, blank=True, null=True)


class GitUser(BaseModel):
    username = models.CharField(max_length=120)
    git_id = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    avatar_url = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    links = JSONField(null=True, blank=True)


class Taxonomy(BaseModel):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=500, null=True, blank=True)
    slug = models.CharField(max_length=125, null=True, blank=True)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.SET_NULL, null=True, blank=True)
    options = JSONField(null=True, blank=True)
    flags = ArrayField(models.CharField(max_length=50, null=True, blank=True), null=True, blank=True)
    visible = models.BooleanField(default=False)

    def all_children(self):
        out = []
        child = self.children.all()
        if not child:
            return []
        for c in child:
            out.append(c)
            out = out + list(c.all_children())
        return out

    def __str__(self):
        return self.name


class Repository(BaseModel):
    name = models.CharField(max_length=120)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    options = JSONField(null=True, blank=True)
    point = models.FloatField(default=0)
    date_published = models.DateTimeField(default=timezone.now)

    read_me = models.TextField(null=True, blank=True)
    id_github = models.CharField(max_length=300, null=True, blank=True)
    id_npm = models.CharField(max_length=300, null=True, blank=True)
    data_npm = JSONField(null=True, blank=True)
    data_github = JSONField(null=True, blank=True)
    data_source = JSONField(null=True, blank=True)
    data_meta = JSONField(null=True, blank=True)
    last_fetch = models.DateTimeField(default=timezone.now)
    score = JSONField(null=True, blank=True)
    medias = models.ManyToManyField(Media, related_name="repositories", blank=True)

    author = models.ForeignKey(GitUser, related_name="repositories", null=True, blank=True, on_delete=models.CASCADE)
    taxonomies = models.ManyToManyField(Taxonomy, related_name="repositories", blank=True)
    contributes = models.ManyToManyField(GitUser, related_name="contribute_repositories", blank=True)
