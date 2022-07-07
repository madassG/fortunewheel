from pathlib import Path

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from clients.models import Client, Reward, Wins, Question
from clients.tasks import send_letter
from glisti.email_content import REWARDS
from datetime import datetime, timezone
import random


def get_reward(request, email: str):
    key = request.GET.get('key')
    if not key:
        return JsonResponse({'success': False,
                             'error_message': 'Предоставьте ключ в GET параметр key',
                             'error_code': 401,
                             'reward_code': None,
                             'reward_text': ''})
    user = Client.objects.filter(email=email)
    if not user:
        return JsonResponse({'success': False,
                             'error_message': f'Пользователь с почтой {email} не найден.',
                             'error_code': 404,
                             'reward_code': None,
                             'reward_text': ''})
    user = user[0]

    if user.code != key:
        return JsonResponse({'success': False,
                             'error_message': 'Предоставлен неверный ключ для пользователя.',
                             'error_code': 403,
                             'reward_code': None,
                             'reward_text': ''})

    if user.rolls == 0:
        return JsonResponse({'success': False,
                             'error_message': 'У вас не осталось вращений.',
                             'error_code': 401,
                             'reward_code': None,
                             'reward_text': ''})
    user.rolls = user.rolls - 1
    user.save()
    now = datetime.now(tz=timezone.utc)
    rewards = Reward.objects.filter(drop_start__lte=now, drop_end__gte=now, quantity__gt=0)
    anytime_prizes = Reward.objects.filter(quantity=-1)

    if not user.dropped_required and user.rolls == 0:
        user.rolls = 0
        user.dropped_required = True
        user.save()
        prize = Reward.objects.get(required_for_type=user.course)
        return JsonResponse({
            'success': True,
            'error_message': '',
            'error-code': None,
            'reward_code': prize.prize_code,
            'reward_text': prize.title
        })

    if random.random() < user.probability and len(rewards) > 0:
        prize = rewards[random.randint(0, len(rewards) - 1)]
        prize.quantity = prize.quantity - 1
        prize.save()

        send_mail_prize(user, prize)

        return JsonResponse({
            'success': True,
            'error_message': '',
            'error-code': None,
            'reward_code': prize.prize_code,
            'reward_text': prize.title
        })
    else:
        prize = anytime_prizes[random.randint(0, len(anytime_prizes) - 1)]
        if prize.required_for_type == user.course:
            user.dropped_required = True
            user.save()

        send_mail_prize(user, prize)
        return JsonResponse({
            'success': True,
            'error_message': '',
            'error-code': None,
            'reward_code': prize.prize_code,
            'reward_text': prize.title
        })


def index(request):
    email = request.GET.get('email')
    key = request.GET.get('key')

    if not email or not key:
        return render(request, 'redirect.html', {'error': 'Ошибка. Перейдите по ссылке с почты!'})

    user = Client.objects.filter(email=email)
    if not user:
        return render(request, 'redirect.html',
                      {'error': 'Приобретите курс либо попробуйте позже.'})

    if user[0].code != key:
        return render(request, 'redirect.html',
                      {'error': 'Ошибка аутентификации. Попробуйте снова перейти по ссылке из письма'})

    if request.method == 'POST':
        Question(author=user[0].email, question=request.POST.get('text')).save()
        return render(request, 'index.html', {'user': user[0], 'key': key})

    return render(request, 'index.html', {'user': user[0], 'key': key})


def send_mail_prize(user, prize):
    Wins(winner=user, prize=prize).save()
    image_path = 'static/img/email_picture.JPG'
    image_name = Path(image_path).name
    body = f'<html><head></head><body><img src="cid:{image_name}"/>Здравствуйте, {user.name}.<br><br>{REWARDS[prize.prize_code]["text"]}</body></html>'
    send_letter.delay([user.email], REWARDS[prize.prize_code]["topic"], body)
