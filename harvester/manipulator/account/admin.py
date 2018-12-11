from django.contrib import admin
from account.models import Account

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'nickname', 'real_name']
    ordering = ('-create_time',)
    list_filter = ('nickname',)
    search_fields = ('nickname', 'real_name')

    class Meta:
        model = Account


admin.site.register(Account, AccountAdmin)
