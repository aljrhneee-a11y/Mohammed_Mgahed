from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name="اسم الدورة")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الإنشاء")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="أنشئ بواسطة")
    
    class Meta:
        verbose_name = "دورة"
        verbose_name_plural = "الدورات"
    
    def __str__(self):
        return self.name

class Participant(models.Model):
    # تم تعديل الـ ID ليكون رقم القيد الجامعي (Primary Key)
    # تنسيق رقم القيد الجامعي عادة ما يكون أرقام، سنستخدم CharField لمرونة التنسيق
    university_id = models.CharField(primary_key=True, max_length=20, verbose_name="رقم العسكري ")
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='participants', verbose_name="الدورة")
    
    full_name = models.CharField(max_length=200, verbose_name="الاسم الخماسي")
    jihad_name = models.CharField(max_length=100, verbose_name="الاسم الجهادي")
    birth_year = models.IntegerField(verbose_name="سنة الميلاد")
    governorate = models.CharField(max_length=100, verbose_name="المحافظة")
    directorate = models.CharField(max_length=100, verbose_name="المديرية")
    isolation = models.CharField(max_length=100, verbose_name="العزلة")
    village = models.CharField(max_length=100, verbose_name="القرية")
    specialization = models.CharField(max_length=200, verbose_name="التخصص")
    affiliation = models.CharField(max_length=200, verbose_name="التبعية")
    contact_number = models.CharField(max_length=20, verbose_name="رقم التواصل")
    
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="أدخل بواسطة")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الإدخال")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")
    
    class Meta:
        verbose_name = "مشارك"
        verbose_name_plural = "المشاركون"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.university_id})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=[
        ('user', 'مستخدم عادي'),
        ('admin', 'مسؤول')
    ], default='user', verbose_name="الصلاحية")
    
    class Meta:
        verbose_name = "ملف المستخدم"
        verbose_name_plural = "ملفات المستخدمين"
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions', verbose_name="المستخدم")
    permission_name = models.CharField(max_length=100, verbose_name="اسم الصلاحية")
    is_granted = models.BooleanField(default=False, verbose_name="ممنوحة")
    granted_at = models.DateTimeField(default=timezone.now, verbose_name="تاريخ المنح")
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='granted_permissions', verbose_name="منحت بواسطة")

    class Meta:
        verbose_name = "صلاحية مستخدم"
        verbose_name_plural = "صلاحيات المستخدمين"
        unique_together = ('user', 'permission_name')

    def __str__(self):
        return f"{self.user.username} - {self.permission_name} ({'ممنوحة' if self.is_granted else 'غير ممنوحة'})"
