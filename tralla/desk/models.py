from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# class Desk(models.Model):
    # user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
#     # name = User.username
#     # name = models.CharField(User.username, max_length=150, default='name')
#     # boards = models.ManyToManyField('Board')

    # class Meta:
    #     verbose_name = 'Рабочее место'
    #     verbose_name_plural = 'Рабочие места'

    # def __str__(self):
    #     return self.user.username


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    data = models.JSONField()

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    def __str__(self):
        return self.name
