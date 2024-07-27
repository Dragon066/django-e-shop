from rest_framework import serializers
from catalog.models import Product
from user.models import User


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'price', 'quantity']


class ProductEditSerializer(serializers.ModelSerializer):    
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ['owner']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
