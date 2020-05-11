from django.core.management.base import BaseCommand
from apps.repository.models import Repository, Taxonomy, GitUser
from utils.slug import _slug_strip, vi_slug
from django.db.models import Q
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        q = ~Q(id_github=None) | Q(id_github='')
        queryset = Repository.objects.filter(q)
        for repo in queryset:
            url = repo.id_github.replace("https://github.com/", "")
            r = requests.get("https://api.github.com/repos/" + url,
                             auth=('hoanglam.bk57@gmail.com', 'Hoanganhlam@no99'))
            if r.status_code == 200:
                data = r.json()
                backup = repo.data_github if repo.data_github is not None else {}
                backup["created_at"] = data.get("created_at")
                backup["updated_at"] = data.get("updated_at")
                backup["starsCount"] = data.get("stargazers_count")
                backup["forksCount"] = data.get("forks_count")
                owner = data.get("owner")
                git_user = GitUser.objects.filter(username=owner.get("login")).first()
                if git_user is None:
                    git_user = GitUser(username=owner.get("login"), avatar_url=owner.get("avatar_url"))
                else:
                    git_user.avatar_url = owner.get("avatar_url")
                git_user.save()
                repo.author = git_user
                repo.data_github = backup
                if repo.full_name is None:
                    repo.full_name = url
                repo.save()
                print(repo.id)
