import requests
from django.core.management.base import BaseCommand
from apps.repository.models import Repository, GitUser
from django.db.models import Q

query = """
query ContributorsQuery($packageName: String!){
    package(name: $packageName) {
        collaboratorCount
        collaborators(first: 200) {
            edges {
                node {
                    avatarUrl
                    bio
                    commitCount
                    mergedPullRequestCount
                    name
                    pullRequestCount
                    email
                }
            }
        }
        id
    }
}
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        q = ~Q(id_github=None) & Q(contributes=None)
        queryset = Repository.objects.filter(q)
        url = "https://openbase.io/api/graphql"
        for repo in queryset:
            r = requests.post(url, json={"query": query, "variables": {"packageName": repo.name}})
            if r.status_code == 200:
                data = r.json()
                edges = data.get("data").get("package").get("collaborators").get("edges")
                for edg in edges:
                    git_user = GitUser.objects.filter(email=edg.get("node").get("email")).first()
                    if git_user is None:
                        git_user = GitUser(
                            full_name=edg.get("node").get("name"),
                            avatar_url=edg.get("node").get("avatarUrl"),
                            email=edg.get("node").get("email")
                        )
                        git_user.save()
                    if git_user not in repo.contributes.all():
                        repo.contributes.add(git_user)
                        print(repo.id)