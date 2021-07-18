from django.contrib import admin
from django.urls import path, include
from .views import *
from account.views import (
    AccountViewsets,
    InvestorViewsets,
    BorrowerViewsets
)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('accounts',AccountViewsets)
router.register('investors',InvestorViewsets)
router.register('borrowers',BorrowerViewsets)
router.register('requestloans',LoanRequestViewsets)
router.register('offers',LoanOfferViewsets)
router.register('loans',LoanViewsets)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')) ,
    # Token authentication
    path('api-token-auth', obtain_auth_token, name="login"),
    #viewsets for all models
    path('viewsets/', include(router.urls)),

    
    path('loan-offers/', loan_offers_list),
    path('request-loan/', requested_loan),
    path('accept-offer/', accept_offer),
    path('pay/', pay_scheduled_payment),
    path('loans/', get_loans),
    path('loans/create', create_loan)

]
