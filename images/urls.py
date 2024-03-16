from django.urls import path
from .views import UploadView, DeleteView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='image_upload'),
    path('delete/<int:pk>', DeleteView.as_view(), name='image_del'),
]