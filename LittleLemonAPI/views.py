from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

@api_view()
def menu_items(request):
    items = MenuItem.objects.select_related('category').all()
    serializer = MenuItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serializer = MenuItemSerializer(item)
    return Response(serializer.data)