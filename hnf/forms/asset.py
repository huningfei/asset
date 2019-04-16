#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from django import forms
from hnf import models


class AssetForm(ModelForm):
    class Meta:
        model = models.Asset
        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super(AssetForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' # 应用样式
            # field.widget.attrs['id'] = 'time' # 应用样式
            field.widget.attrs['placeholder'] = field.label #默认显示的字段
        # self.fields['brand'].empty_label = "请选择品牌"
        self.fields['other'].required = False
        self.fields['return_time'].required = False



class PaymentUserForm(ModelForm):
    class Meta:
        model = models.Asset
        exclude = ['customer',]

    def __init__(self, *args, **kwargs):
        super(PaymentUserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
