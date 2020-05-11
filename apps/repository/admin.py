from django.contrib import admin
from apps.repository.models import Media, GitUser, Taxonomy, Repository

# Register your models here.
admin.site.register((Media, Taxonomy, Repository, GitUser))
