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
    response_msg = models.TextField(verbose_name='Ответное сообщение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='documents')
    file = models.FileField(upload_to='documents/', verbose_name='Файл', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_sick_leave = models.BooleanField('больничный', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = "Документы"


class News(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название новости')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='news/', verbose_name='Изображение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = "Новости"


class Client(models.Model):
    telegram_user_id = models.IntegerField(unique=True)
    full_name = models.CharField('ФИО', max_length=200, blank=True, default='')
    telegram_user_name = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return str(self.telegram_user_id)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = "Клиенты"


class SickLeave(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.CharField('Дата больничного', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Больничный'
        verbose_name_plural = "Больничный"


class SingletoneModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Employer(SingletoneModel):
    initials = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='employer/', verbose_name='Изображение')

    def __str__(self):
        return self.initials

    class Meta:
        verbose_name = 'Лучший Сотрудник'
        verbose_name_plural = "Лучшие Сотрудники"
