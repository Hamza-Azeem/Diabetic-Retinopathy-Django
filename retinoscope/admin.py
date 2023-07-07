from django.contrib import admin
from .models import Account, History
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class AccountInLine(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = "Accounts"

class custmoizeUserAdmin(UserAdmin):
    inlines = (AccountInLine, )
# Register your models here.

admin.site.unregister(User)
admin.site.register(User, custmoizeUserAdmin)
admin.site.register(History)
