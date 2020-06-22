from apps.repository.models import Repository
from rest_framework import serializers


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'name']
        extra_kwargs = {}

    def to_representation(self, instance):
        return super(RepositorySerializer, self).to_representation(instance)
