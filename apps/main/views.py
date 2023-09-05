import datetime

from django.db.models import F, Q
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import asyncio

from apps.bot.utils import send_message
from apps.main.models import Holiday, Client
from conf.settings import DOMAIN


# Create your views here.
@csrf_exempt
def webhook(reqeust):
    check_client_active_days()
    return JsonResponse({'success': True,
                         'message': 'Вся информация успешно сохранена. Вы можете распечатать чек и закрыть эту страницу.',
                         'data': 'data', 'redirect': False},
                        status=200)


def check_client_active_days():
    """
    send notification to admin about client active  length
    """
    admins_telegram_ids = Client.objects.filter(is_admin=True).values_list('telegram_user_id', flat=True)
    today = timezone.now().date()
    three_month_clients = Client.objects.filter(date_of_receipt=today - datetime.timedelta(days=90))
    six_month_clients = Client.objects.filter(date_of_receipt=today - datetime.timedelta(days=180))
    nine_month_clients = Client.objects.filter(date_of_receipt=today - datetime.timedelta(days=270))
    one_year_clients = Client.objects.filter(date_of_receipt=today - datetime.timedelta(days=365))
    for admin_id in admins_telegram_ids:
        for client in three_month_clients:
            url = f"{DOMAIN}main/client/{client.id}/change/"
            text = f"<a href='{url}'>ФИО:{client.full_name_from_passport}.</a>\nПрошло 3 месяц"
            asyncio.run(send_message(admin_id, text, None))
        for client in six_month_clients:
            url = f"{DOMAIN}main/client/{client.id}/change/"
            text = f"<a href='{url}'>ФИО:{client.full_name_from_passport}.</a>\nПрошло 6 месяц"
            asyncio.run(send_message(admin_id, text, None))
        for client in nine_month_clients:
            url = f"{DOMAIN}main/client/{client.id}/change/"
            text = f"<a href='{url}'>ФИО:{client.full_name_from_passport}.</a>\nПрошло 9 месяц"
            asyncio.run(send_message(admin_id, text, None))
        for client in one_year_clients:
            url = f"{DOMAIN}main/client/{client.id}/change/"
            text = f"<a href='{url}'>ФИО:{client.full_name_from_passport}.</a>\nПрошло 1 год"
            asyncio.run(send_message(admin_id, text, None))
