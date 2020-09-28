# Third Party Stuff
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# fulfill Stuff
from fulfill.base import response
from fulfill.product.models import Product, ProductFile

from .serializers import ProductFileSerializer, ProductSerializer
from .tasks import product_upload_task


class ProductViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('name', 'sku', 'description')
    ordering_fields = ('name', 'sku', 'description')
    filterset_fields = ('name', 'sku', 'description')

    @action(methods=["DELETE"], detail=False)
    def deleteall(self, request):
        Product.objects.all().delete()
        return response.Ok({"success": "Deleted all records."})


class UploadProductViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
        This viewset will upload data from csv to product table
    """
    queryset = ProductFile.objects.all()
    serializer_class = ProductFileSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            task = product_upload_task.delay(serializer.data['id'])
            data = serializer.data
            data['task_id'] = task.task_id
            return response.Created(data)
        else:
            return response.BadRequest(serializer.errors)
