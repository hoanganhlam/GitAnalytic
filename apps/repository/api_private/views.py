from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from base import pagination
from . import serializers
from apps.repository import models
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import api_view


class MediaViewSet(viewsets.ModelViewSet):
    models = models.Media
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.MediaSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title', 'description']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if not hasattr(serializer.validated_data, "user"):
            serializer.validated_data["user"] = request.user
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TaxonomyViewSet(viewsets.ModelViewSet):
    models = models.Taxonomy
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.TaxonomySerializer
    permission_classes = permissions.IsAuthenticated,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['name']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class GitUserViewSet(viewsets.ModelViewSet):
    models = models.GitUser
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.GitUserSerializer
    permission_classes = permissions.IsAuthenticated,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['username']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RepositoryViewSet(viewsets.ModelViewSet):
    models = models.Repository
    queryset = models.objects.order_by('-id').prefetch_related('taxonomies', 'medias').select_related('author')
    serializer_class = serializers.RepositorySerializer
    permission_classes = permissions.IsAuthenticated,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['name', 'description']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        check_git_empty = request.GET.get("git_empty")
        taxonomies = request.GET.get("taxonomies")
        q = Q()
        if check_git_empty and check_git_empty == 'true':
            q = ~Q(id_github=None) | Q(id_github='')
        if taxonomies:
            taxonomy_ids = taxonomies.split(',')
            q = q & Q(taxonomies__id__in=[int(i) for i in taxonomy_ids])
        self.queryset = self.queryset.filter(q)
        return super(RepositoryViewSet, self).list(request, *args, **kwargs)


@api_view(['GET'])
def re_fetch(request, pk):
    return Response()


@api_view(['GET'])
def re_fetch(request, pk):
    return Response()
