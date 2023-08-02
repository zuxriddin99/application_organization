from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"
        ordering = ['id']


class Document(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название документа')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='documents')
    file = models.FileField(upload_to='documents/', verbose_name='Файл')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = "Документы"


class News(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название новости')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='news/', verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = "Новости"


class Client(models.Model):
    telegram_user_id = models.IntegerField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return str(self.telegram_user_id)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = "Клиенты"
