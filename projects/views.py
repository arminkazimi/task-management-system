from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Project.objects.filter(
            collaborators=self.request.user
        ) | Project.objects.filter(
            owner=self.request.user
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
