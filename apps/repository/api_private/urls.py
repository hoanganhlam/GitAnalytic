from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url

router = DefaultRouter()
router.register(r'taxonomies', views.TaxonomyViewSet)
router.register(r'git-users', views.GitUserViewSet)
router.register(r'repositories', views.RepositoryViewSet)
router.register(r'medias', views.MediaViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
