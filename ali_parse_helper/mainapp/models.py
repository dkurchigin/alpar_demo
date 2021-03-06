from django.db import models
from accounts.models import CustomUser


class ParsingTasks(models.Model):
    class Meta:
        verbose_name = 'Задача для парсинга'
        verbose_name_plural = 'Задачи для парсинга'

    link = models.TextField(verbose_name='Ссылка')
    activate = models.BooleanField(verbose_name='Активно?', default=True)
    update_time = models.IntegerField(verbose_name='Время обновления(в часах)', default=24)
    task_user_id = models.ForeignKey(CustomUser, verbose_name='ID пользователя', on_delete=models.CASCADE,
                                related_name='task_user_id')

    def __str__(self):
        return self.link


class ParsingResults(models.Model):
    class Meta:
        verbose_name = 'Результаты парсинга'
        verbose_name_plural = 'Результаты парсинга'

    task_id = models.ForeignKey(ParsingTasks, verbose_name='ID задания', on_delete=models.CASCADE, related_name='task_id')
    status = models.IntegerField(verbose_name='Код статуса')
    json = models.TextField(verbose_name='JSON', default='')
    datetime = models.DateTimeField(verbose_name='Дата и время', auto_now_add=True)

    def __str__(self):
        return f'{self.task_id}|{self.datetime}'
