from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(User, related_name='shared_projects', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
