from django.db import models


class Client(models.Model):
    ORDER_TYPE = (
        (1, 'Клещи'),
        (2, 'Глисты'),
    )

    COURSE_TRANSLATE = ['Клещи', 'Глисты']

    email = models.CharField(max_length=100, verbose_name='Почта', unique=True)
    name = models.CharField(max_length=100, verbose_name='Имя', null=True, blank=True)
    course = models.PositiveSmallIntegerField(
        choices=ORDER_TYPE,
        default=1,
        verbose_name='Покупка'
    )
    rolls = models.IntegerField(default=0)
    code = models.CharField(max_length=100)
    dropped_required = models.BooleanField(default=False)
    probability = models.FloatField(default=0.1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} {self.COURSE_TRANSLATE[self.course - 1]}'


class Reward(models.Model):
    ORDER_TYPE = (
        (1, 'Клещи'),
        (2, 'Глисты'),
        (3, 'Необязательный')
    )
    title = models.CharField(max_length=200)
    prize_code = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    drop_start = models.DateTimeField()
    drop_end = models.DateTimeField()
    required_for_type = models.PositiveSmallIntegerField(
        choices=ORDER_TYPE,
        default=3,
        verbose_name='Обязательный приз для:'
    )

    def __str__(self):
        return f'{self.title} {self.quantity}'


class Wins(models.Model):
    winner = models.ForeignKey(Client, on_delete=models.CASCADE)
    prize = models.ForeignKey(Reward, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.winner} - {self.prize}'


class Question(models.Model):
    author = models.CharField(max_length=100)
    question = models.TextField()

    def __str__(self):
        return f'{self.author}: {self.question[:20]}'
