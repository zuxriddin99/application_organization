import datetime

from django.contrib import admin
from django import forms  # Add this import
import asyncio
from apps.bot.utils import send_message_to_users, send_message

from .models import Category, Document, News, Client, Employer, SickLeave, Holiday
from django.forms import TextInput, Textarea
from django.db import models

from ..bot.config import bot


class HolidayInlineForm(forms.ModelForm):
    # Add your custom field here
    msg = forms.CharField(label='Сообщение для клиента', required=False, max_length=500)

    class Meta:
        model = Holiday
        fields = '__all__'  # Include all fields from the Book model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_data = self.instance.__dict__.copy()

    def save(self, commit=False):
        msg = self.cleaned_data['msg']
        status = self.instance.get_status_display()
        old_status = self.initial_data['status']
        if msg:
            asyncio.run(send_message(self.instance.client.telegram_user_id,
                                     msg,
                                     None))
        if old_status != self.instance.status and self.instance.start_date > datetime.date.today():
            asyncio.run(send_message(self.instance.client.telegram_user_id,
                                     f"Статус вашего запроса изменился на {status}",
                                     None))
        instance = super(HolidayInlineForm, self).save(commit=False)

        # Add your custom logic to modify the instance before saving
        # For example, you can modify instance.field_name
        if commit:
            instance.save()
        return instance


class DocumentInlineAdmin(admin.TabularInline):
    model = Document
    extra = 1
    fields = ['id', 'name', 'response_msg', 'file']
    readonly_fields = ['id']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        else:
            return ['name']


class SickLeaveInlineAdmin(admin.TabularInline):
    model = SickLeave
    extra = 0
    fields = ['start_date', 'end_date', 'created_at', ]
    readonly_fields = ['start_date', 'end_date', 'created_at', ]


class HolidayInlineAdmin(admin.TabularInline):
    model = Holiday
    form = HolidayInlineForm
    extra = 0

    fields = ['type_holiday', 'start_date', 'end_date', 'status', 'created_at', 'msg']
    # readonly_fields = ['type_holiday', 'start_date', 'end_date', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    inlines = [DocumentInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.exclude(id__in=[5, 4])

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        else:
            return ['name', 'parent']


# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ['telegram_user_id', 'full_name', 'created_at', 'holiday_quantity']
#     inlines = [SickLeaveInlineAdmin]
#
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['telegram_user_id', 'full_name', 'created_at', 'holiday_quantity', 'is_approved']
    inlines = [SickLeaveInlineAdmin, HolidayInlineAdmin]
    save_on_top = True
    save_as = True
    list_editable = ('is_approved', 'holiday_quantity')
    search_fields = ('full_name', 'telegram_user_name', 'telegram_user_id')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


admin.site.register(Employer)
