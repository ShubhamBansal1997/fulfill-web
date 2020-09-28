# Third Party Stuff
from rest_framework.routers import DefaultRouter

# fulfill Stuff
from fulfill.base.api.routers import SingletonRouter
from fulfill.product.api import ProductViewSet, UploadProductViewSet
from fulfill.users.api import CurrentUserViewSet
from fulfill.users.auth.api import AuthViewSet

default_router = DefaultRouter(trailing_slash=False)
singleton_router = SingletonRouter(trailing_slash=False)

# Register all the django rest framework viewsets below.
default_router.register("auth", AuthViewSet, basename="auth")
singleton_router.register("me", CurrentUserViewSet, basename="me")
default_router.register("product", ProductViewSet, basename="product")
default_router.register("file_upload", UploadProductViewSet, basename="uploadfile")


# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls + singleton_router.urls
