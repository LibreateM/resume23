from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import json, io, re
from .models import Resume
from .pdf_utils import generate_resume_pdf
from .ai_utils import generate_ai_resume


def home(request):
    return render(request, 'home.html')

def about(request):
        features = [
        "AI-powered content generation",
        "ATS compatibility analysis and scoring", 
        "4 professional PDF templates",
        "User dashboard to manage all resumes",
        "Secure account with full history",
    ]
    return render(request, 'about.html',{'features': features})

def contact(request):
    if request.method == 'POST':
        messages.success(request, "Thanks for contacting us! We'll get back to you soon.")
        return redirect('contact')
    return render(request, 'contact.html')

def templates_page(request):
    return render(request, 'templates_page.html')


@login_required
def builder(request):
    if request.method == 'POST':
        data = request.POST
        edu_list, exp_list, skill_list, proj_list, cert_list = [], [], [], [], []

        # Parse education
        schools = data.getlist('edu_school[]')
        degrees = data.getlist('edu_degree[]')
        years = data.getlist('edu_year[]')
        gpas = data.getlist('edu_gpa[]')
        for i in range(len(schools)):
            if schools[i].strip():
                edu_list.append({'school': schools[i], 'degree': degrees[i] if i < len(degrees) else '', 'year': years[i] if i < len(years) else '', 'gpa': gpas[i] if i < len(gpas) else ''})

        # Parse experience
        companies = data.getlist('exp_company[]')
        roles = data.getlist('exp_role[]')
        dates = data.getlist('exp_dates[]')
        descs = data.getlist('exp_desc[]')
        for i in range(len(companies)):
            if companies[i].strip():
                exp_list.append({'company': companies[i], 'role': roles[i] if i < len(roles) else '', 'dates': dates[i] if i < len(dates) else '', 'description': descs[i] if i < len(descs) else ''})

        # Parse skills
        skills_raw = data.get('skills', '')
        skill_list = [s.strip() for s in skills_raw.split(',') if s.strip()]

        # Parse projects
        pnames = data.getlist('proj_name[]')
        purls = data.getlist('proj_url[]')
        pdescs = data.getlist('proj_desc[]')
        for i in range(len(pnames)):
            if pnames[i].strip():
                proj_list.append({'name': pnames[i], 'url': purls[i] if i < len(purls) else '', 'description': pdescs[i] if i < len(pdescs) else ''})

        # Parse certifications
        cnames = data.getlist('cert_name[]')
        cissuers = data.getlist('cert_issuer[]')
        cdates = data.getlist('cert_date[]')
        for i in range(len(cnames)):
            if cnames[i].strip():
                cert_list.append({'name': cnames[i], 'issuer': cissuers[i] if i < len(cissuers) else '', 'date': cdates[i] if i < len(cdates) else ''})

        resume = Resume.objects.create(
            user=request.user,
            title=data.get('resume_title', 'My Resume'),
            template=data.get('template', 'classic'),
            full_name=data.get('full_name', ''),
            job_title=data.get('job_title', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            location=data.get('location', ''),
            linkedin=data.get('linkedin', ''),
            website=data.get('website', ''),
            summary=data.get('summary', ''),
            education_data=json.dumps(edu_list),
            experience_data=json.dumps(exp_list),
            skills_data=json.dumps(skill_list),
            projects_data=json.dumps(proj_list),
            certifications_data=json.dumps(cert_list),
        )
        messages.success(request, "Resume saved successfully!")
        return redirect('resume_detail', pk=resume.pk)
    return render(request, 'resumes/builder.html')


@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, 'resumes/detail.html', {'resume': resume})


