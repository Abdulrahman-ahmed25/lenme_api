from rest_framework import serializers

from .models import *
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
        'borrower_id', 
        'investor_id',
        'amount_money', 
        'loan_period_in_days',
        'annual_percentage_rate',
        'status',
        'date_founded'
        ]

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = [
        'borrower_id', 
        'amount_money', 
        'loan_period_in_days',
        ]

class LoanOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOffer
        fields = [
            'id',
            'investor_id',
            'accepted_by',
            'loan_request_id',
            'amount_money', 
            'loan_period_in_days',
            'annual_percentage_rate',
            'is_available'
        ]

class ScheduledPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledPayment
        fields = [
            'id',
            'loan_id',
            'deadline',
            'amount_money',
            'is_paid'
        ]

class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = [
            'scheduled_payment_id',
            'payment_date',
            'payment_confirmed'
        ]