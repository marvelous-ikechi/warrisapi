from django.contrib import admin
from .models import File

# Register your models here.

# class FileAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('file_name',)}

admin.site.register(File)
