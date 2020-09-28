# Third Party Stuff
from rest_framework import serializers

from .models import Product, ProductFile


class ProductSerializer(serializers.ModelSerializer):
    """
    serializes the data of the basic Product api
    """

    class Meta:
        model = Product
        fields = '__all__'


class ProductFileSerializer(serializers.ModelSerializer):
    """
    serializes the data of the basic Product api
    """

    class Meta:
        model = ProductFile
        fields = '__all__'
