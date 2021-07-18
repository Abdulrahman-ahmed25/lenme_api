from .models import *
from .serializers import *
from .controllers import LoanController, LoanOfferController, LoanRequestController, LoanPaymentController
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status,viewsets, filters
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class LoanRequestViewsets(viewsets.ModelViewSet):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    authentication_classes = [TokenAuthentication]

class LoanOfferViewsets(viewsets.ModelViewSet):
    queryset = LoanOffer.objects.all()
    serializer_class = LoanOfferSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    authentication_classes = [TokenAuthentication]

class LoanViewsets(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    authentication_classes = [TokenAuthentication]

@api_view(['GET'])
def get_loans(request):
    if request.method == 'GET':
        return Response(LoanController().get_loans().data)
        
@api_view(['POST'])
def create_loan(request):
    if request.method == 'POST':
        loan = LoanController.create_loan(request.data.borrower,request.data.investor_id, request.data.offer )
        serializer = LoanSerializer(loan, many=False)
        json = {
            'message': 'Loan is Created',
            'result': serializer.data
        }
        return Response(json , status=status.HTTP_200_OK)

@api_view(['GET'])
def loan_offers_list(request):
    if request.method == 'GET':
      controller = LoanOfferController()
      return Response(controller.get_loan_offers().data)

# xxxxxxxxxxxx
@api_view(['POST'])
def requested_loan(request):
    if request.method == 'POST':
        available_loan_offers = LoanRequestController().request_loan(request.data)
        if available_loan_offers == None:
            return Response('fail', status=status.HTTP_400_BAD_REQUEST)
        return Response(available_loan_offers.data)

@api_view(['POST'])
def accept_offer(request):
    if request.method == 'POST':
        scheduled_payments = LoanOfferController().get_accepted_offer(request.data.get("offer_id"), request.data.get("borrower_id"))
    if scheduled_payments == None:
        return Response('fail', status=status.HTTP_400_BAD_REQUEST)
    return Response(scheduled_payments)

@api_view(['POST'])
def pay_scheduled_payment(request):
    if request.method == 'POST':
        payment_confirmation = LoanPaymentController().pay(request.data.get("scheduled_payment_id"))
        if payment_confirmation == None:
            return Response('Not payed')
        return Response(payment_confirmation)
        