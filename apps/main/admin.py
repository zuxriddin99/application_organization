from django.contrib import admin

from .models import Category, Document, News, Client


class DocumentInlineAdmin(admin.TabularInline):
    model = Document
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    inlines = [DocumentInlineAdmin]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['telegram_user_id', 'phone_number', 'created_at']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
