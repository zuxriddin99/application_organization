from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# #
# # class Category(MPTTModel):
# #     """Категории"""
# #     name = models.CharField(
# #         'Название категории', max_length=250, unique=True
# #     )
# #     parent = TreeForeignKey(
# #         'self', verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE,
# #         blank=True, null=True
# #     )
# #
# #
# #     class Meta:
# #         verbose_name = 'Категория'
# #         verbose_name_plural = 'Категории'
# #         ordering = ['id']
#
#     def __str__(self):
#         return self.name
class Category(MPTTModel):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    parent = TreeForeignKey(
        'self', verbose_name='Родительская категория', related_name='children', on_delete=models.CASCADE,
        blank=True, null=True
    )

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
    class PassportTypeEnum(models.TextChoices):
        RUSSIAN = 'russian', 'Рус'
        UZBEK = 'uzbek', "Узб"

    telegram_user_id = models.IntegerField(unique=True)
    full_name = models.CharField('ФИО', max_length=200, blank=True, default='')
    telegram_user_name = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    holiday_quantity = models.IntegerField(blank=True, null=True, verbose_name='Количество выходных')
    is_approved = models.BooleanField(default=False, verbose_name='Одобренный')
    full_name_from_passport = models.CharField('ФИО по паспорту', max_length=250, blank=True, default='')
    passport_seria = models.CharField('Серия паспорта', max_length=250, blank=True, default='')
    date_of_receipt = models.DateField('Дата приёма', blank=True, null=True)
    job_title = models.CharField('Должность', max_length=250, blank=True, default='')
    department = models.CharField('Департамент', max_length=250, blank=True, default='')
    is_admin = models.BooleanField('Администратор', default=False)

    def __str__(self):
        return str(self.telegram_user_id)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = "Клиенты"


class SickLeave(models.Model):
    class SickLeaveEnum(models.TextChoices):
        PREGNANCY = 'Больничный по беременности и родам', 'Больничный по беременности и родам'
        SICK = 'Больничный по болезни', "Больничный по болезни"
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.CharField('Дата больничного', blank=True, default='')
    start_date = models.DateField('Дата начала', blank=True, null=True)
    end_date = models.DateField('Дата окончания', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    type_sick = models.CharField(verbose_name='Тип Больничный', choices=SickLeaveEnum.choices, blank=True, null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Больничный'
        verbose_name_plural = "Больничный"


class Holiday(models.Model):
    class HolidayStatusEnum(models.TextChoices):
        WAITING = 'waiting', 'В ожидании'
        APPROVED = 'approved', "Одобренный"
        CANCELLED = 'cancelled', "Отменено"

    class HolidayTypeEnum(models.TextChoices):
        WAITING = 'Отпуск без содержания', 'Отпуск без содержания'
        APPROVED = 'Отпуск по уходу за ребенком', "Отпуск по уходу за ребенком"
        CANCELLED = 'Ежегодный отпуск', "Ежегодный отпуск"

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField('Дата начала отпуска', blank=True, null=True)
    end_date = models.DateField('Дата окончания отпуска', blank=True, null=True)
    date = models.CharField('Дата отпуск', blank=True, default='')
    type_holiday = models.CharField(verbose_name='Тип отпуск', choices=HolidayTypeEnum.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    status = models.CharField('Статус', max_length=10, choices=HolidayStatusEnum.choices,
                              default=HolidayStatusEnum.WAITING)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Отпуск'
        verbose_name_plural = "Отпуск"
        ordering = ['-id']


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


class Employer(models.Model):
    initials = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='employer/', verbose_name='Изображение')

    def __str__(self):
        return self.initials

    class Meta:
        verbose_name = 'Лучший Сотрудник'
        verbose_name_plural = "Лучшие Сотрудники"
