# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
# from django.core import settings
from django.conf.urls.static import static
from core import settings
urlpatterns = [

    # The home page
    path('', views.index, name='index'),
    path('index/', views.indexa, name='home'),
    
    # path('login/', views.login, name='login'),
    
    # Admin
    path('add-manager/',views.add_manager,name='add_manager'),
    path('manager_lists/',views.manager_list,name='manager_lists'),
    path('edit_manager/<int:user_id>',views.edit_manager,name='edit_manager'),
    path('delete_manager/<int:user_id>',views.delete_manager,name='delete_manager'),
    path('user_list/',views.user_list,name='user_list'),
    path('delete_user/<int:user_id>',views.delete_user,name='delete_user'),
    path('admin_profile/<int:user_id>',views.admin_profile,name='admin_profile'),
    path('notification/<int:user_id>',views.notification,name='notification'),
    path('notification_edit/<int:user_id>/<int:not_id>',views.notification_edit,name='notification_edit'),
    path('notification_delete/<int:user_id>/<int:not_id>',views.notification_delete,name='notification_delete'),
    # Manager
    path('manager/',views.manager,name='manager'),
    path('manager/add-emp/',views.add_emp,name='add_emp'),
    path('manager/emp_lists/',views.emp_list,name='emp_lists'),
    path('manager/edit_emp/<int:user_id>',views.edit_emp,name='edit_emp'),
    path('manager/delete_emp/<int:user_id>',views.delete_emp,name='delete_emp'),
    path('manager/profile/<int:user_id>',views.user_profile,name='user_profile'),
    path('manager/notification/<int:user_id>',views.notification,name='manager_notification'),
    path('manager/notification_edit/<int:user_id>/<int:not_id>',views.notification_edit,name='manager_notification_edit'),
    path('manager/notification_delete/<int:user_id>/<int:not_id>',views.notification_delete,name='manager_notification_delete'),
    path('manager/product/submit',views.add_product_manager,name='product.submit'),
    # path('manager/supplier/requests/',views.supplier_requests,name='supplier_requests'),
    path('manager/product_logs',views.product_logs,name='product_logs'),
    path('manager/product_stats',views.product_stats,name='product_stats'),
    path('manager/supplier_req',views.supplier_req,name='supplier_req'),
    path('manager/supplier_req/<int:req_id>/<int:dec>',views.manager_req_acc,name='manager_req_acc'),
    path('manager/ops_req/',views.ops_req,name='ops_req'),
    path('manager/qrcode',views.qr,name='qrcode'),
    # Supplier
    path('supplier/',views.supplier,name='supplier'),
    path('suppler/put_request/',views.sup_request,name='put_request'),
    path('supplier/requests/',views.sup_request_history,name='sup_request_history'),
    path('supplier/profile/<int:user_id>',views.user_profile,name='sup_user'),
    path('supplier/notification/<int:user_id>',views.notification,name='supplier_notification'),
    path('supplier/notification_edit/<int:user_id>/<int:not_id>',views.notification_edit,name='supplier_notification_edit'),
    path('supplier/notification_delete/<int:user_id>/<int:not_id>',views.notification_delete,name='supplier_notification_delete'),
    # OpTeam
    path('op/',views.op,name='opteam'),
    path('op/put_request/',views.op_request,name='op_request'),
    path('op/requests/',views.op_request_history,name='op_request_history'),
    path('op/profile/<int:user_id>',views.user_profile,name='op_user'),
    path('op/notification/<int:user_id>',views.notification,name='op_notification'),
    path('op/notification_edit/<int:user_id>/<int:not_id>',views.notification_edit,name='op_notification_edit'),
    path('op/notification_delete/<int:user_id>/<int:not_id>',views.notification_delete,name='op_notification_delete'),
    # WarTeam
    path('war/',views.war,name='war'),
    path('war/get_request/',views.op_request,name='op_requests'),
    path('war/requests/',views.war_req,name='war_req'),
    path('war/vendor/requests/',views.vendor_request,name='vendor_request'),
    path('war/requests/<int:req_id>/<int:dec>',views.war_req_acc,name='war_req_acc'),
    path('war/profile/<int:user_id>',views.user_profile,name='war_user'),
    path('war/notification/<int:user_id>',views.notification,name='war_notification'),
    path('war/notification_edit/<int:user_id>/<int:not_id>',views.notification_edit,name='war_notification_edit'),
    path('war/notification_delete/<int:user_id>/<int:not_id>',views.notification_delete,name='war_notification_delete'),
    path('war/product_logs',views.war_product_logs,name='war_product_logs'),
    path('war/product_stats',views.war_product_stats,name='war_product_stats'),
    # Matches any html file
    # Delete Stats Product
    path('delete_product/<str:name>',views.delete_product,name='delete_product'),
    # API 
    path('api/monthly-data/', views.MonthlyDataAPIView.as_view(), name='monthly_data_api'),
    path('api/monthly-avg/', views.MonthlyAvgAPIView.as_view(), name='monthly_data_api'),
    path('api/monthly-dlt/', views.MonthlyDltAPIView.as_view(), name='monthly_data_api'),
    path('api/monthly-daily/', views.DailyDataAPIView.as_view(), name='monthly_data_api'),
    path('api/get_users_by_category/', views.get_users_by_category, name='get_users_by_category'),
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)