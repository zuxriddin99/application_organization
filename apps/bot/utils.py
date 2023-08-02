from django.db.models import Q

from apps.main import models as main_models
from asgiref.sync import sync_to_async
from typing import List


@sync_to_async
def get_all_categories_list() -> List[str]:
    """
    :return all categories name list
    """
    categories = main_models.Category.objects.all().values_list('name', flat=True)
    for c in categories:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Category.objects.all()
        '''
        pass
    return list(categories)


@sync_to_async
def get_documents_list(category_name: str) -> List[str]:
    """
    :return documents list
    """
    if category_name == '':
        f = Q()
    else:
        f = Q(category__name=category_name)
    documents = main_models.Document.objects.filter(f).values_list('name', flat=True)
    for c in documents:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Category.objects.all()
        '''
        pass
    return list(documents)


@sync_to_async
def return_document(name: str) -> main_models.Document:
    """
    :return document
    """
    document = main_models.Document.objects.aget(name=name)
    return document
