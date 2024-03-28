from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import PerevalSerializer
from drf_yasg.utils import swagger_auto_schema

class PerevalCreateViewset(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer
    filterset_fields = ('user__email',)
    http_method_names = ['get', 'post', 'create']

    def create(self, request, *args, **kwargs):
        global response_data
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 200,
                'message': '',
                'id': serializer.data.get('id')
            }
        elif status.HTTP_500_INTERNAL_SERVER_ERROR:
            response_data = {
                'status': 500,
                'message': 'Ошибка подключения к базе данных',
                'id': serializer.data.get('id')
            }
        elif status.HTTP_400_BAD_REQUEST:
            response_data = {
                'status': 400,
                'message': 'Неверный запрос',
                'id': serializer.data.get('id')
            }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(responce_body=PerevalSerializer)
    def list(self, request, *args, **kwargs):
        return super(PerevalCreateViewset, self).list(request, *args, **kwargs)
    @swagger_auto_schema(responce_body=PerevalSerializer)
    def create(self, request, *args, **kwargs):
        return super(PerevalCreateViewset, self).create(request, *args, **kwargs)
    @swagger_auto_schema(responce_body=PerevalSerializer)
    def update(self, request, *args, **kwargs):
        return super(PerevalCreateViewset, self).update(request, *args, **kwargs)



