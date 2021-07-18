from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters,viewsets

# Create your views here.
class AccountViewsets(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerialization
    filter_backends = [filters.SearchFilter]
    search_fields = ['mobile','username']
    authentication_classes = [TokenAuthentication]

class InvestorViewsets(viewsets.ModelViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerialization
    filter_backends = [filters.SearchFilter]
    search_fields = ['mobile','username']
    authentication_classes = [TokenAuthentication]

class BorrowerViewsets(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerialization
    filter_backends = [filters.SearchFilter]
    search_fields = ['mobile','username']
    authentication_classes = [TokenAuthentication]