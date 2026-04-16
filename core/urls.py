from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.dashboard),
    path('logs/', views.logs),
    path('employees/', views.employees, name='employees'),
    path('employees/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('employees/export/', views.export_employees, name='export_employees'),
    path('branches/', views.branches, name='branches'),
    path('branches/upload/', views.upload_branches_excel, name='upload_branches_excel'),
    path('branches/export/', views.export_branches, name='export_branches'),
    path('branches/edit/<int:id>/', views.edit_branch, name='edit_branch'),
    path('branches/delete/<int:id>/', views.delete_branch, name='delete_branch'),


    path('calendar/', views.calendar),
    path('notice/', views.notice),
    path('compliance/', views.compliance),
    path('compliance/new/', views.compliance_form),
    path('forms/', views.forms),
    path('convert/', views.convert),
]