from apps.repository.models import Taxonomy, GitUser, Repository, Media
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail


class MediaSerializer(serializers.ModelSerializer):
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
        extra_fields = ['sizes']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(MediaSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def to_representation(self, instance):
        return super(MediaSerializer, self).to_representation(instance)

    def get_sizes(self, instance):
        if instance.path:
            return {
                "thumb_64_64": get_thumbnail(instance.path, '64x64', crop='center', quality=100).url,
                "thumb_640_250": get_thumbnail(instance.path, '640x250', crop='center', quality=100).url,
                "thumb_325_150": get_thumbnail(instance.path, '325x150', crop='center', quality=100).url
            }
        else:
            return {}


class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = '__all__'
        extra_kwargs = {
            # 'slug': {'read_only': True}
        }

    def to_representation(self, instance):
        return super(TaxonomySerializer, self).to_representation(instance)


class GitUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitUser
        fields = '__all__'
        extra_kwargs = {}

    def to_representation(self, instance):
        return super(GitUserSerializer, self).to_representation(instance)


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'
        extra_kwargs = {}

    def to_representation(self, instance):
        self.fields['taxonomies'] = TaxonomySerializer(read_only=True, many=True)
        self.fields['medias'] = MediaSerializer(read_only=True, many=True)
        self.fields['author'] = GitUserSerializer(read_only=True)
        return super(RepositorySerializer, self).to_representation(instance)
