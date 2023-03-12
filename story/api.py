from rest_framework import filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Item
from .serializers import ItemSerializer

class ItemViewSets(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    http_method_names = ["get", "post", "delete", "patch"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["item_type", "by", "editable"]
    search_fields = ["title", "by"]
    ordering_fields = ["created"]

    def partial_update(self, request, pk=None):
        item = self.get_object()
        if item.editable:
            return super().partial_update(request, pk)
        else:
            return Response({'error': 'Item is not editable'}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        item = self.get_object()
        if item.editable:
            return super().destroy(request, pk)
        else:
            return Response({'error': 'Item cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST)