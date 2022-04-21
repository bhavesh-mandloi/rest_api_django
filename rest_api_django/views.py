from xmlrpc.client import ResponseError
from django.http import JsonResponse
from .models import IoT_Data
from .serializers import IotdataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


authentication_classes = [JWTAuthentication]
permission_classes = [IsAuthenticated]

@api_view(['GET', 'POST'])
def device_list(request, format=None):
    # get all the device names
    # serialize them 
    # gets all the json
    
    if request.method == 'GET':
        
        devices = IoT_Data.objects.all()
        serializer = IotdataSerializer(devices, many=True)
        return Response({'IOT-Devices': serializer.data})
    
    if request.method == 'POST':
        
        serializer = IotdataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def device_details(request, Serial_no):
    
    try:
        dev = IoT_Data.objects.get(pk=Serial_no)
    except IoT_Data.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IotdataSerializer(dev)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = IotdataSerializer(dev, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        dev.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  