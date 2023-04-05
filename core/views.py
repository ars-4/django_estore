from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from core.utils import get_or_create_token
from core.models import Product, Category, Order, OrderItem, Cart, SubCategory, Person, User
from core.serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer, CartSerializer, SubCategorySerializer, PersonSerializer

# Create your views here.

@api_view(['GET'])
def index(request):
    if request.user.is_authenticated:
        return Response({'detail': str(request.user), 'error': 'false'}, status=200)
    else:
        return Response({'detail': 'Hello, World!', 'error': 'true'}, status=401)
    

@api_view(['POST'])
def login(request):
    data = request.data
    try:
        if '@' in data.get('username'):
            user = Person.objects.get(user__email=data['username'])
            serializer = PersonSerializer(user, many=False)
        else:
            user = Person.objects.get(user__username=data['username'])
            serializer = PersonSerializer(user, many=False)
        if user.user.check_password(data['password']):
            return Response({'detail': 'Login successful', 'data': serializer.data, 'token': get_or_create_token(user.user), 'error': 'false'}, status=200)
        else:
            return Response({'detail': 'Invalid credentials', 'error': 'true'}, status=401)
    except Exception as e:
        return Response({'detail': str(e), 'error': 'true'}, status=401)
    

@api_view(['POST'])
def register(request):
    data = request.data
    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        person = Person.objects.create(
            user=user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            address_street=data['address_street'],
            address_city=data['address_city'],
            address_state=data['address_state'],
            address_zip=data['address_zip']
        )
        user.save()
        person.save()
        return Response({'detail': 'Registration successful'}, status=201)
    except Exception as e:
        return Response({'detail': str(e)}, status=401)



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        subcategory = self.request.query_params.get('subcategory', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        if subcategory is not None:
            queryset = queryset.filter(subcategory=subcategory)
        return queryset
    
    def create(self, request):
        person = Person.objects.get(user=request.user)
        if request.user.is_authenticated and person.role == 'admin':
            data = request.data
            product = Product.objects.create(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                category=Category.objects.get(id=data['category']),
                subcategory=SubCategory.objects.get(id=data['subcategory']),
                image=data['image']
            )
            product.save()
            return Response({'detail': 'Product created successfully', 'product_id': product.id}, status=201)
        else:
            return Response({'detail': 'You are not authorized to perform this action'}, status=401)



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request):
        person = Person.objects.get(user=request.user)
        if request.user.is_authenticated and person.role == 'admin':
            data = request.data
            category = Category.objects.create(
                name=data['name']
            )
            category.save()
            return Response({'detail': 'Category created successfully', 'category_id': category.id}, status=201)
        else:
            return Response({'detail': 'You are not authorized to perform this action'}, status=401)



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.filter(person=Person.objects.get(user=self.request.user))
        return queryset

    def create(self, request):
        cart = Cart.objects.get(id=int(request.data['cart']))
        order = Order.objects.create(
            person=Person.objects.get(user=request.user),
            cart=cart,
            total=cart.total
        )
        order.save()
        return Response({'message': 'Order created successfully', 'order_id': order.id}, status=201)



class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]



class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Cart.objects.filter(person=Person.objects.get(user=self.request.user))
        return queryset
    
    def create(self, request):
        data = request.data
        cart = Cart.objects.create(
            person=Person.objects.get(user=request.user)
        )
        cart_total = 0
        for item in data['products']:
            product = Product.objects.get(id=item['id'])
            cart_total += int(product.price)*int(item['quantity'])
            OrderItem.objects.create(product=product, cart=cart, quantity=item['quantity'], price=product.price, total=str(int(product.price)*int(item['quantity'])))
        
        cart.total = str(cart_total)
        cart.save()
        return Response({'message': 'Cart created successfully', 'cart_id': cart.id}, status=201)


class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def create(self, request):
        person = Person.objects.get(user=request.user)
        if request.user.is_authenticated and person.role == 'admin':
            data = request.data
            subcategory = SubCategory.objects.create(
                name=data['name'],
                category=Category.objects.get(id=int(data['category']))
            )
            subcategory.save()
            return Response({'detail': 'Subcategory created successfully', 'subcategory_id': subcategory.id}, status=201)
        else:
            return Response({'detail': 'You are not authorized to perform this action'}, status=401)


