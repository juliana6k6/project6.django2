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
    start_datetime_mailing = models.DateField(verbose_name='дата и время первой отправки рассылки',
                                              default=datetime.datetime.now())
    stop_datetime_mailing = models.DateTimeField(verbose_name='дата и время последней отправки рассылки',
                                                 default=datetime.datetime.now)
    mailing_period = models.CharField(max_length=25, verbose_name='Периодичность рассылки', choices=PERIOD_CHOICES,
                                      default='once')
    mailing_status = models.CharField(max_length=25, verbose_name='Статус выполнения рассылки', choices=STATUS_CHOICES,
                              default='created')

    client = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE, **NULLABLE)






