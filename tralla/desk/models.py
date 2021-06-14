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
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    # def get_absolute_url(self):
    #     from django.urls import reverse
    #     return reverse('people.views.details', args=[str(self.id)])

    def __str__(self):
        return f'Название: {self.name}, Владелец: {self.user}'


class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    position = models.IntegerField(default=0)

    def __str__(self):
        return f'Название: {self.name}, Доска: {self.board.name}, Владелец: {self.user}'


class Card(models.Model):
    name = models.TextField()
    description = models.TextField(null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    position = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def is_overdue(self):
        return True
