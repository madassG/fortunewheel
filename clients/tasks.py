from datetime import datetime
from email.mime.image import MIMEImage

import requests
import hashlib
import logging
import time
from glisti.celery import app
from glisti.settings import GC_API, GC_ACCOUNT, GROUP_ID_TICKS, GROUP_ID_WORMS, EMAIL_HOST_USER, SECRET_KEY
from django.core.mail import send_mail, EmailMultiAlternatives
from pathlib import Path
from clients.models import Client


logger = logging.getLogger('glisti.celery')


def get_group_items(group_id: str) -> list:
    response = requests.get(f'https://{GC_ACCOUNT}.getcourse.ru/pl/api/account/groups/{group_id}/users?key={GC_API}&created_at[from]=2022-05-25').json()

    if not response.get('success'):
        logger.error(f'{response.get("error_message")} - {response.get("error_code")}')
        return []

    export_id = response.get('info').get('export_id')

    if not export_id:
        logger.error(
            f'Export ID недоступен. {response.get("error_message")} - {response.get("error_code")}')
        return []

    url = f'https://{GC_ACCOUNT}.getcourse.ru/pl/api/account/exports/{export_id}?key={GC_API}'

    response = requests.get(url).json()

    k = 10
    while not response.get('success') and response.get('error_code') == 909 and k > 0:
        time.sleep(10)
        response = requests.get(url).json()
        k -= 1

    if not response.get('success') or not response.get('info').get('items'):
        logger.error(f'Export заказов недоступен. {response.get("error_message")} - {response.get("error_code")}')
        return []

    return response['info']['items']


def add_user(email: str, name: str, course: int):
    s = f'{email}{(datetime.now() - datetime(1970, 1, 1)).total_seconds()}'
    code = hashlib.sha256(s.encode()).hexdigest()
    new_user = Client(email=email, name=name, course=(course+1), rolls=(2 + 3*course), code=code)
    new_user.save()
    send_letter([email],
                'БЕСПРОИГРЫШНОЕ КОЛЕСО ЗДОРОВЬЯ',
                f'Здравствуйте, {new_user.name}'
                f'<br><br>Поздравляю Вас с покупкой🤗 и приглашаю принять участие в БЕСПРОИГРЫШНОМ Колесе Здоровья 🎁'
                f'<br><br>🍏Вам нужно перейти по ссылке, указанной в письме '
                f'<br>🍏На сайте вы найдёте Колесо Здоровья и под ним увидите кнопку «Крутить колесо»'
                f'<br>🍏Нажимайте на кнопку и выигрывайте призы!'
                f'<br><br>Информация о выигранном подарке придёт вам на почту.'
                f'<br><br>от необходимая ссылка ⬇️⬇️⬇️'
                f'<br><a href="www.forma.com/?email={email}&key={code}">www.forma.com/?email={email}&key={code}</a>')


@app.task(name="tasks.get-users")
def get_users():
    # Рассылка по клещам, добавление в бд
    for user in get_group_items(GROUP_ID_TICKS):
        existing = Client.objects.filter(email=user[1])
        if not existing:
            add_user(user[1], user[5], 0)

    # Рассылка по глистам, добавление в бд
    for user in get_group_items(GROUP_ID_WORMS):
        existing = Client.objects.filter(email=user[1])
        if not existing:
            add_user(user[1], user[5], 1)


@app.task(name='tasks.send-letter')
def send_letter(recipients, subject, message):
    image_path = 'static/img/email_picture.JPG'
    image_name = Path(image_path).name
    email = EmailMultiAlternatives(subject=subject,
                                   body=message,
                                   from_email=EMAIL_HOST_USER,
                                   to=recipients)
    email.content_subtype = 'html'
    email.mixed_subtype = 'related'

    with open(image_path, mode='rb') as f:
        image = MIMEImage(f.read())
        email.attach(image)
        image.add_header('Content-ID', f"{image_name}")
    email.send()
