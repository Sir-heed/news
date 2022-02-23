from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.serializers import ItemSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from story.models import Item

# Create your views here.
class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['item_type']

    def list(self, request):
        queryset = Item.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Item not found'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(ItemSerializer(item).data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Item not found'
            }, status=status.HTTP_404_NOT_FOUND)
        if item.editable == False:
            return Response({
                'status': False,
                'message': 'Cannot edit item'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.get_serializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            item = serializer.save()
            return Response({
                "message": "Item updated successfully",
                "status": True,
                "item": ItemSerializer(item).data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Item not found'
            }, status=status.HTTP_404_NOT_FOUND)
        if item.editable == False:
            return Response({
                'status': False,
                'message': 'Cannot delete item'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        item.delete()
        return Response({
            'status': True,
            'message': 'Item deleted successfully'
        }, status=status.HTTP_200_OK)