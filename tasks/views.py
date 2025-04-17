from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'project', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date']
    ordering = ['-created_at']

    def get_queryset(self):
        return Task.objects.filter(
            project__collaborators=self.request.user
        ) | Task.objects.filter(
            project__owner=self.request.user
        ) | Task.objects.filter(
            assigned_to=self.request.user
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
