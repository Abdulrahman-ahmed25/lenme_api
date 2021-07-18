from django.db import models
from account.models import Investor,Borrower
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
LOAN_STATUS_FOUNDED = 0
LOAN_STATUS_COMPLETED = 1
STATUS_CHOICES  = [(LOAN_STATUS_FOUNDED,'FOUNDED'), (LOAN_STATUS_COMPLETED,'COMPLETED')]

class Loan(models.Model):
    borrower_id         = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    investor_id         = models.ForeignKey(Investor, on_delete=models.CASCADE)
    amount_money        = models.DecimalField(max_digits=7, decimal_places=2)
    loan_period_in_days         = models.PositiveIntegerField()
    annual_percentage_rate      = models.DecimalField(max_digits=3, decimal_places=1)
    status      = models.IntegerField(choices=STATUS_CHOICES, default = 'FOUNDED')
    date_founded = models.DateField(null=True)

class LoanRequest(models.Model):
    borrower_id         = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    amount_money        = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(50),MaxValueValidator(5000)])
    loan_period_in_days = models.PositiveIntegerField()

class LoanOffer(models.Model):
    investor_id         = models.ForeignKey(Investor, on_delete=models.CASCADE)
    accepted_by         = models.ForeignKey(Borrower, on_delete=models.CASCADE, null=True, blank=True)
    loan_request_id     = models.ForeignKey(LoanRequest,on_delete=models.CASCADE)
    amount_money        = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(50),MaxValueValidator(5000)])
    loan_period_in_days         = models.PositiveIntegerField()
    annual_percentage_rate      = models.DecimalField(max_digits=3, decimal_places=1)
    is_available        = models.BooleanField(default=True)

class ScheduledPayment(models.Model):
    loan_id         = models.ForeignKey(Loan, on_delete=models.CASCADE)
    deadline        = models.DateField(null=True)
    amount_money    = models.PositiveIntegerField()
    is_paid         = models.BooleanField(default=False)

class LoanPayment(models.Model):
    scheduled_payment_id    = models.ForeignKey(ScheduledPayment, on_delete=models.CASCADE)
    payment_date            = models.DateField(null=True)
    payment_confirmed       = models.BooleanField(default=False)