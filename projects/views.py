from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for managing projects in the system.
    Provides CRUD operations and collaboration management."""

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Project.objects.none()
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(
            collaborators=self.request.user
        ) | Project.objects.filter(
            owner=self.request.user
        )

    @swagger_auto_schema(
        method='post',
        operation_description='Add a collaborator to the project',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user to add as collaborator')
            }
        ),
        responses={
            200: ProjectSerializer,
            400: 'Bad Request - user_id is required',
            403: 'Permission Denied - Only project owner can add collaborators',
            404: 'Not Found - User not found'
        }
    )
    @action(detail=True, methods=['post'])
    def add_collaborator(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if project.owner != request.user:
            return Response({'error': 'Only project owner can add collaborators'}, 
                          status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            project.collaborators.add(user)
            return Response(ProjectSerializer(project).data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        method='post',
        operation_description='Remove a collaborator from the project',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user to remove from collaborators')
            }
        ),
        responses={
            200: ProjectSerializer,
            400: 'Bad Request - user_id is required',
            403: 'Permission Denied - Only project owner can remove collaborators',
            404: 'Not Found - User not found'
        }
    )
    @action(detail=True, methods=['post'])
    def remove_collaborator(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if project.owner != request.user:
            return Response({'error': 'Only project owner can remove collaborators'}, 
                          status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            project.collaborators.remove(user)
            return Response(ProjectSerializer(project).data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
