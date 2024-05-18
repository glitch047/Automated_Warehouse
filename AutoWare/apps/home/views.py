# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MonthlyDataSerializer,MonthlyAvgSerializer,DailyDataSerializer
from django.db.models import Count
from django.db.models.functions import ExtractMonth,ExtractDay
import qrcode
from PIL import Image
from io import BytesIO
import base64
# from django.contrib.auth.models import User
from .models import (
    Manager,
    WareTeams,
    Supplier,
    OpTeam,
    Product,
    Notification,
    VendorRequest,
    Request,
    VendorRequestImage,
    ProductDeleted,
    ProductLogs,
    ProductAddModels,
    QR
)
from .forms import (
    ManagerForm,
    UserForm,
    NotificationForm,
    EmpForm,
    SupReqForm,
    ReqForm,
    AddProductForm
)
from apps.authentication.models import User
from collections import Counter
from django.db.models import Q


@login_required(login_url="/login/")
def indexa(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    # html_template=loader.get_template('home/landing.html')
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def index(request):
    context = {'segment': 'index'}

    # html_template = loader.get_template('home/index.html')
    html_template=loader.get_template('home/landing.html')
    return HttpResponse(html_template.render(context, request))
# Admin 
def add_manager(request):
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            if password == retype_password:
                # First, create the User instance
                user = User.objects.create_user(
                    username=username, password=password,
                    email=email, is_manager=True
                )
                # Then, create the Manager instance with the created user
                Manager.objects.create(user=user, name=name, address=address)
                return redirect('/index')
    else:
        form = ManagerForm()
        context = {'segment': 'add_manager'}
        return render(request, 'home/add_manager.html', {'form': form, **context})
    
def manager_list(request):
    managers = Manager.objects.all()
    context = {'segment': 'manager_list'}
    return render(request, 'home/manager_lists.html', {'managers': managers,**context})

def edit_manager(request,user_id):
    manager = get_object_or_404(Manager, user__id=user_id)
    if request.method == 'POST':
        form = ManagerForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            if password == retype_password:
                user = get_object_or_404(User, id=user_id)
                user.username = username
                user.email = email
                user.set_password(password)
                user.save()
                manager = Manager.objects.filter(user=user).first()
                if manager:
                    manager.name = name
                    manager.address = address
                    manager.save()
                return redirect('/index')
    else:
        form = ManagerForm(initial={
            'name': manager.name,
            'address': manager.address,
            'email': manager.user.email,
            'username': manager.user.username
        })
        return render(request, 'home/manager_edit.html', {'form': form})

def delete_manager(request,user_id):
    user = get_object_or_404(User, id=user_id)
    manager = Manager.objects.filter(user=user).first()
    if manager:
        manager.delete()
    user.delete()
    managers = Manager.objects.all()
    context = {'segment': 'manager_list'}
    return render(request, 'home/manager_lists.html', {'managers': managers, **context})

def user_list(request):
    users = User.objects.all()
    context = {'segment': 'user_list'}
    return render(request, 'home/user_lists.html', {'users': users, **context})

# Conduct Testing of this function at the end
def delete_user(request,user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_manager:
        manager = Manager.objects.filter(user=user).first()
    if user.is_warteam:
        warteam = WareTeams.objects.filter(user=user).first()
    if user.is_opsteam:
        opsteam = OpTeam.objects.filter(user=user).first()
    if user.is_supplier:
        supplier = Supplier.objects.filter(user=user).first()
    if user.is_superuser:
        superuser = User.objects.filter(user=user).first()
    if manager:
        manager.delete()
        user.delete()
    elif warteam:
        warteam.delete()
        user.delete()
    elif opsteam:
        opsteam.delete()
        user.delete()
    elif supplier:
        supplier.delete()
        user.delete()
    elif superuser:
        superuser.delete()
    
    managers = Manager.objects.all()
    context = {'segment': 'manager_list'}
    return render(request, 'home/manager_lists.html', {'managers': managers, **context})

def admin_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            image = request.FILES.get('image')
            if password == retype_password:
                user = get_object_or_404(User, id=user_id)
                user.username = username
                user.email = email
                user.set_password(password)
                if image:
                    user.image = image
                user.save()
                return redirect('/index')
    else:
        form = UserForm(initial={   
            'email': user.email,
            'username': user.username
        })
        context = {'segment': 'admin_profile'}
        return render(request, 'home/user.html', {'form': form, **context})

def notification(request,user_id,not_id=None):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']
            if user.is_opsteam:
                assigened_to_value = form.cleaned_data['assigned_op']
                assignee_value=request.POST.get('tname')
                if assignee_value == 'all':
                    user_assigned=None
                else:
                    user_assigned = get_object_or_404(User, id=assignee_value)
            elif user.is_supplier:
                assigened_to_value = form.cleaned_data['assigned_sup']
                user_assigned=None
            elif user.is_warteam:
                assigened_to_value = form.cleaned_data['assigned_war']
                assignee_value=request.POST.get('tname')
                if assignee_value == 'all':
                    user_assigned=None
                else:
                    user_assigned = get_object_or_404(User, id=assignee_value)
            elif user.is_superuser:
                assigened_to_value = form.cleaned_data['assigned_to']
                user_assigned=None
            else:
                assigened_to_value = form.cleaned_data['assigned_to']
                assignee_value=request.POST.get('tname')
                if assignee_value == 'all':
                    user_assigned=None
                else:
                    user_assigned = get_object_or_404(User, id=assignee_value)
            status_value = form.cleaned_data['status']
            if assigened_to_value == '1':
                is_manager = True
                is_warteam = False
                is_opsteam = False
                is_supplier = False
            elif assigened_to_value == '2':
                is_manager = False
                is_warteam = True
                is_opsteam = False
                is_supplier = False
            elif assigened_to_value == '3':
                is_manager = False
                is_warteam = False
                is_opsteam = True
                is_supplier = False
            elif assigened_to_value == '4':
                is_manager = False
                is_warteam = False
                is_opsteam = False
                is_supplier = True
            if status_value == '1':
                status = True
            else:
                status = False
            Notification.objects.create(
                user=user, title=title, message=message,status=status,is_manager=is_manager,is_opsteam=is_opsteam,is_supplier=is_supplier,is_warteam=is_warteam,
                assigned_to=user_assigned
            )
            if user.is_manager:
                return redirect('/manager')
            elif user.is_opsteam:
                return redirect('/op')
            elif user.is_supplier:
                return redirect('/supplier')
            elif user.is_warteam:
                return redirect('/war')
            return redirect('/index')
    else:
        form = NotificationForm()
        notifications=Notification.objects.filter(user_id=user)
        users = User.objects.filter(Q(is_opsteam=True) | Q(is_supplier=True) | Q(is_warteam=True))
        context = {'segment': 'notification'}
        if user.is_manager:
                # assigned_notifications=Notification.objects.filter(is_manager=True)
                get_notifications=Notification.objects.filter(Q(is_manager=True) & Q(assigned_to=None))
                specific_notifications=Notification.objects.filter(assigned_to=user)
                assigned_notifications = get_notifications | specific_notifications
                return render(request, 'Manager/home/notifications.html', {'form': form, **context, 'notifications':notifications, 'assigned_notifications':assigned_notifications, 'users':users})
        if user.is_opsteam:
                get_notifications=Notification.objects.filter(Q(is_opsteam=True) & Q(assigned_to=None))
                specific_notifications=Notification.objects.filter(assigned_to=user)
                assigned_notifications = get_notifications | specific_notifications
                return render(request, 'Op/home/notifications.html', {'form': form, **context, 'notifications':notifications, 'assigned_notifications':assigned_notifications})
        if user.is_warteam:
                get_notifications=Notification.objects.filter(Q(is_warteam=True) & Q(assigned_to=None))
                specific_notifications=Notification.objects.filter(assigned_to=user)
                assigned_notifications = get_notifications | specific_notifications
                return render(request, 'WareHouse/home/notifications.html', {'form': form, **context, 'notifications':notifications, 'assigned_notifications':assigned_notifications})
        if user.is_supplier:
                get_notifications=Notification.objects.filter(Q(is_supplier=True) & Q(assigned_to=None))
                specific_notifications=Notification.objects.filter(assigned_to=user)
                assigned_notifications = get_notifications | specific_notifications
                return render(request, 'Supplier/home/notifications.html', {'form': form, **context, 'notifications':notifications, 'assigned_notifications':assigned_notifications})
        return render(request, 'home/notifications.html', {'form': form, **context, 'notifications':notifications})
    
def notification_edit(request,user_id,not_id):
    user = get_object_or_404(User, id=user_id)
    notification = get_object_or_404(Notification, id=not_id)
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']
            status_value = form.cleaned_data['status']
            if status_value == '1':
                status = True
            else:
                status = False
            notification.title = title
            notification.message = message
            notification.status = status
            notification.save()
            if user.is_manager:
                return redirect('/manager')
            elif user.is_opsteam:
                return redirect('/op')
            elif user.is_supplier:
                return redirect('/supplier')
            elif user.is_warteam:
                return redirect('/war')
            else:
                return redirect('/index')
    else:
        if notification.is_manager:
            assigned_person = '1'
        elif notification.is_warteam:
            assigned_person = '2'
        elif notification.is_opsteam:
            assigned_person = '3'
        elif notification.is_supplier:
            assigned_person = '4'
        
        if notification.status:
            status = '1'
        else:
            status = '0'
        if user.is_superuser :
            form = NotificationForm(initial={
                'title': notification.title,
                'message': notification.message,
                'assigned_to': assigned_person,
                'status': status 
            })
        elif user.is_manager:
            form = NotificationForm(initial={
                'title': notification.title,
                'message': notification.message,
                # 'assigned_to': assigned_person,
                'status': status
            })
            notification = Notification.objects.get(pk=not_id)
            assigned_to_person = notification.assigned_to
            
        elif user.is_opsteam or user.is_warteam:
            form = NotificationForm(initial={
                'title': notification.title,
                'message': notification.message,
                # 'assigned_op': assigned_person,
                'status': status 
            })
            notification = Notification.objects.get(pk=not_id)
            assigned_to_person = notification.assigned_to
        else:
            form = NotificationForm(initial={
                'title': notification.title,
                'message': notification.message,
                'assigned_sup': assigned_person,
                'status': status 
            })
        context = {'segment': 'notification_edit'}
        notifications=Notification.objects.filter(user_id=user)
        if user.is_manager:
                assigned_notifications=Notification.objects.filter(user_id=user)
                return render(request, 'Manager/home/notifications_edit.html', {'form': form, **context, 'notifications':notifications, 'assigned_notifications':assigned_notifications,'assigned_to_person':assigned_to_person,'assigned_person':assigned_person})
        elif user.is_opsteam:
                assigned_notifications=Notification.objects.filter(user_id=user)
                return render(request, 'Op/home/notifications_edit.html', {'form': form, **context, 'notifications':notifications, 'assigned_notifications':assigned_notifications,'assigned_to_person':assigned_to_person,'assigned_person':assigned_person})
        elif user.is_warteam:
                assigned_notifications=Notification.objects.filter(user_id=user)
                return render(request, 'WareHouse/home/notifications_edit.html', {'form': form, **context, 'notifications':notifications, 'assigned_notifications':assigned_notifications,'assigned_to_person':assigned_to_person,'assigned_person':assigned_person})
        elif user.is_supplier:
                assigned_notifications=Notification.objects.filter(user_id=user)
                return render(request, 'Supplier/home/notifications.html', {'form': form, **context, 'notifications':notifications, 'assigned_notifications':assigned_notifications})
        else:
            return render(request, 'home/notifications.html', {'form': form, **context, 'notifications':notifications})

def notification_delete(request,user_id,not_id):
    user = get_object_or_404(User, id=user_id)
    notification = get_object_or_404(Notification, id=not_id)
    notification.delete()
    context = {'segment': 'index'}
    if user.is_manager:
        return redirect('/manager')
    elif user.is_opsteam:
        return redirect('/op')
    elif user.is_supplier:
        return redirect('/supplier')
    elif user.is_warteam:
        return redirect('/war')
    else:   
        return render(request, 'home/index.html', {**context})

def admin_reports(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, "Hello, World!")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

# Manager
@login_required(login_url="/manager/")
def manager(request):
    context = {'segment': 'index'}
    return render(request, 'Manager/home/index.html', context)

def add_product_manager(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ProductAddModels.objects.create(name=name)
        context = {'segment': 'index'}
        return render(request, 'Manager/home/index.html', context)

def add_emp(request, user_id=None):
    if request.method == 'POST':
        manager_id=request.user
        form = EmpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            team = form.cleaned_data['team']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            # manager = Manager.objects.filter(user=manager_id).first()
            manager=None
            if password == retype_password:
                if team =='1':
                    user = User.objects.create_user(
                        username=username, password=password,
                        email=email, is_warteam=True
                    )
                    WareTeams.objects.create(user=user, name=name, address=address,manager=manager)
                else:
                    user = User.objects.create_user(
                        username=username, password=password,
                        email=email, is_opsteam=True
                    )
                    OpTeam.objects.create(user=user, name=name, address=address,manager=manager)
            return redirect('/manager')
    else:
        form = EmpForm()
    context = {'segment': 'add_emp'}
    return render(request, 'Manager/home/add_emp.html',{'form':form, **context})

def emp_list(request):
    warteams = WareTeams.objects.all()
    opsteam = OpTeam.objects.filter()
    context = {'segment': 'emp_list'}
    return render(request, 'Manager/home/emp_lists.html', {'warteams': warteams, 'opsteam': opsteam ,**context})

def edit_emp(request,user_id=None):
    user = get_object_or_404(User, id=user_id)
    # manager_id=request.user
    # manager = Manager.objects.filter(user=manager_id).first()
    if user.is_warteam:
        emp = get_object_or_404(WareTeams, user__id=user_id)
    if user.is_opsteam:
        emp = get_object_or_404(OpTeam, user__id=user_id)
    if request.method == 'POST':
        form = EmpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            team = form.cleaned_data['team'] 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            if password == retype_password:
                user = get_object_or_404(User, id=user_id)
                user.username = username
                user.email = email
                user.set_password(password)
                if team =='1':
                    user.is_warteam = True
                    user.is_opsteam = False
                    user.save()
                    data = WareTeams.objects.filter(user=user).first()
                    if data:
                        data.name = name
                        data.address = address
                        data.save()
                    else:
                        WareTeams.objects.create(user=user, name=name, address=address)
                    data_rem=OpTeam.objects.filter(user=user).first()
                    if data_rem:
                        data_rem.delete()
                else:
                    user.is_warteam = False
                    user.is_opsteam = True
                    user.save()
                    data = OpTeam.objects.filter(user=user).first()
                    if data:
                        data.name = name
                        data.address = address
                        data.save()
                    else:
                        OpTeam.objects.create(user=user, name=name, address=address)
                    data_rem=WareTeams.objects.filter(user=user).first()
                    if data_rem:
                        data_rem.delete()
                return redirect('/manager/emp_lists')
    else:
        if emp.user.is_warteam:
            team = '1'
        else:
            team = '0'
        print(team)
        form = EmpForm(initial={
            'name': emp.name,
            'address': emp.address,
            'email': emp.user.email,
            'username': emp.user.username,
            'team': team
        })
        emp = WareTeams.objects.filter(user=user).first()
        print(emp)
        return render(request, 'Manager/home/emp_edit.html', {'form': form, 'emp': emp})

def delete_emp(request,user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_warteam:
        warteam = WareTeams.objects.filter(user=user).first()
        warteam.delete()
    if user.is_opsteam:
        opsteam = OpTeam.objects.filter(user=user).first()
        opsteam.delete()
    user.delete()
    manager = request.user.manager
    warteams = WareTeams.objects.filter(manager=manager)
    opsteam = OpTeam.objects.filter(manager=manager)
    context = {'segment': 'emp_list'}
    return render(request, 'Manager/home/emp_lists.html', {'warteams': warteams, 'opsteam': opsteam ,**context})

# def supplier_requests(request,user_id=None):
#     return render(request, 'Manager/home/vendor_requests.html')

def product_logs(request,user_id=None):
    product_list=ProductLogs.objects.all()
    paginated = Paginator(product_list, 15)
    page_number  = request.GET.get('page')
    page = paginated.get_page(page_number)
    context = {'segment': 'product_logs'}
    return render(request, 'Manager/home/product_logs.html', {'page': page, 'product_list': product_list, **context})
    
def product_stats(request, user_id=None):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ProductAddModels.objects.create(name=name)
        # context = {'segment': 'index'}
        # return render(request, 'Manager/home/index.html', context)
    product_list = Product.objects.all()
    paginated = Paginator(product_list, 15)
    page_number = request.GET.get('page')
    page = paginated.get_page(page_number)
    form = AddProductForm()
    latest_dates = Product.objects.values('name').annotate(latest_date=Max('created_date'))

    product_count = {}
    for product in product_list:
        product_count[product.name] = product_count.get(product.name, 0) + 1
        
    product_names= list(product_count.keys())
    product_counts = list(product_count.values())
    # print(product_count)
    context = {
        'segment': 'product_stats',
        'page': page,
        'product_counts': product_counts,
        'product_names': product_names,
        'latest_dates': latest_dates,
        'form':form
    }
    return render(request, 'Manager/home/product_stats.html', context)

def war_product_logs(request,user_id=None):
    product_list=ProductLogs.objects.all()
    paginated = Paginator(product_list, 15)
    page_number  = request.GET.get('page')
    page = paginated.get_page(page_number)
    context = {'segment': 'product_logs'}
    return render(request, 'WareHouse/home/product_logs.html', {'page': page, 'product_list': product_list, **context})

# def product_stats(request, user_id=None):
#         # context = {'segment': 'index'}
#         # return render(request, 'Manager/home/index.html', context)
#     product_list = Product.objects.all()
#     paginated = Paginator(product_list, 15)
#     page_number = request.GET.get('page')
#     page = paginated.get_page(page_number)
#     form = AddProductForm()
#     latest_dates = Product.objects.values('name').annotate(latest_date=Max('created_date'))
    

def war_product_stats(request, user_id=None):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ProductAddModels.objects.create(name=name)
    product_list = Product.objects.all()
    paginated = Paginator(product_list, 15)
    page_number = request.GET.get('page')
    page = paginated.get_page(page_number)
    form = AddProductForm()
    latest_dates = Product.objects.values('name').annotate(latest_date=Max('created_date'))
    
    # Calculate product counts
    product_count = {}
    product_id={}
    for product in product_list:
        product_count[product.name] = product_count.get(product.name, 0) + 1
        product_id[product.name] = product_id.get(product.name, 0) + product.id
        
    product_names= list(product_count.keys())
    product_counts = list(product_count.values())
    product_ids = list(product_id.values())
    # print(product_count)
    context = {
        'segment': 'product_stats',
        'page': page,
        'product_counts': product_counts,
        'product_names': product_names,
        'latest_dates': latest_dates,
        'form':form
    }
    print(latest_dates)
    return render(request, 'WareHouse/home/product_stats.html', context)

def delete_product(request,name):
    user=request.user
    delete=Product.objects.filter(name=name)
    delete_2=ProductAddModels.objects.filter(name=name)
    delete.delete()
    if delete_2:
        delete_2.delete()
    if user.is_manager:
        return redirect('/manager/product_stats')
    else:
        return redirect('/war/product_stats')
    
def supplier_req(request, user_id=None):
    user=request.user
    requests = VendorRequest.objects.filter(status='2')
    prev_requests = VendorRequest.objects.filter(Q(status='1') | Q(status='0'))
    context = {'segment': 'supplier_requests'}
    return render(request, 'Manager/home/vendor_requests.html', {'requests': requests,'prev_requests':prev_requests, **context})

def manager_req_acc(request, dec=None, req_id=None):
    request = get_object_or_404(VendorRequest, id=req_id)
    if dec == 1:
        request.status = '1'
        request.save()
    else:
        request.status = '0'
        request.save()
    return redirect('/manager/supplier_req')

def ops_req(request, user_id=None):
    user=request.user
    requests = Request.objects.filter(status='2')
    prev_requests = Request.objects.filter(Q(status='1') | Q(status='0'))
    context = {'segment': 'op_req'}
    return render(request, 'Manager/home/op_requests.html', {'requests': requests,'prev_requests':prev_requests, **context})

# Supplier
def supplier(request):
    context = {'segment': 'index'}
    user=request.user
    requests = VendorRequest.objects.filter(user=user)
    return render(request, 'Supplier/home/product_req.html', {'requests': requests, **context})

def sup_request(request, user_id=None):
    if request.method == 'POST':
        sup_id = request.user
        form = SupReqForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.cleaned_data['name']
            quote = form.cleaned_data['quote']
            quantity = form.cleaned_data['quantity']
            desp = form.cleaned_data['desp']
            images = request.FILES.get('image')

            supplier = Supplier.objects.filter(user=sup_id).first()
            VendorRequest.objects.create(
                    product=product, quote=quote,
                    quantity=quantity, desp=desp,user=sup_id,status='2',image=images
                    )
            # for img in images:
            #     VendorRequestImage.objects.create(request=request_obj, image=img)
            #     print("1")
            return redirect('/supplier')
    else:
        form = SupReqForm()
    context = {'segment': 'add_sup_req'}
    return render(request, 'Supplier/home/add_req.html',{'form':form, **context})

def sup_request_history(request, user_id=None):
    user=request.user
    requests = VendorRequest.objects.filter(user=user)
    context = {'segment': 'sup_request_history'}
    return render(request, 'Supplier/home/product_req.html', {'requests': requests, **context})

# OP
def op(request):
    context = {'segment': 'index'}
    # return render(request, 'Op/home/add_req.html', context)
    form = ReqForm()
    unique_product_names = Product.objects.values('name').distinct()
    return render(request, 'Op/home/add_req.html', {'form':form,'unique_product_names':unique_product_names, **context})

def op_request(request):
    if request.method == 'POST':
        op_id = request.user
        form = ReqForm(request.POST)
        product=request.POST.get('name')
        print(product)
        product_id=Product.objects.filter(name=product).first()
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            Request.objects.create(
                    product=product_id,
                    quantity=quantity,user=op_id,status='2',
                    )
            return redirect('/op')            
    else:
        form = ReqForm()
        unique_product_names = Product.objects.values('name').distinct()
    context = {'segment': 'op_request'}
    return render(request, 'Op/home/add_req.html', {'form':form,'unique_product_names':unique_product_names, **context})

def vendor_request(request):
    user=request.user
    requests = VendorRequest.objects.filter(status='2')
    prev_requests = VendorRequest.objects.filter(Q(status='1') | Q(status='0'))
    context = {'segment': 'vendor_request'}
    return render(request, 'WareHouse/home/vn_requests.html', {'requests': requests,'prev_requests':prev_requests, **context})

def op_request_history (request, user_id=None):
    user=request.user
    requests = Request.objects.filter(user=user)
    context = {'segment': 'request_history'}
    return render(request, 'Op/home/product_req.html', {'requests': requests, **context})

# Warehouse Team
def war(request):
    context = {'segment': 'index'}
    return render(request, 'WareHouse/home/index.html', context)

def war_req(request, user_id=None):
    user=request.user
    requests = Request.objects.filter(status='2')
    prev_requests = Request.objects.filter(Q(status='1') | Q(status='0'))
    context = {'segment': 'war_req'}
    return render(request, 'WareHouse/home/op_requests.html', {'requests': requests,'prev_requests':prev_requests, **context})

def war_req_acc(request, dec=None, req_id=None):
    request = get_object_or_404(Request, id=req_id)
    if dec == 1:
        request.status = '1'
        name=request.product
        quantity=request.quantity
        products_to_delete  = Product.objects.filter(name=name)[:quantity]
        for product in products_to_delete:
            product_log = ProductLogs.objects.create(
                name=product.name,
                batchno=product.batchno,
                productno=product.productno,
                action='Deleted'
            )
            product_deleted = ProductDeleted.objects.create(
                name=product.name,
                batchno=product.batchno,
                productno=product.productno,
            )
            product.delete()
        request.save()
    else:
        request.status = '0'
        request.save()
    return redirect('war')

def war_request_history (request, user_id=None):
    user=request.user
    requests = Request.objects.filter(user=user)
    context = {'segment': 'request_history'}
    return render(request, 'WarHouse/home/product_req.html', {'requests': requests, **context})

# Graphs
# Monthly Added Products
class MonthlyDataAPIView(APIView):
    def get(self, request):
        monthly_data = Product.objects.annotate(month=ExtractMonth('created_date')).values('month').annotate(count=Count('id')).order_by('month')
        def sort_key(item):
            return int(item['month'])
        monthly_data = sorted(monthly_data, key=sort_key)
        serializer = MonthlyDataSerializer(monthly_data, many=True)
        # print(serializer.data)
        return Response(serializer.data)
    
from django.http import JsonResponse    
def get_users_by_category(request):
    selected_category = request.GET.get('category', None)
    if selected_category:
        if selected_category == '1':
            users = User.objects.filter(is_manager=True)
        elif selected_category == '2':
            users = User.objects.filter(is_warteam=True)
        elif selected_category == '3':
            users = User.objects.filter(is_opsteam=True)
        elif selected_category == '4':
            users = User.objects.filter(is_supplier=True)
        else:
            users = User.objects.none()  # Return an empty queryset if category is invalid
    else:
        users = User.objects.none()  # Return an empty queryset if no category is selected
    data = [{'id': user.id, 'username': user.username} for user in users]
    print(data)
    return JsonResponse(data, safe=False)
# class MonthlyDataAPIView(APIView):
#     def get(self, request):
#         # Fetch data from the database and format it
#         monthly_data = Product.objects.annotate(month=ExtractMonth('created_date')).values('month').annotate(count=Count('id'))
        
#         # Sort the monthly data by month
#         sorted_response = sorted(monthly_data, key=lambda x: int(x['month']))
        
#         return Response(sorted_response)

# Avg for Added and Deleted Products
class MonthlyAvgAPIView(APIView):
    def get(self, request):
        monthly_data = Product.objects.annotate(month=ExtractMonth('created_date')).values('month').annotate(count=Count('id')).order_by('month')
        monthly_data_dlt = ProductDeleted.objects.annotate(month=ExtractMonth('created_date')).values('month').annotate(count=Count('id')).order_by('month')
        
        monthly_data_dict = {item['month']: item['count'] for item in monthly_data}
        monthly_data_dlt_dict = {item['month']: item['count'] for item in monthly_data_dlt}
        combined_monthly_avg_data = []
        for month in range(1, 13):
            data_count = monthly_data_dict.get(month, 0)
            data_dlt_count = monthly_data_dlt_dict.get(month, 0)
            combined_avg = (data_count + data_dlt_count) // 2 
            combined_monthly_avg_data.append({
                'month': month,
                'monthly_data_avg': data_count,
                'monthly_data_deleted_avg': data_dlt_count,
                'combined_avg': combined_avg
            })
        serializer = MonthlyAvgSerializer(combined_monthly_avg_data, many=True)
        return Response(serializer.data)
# Monthly Deleted Products
class MonthlyDltAPIView(APIView):
    def get(self, request):
        monthly_data = ProductDeleted.objects.annotate(month=ExtractMonth('created_date')).values('month').annotate(count=Count('id'))
        serializer = MonthlyDataSerializer(monthly_data, many=True)
        # print(serializer.data)
        return Response(serializer.data)
# Daily Avg
class DailyDataAPIView(APIView):
    def get(self, request):
        daily_data = Product.objects.annotate(
            day=ExtractDay('created_date'),
            month=ExtractMonth('created_date')
        ).values('day', 'month').annotate(count=Count('id'))
        serializer = DailyDataSerializer(daily_data, many=True)
        print(serializer.data)
        return Response(serializer.data)
# For All Users
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            image = request.FILES.get('image')
            if password == retype_password:
                user = get_object_or_404(User, id=user_id)
                user.username = username
                user.email = email
                user.set_password(password)
                if image:
                    user.image = image
                user.save()
                return redirect('/login')
        return redirect('/manager')
    else:
        form = UserForm(initial={   
            'email': user.email,
            'username': user.username
        })
        context = {'segment': 'user_profile'}
        if user.is_manager:
            return render(request, 'Manager/home/user.html', {'form': form, **context})
        elif user.is_supplier:
            return render(request, 'Supplier/home/user.html', {'form': form, **context})
        elif user.is_opsteam:
            return render(request, 'Op/home/user.html', {'form': form, **context})
        elif user.is_warteam:
            return render(request, 'WareHouse/home/user.html', {'form': form, **context})
        else:
            return render(request, 'home/user.html', {'form': form, **context})
        
from django.core.files.base import ContentFile 
def qr(request):
    context = {'segment': 'qr'}
    # data={}
    if request.method == "POST":
        qr_text = request.POST.get("qr_text", "")
        qr_image = qrcode.make(qr_text, box_size=15)
        qr_image_pil = qr_image.get_image()
        stream = BytesIO()
        qr_image_pil.save(stream, format='PNG')
        qr_code = QR.objects.create(data=qr_text)
        qr_code.image.save(f'{qr_text}.png', ContentFile(stream.getvalue()), save=True)  # Use ContentFile
        qr_image_data = stream.getvalue()
        qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
        context['qr_image_base64'] = qr_image_base64
        context['variable'] = qr_text
        
        
    # context = {'segment': 'qr'}
    return render(request, 'Manager/home/qr.html', context=context)