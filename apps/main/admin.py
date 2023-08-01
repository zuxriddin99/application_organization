from django.contrib import admin

from .models import Category, Document, News

admin.site.register(Category)
admin.site.register(Document)
admin.site.register(News)
