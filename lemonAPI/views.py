from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from .models import MenuItem
from rest_framework.response import Response
from .serializers import MenuItemSerializer
from .serializers import MenuItemHide
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework import viewsets
# Create your views here.


# class MenuItemView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
 
class MenuItemSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    search_fields = ['title', 'category__title']
        
@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    item = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(item, many=True)
    return Response({"data": serialized_item.data}, template_name='menu.html')
    
@api_view(['GET', 'POST'])   
def menuItem(request):
    if request.method == "GET":
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        price_num = request.query_params.get('price')
        search = request.query_params.get('search')
        order = request.query_params.get('order')
        perpage = request.query_params.get('perpage', default = 2)
        page = request.query_params.get('page', default = 1)

        if category_name:
            items = items.filter(category__title = category_name)
        if price_num:
            items = items.filter(price__lte = price_num)
        if search:
            items = items.filter(title__startswith=search)
        if order:
            order_field = order.split(",")
            items = items.order_by(*order_field)
            
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []    
        seria = MenuItemSerializer(items, many = True)
        return Response(seria.data)
    elif request.method == "POST":
        items = MenuItemSerializer(data=request.data)
        items.is_valid(raise_exception=True)
        items.save()
        return Response(items.data, status.HTTP_201_CREATED)

@api_view(['GET'])
def singleItem(request, pk):
    itmes = MenuItem.objects.get(pk=pk)
    seria = MenuItemSerializer(itmes)
    return Response(seria.data)