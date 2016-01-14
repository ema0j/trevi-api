from rest_framework import serializers
from recomm.models import Music


class RecommSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('artist', 'track', 'created_at')

'''
def create(self, validated_data):
    return Music.objects.create(**validated_data)

def update(self, instance, validated_data):
    instance.models
'''
