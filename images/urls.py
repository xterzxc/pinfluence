from django.urls import path
from .views import UploadView, DeleteView, CommentsImg, CommentCreate

urlpatterns = [
    path('upload/', UploadView.as_view(), name='image_upload'),
    path('delete/<int:pk>', DeleteView.as_view(), name='image_del'),
    path('comments/id/<int:image_id>/', CommentsImg.as_view(), name='comments-by-img'),
    path('comments/create/', CommentCreate.as_view(), name='comment-create'),
]