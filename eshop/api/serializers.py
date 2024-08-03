from catalog.models import Product
from rest_framework import serializers
from user.models import User


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializes a Product model instance for read-only views.

    Public view.
    """

    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "price", "quantity"]


class ProductEditSerializer(serializers.ModelSerializer):
    """
    Serializes a Product model instance for read-write views.

    Login required.
    """

    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ["owner"]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes a User model instance for API requests.
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Creates and saves a new User instance with
        the provided validated data.
        """
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
