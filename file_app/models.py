import os
from typing import ItemsView
from django.db import models
# from .views import validate_file_extension
from django.core.validators import FileExtensionValidator
from django.urls import reverse


# Create your models here.


class File(models.Model):
    file_name = models.FileField(upload_to='media/files', blank=False, null=False,
                                 validators=[FileExtensionValidator(['csv', 'xlsx'])])
    date_added = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('file_detail', args=[str(self.id)])

    def __str__(self):
        return os.path.basename(self.file_name.name)
