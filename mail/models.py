import datetime

from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    '''Получатели рассылки'''
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', **NULLABLE)
    surname = models.CharField(max_length=100, verbose_name="Отчество")
    contact_email = models.EmailField(verbose_name='Емейл', unique=True)
    comment = models.TextField(max_length=300, verbose_name="Комментарий", help_text="Напишите уточняющую информацию",
                               **NULLABLE)

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.contact_email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('last_name', 'first_name', 'contact_email')


class Message(models.Model):
    """Сообщение рассылки"""
    title = models.CharField(max_length=100, verbose_name='Тема письма', default='Без темы')
    body = models.TextField(verbose_name='Основное содержание', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('title',)


class Mailing(models.Model):
    '''Настройки рассылки'''
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    PERIOD_CHOICES = [
        ('once', '1 раз'),
        ('every_day', 'Ежедневно'),
        ('every_week', 'Еженедельно'),
        ('every_month', 'Ежемесячно'),
    ]
    start_datetime_mailing = models.DateField(verbose_name='Дата и время начала отправки рассылки',
                                              default=datetime.datetime.now())
    stop_datetime_mailing = models.DateTimeField(verbose_name='Дата и время окончания отправки рассылки',
                                                 default=datetime.datetime.now)
    mailing_period = models.CharField(max_length=25, verbose_name='Периодичность рассылки', choices=PERIOD_CHOICES,
                                      default='once')
    mailing_status = models.CharField(max_length=25, verbose_name='Статус выполнения рассылки', choices=STATUS_CHOICES,
                              default='created')

    clients = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    message = models.ForeignKey(Message, verbose_name='Сообщение рассылки', on_delete=models.CASCADE, **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='Название рассылки', **NULLABLE)
    is_active = models.BooleanField(verbose_name='Активность рассылки', default=True)


def __str__(self):
    return f'{self.name}, Начало {self.start_datetime_mailing}, повтор {self.mailing_period}, ' \
           f'статус {self.mailing_status}'


class Meta:
    verbose_name = 'Рассылка'
    verbose_name_plural = 'Рассылки'


class Mail_attempt(models.Model):
    """Попытка отправки рассылки"""

    STATUS_CHOICES = [
        ('Succes', 'Успешно'),
        ('Non-succes', 'Неуспешно')
    ]
    attempt_time = models.DateTimeField(verbose_name='Дата и время последней попытки', **NULLABLE)
    attempt_status = models.CharField(max_length=20, verbose_name='Статус попытки', choices=STATUS_CHOICES,
                                      default='Succes')
    server_response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)

    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', on_delete=models.CASCADE, **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент рассылки', **NULLABLE)


    def __str__(self):
        return f'Попытка отправки рассылки {self.attempt_time}, статус - {self.attempt_status}'

    class Meta:
        verbose_name = 'Попытка отправки рассылки'
        verbose_name_plural = 'Попытки отправки рассылки'



