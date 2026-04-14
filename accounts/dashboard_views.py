from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from resumes.models import Resume
from ats_checker.models import ATSCheck
from django.db.models import Avg


@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    ats_checks = ATSCheck.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    avg_score = ats_checks.aggregate(Avg('score'))['score__avg']
    avg_score = round(avg_score, 1) if avg_score else 0
    
    # Latest ATS score per resume
    resume_with_scores = []
    for r in resumes[:6]:
        latest_ats = ATSCheck.objects.filter(user=request.user, resume=r).order_by('-created_at').first()
        resume_with_scores.append({
            'resume': r,
            'ats': latest_ats,
        })
    
    context = {
        'resumes': resumes,
        'resume_with_scores': resume_with_scores,
        'ats_checks': ats_checks,
        'total_resumes': resumes.count(),
        'avg_ats_score': avg_score,
        'total_ats_checks': ATSCheck.objects.filter(user=request.user).count(),
    }
    return render(request, 'dashboard/dashboard.html', context)
