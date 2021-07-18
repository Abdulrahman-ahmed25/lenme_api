from .models import *
from .serializers import *
import datetime
from .lenme import *
# dateutil.relativedelta provides extra functionality 
#A relativedelta has many more parameters than a timedelta:
from dateutil.relativedelta import relativedelta

class LoanController:
    def get_loans(self):
        loans = Loan.objects.all()
        return LoanSerializer(loans, many=True)
    
    def create_loan(self,borrower_id,investor,offer):
        loan = {
            'borrow_id'     :   borrower_id,
            'investor_id'   :   investor.id,
            'amount_money'  :   offer.amount_money,
            'loan_period_in_days'   :   offer.loan_period_in_days,
            'annual_percentage_rate':   offer.annual_percentage_rate,
            'status'        :   LOAN_STATUS_FOUNDED,
            'date_founded'  :   datetime.date.today()
        }
        return loan

    def check_loan_fully_paid(self, id):
        unpaid = ScheduledPaymentController().get_unpaid(id)
        if len(unpaid) == 0:
            Loan.objects.update(id=id, status=LOAN_STATUS_COMPLETED)
        else:
            Loan.objects.update(id=id, status=LOAN_STATUS_FOUNDED)
    
class LoanOfferController:
    def get_loan_offers(self):
        loan_offers = LoanOffer.objects.all()
        return LoanOfferSerializer(loan_offers, many=True)

    def get_available_loan_offers(self):
        available_loan_offers = LoanOffer.objects.filter(is_available=True)
        return LoanOfferSerializer(available_loan_offers, many=True)
    
    def get_accepted_offer(self, offer_id, borrower_id):
        accepted_offer = LoanOffer.objects.get(id=offer_id)
        if not accepted_offer.is_available:
            return None
        investor = Investor.objects.get(id=accepted_offer.investor_id.id)
        if investor.invest_money >= accepted_offer.amount_money + LENME_FEE:
            accepted_offer.accepted_by  = Borrower(id=borrower_id)
            accepted_offer.is_available = False
            accepted_offer.save()
            loan = LoanController.create_loan(borrower_id, investor, accepted_offer)
            loan_serializer = LoanSerializer(data = loan)
            if loan_serializer.is_valid():
                loan = loan_serializer.save()
            else:
                ## TODO: Clean Up
                return None

            #to calculate the number of months from loan_period_in_days 
            number_of_months = accepted_offer.loan_period_in_days // 30

            #to calculate the total amount -> (15/100) * (6/12) = 0.075
            total_amount = ((accepted_offer.annual_percentage_rate)/100) * (number_of_months/12)

            #to calculate the monthly payment -> (5000 * (1 + 0.075))/6 = 895.83
            monthly_payment = (accepted_offer.amount_money * (1 + total_amount))/number_of_months
            scheduledPaymentController = ScheduledPaymentController()

            #increment date by 1 month for each payment
            today = datetime.date.today()
            scheduled_payments = []
            for i in range(number_of_months):
                deadline = today + relativedelta(months=i+1)
                scheduled_pay = ScheduledPaymentController.create_scheduled_payment(monthly_payment, loan, deadline)
                scheduled_payments.append(scheduled_pay)
                serializer = ScheduledPaymentSerializer(data=scheduled_pay)
                if serializer.is_valid():
                    id = serializer.save().id
                    scheduled_payments[i]['id'] = id
            return scheduled_payments
        return None

class LoanRequestController:
    def request_loan(self, data):
        loan_request = LoanRequestSerializer(data=data)
        if loan_request.is_valid():
            if not LoanRequest.objects.filter(borrower_id=data['borrower_id']):
                loan_request.save()
            return LoanOfferController().get_available_loan_offers()
        return None

class ScheduledPaymentController:
    def create_scheduled_payment(self, amount_money, loan, deadline):
        scheduled_payment = {
            'loan_id': loan.id,
            'deadline': deadline,
            'amount_money': amount_money
        }
        return scheduled_payment

    def get_scheduled_payment(self, id):
        try:
            scheduled_payment = ScheduledPayment.objects.get(id=id)
            return scheduled_payment
        except:
            return None

    def mark_as_paid(self, id):
        scheduled_payment = self.get(id)
        if not scheduled_payment == None:
            scheduled_payment.is_paid = True
            scheduled_payment.save()
            return True
        return False

    def get_unpaid(self, loan_id):
        return ScheduledPayment.objects.filter(loan_id=loan_id, is_paid=False)

class LoanPaymentController:
    def create(self, scheduled_payment_id):
        loan_payment = {
            'payment_date': datetime.date.today(),
            'scheduled_payment_id': scheduled_payment_id,
            'payment_confirmed': True
        }
        return loan_payment
    
    def get_from_scheduled_payment(self, scheduled_payment_id):
        try:
            return LoanPayment.objects.filter(scheduled_payment_id=scheduled_payment_id)
        except:
            return None

    def pay(self, scheduled_payment_id):
        loan_payment = self.get_from_scheduled_payment(scheduled_payment_id)
        if not len(loan_payment) == 0:
            return 'already paid!'
        scheduledPaymentController = ScheduledPaymentController()
        scheduled_payment = scheduledPaymentController.get_scheduled_payment(scheduled_payment_id)
        loan_payment = self.create(scheduled_payment_id)
        if not scheduled_payment == None:
            if scheduledPaymentController.mark_as_paid(scheduled_payment.id):
                    serializer = LoanPaymentSerializer(data=loan_payment)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        LoanController().check_loan_fully_paid(scheduled_payment.loan_id.id)
                        return serializer.data