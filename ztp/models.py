
from django.db import models

class DockerContainer(models.Model):
    name = models.CharField(max_length=100)
    container_id = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=100)
    last_status = models.CharField(max_length=20)

    def __str__(self):
        return self.name
