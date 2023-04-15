from django.contrib.auth.models import User,Group
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Category, Rating
from rest_framework_csv.renderers import CSVRenderer
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from .models import Book, MenuItem, FoodItem
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from .serializers import MenuItemSerializer, MenuItemsSerializers, CategorySerializer, FoodItemSerializer, \
    MenuSerializer, RatingSerializer
from rest_framework.decorators import api_view, renderer_classes, throttle_classes
from rest_framework.views import APIView
from django.core.paginator import Paginator,EmptyPage
from rest_framework.decorators import permission_classes
# Create your views here
#
from .throttles import TenCallsPerMinute


@api_view(['GET','POST'])
def menu(request):
    if request.method == "GET":
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default = 1)
        page = request.query_params.get('page', default = 1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte = to_price) #price__lte
        if search:
            items = items.filter(title__icontains=search)
        # if ordering:
        #     items = items.order_by(ordering)
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page)
        except:
            items = []
        serialized_item = MenuItemSerializer(items, many=True, context={'request': request})
        return Response(serialized_item.data)

    if request.method == "POST":
        serialized_item = MenuItemSerializer(data=request.data) # to deserialize a data you need to pass it through the serializer
        serialized_item.is_valid(raise_exception=True)

@api_view()
def menu_singleitem(request, pk):
    items = get_object_or_404(MenuItem,pk=pk)
    serializer_data = MenuItemsSerializers(items)
    return Response(serializer_data.data)


@api_view()
def category_detail(request,pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)

class MenuItemView(generics.ListCreateAPIView):
    queryset =  MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer



@api_view(['GET','POST', 'PUT'])
def bookss(request):
    return Response("List of the books", status=status.HTTP_200_OK)

@csrf_exempt
def books(request):
    if request.method =='GET':
        books = Book.objects.all().values()
        return JsonResponse({'books':list(books)})
    elif request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        book = Book(title=title, author=author, price=price)
        try:
            book.save()
        except IntegrityError:
            return JsonResponse({'error':'true','message':'required field missing'},status=400)

        return JsonResponse(model_to_dict(book), status=201)

# Class BookView(viewsets.ViewSet):
# 	def list(self, request):
# 	    return Response({"message":"All books"}, status.HTTP_200_OK)
# 	def create(self, request):
# 	    return Response({"message":"Creating a book"}, status.HTTP_201_CREATED)
# 	def update(self, request, pk=None):
# 	    return Response({"message":"Updating a book"}, status.HTTP_200_OK)
# 	def retrieve(self, request, pk=None):
# 	    return Response({"message":"Displaying a book"}, status.HTTP_200_OK)
# 	def partial_update(self, request, pk=None):
#         return Response({"message":"Partially updating a book"}, status.HTTP_200_OK)
# 	def destroy(self, request, pk=None):
#         return Response({"message":"Deleting a book"}, status.HTTP_200_OK)


class BookList(APIView):
    def get(self, request):
        author = request.GET.get('author')
        if (author):
            return Response({'message':"List of the books " + author }, status.HTTP_200_OK)

        return Response({'message': "List of the books"}, status.HTTP_200_OK)

    def post(self, request):
        return Response({'title':request.data.get('title')}, status.HTTP_200_OK)

class Book(APIView):
    def get(self, request,pk):
        return Response({'message':"List of the books " + str(pk) }, status.HTTP_200_OK)

#
# @api_view()
# @renderer_classes([CSVRenderer])
# def menu(request):
#     items = MenuItem.objects.select_related('category').all()
#     serialized_item = MenuItemSerializer(items,many=True, context={'request': request})
#     return Response({'data':serialized_item.data}, template_name='menu-item.html')

@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)

class FoodItemView(generics.ListCreateAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

class FoodItemSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    
class MenuItemViewset(viewsets.ModelViewSet):
    #throttle_classes = [AnonRateThrottle,UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    ordering_fields= ['price', 'inventory']
    search_fields = ['title', 'category__title']

    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]

#lab
class CategoryViews(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Menuview(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price','inventory']
    search_fields = ['category__title']

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "some secret message for managers only"})
    else:
        return Response({"message": "You are not authorized"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute]) #UserRateThrottle
def throttle_check_auth(request):
    return Response({"message":"message for the logged in user only"})

# class MenuItemsViewSet(viewsets.ModelViewSet):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


@api_view(['POST'])
@permission_classes(IsAdminUser)
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name = 'Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message": "ok "})
    return Response({"message":"error"}, status=status.HTTP_400_BAD_REQUEST)

class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if (self.request.method == "GET"):
            return []
        return [IsAuthenticated()]