@login_required
def resume_edit(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        data = request.POST
        edu_list, exp_list, skill_list, proj_list, cert_list = [], [], [], [], []

        schools = data.getlist('edu_school[]')
        degrees = data.getlist('edu_degree[]')
        years = data.getlist('edu_year[]')
        gpas = data.getlist('edu_gpa[]')
        for i in range(len(schools)):
            if schools[i].strip():
                edu_list.append({'school': schools[i], 'degree': degrees[i] if i < len(degrees) else '', 'year': years[i] if i < len(years) else '', 'gpa': gpas[i] if i < len(gpas) else ''})

        companies = data.getlist('exp_company[]')
        roles = data.getlist('exp_role[]')
        dates = data.getlist('exp_dates[]')
        descs = data.getlist('exp_desc[]')
        for i in range(len(companies)):
            if companies[i].strip():
                exp_list.append({'company': companies[i], 'role': roles[i] if i < len(roles) else '', 'dates': dates[i] if i < len(dates) else '', 'description': descs[i] if i < len(descs) else ''})

        skills_raw = data.get('skills', '')
        skill_list = [s.strip() for s in skills_raw.split(',') if s.strip()]

        pnames = data.getlist('proj_name[]')
        purls = data.getlist('proj_url[]')
        pdescs = data.getlist('proj_desc[]')
        for i in range(len(pnames)):
            if pnames[i].strip():
                proj_list.append({'name': pnames[i], 'url': purls[i] if i < len(purls) else '', 'description': pdescs[i] if i < len(pdescs) else ''})

        cnames = data.getlist('cert_name[]')
        cissuers = data.getlist('cert_issuer[]')
        cdates = data.getlist('cert_date[]')
        for i in range(len(cnames)):
            if cnames[i].strip():
                cert_list.append({'name': cnames[i], 'issuer': cissuers[i] if i < len(cissuers) else '', 'date': cdates[i] if i < len(cdates) else ''})

        resume.title = data.get('resume_title', resume.title)
        resume.template = data.get('template', resume.template)
        resume.full_name = data.get('full_name', '')
        resume.job_title = data.get('job_title', '')
        resume.email = data.get('email', '')
        resume.phone = data.get('phone', '')
        resume.location = data.get('location', '')
        resume.linkedin = data.get('linkedin', '')
        resume.website = data.get('website', '')
        resume.summary = data.get('summary', '')
        resume.education_data = json.dumps(edu_list)
        resume.experience_data = json.dumps(exp_list)
        resume.skills_data = json.dumps(skill_list)
        resume.projects_data = json.dumps(proj_list)
        resume.certifications_data = json.dumps(cert_list)
        resume.save()
        messages.success(request, "Resume updated successfully!")
        return redirect('resume_detail', pk=resume.pk)
    return render(request, 'resumes/builder.html', {'resume': resume, 'editing': True})


@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, "Resume deleted.")
        return redirect('dashboard')
    return render(request, 'resumes/confirm_delete.html', {'resume': resume})


@login_required
def download_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    buffer = generate_resume_pdf(resume)
    filename = f"{resume.full_name or 'resume'}_CV.pdf".replace(' ', '_')
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def ai_builder(request):
    if request.method == 'POST':
        job_role = request.POST.get('job_role', '').strip()
        skills = request.POST.get('skills', '').strip()
        experience_years = request.POST.get('experience_years', '').strip()
        education = request.POST.get('education', '').strip()
        extra_info = request.POST.get('extra_info', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not job_role or not skills:
            messages.error(request, "Job role and skills are required.")
            return render(request, 'resumes/ai_builder.html')

        try:
            resume_data = generate_ai_resume(job_role, skills, experience_years, education, extra_info)
            resume = Resume.objects.create(
                user=request.user,
                title=f"AI: {job_role}",
                template='modern',
                full_name=full_name,
                job_title=job_role,
                email=email,
                phone=phone,
                summary=resume_data.get('summary', ''),
                experience_data=json.dumps(resume_data.get('experience', [])),
                skills_data=json.dumps(resume_data.get('skills', [])),
                education_data=json.dumps(resume_data.get('education', [])),
                projects_data=json.dumps(resume_data.get('projects', [])),
                certifications_data=json.dumps(resume_data.get('certifications', [])),
                is_ai_generated=True,
            )
            messages.success(request, "AI Resume generated successfully!")
            return redirect('resume_detail', pk=resume.pk)
        except Exception as e:
            messages.error(request, f"AI generation failed: {str(e)}")
    items = [
        "Professional Summary",
        "Role-specific Work Experience",
        "ATS-optimized Skills List",
        "Relevant Projects",
        "Certifications Suggestions"
    ]
    return render(request, 'resumes/ai_builder.html',{'items': items})
