from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
import cloudinary.uploader
from .models import Image





class DeleteView(APIView):
    parser_classes = (MultiPartParser, JSONParser,)
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:
            image = Image.objects.get(id=pk)
        except Image.DoesNotExist:
            return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)


        if image.user != request.user:
            return Response({"message": "You have no permissions"}, status=status.HTTP_403_FORBIDDEN)

        try:
            public_id = image.image.url.split("/upload/")[1].split("/")[-1]
            cloudinary.uploader.destroy(public_id)

        except Exception as e:
            return Response({"message": "Error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        image.delete()

        return Response({"message": "Image deleted"}, status=status.HTTP_204_NO_CONTENT)






class UploadView(APIView):
    parser_classes = (MultiPartParser, JSONParser,)
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        file = request.data.get('picture')

        upload_data = cloudinary.uploader.upload(file)

        image = Image(
            title=upload_data.get('original_filename', ''),
            description=request.data.get('description', ''),
            user=request.user,
            image=upload_data.get('url', ''),
        )

        image.save()

        return Response({
            'status': 'success',
            'data': {
                'id': image.id,
                'title': image.title,
                'description': image.description,
                'uploaded_at': image.uploaded_at,
            },
        }, status=201)