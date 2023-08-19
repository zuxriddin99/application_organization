from django.contrib import admin

from .models import Category, Document, News, Client, Employer, SickLeave
from django.forms import TextInput, Textarea
from django.db import models

from ..bot.config import bot


class DocumentInlineAdmin(admin.TabularInline):
    model = Document
    extra = 1


class SickLeaveInlineAdmin(admin.TabularInline):
    model = SickLeave
    extra = 0
    fields = ['date', 'created_at']
    readonly_fields = ['date', 'created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    inlines = [DocumentInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.exclude(id__in=[5, 6])

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        else:
            return ['name']


# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ['telegram_user_id', 'full_name', 'created_at', 'holiday_quantity']
#     inlines = [SickLeaveInlineAdmin]
#
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['telegram_user_id', 'full_name', 'created_at', 'holiday_quantity', 'is_approved']
    inlines = [SickLeaveInlineAdmin]
    save_on_top = True
    save_as = True
    list_editable = ('is_approved', 'holiday_quantity')
    search_fields = ('full_name', 'telegram_user_name', 'telegram_user_id')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


admin.site.register(Employer)
