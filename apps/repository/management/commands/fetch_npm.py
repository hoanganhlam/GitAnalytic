import requests
from django.core.management.base import BaseCommand
from django.db.models import Q

from apps.repository.models import Repository


class Command(BaseCommand):
    def handle(self, *args, **options):
        headers = {'Accept': 'application/vnd.github.mercy-preview+json', 'origin': 'x-requested-with'}
        q = ~Q(id_github=None) | Q(id_github='')
        q = q & Q(taxonomies__slug="vue-loader")
        queryset = Repository.objects.filter(q)
        for repo in queryset:
            url = repo.id_npm.replace("https://www.npmjs.com/package/", "")
            r = requests.get(
                "https://cors-anywhere.herokuapp.com/https://api.npms.io/v2/package/" + url,
                headers=headers)
            if r.status_code == 200:
                data = r.json()
                if data.get("collected").get("npm") is not None:
                    repo.data_npm = data.get("collected").get("npm")
                if data.get("collected").get("github") is not None:
                    repo.data_github = data.get("collected").get("github")
                if data.get("collected").get("source") is not None:
                    repo.data_source = data.get("collected").get("source")
                if data.get("collected").get("metadata") is not None:
                    repo.data_meta = data.get("collected").get("metadata")

                # 2020-04-07T12:46:26.075Z
                repo.last_fetch = data.get("analyzedAt")
                if repo.data_npm is not None:
                    last_download = repo.data_npm.get("downloads")[-1:]
                    if len(last_download) > 0:
                        repo.data_npm["downloadsCount"] = last_download[0].get("count")
                repo.save()
