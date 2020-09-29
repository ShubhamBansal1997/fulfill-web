# Third Party Stuff
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# fulfill Stuff
from fulfill.base import response
from fulfill.product.models import Product

from .serializers import ProductFileSerializer, ProductSerializer
from .services import get_presigned_url
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


class UploadProductViewSet(viewsets.GenericViewSet):
    """
        This viewset will give pre signed url
        and start the task to upload data
    """
    serializer_class = ProductFileSerializer
    permission_classes = (AllowAny,)

    @action(methods=["GET"], detail=False)
    def pre_signed_url(self, request):
        url, file_name = get_presigned_url()
        return response.Ok({"url": url, "file_name": file_name})

    @action(methods=["POST"], detail=False)
    def start_task(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            task = product_upload_task.delay(serializer.data['filename'])
            data = serializer.data
            data['task_id'] = task.task_id
            return response.Ok(data)
        else:
            return response.BadRequest(serializer.errors)
