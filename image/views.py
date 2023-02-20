import os
from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ImageHostingAPI.settings import MEDIA_ROOT
from image.fileschecker import files_checker
from image.imagecreator import create_image
from image.models import Image
from image.serializers import ImageSerializer



class ImageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        images = Image.objects.filter(uploader=user)
        serializer = ImageSerializer(images, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        images_list = []
        files = list(request.data.values())
        if not files:
            return Response({'error': "HTTP request does not contain image(s)."},
                            status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if files_checker(files):
            for image in files:
                image = Image.objects.create(
                    image=image,
                    uploader=user
                )
                images_list.append(image)
            serializer = ImageSerializer(images_list, many=True, context={'request':request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': "Image(s) should be in the format PNG or JPG."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def media_access(request, path, *args, **kwargs):
    content = {
        'error': 'Does not exist'
    }

    if path[-1] == "/":
        path = path[:-1]
    image = Image.objects.filter(image__contains=path).first()

    if image:
        if image.uploader != request.user:
            return Response(content)
        height = request.GET.get('height')
        if str(height) not in request.user.tier.thumbnail_sizes or height == '':
            if not [key for (key, value) in request.GET.items()]:
                response = FileResponse(open(MEDIA_ROOT + '/' + path, 'rb'))
                return response
            return Response(content)
        root = MEDIA_ROOT + '/' + 'user_' + str(request.user.id) + '/' + str(height)
        try:
            os.mkdir(root)
            create_image(MEDIA_ROOT, root, path, height)
            response = FileResponse(open(root + '/' + path.split('/')[-1], 'rb'))
            return response

        except FileExistsError:
            try:
                response = FileResponse(open(root + '/' + path.split('/')[-1], 'rb'))
                return response
            except FileNotFoundError:
                create_image(MEDIA_ROOT, root, path, height)
                response = FileResponse(open(root + '/' + path.split('/')[-1], 'rb'))
                return response
    return Response(content)
