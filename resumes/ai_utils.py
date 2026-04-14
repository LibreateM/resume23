from openai import OpenAI
import json
import re
from django.conf import settings


def generate_ai_resume(job_role, skills, experience_years, education, extra_info):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = f"""
You are a professional resume writer. Create a complete, ATS-optimized resume in JSON format.

Job Role: {job_role}
Skills: {skills}
Years of Experience: {experience_years or 'Not specified'}
Education: {education or 'Not specified'}
Additional Info: {extra_info or 'None'}

Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks, just raw JSON):
{{
  "summary": "Professional summary paragraph (2-3 sentences, ATS optimized)",
  "experience": [
    {{
      "company": "Company Name",
      "role": "Job Title",
      "dates": "Start – End",
      "description": "• Achievement 1\\n• Achievement 2\\n• Achievement 3"
    }}
  ],
  "education": [
    {{
      "school": "University Name",
      "degree": "Degree Name",
      "year": "Year range",
      "gpa": ""
    }}
  ],
  "skills": ["skill1", "skill2", "skill3"],
  "projects": [
    {{
      "name": "Project Name",
      "url": "",
      "description": "Brief project description with technologies used"
    }}
  ],
  "certifications": [
    {{
      "name": "Certification Name",
      "issuer": "Issuing Organization",
      "date": "Year"
    }}
  ]
}}

Make it realistic, professional, and tailored for {job_role}. Include 2-3 experience entries, 2-3 projects, relevant certifications.
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
