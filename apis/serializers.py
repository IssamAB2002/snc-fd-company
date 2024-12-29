from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from core.models import BannerArticle
from shopping.models import Article, Category, SubCategory
from users.models import Order, OrderItem
# younes123789
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'  # Supports email or phone input

    def validate(self, attrs):
        username = attrs.get(self.username_field)
        password = attrs.get('password')
        # Use the custom backend to authenticate
        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:    
            # Debugging hints to track the issue
            if not User.objects.filter(email=username).exists() and not User.objects.filter(phone_number=username).exists():
                raise serializers.ValidationError('User not found with the provided username.')
            else:
                raise serializers.ValidationError('Invalid credentials. Please try again.')

        # Generate tokens using the parent class
        data = super().validate(attrs)
        # Add additional user details to the response
        data['email'] = user.email
        data['phone_number'] = user.phone_number
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        return data
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'state', 'city', 'street', 'sec_phone_number', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Let Django handle password hashing
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            state=validated_data.get('state'),
            city=validated_data.get('city'),
            street=validated_data.get('street'),
            sec_phone_number=validated_data.get('sec_phone_number'),
        )
        if user.last_name:
            print(f'{user.last_name} Joined us')
        else: 
            print("User's name is not registered !")
        user.set_verification_codes()
        user.save()
        return user
    
    # def banner aricles serializer
class BannerArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerArticle
        fields = ['title', 'description', 'image']

# def products articles serializer
class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields =  '__all__'
    # use method field get function to fetch related fields
    # parent category
    def get_category(self, obj):
        return obj.subcategory.category.name
    # subcategory
    def get_subcategory(self, obj):
        return obj.subcategory.name
    # brand
    def get_brand(self, obj):
        return obj.brand.name if obj.brand else None
    # first image
    def get_image(self, obj):
        first_image = obj.images.first()  
        return first_image.image.url if first_image else None

# def category serializer class
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class OrderItemSerializer(serializers.ModelSerializer):
    article_name = serializers.ReadOnlyField(source='article.name')
    image = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id', 'article', 'article_name', 'quantity', 'price', 'image']
    
    def get_image(self, obj):
        first_image = obj.article.images.first()
        return first_image.image.url if first_image else None
    
class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()  # Example for fetch data

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_name', 'created_at', 'total_price', 'items', 'is_sent']
        read_only_fields = ['created_at', 'total_price']  # These are not required for creation

    def get_items(self, obj):
        if self.instance:  # Fetch scenario
            return OrderItemSerializer(obj.items.all(), many=True).data
        return self.initial_data.get('items', [])  # Use raw input data for creation
    def get_user_name(self, obj):
        if obj.user.last_name:
            return obj.user.last_name
        else:
            return obj.user.email
    def create(self, validated_data):
        items_data = self.initial_data.get('items', [])
        user = validated_data.get('user')
        order = Order.objects.create(user=user)
        total_price = 0

        for item_data in items_data:
            article = Article.objects.get(id=item_data['article'])
            quantity = item_data['quantity']
            price = article.wholesale_price * quantity
            OrderItem.objects.create(order=order, article=article, quantity=quantity, price=price)
            total_price += price

        order.total_price = total_price
        order.save()
        return order
 