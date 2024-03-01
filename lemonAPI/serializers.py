from rest_framework import serializers
from .models import MenuItem, Category
from rest_framework.validators import UniqueValidator
from decimal import Decimal
import bleach

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source = 'inventory')
    after_tax = serializers.SerializerMethodField(method_name = 'tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if (attrs['price'] < 2):
            raise serializers.ValidationError('must over 2')
        return super().validate(attrs)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'after_tax', 'category_id', 'category'] 
        depth = 1
        extra_kwargs = {
            "title": {
                "validators":[UniqueValidator(queryset=MenuItem.objects.all())]
                }
        }
    def tax(self, product:MenuItem):
        return product.price * Decimal(1.3)
        
class MenuItemHide(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length = 50)           