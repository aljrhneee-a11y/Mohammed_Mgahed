from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Course, Participant, UserProfile
from django.contrib.auth.models import User
import json

def index_view(request):
    courses = []
    if request.user.is_authenticated:
        # التأكد من وجود ملف شخصي
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if profile.role == 'admin' or request.user.is_superuser:
            return redirect('dept:admin_dashboard')
            
        # للمستخدم العادي، نعرض فقط الدورات التي أنشأها
        courses = Course.objects.filter(created_by=request.user)
    return render(request, 'dept/index.html', {'courses': courses})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dept:index')
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, f"مرحباً بك يا {user.username}")
            return redirect('dept:index')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة")
    return render(request, 'dept/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dept:index')
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        p_confirm = request.POST.get('password_confirm')
        
        if p != p_confirm:
            messages.error(request, "كلمات المرور غير متطابقة")
        elif User.objects.filter(username=u).exists():
            messages.error(request, "اسم المستخدم موجود مسبقاً")
        else:
            user = User.objects.create_user(username=u, password=p)
            UserProfile.objects.create(user=user, role='user')
            login(request, user)
            messages.success(request, "تم إنشاء الحساب وتسجيل الدخول بنجاح")
            return redirect('dept:index')
    return render(request, 'dept/register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "تم تسجيل الخروج بنجاح")
    return redirect('dept:login')

@login_required
def admin_dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if profile.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "ليس لديك صلاحية الوصول لهذه الصفحة")
        return redirect('dept:index')
    
    courses = Course.objects.all()
    users = User.objects.all()
    return render(request, 'dept/admin.html', {
        'courses': courses,
        'users': users
    })

@login_required
def create_course(request):
    if request.method == 'POST':
        name = request.POST.get('course_name')
        if name:
            Course.objects.create(name=name, created_by=request.user)
            messages.success(request, f"تم إنشاء الدورة '{name}' بنجاح")
        else:
            messages.error(request, "يجب إدخال اسم الدورة")
    return redirect('dept:index')

@login_required
def delete_course(request, course_id):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        messages.error(request, "المسؤولون فقط يمكنهم حذف الدورات")
        return redirect('dept:index')
    
    course = get_object_or_404(Course, id=course_id)
    name = course.name
    course.delete()
    messages.success(request, f"تم حذف الدورة '{name}' وجميع المشاركين فيها")
    return redirect('dept:index')

@login_required
def add_participant(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        try:
            Participant.objects.create(
                university_id=request.POST.get('university_id'),
                course=course,
                full_name=request.POST.get('full_name'),
                jihad_name=request.POST.get('jihad_name'),
                birth_year=request.POST.get('birth_year'),
                governorate=request.POST.get('governorate'),
                directorate=request.POST.get('directorate'),
                isolation=request.POST.get('isolation'),
                village=request.POST.get('village'),
                specialization=request.POST.get('specialization'),
                affiliation=request.POST.get('affiliation'),
                contact_number=request.POST.get('contact_number'),
                entered_by=request.user
            )
            messages.success(request, "تم إضافة المشارك بنجاح")
            return redirect('dept:list_participants', course_id=course.id)
        except Exception as e:
            messages.error(request, f"خطأ في الإضافة: {str(e)}")
            
    return render(request, 'dept/add_particiipant.html', {'course': course})

@login_required
def list_participants(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    participants = course.participants.all()
    return render(request, 'dept/list_participants.html', {'course': course, 'participants': participants})

@login_required
def edit_participant(request, course_id, participant_id):
    course = get_object_or_404(Course, id=course_id)
    participant = get_object_or_404(Participant, university_id=participant_id)
    
    if request.method == 'POST':
        participant.full_name = request.POST.get('full_name')
        participant.jihad_name = request.POST.get('jihad_name')
        participant.birth_year = request.POST.get('birth_year')
        participant.governorate = request.POST.get('governorate')
        participant.directorate = request.POST.get('directorate')
        participant.isolation = request.POST.get('isolation')
        participant.village = request.POST.get('village')
        participant.specialization = request.POST.get('specialization')
        participant.affiliation = request.POST.get('affiliation')
        participant.contact_number = request.POST.get('contact_number')
        participant.save()
        messages.success(request, "تم تحديث بيانات المشارك بنجاح")
        return redirect('dept:list_participants', course_id=course.id)
        
    return render(request, 'dept/edit_participant.html', {'course': course, 'participant': participant})

@login_required
def delete_participant(request, course_id, participant_id):
    participant = get_object_or_404(Participant, university_id=participant_id)
    participant.delete()
    messages.success(request, "تم حذف المشارك بنجاح")
    return redirect('dept:list_participants', course_id=course_id)

@login_required
def add_user_api(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return JsonResponse({'success': False, 'error': 'غير مصرح لك'})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            role = data.get('role', 'user')
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'اسم المستخدم موجود مسبقاً'})
            
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, role=role)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'طلب غير صالح'})

# دوال إضافية (يمكن إكمالها لاحقاً)
@login_required
def manage_data(request):
    return render(request, 'dept/manage_data.html')

from django.http import HttpResponse
from io import BytesIO

@login_required
def export_csv(request):
    try:
        import pandas as pd
    except ImportError:
        messages.error(request, "عذراً، ميزة تصدير Excel تتطلب تثبيت مكتبة pandas. يرجى تشغيل الأمر: pip install pandas openpyxl")
        return redirect(request.META.get('HTTP_REFERER', 'dept:index'))

    course_id = request.GET.get('course_id')
    if course_id:
        course = get_object_or_404(Course, id=course_id)
        participants = Participant.objects.filter(course=course)
        filename = f"participants_{course.name}.xlsx"
    else:
        participants = Participant.objects.all()
        filename = "all_participants.xlsx"

    data = []
    for p in participants:
        data.append({
            'رقم العسكري': p.university_id,
            'الاسم الخماسي': p.full_name,
            'الاسم الجهادي': p.jihad_name,
            'سنة الميلاد': p.birth_year,
            'المحافظة': p.governorate,
            'المديرية': p.directorate,
            'العزلة': p.isolation,
            'القرية': p.village,
            'التخصص': p.specialization,
            'التبعية': p.affiliation,
            'رقم التواصل': p.contact_number,
            'الدورة': p.course.name,
            'تاريخ الإدخال': p.created_at.strftime('%Y-%m-%d')
        })

    df = pd.DataFrame(data)
    
    output = BytesIO()
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='المشاركين')
    except ImportError:
        messages.error(request, "عذراً، ميزة تصدير Excel تتطلب تثبيت مكتبة openpyxl. يرجى تشغيل الأمر: pip install openpyxl")
        return redirect(request.META.get('HTTP_REFERER', 'dept:index'))
    
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def edit_course_name(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        new_name = request.POST.get('course_name')
        if new_name:
            course.name = new_name
            course.save()
            messages.success(request, "تم تعديل اسم الدورة")
    return redirect('dept:index')

@login_required
def toggle_user_role(request, user_id):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        messages.error(request, "غير مصرح لك بالقيام بهذا الإجراء")
        return redirect('dept:admin_dashboard')
    
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "لا يمكنك تغيير رتبة حسابك الخاص")
        return redirect('dept:admin_dashboard')
        
    profile, created = UserProfile.objects.get_or_create(user=target_user)
    old_role = profile.role
    new_role = 'admin' if old_role == 'user' else 'user'
    profile.role = new_role
    profile.save()
    
    messages.success(request, f"تم تغيير رتبة {target_user.username} إلى {profile.get_role_display()}")
    return redirect('dept:admin_dashboard')
