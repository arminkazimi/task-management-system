from rest_framework import serializers
from .models import Project
from djoser.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'updated_at',
                'owner', 'collaborators', 'tasks_count']
        read_only_fields = ['created_at', 'updated_at', 'owner']

    def get_tasks_count(self, obj):
        return obj.tasks.count()

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)