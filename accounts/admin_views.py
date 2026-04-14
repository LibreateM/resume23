from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Avg
from resumes.models import Resume
from ats_checker.models import ATSCheck


def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin, login_url='/dashboard/')
def admin_dashboard(request):
    total_users = User.objects.count()
    total_resumes = Resume.objects.count()
    total_ats = ATSCheck.objects.count()
    avg_score = ATSCheck.objects.aggregate(Avg('score'))['score__avg'] or 0
    
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_resumes = Resume.objects.select_related('user').order_by('-created_at')[:5]
    
    # Users with most resumes
    top_users = User.objects.annotate(resume_count=Count('resumes')).order_by('-resume_count')[:5]
    
    context = {
        'total_users': total_users,
        'total_resumes': total_resumes,
        'total_ats': total_ats,
        'avg_score': round(avg_score, 1),
        'recent_users': recent_users,
        'recent_resumes': recent_resumes,
        'top_users': top_users,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(is_admin, login_url='/dashboard/')
def admin_users(request):
    users = User.objects.annotate(
        resume_count=Count('resumes'),
        ats_count=Count('ats_checks')
    ).order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})


@login_required
@user_passes_test(is_admin, login_url='/dashboard/')
def toggle_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, "You cannot deactivate yourself.")
    else:
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User {user.username} has been {status}.")
    return redirect('admin_users')


@login_required
@user_passes_test(is_admin, login_url='/dashboard/')
def admin_resumes(request):
    resumes = Resume.objects.select_related('user').order_by('-created_at')
    return render(request, 'admin_panel/resumes.html', {'resumes': resumes})


@login_required
@user_passes_test(is_admin, login_url='/dashboard/')
def delete_resume_admin(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    resume.delete()
    messages.success(request, "Resume deleted.")
    return redirect('admin_resumes')


@login_required
@user_passes_test(is_admin, login_url='/dashboard/')
def admin_ats(request):
    checks = ATSCheck.objects.select_related('user', 'resume').order_by('-created_at')
    return render(request, 'admin_panel/ats.html', {'checks': checks})
