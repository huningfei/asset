#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from hnf import models
from django import forms


class UserinfoForm(ModelForm):
    class Meta:
        model = models.Userinfo
        fields = "__all__"
        widgets = {
            "password": forms.widgets.PasswordInput(attrs={"class": "form-control"}),
    }

    def __init__(self, *args, **kwargs):
        super(UserinfoForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
