from django.db import models
# from .views import validate_file_extension

# Create your models here.
class File(models.Model):
  file = models.FileField(upload_to='media/files', blank=False, null=False)
  date_added = models.DateTimeField(auto_now_add=True)

