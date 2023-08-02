from django.contrib import admin

from .models import Category, Document, News, Client

admin.site.register(Category)
admin.site.register(Document)
admin.site.register(News)
admin.site.register(Client)
