# Third Party Stuff
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    serializes the data of the basic Product api
    """

    class Meta:
        model = Product
        fields = '__all__'


class ProductFileSerializer(serializers.Serializer):
    """
    serializes the data of the product upload api
    """
    filename = serializers.CharField(required=True)
