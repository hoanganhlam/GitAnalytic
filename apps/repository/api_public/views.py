from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils.other import get_paginator
from django.db import connection
from apps.repository.models import Taxonomy


def get_all_taxonomies(q_taxonomies):
    taxonomies = None
    if q_taxonomies is not None:
        arr = q_taxonomies.split(',')
        tax_queryset = Taxonomy.objects.filter(id__in=[int(i) for i in arr])
        arr2 = []
        for q in tax_queryset:
            arr2.append(q)
            arr2 = arr2 + q.all_children()
        taxonomies = "{" + ','.join([str(elem.id) for elem in arr2]) + "}"
    return taxonomies


@api_view(['GET'])
def list_repository(request):
    p = get_paginator(request)
    print(p.get("order_by"))
    with connection.cursor() as cursor:
        cursor.execute("SELECT FETCH_REPOSITORIES(%s, %s, %s, %s, %s, %s)",
                       [
                           p.get("page_size"),
                           p.get("offs3t"),
                           p.get("order_by"),
                           p.get("search"),
                           get_all_taxonomies(request.GET.get("taxonomies")),
                           request.GET.get("author")
                       ])
        result = cursor.fetchone()[0]
        if result.get("results") is None:
            result["results"] = []
        return Response(result)


@api_view(['GET'])
def detail_repository(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT FETCH_REPOSITORY(%s)", [pk])
        out = cursor.fetchone()[0]
    return Response(out)


@api_view(['GET'])
def list_taxonomy(request):
    p = get_paginator(request)
    if request.GET.get("kind") == "category" and request.GET.get("parent") is not None:
        parents = "{" + request.GET.get("parent") + "}"
    else:
        parents = get_all_taxonomies(request.GET.get("parent"))
    with connection.cursor() as cursor:
        cursor.execute("SELECT FETCH_TAXONOMIES(%s, %s, %s, %s, %s)",
                       [
                           p.get("page_size"),
                           p.get("offs3t"),
                           p.get("search"),
                           request.GET.get("flag"),
                           parents
                       ])
        result = cursor.fetchone()[0]
        if result.get("results") is None:
            result["results"] = []
        return Response(result)


@api_view(['GET'])
def detail_taxonomy(request, slug):
    with connection.cursor() as cursor:
        cursor.execute("SELECT FETCH_TAXONOMY(%s)", [slug])
        out = cursor.fetchone()[0]
    return Response(out)
