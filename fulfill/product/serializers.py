# Third Party Stuff
from django.conf import settings
from rest_framework import exceptions, serializers
from rest_hooks.models import Hook

from .models import Product

HOOK_EVENTS = getattr(settings, 'HOOK_EVENTS', [])


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


class HookSerializer(serializers.ModelSerializer):
    """
    serializes the hook data
    """

    def validate_event(self, event):
        if event not in HOOK_EVENTS:
            err_msg = "Unexpected event {}".format(event)
            raise exceptions.ValidationError(detail=err_msg, code=400)
        return event

    class Meta:
        model = Hook
        fields = '__all__'
        read_only_fields = ('user',)
