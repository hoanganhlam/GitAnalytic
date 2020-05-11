from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from django.urls import path

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^repositories/$', views.list_repository),
    url(r'^repositories/(?P<pk>[0-9]+)/$', views.detail_repository),
    url(r'^taxonomies/$', views.list_taxonomy),
    path('taxonomies/<slug:slug>/', views.detail_taxonomy),
]
