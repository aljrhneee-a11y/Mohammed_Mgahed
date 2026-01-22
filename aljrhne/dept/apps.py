from django.apps import AppConfig


class DeptConfig(AppConfig):
    name = 'dept'

from django.apps import AppConfig

class DeptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dept'
    verbose_name = 'إدارة الدورات'  # اسم عربي للتطبيق