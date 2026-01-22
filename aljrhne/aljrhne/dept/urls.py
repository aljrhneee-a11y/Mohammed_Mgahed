from django.urls import path
from . import views

app_name = 'dept'

urlpatterns = [
    # الصفحات الأساسية
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # الإدارة (تم تغيير المسار لتجنب التضارب مع Django Admin)
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/manage-data/', views.manage_data, name='manage_data'),
    path('dashboard/export-csv/', views.export_csv, name='export_csv'),
    path('dashboard/add-user/', views.add_user_api, name='add_user_api'),
    path('dashboard/user/<int:user_id>/toggle-role/', views.toggle_user_role, name='toggle_user_role'),
    
    # الدورات
    path('course/create/', views.create_course, name='create_course'),
    path('course/<uuid:course_id>/delete/', views.delete_course, name='delete_course'),
    path('course/<uuid:course_id>/edit/', views.edit_course_name, name='edit_course_name'),
    
    # المشاركون
    path('course/<uuid:course_id>/add-participant/', views.add_participant, name='add_participant'),
    path('course/<uuid:course_id>/participants/', views.list_participants, name='list_participants'),
    path('course/<uuid:course_id>/participant/<str:participant_id>/edit/', views.edit_participant, name='edit_participant'),
    path('course/<uuid:course_id>/participant/<str:participant_id>/delete/', views.delete_participant, name='delete_participant'),
]
