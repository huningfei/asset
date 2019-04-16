# -*- coding: utf-8 -*-
from django.shortcuts import render
import os
import mimetypes
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
import xlrd
from asset import mypage
from hnf.forms.customer import UserinfoForm
from hnf.forms.asset import AssetForm
from hnf import models

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from hnf.utils.urls import memory_reverse

# Create your views here.
# 登录页面
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        next_url = request.GET.get("next")

        username = request.POST.get("username")
        pwd = request.POST.get("password")
        user_obj = auth.authenticate(request, username=username, password=pwd)
        if user_obj:
            auth.login(request, user_obj)  # # 给该次请求设置了session数据，并在响应中回写cookie
            if next_url:
                return redirect(next_url)
            else:
                return redirect("/asset/list/")
        else:
            return render(request, "login.html", {"error_msg": "用户名或密码错误"})

# 注销页面
def logout(request):
    auth.logout(request)
    return redirect("/login/")

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'result.html', {'error_msg': error_msg})

    # post_list = models.Asset.objects.filter(leader__icontains=q)
    # for i in post_list:
    data_list=models.Asset.objects.filter(leader__contains=q)
    return render(request, 'result.html', {'error_msg': error_msg, 'post_list': data_list})

# def user_list(request):
#     """
#     用户列表
#     :return:
#     """
#     data_list = models.Userinfo.objects.all()
#
#     return render(request, 'user_list.html', {'data_list': data_list})


# def user_add(request):
#     """
#     添加用户
#     :param request:
#     :return:
#     """
#     if request.method == 'GET':
#         form = UserinfoForm()
#         return render(request, 'user_add.html', {'form': form})
#     form = UserinfoForm(data=request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect('/user/list/')
#     return render(request, 'user_add.html', {'form': form})
#
#
# def user_edit(request, cid):
#     """
#     编辑客户
#     :return:
#     """
#     obj = models.Userinfo.objects.get(id=cid)
#     if request.method == 'GET':
#         form = UserinfoForm(instance=obj)
#         return render(request, 'user_edit.html', {'form': form})
#     form = UserinfoForm(data=request.POST, instance=obj)
#     if form.is_valid():
#         form.save()
#         return redirect('/user/list/')
#     return render(request, 'user_edit.html', {'form': form})
#
#
# def user_del(request, cid):
#     """
#     删除客户
#     :param request:
#     :param cid:
#     :return:
#     """
#     models.Userinfo.objects.filter(id=cid).delete()
#     return redirect('/user/list/')


# def user_import(request):
#     """
#     批量导入用户
#     :param request:
#     :return:
#     """
#
#     if request.method == 'GET':
#         return render(request, 'user_import.html')
#
#     context = {'status': True, 'msg': '导入成功'}
#     try:
#         customer_excel = request.FILES.get('customer_excel')
#         """
#         打开上传的Excel文件，并读取内容
#         注：打开本地文件时，可以使用：workbook = xlrd.open_workbook(filename='本地文件路径.xlsx')
#         """
#         workbook = xlrd.open_workbook(file_contents=customer_excel.file.read())
#
#         # sheet = workbook.sheet_by_name('工作表1')
#         sheet = workbook.sheet_by_index(0)
#         row_map = {
#             0: {'text': '用户名', 'name': 'username'},
#             1: {'text': '密码', 'name': 'password'},
#             2: {'text': '部门', 'name': 'department'},
#
#         }
#         object_list = []
#         for row_num in range(1, sheet.nrows):
#             row = sheet.row(row_num)
#             print(row)
#             row_dict = {}
#             for col_num, name_text in row_map.items():
#                 row_dict[name_text['name']] = row[col_num].value
#             object_list.append(models.Userinfo(**row_dict))
#
#         models.Userinfo.objects.bulk_create(object_list, batch_size=20)
#     except Exception as e:
#         context['status'] = False
#         context['msg'] = '导入失败'
#
#     return render(request, 'user_import.html', context)
#
#
# def user_tpl(request):
#     """
#     下载批量导入Excel列表
#     :param request:
#     :return:
#     """
#     tpl_path = os.path.join(settings.BASE_DIR, 'hnf', 'files', '批量导入用户模板.xlsx')
#     content_type = mimetypes.guess_type(tpl_path)[0]
#     print(content_type)
#     response = FileResponse(open(tpl_path, mode='rb'), content_type=content_type)
#     response['Content-Disposition'] = "attachment;filename=%s" % 'user_excel_tpl.xlsx'
#     return response

