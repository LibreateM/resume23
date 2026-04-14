from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ATSCheck
from resumes.models import Resume
from openai import OpenAI
from django.conf import settings
import json, re

try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False


def extract_text_from_pdf(pdf_file):
    if not PDF_SUPPORT:
        return ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception:
        return ""


def analyze_with_gemini(resume_text, job_description):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = f"""
You are an expert ATS (Applicant Tracking System) analyzer. Analyze the following resume.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000] if job_description else "General professional position"}

Return ONLY a valid JSON object (no markdown, no code blocks):
{{
  "score": <integer 0-100>,
  "feedback": "<2-3 sentence overall feedback>",
  "keywords_found": ["keyword1", "keyword2"],
  "keywords_missing": ["missing1", "missing2"],
  "suggestions": [
    "Specific actionable suggestion 1",
    "Specific actionable suggestion 2",
    "Specific actionable suggestion 3",
    "Specific actionable suggestion 4",
    "Specific actionable suggestion 5"
  ],
  "sections_analysis": {{
    "contact_info": <0-100>,
    "summary": <0-100>,
    "experience": <0-100>,
    "skills": <0-100>,
    "education": <0-100>,
    "formatting": <0-100>
  }}
}}

Score based on: keyword matching, completeness, action verbs, quantified achievements, ATS compatibility, formatting.
"""

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
    )
    text = response.choices[0].message.content.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    data = json.loads(text.strip())
    return data


@login_required
def ats_checker(request):
    user_resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    result = None
    ats_check = None

    if request.method == 'POST':
        resume_text = request.POST.get('resume_text', '').strip()
        job_description = request.POST.get('job_description', '').strip()
        resume_id = request.POST.get('resume_id', '')

        # Handle PDF upload
        if 'resume_pdf' in request.FILES and not resume_text:
            pdf_file = request.FILES['resume_pdf']
            resume_text = extract_text_from_pdf(pdf_file)
            if not resume_text:
                messages.error(request, "Could not extract text from PDF. Please paste text manually.")
                return render(request, 'ats_checker/checker.html', {'user_resumes': user_resumes})

        # Load from saved resume
        linked_resume = None
        if resume_id:
            try:
                linked_resume = Resume.objects.get(pk=resume_id, user=request.user)
                if not resume_text:
                    parts = []
                    if linked_resume.full_name: parts.append(linked_resume.full_name)
                    if linked_resume.job_title: parts.append(linked_resume.job_title)
                    if linked_resume.summary: parts.append(linked_resume.summary)
                    for exp in linked_resume.get_experience():
                        parts.append(f"{exp.get('role','')} at {exp.get('company','')}: {exp.get('description','')}")
                    for edu in linked_resume.get_education():
                        parts.append(f"{edu.get('degree','')} from {edu.get('school','')}")
                    parts.append("Skills: " + ", ".join(linked_resume.get_skills()))
                    resume_text = "\n".join(parts)
            except Resume.DoesNotExist:
                pass

        if not resume_text:
            messages.error(request, "Please provide resume text, upload a PDF, or select a saved resume.")
            return render(request, 'ats_checker/checker.html', {'user_resumes': user_resumes})

        try:
            data = analyze_with_gemini(resume_text, job_description)
            ats_check = ATSCheck.objects.create(
                user=request.user,
                resume=linked_resume,
                resume_text=resume_text[:5000],
                job_description=job_description,
                score=data.get('score', 0),
                feedback=data.get('feedback', ''),
                keywords_found=json.dumps(data.get('keywords_found', [])),
                keywords_missing=json.dumps(data.get('keywords_missing', [])),
                suggestions=json.dumps(data.get('suggestions', [])),
            )
            result = data
            result['check_id'] = ats_check.pk
            messages.success(request, f"ATS Analysis complete! Your score: {data.get('score', 0)}/100")
        except Exception as e:
            messages.error(request, f"Analysis failed: {str(e)}")

    history = ATSCheck.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'ats_checker/checker.html', {
        'user_resumes': user_resumes,
        'result': result,
        'ats_check': ats_check,
        'history': history,
    })


@login_required
def ats_history(request):
    checks = ATSCheck.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ats_checker/history.html', {'checks': checks})


@login_required
def ats_detail(request, pk):
    check = get_object_or_404(ATSCheck, pk=pk, user=request.user)
    return render(request, 'ats_checker/detail.html', {'check': check})
