from rest_framework import viewsets, parsers
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
