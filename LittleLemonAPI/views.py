from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer, MenuItemSerializer2
from .throttles import TenCallsPerMinuteThrottle

from django.contrib.auth.models import User, Group

# Create your views here.


@api_view(['GET', 'POST'])
def menu_items(request):
    """
    if we want to filter by multiple items
    eg: api/menu-items/?ordering=price,inventory

    the ordering will be first done with price followed by inventory

        ordering_fields = ordering.split(',')
        items = items.order_by(*ordering_fields)

    eg: api/menu-items/?ordering=price
        items = items.order_by(ordering)
        This will order with price
    """
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.GET.get('category')
        to_price = request.GET.get('price')
        search = request.GET.get('search')
        ordering = request.GET.get('ordering')
        perpage = request.GET.get('perpage', default=2)
        page = request.GET.get('page', default=1)

        if category_name:
            items = items.filter(category__name=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            # items = items.order_by(ordering)
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_items = MenuItemSerializer2(items, many=True, context={'request': request})
        return Response(serialized_items.data)

        # serializer = MenuItemSerializer(items, many=True)
        # return Response(serializer.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serializer = MenuItemSerializer(item)
    return Response(serializer.data)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)


class MenuItemsViewSet(viewsets.ModelViewSet):
    """
    throttle_classes should be commented if we are using def get_throttles
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    """
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    search_fields = ['title', 'category__title']

    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret message"})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Only manager should see this"})
    return Response({"message": "Unauthorized"}, 403)


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "successful"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinuteThrottle])
def throttle_check_auth(request):
    return Response({"message": "message for logged in users only"})


@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
            return Response({"message": "User added"})
        if request.method == 'DELETE':
            managers.user_set.remove(user)
    return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)

