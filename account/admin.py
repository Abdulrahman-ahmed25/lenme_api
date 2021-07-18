from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Investor, Borrower

class AccountAdmin(UserAdmin):
    list_display = ('mobile', 'username', 'is_admin', 'is_staff','is_investor','is_borrower')
    search_fields= ('mobile', 'username')
    readonly_fields = ['id','last_login']
    filter_horizontal=()
    list_filter=()
    fieldsets = ()
admin.site.register(Account, AccountAdmin)
admin.site.register(Investor)
admin.site.register(Borrower)