from rest_framework import serializers
from .models import Investor,Borrower, Account

class AccountSerialization(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = Account
        fields='__all__'
        #to make password invisable
        extra_kwargs = {'password':{'write_only':True}, 'required':True}

class InvestorSerialization(AccountSerialization):
    class Meta:
        model = Investor
        fields='__all__'

class BorrowerSerialization(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields='__all__'