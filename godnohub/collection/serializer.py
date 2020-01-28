from .models import *
from rest_framework import serializers


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name']


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['rate', 'name']


class CardSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    type = TypeSerializer()
    rating = RatingSerializer()

    class Meta:
        model = Card
        fields = ['id',
                  'title',
                  'imgur_url',
                  'color',
                  'type',
                  'rating',
                  'tags']


class LaterSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostCard
        fields = ['id',
                  'title',
                  'imgur_url',
                  'color',
                  'type',
                  'tags']


class NewsSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    type = TypeSerializer()
    rating = RatingSerializer()
    timestamp = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = Card
        fields = ['id',
                  'title',
                  'imgur_url',
                  'color',
                  'type',
                  'rating',
                  'tags',
                  'timestamp',
                  'owner']