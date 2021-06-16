from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    def __str__(self):
        return f'Название: {self.name}, Владелец: {self.user}'


class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    position = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Колонка'
        verbose_name_plural = 'Колонки'

    def __str__(self):
        return f'Название: {self.name}, Доска: {self.board.name}, Владелец: {self.user}'


class Card(models.Model):
    name = models.TextField()
    description = models.TextField(null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    position = models.IntegerField()

    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'

    def __str__(self):
        return self.name