@login_required()
def asset_list(request):
    """
    资产列表
    :return:
    """
    data_list = models.Asset.objects.all()
    print(data_list)
    total_count = data_list.count()

    current_page = request.GET.get("page")

    page_boj = mypage.MyPage(current_page, total_count, url_prefix="asset/list")
    data = data_list[page_boj.start:page_boj.end]  # 从第几页显示到第几页

    page_html = page_boj.page_html()  # 页面
    page_num = page_boj.num()  # 序号

    return render(request, 'asset_list.html', {'data_list': data, 'page_html': page_html, 'num': page_num})


def asset_add(request):
    """
    添加资产
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = AssetForm()
        return render(request, 'asset_add.html', {'form': form})
    form = AssetForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/asset/list/')
    return render(request, 'asset_add.html', {'form': form})


def asset_edit(request, cid):
    """
    编辑资产
    :return:
    """
    obj = models.Asset.objects.get(id=cid)
    if request.method == 'GET':
        form = AssetForm(instance=obj)
        return render(request, 'asset_edit.html', {'form': form})
    form = AssetForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/asset/list/')
    return render(request, 'asset_edit.html', {'form': form})


def asset_del(request, cid):
    """
    删除资产
    :param request:
    :param cid:
    :return:
    """
    # models.Asset.objects.filter(id=cid).delete()
    #
    # return redirect('/asset/list/')

    origin = memory_reverse(request, 'asset_list')
    print(origin)
    if request.method == 'GET':
        return render(request, 'delete.html', {'cancel': origin})
    models.Asset.objects.filter(id=cid).delete()
    return redirect(origin)


def asset_import(request):
    """
    批量导入
    :param request:
    :return:
    """

    if request.method == 'GET':
        return render(request, 'asset_import.html')

    context = {'status': True, 'msg': '导入成功'}
    try:
        customer_excel = request.FILES.get('customer_excel')
        """
        打开上传的Excel文件，并读取内容
        注：打开本地文件时，可以使用：workbook = xlrd.open_workbook(filename='本地文件路径.xlsx')
        """
        workbook = xlrd.open_workbook(file_contents=customer_excel.file.read())

        # sheet = workbook.sheet_by_name('工作表1')
        sheet = workbook.sheet_by_index(0)
        row_map = {
            0: {'text': '品牌', 'name': 'brand'},
            1: {'text': '型号', 'name': 'model'},
            2: {'text': '编号', 'name': 'number'},
            3: {'text': '领用时间', 'name': 'leader_time'},
            4: {'text': '领用人', 'name': 'leader'},
            5: {'text': '归还时间', 'name': 'return_time'},
            6: {'text': '备注', 'name': 'other'},

        }
        object_list = []
        for row_num in range(1, sheet.nrows):
            row = sheet.row(row_num)
            print(row)
            row_dict = {}
            for col_num, name_text in row_map.items():
                row_dict[name_text['name']] = row[col_num].value
            object_list.append(models.Asset(**row_dict))

        models.Asset.objects.bulk_create(object_list, batch_size=20)
    except Exception as e:
        context['status'] = False
        context['msg'] = '导入失败'

    return render(request, 'asset_import.html', context)


def asset_tpl(request):
    """
    下载批量导入Excel列表
    :param request:
    :return:
    """
    tpl_path = os.path.join(settings.BASE_DIR, 'hnf', 'files', '批量导入资产模板.xlsx')
    content_type = mimetypes.guess_type(tpl_path)[0]
    print(content_type)
    response = FileResponse(open(tpl_path, mode='rb'), content_type=content_type)
    response['Content-Disposition'] = "attachment;filename=%s" % 'asset_excel_tpl.xlsx'
    return response
