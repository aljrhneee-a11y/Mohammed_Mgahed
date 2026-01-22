from django.contrib import admin
from .models import Course, Participant, UserProfile, UserPermission

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'participant_count')
    list_filter = ('created_at',)
    search_fields = ('name',)
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = 'عدد المشاركين'

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'course', 'governorate', 'contact_number', 'entered_by', 'created_at')
    list_filter = ('course', 'governorate', 'created_at')
    search_fields = ('full_name', 'jihad_name', 'contact_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission_name', 'is_granted', 'granted_by', 'granted_at')
    list_filter = ('is_granted', 'permission_name')
    search_fields = ('user__username', 'permission_name')
