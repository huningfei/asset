# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

class Userinfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    department = models.CharField(verbose_name='部门', max_length=32)

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name



class Asset(models.Model):
    """
    资产表
    """
    brand = models.CharField(verbose_name='品牌', max_length=32)
    model = models.CharField(verbose_name='型号', max_length=32)
    number = models.CharField(verbose_name='编号', max_length=32)
    leader_time = models.DateTimeField(verbose_name='领用时间', max_length=32)
    leader = models.CharField(verbose_name='领用人', max_length=32)
    return_time = models.DateTimeField(verbose_name='归还时间', max_length=32,null=True)
    other = models.CharField(verbose_name='备注', max_length=128,null=True)

    def __str__(self):

        return self.leader

    class Meta:
        verbose_name="资产表"
        verbose_name_plural = verbose_name
