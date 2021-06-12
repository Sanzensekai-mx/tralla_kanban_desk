from django.forms import ModelForm, TextInput, Textarea, HiddenInput, CharField, JSONField
from .models import Board


class BoardForm(ModelForm):
    # user = CharField(widget=HiddenInput())
    # name = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Название карты'
    # }))
    # data = JSONField(widget=Textarea(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Json'
    # }))
    class Meta:
        model = Board
        fields = ['name', 'data']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название карты'
            }),
            "data": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Json'
            })
        }
