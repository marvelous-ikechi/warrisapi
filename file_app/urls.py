from django.urls import path
from .views import FileView

urlpatterns = [
    path('', FileView.as_view(), name='file_upload'),
    path('<int:id>/', FileView.as_view(), name='file_detail'),
]
