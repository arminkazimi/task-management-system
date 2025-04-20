from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks in the system.
    Provides CRUD operations and custom actions for task management.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'project', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date']
    ordering = ['-created_at']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(
            project__collaborators=self.request.user
        ) | Task.objects.filter(
            project__owner=self.request.user
        ) | Task.objects.filter(
            assigned_to=self.request.user
        ) | Task.objects.filter(
            created_by=self.request.user
        )

    @swagger_auto_schema(
        method='post',
        operation_description='Assign a task to a specific user',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user to assign the task to')
            }
        ),
        responses={
            200: TaskSerializer,
            400: 'Bad Request - user_id is required',
            403: 'Permission Denied - Only project owner or collaborators can assign tasks',
            404: 'Not Found - Task not found'
        }
    )
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
            
        if not (task.project.owner == request.user or request.user in task.project.collaborators.all()):
            return Response({'error': 'Permission denied'}, status=403)
            
        task.assigned_to_id = user_id
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)
