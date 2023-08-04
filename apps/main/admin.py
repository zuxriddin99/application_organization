from django.contrib import admin

from .models import Category, Document, News, Client, Employer


class DocumentInlineAdmin(admin.TabularInline):
    model = Document
    extra = 1


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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['telegram_user_id', 'phone_number', 'created_at']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


admin.site.register(Employer)
