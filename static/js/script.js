/* ============================================================
   ResumeForge – script.js
   Shared JS for all pages
   ============================================================ */

// ── Scroll-based fade-in observer ──
document.addEventListener('DOMContentLoaded', () => {

  // Fade-up animation via IntersectionObserver
  const fadeEls = document.querySelectorAll('.fade-up');
  if (fadeEls.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    fadeEls.forEach(el => observer.observe(el));
  }

  // Mark active nav link
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.rf-navbar .nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // Navbar scroll shadow
  const navbar = document.querySelector('.rf-navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.style.boxShadow = window.scrollY > 20
        ? '0 4px 30px rgba(0,0,0,0.5)'
        : 'none';
    });
  }
});

// ── Toast Notification ──
function showToast(msg, type = 'success') {
  let toast = document.querySelector('.rf-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'rf-toast';
    document.body.appendChild(toast);
  }
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  toast.innerHTML = `<strong>${icons[type] || '✓'} ${msg}</strong>`;
  toast.style.borderColor = type === 'error' ? '#ff6b6b' : 'var(--saffron)';
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
}

// ── Email validator ──
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ── Password toggle ──
function setupPasswordToggle(inputId, toggleId) {
  const input = document.getElementById(inputId);
  const btn = document.getElementById(toggleId);
  if (!input || !btn) return;
  btn.addEventListener('click', () => {
    const isText = input.type === 'text';
    input.type = isText ? 'password' : 'text';
    btn.innerHTML = isText
      ? '<i class="fa-solid fa-eye"></i>'
      : '<i class="fa-solid fa-eye-slash"></i>';
  });
}

// ── LocalStorage helpers ──
const Store = {
  set: (key, val) => { try { localStorage.setItem(key, JSON.stringify(val)); } catch(e) {} },
  get: (key) => { try { return JSON.parse(localStorage.getItem(key)); } catch(e) { return null; } },
  remove: (key) => { try { localStorage.removeItem(key); } catch(e) {} }
};

/* ============================================================
   CONTACT FORM
   ============================================================ */
(function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let valid = true;

    const name = form.querySelector('#contactName');
    const email = form.querySelector('#contactEmail');
    const message = form.querySelector('#contactMessage');

    [name, email, message].forEach(el => {
      el.classList.remove('is-invalid');
      const errEl = el.nextElementSibling;
      if (errEl && errEl.classList.contains('form-error')) errEl.remove();
    });

    if (!name.value.trim()) {
      showError(name, 'Please enter your name'); valid = false;
    }
    if (!isValidEmail(email.value)) {
      showError(email, 'Please enter a valid email'); valid = false;
    }
    if (message.value.trim().length < 20) {
      showError(message, 'Message must be at least 20 characters'); valid = false;
    }

    if (valid) {
      showToast("Message sent! We'll get back to you soon.");
      form.reset();
    }
  });
})();

function showError(el, msg) {
  el.classList.add('is-invalid');
  const err = document.createElement('span');
  err.className = 'form-error';
  err.textContent = msg;
  el.insertAdjacentElement('afterend', err);
}

/* ============================================================
   SIGN UP FORM
   ============================================================ */
(function initSignupForm() {
  const form = document.getElementById('signupForm');
  if (!form) return;

  setupPasswordToggle('signupPassword', 'toggleSignupPwd');
  setupPasswordToggle('signupConfirm', 'toggleConfirmPwd');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name  = form.querySelector('#signupName').value.trim();
    const email = form.querySelector('#signupEmail').value.trim();
    const pwd   = form.querySelector('#signupPassword').value;
    const conf  = form.querySelector('#signupConfirm').value;

    if (!name)               { showToast('Name is required', 'error'); return; }
    if (!isValidEmail(email)){ showToast('Invalid email address', 'error'); return; }
    if (pwd.length < 8)      { showToast('Password must be 8+ characters', 'error'); return; }
    if (pwd !== conf)         { showToast('Passwords do not match', 'error'); return; }

    Store.set('rf_user', { name, email });
    showToast('Account created! Redirecting…');
    setTimeout(() => window.location.href = 'signin.html', 1800);
  });
})();

/* ============================================================
   SIGN IN FORM
   ============================================================ */
(function initSigninForm() {
  const form = document.getElementById('signinForm');
  if (!form) return;

  setupPasswordToggle('signinPassword', 'toggleSigninPwd');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = form.querySelector('#signinEmail').value.trim();
    const pwd   = form.querySelector('#signinPassword').value;

    if (!isValidEmail(email)) { showToast('Invalid email address', 'error'); return; }
    if (!pwd)                  { showToast('Password is required', 'error'); return; }

    // Simulate login
    showToast('Signed in successfully!');
    setTimeout(() => window.location.href = 'builder.html', 1800);
  });
})();

/* ============================================================
   RESUME BUILDER
   ============================================================ */
(function initBuilder() {
  const builderForm = document.getElementById('resumeBuilderForm');
  if (!builderForm) return;

  // Progress bar steps
  const steps = ['personal', 'education', 'experience', 'skills'];
  let currentStep = 0;

  function updateProgress() {
    const pct = ((currentStep + 1) / steps.length) * 100;
    document.getElementById('builderProgress').style.width = pct + '%';
    document.getElementById('progressLabel').textContent = `Step ${currentStep + 1} of ${steps.length}`;

    steps.forEach((s, i) => {
      const el = document.getElementById('section-' + s);
      if (el) el.style.display = i === currentStep ? 'block' : 'none';
    });

    document.getElementById('btnPrev').disabled = currentStep === 0;
    document.getElementById('btnNext').style.display = currentStep < steps.length - 1 ? 'inline-block' : 'none';
    document.getElementById('btnGenerate').style.display = currentStep === steps.length - 1 ? 'inline-block' : 'none';
  }

  document.getElementById('btnNext')?.addEventListener('click', () => {
    if (currentStep < steps.length - 1) { currentStep++; updateProgress(); }
  });

  document.getElementById('btnPrev')?.addEventListener('click', () => {
    if (currentStep > 0) { currentStep--; updateProgress(); }
  });

  updateProgress();

  // Dynamic Education Entries
  document.getElementById('addEducation')?.addEventListener('click', () => {
    addEntry('educationList', educationEntryHTML());
    attachRemove();
    updatePreview();
  });

  // Dynamic Experience Entries
  document.getElementById('addExperience')?.addEventListener('click', () => {
    addEntry('experienceList', experienceEntryHTML());
    attachRemove();
    updatePreview();
  });

  // Live preview update on any input change
  builderForm.addEventListener('input', updatePreview);
  builderForm.addEventListener('change', updatePreview);

  // Generate / Save
  document.getElementById('btnGenerate')?.addEventListener('click', () => {
    saveResumeData();
    showToast('Resume saved! Download ready.');
  });

  // Initial preview render
  updatePreview();

  // Attach remove buttons
  attachRemove();
})();

function addEntry(containerId, html) {
  const list = document.getElementById(containerId);
  if (!list) return;
  const div = document.createElement('div');
  div.classList.add('entry-block');
  div.innerHTML = html;
  list.appendChild(div);
}

function attachRemove() {
  document.querySelectorAll('.btn-remove-entry').forEach(btn => {
    btn.onclick = () => {
      btn.closest('.entry-block')?.remove();
      updatePreview();
    };
  });
}

function educationEntryHTML() {
  return `
    <div class="row g-2 mb-3 mt-1 p-3" style="background:rgba(255,255,255,0.03);border-radius:10px;border:1px solid rgba(255,255,255,0.07)">
      <div class="col-md-6">
        <label class="rf-form-label">School / University</label>
        <input type="text" class="rf-form-control edu-school" placeholder="MIT" />
      </div>
      <div class="col-md-6">
        <label class="rf-form-label">Degree</label>
        <input type="text" class="rf-form-control edu-degree" placeholder="B.Sc. Computer Science" />
      </div>
      <div class="col-md-6">
        <label class="rf-form-label">Year</label>
        <input type="text" class="rf-form-control edu-year" placeholder="2020 – 2024" />
      </div>
      <div class="col-md-6 d-flex align-items-end">
        <button type="button" class="btn-remove-entry"><i class="fa-solid fa-trash-can me-1"></i>Remove</button>
      </div>
    </div>`;
}

function experienceEntryHTML() {
  return `
    <div class="row g-2 mb-3 mt-1 p-3" style="background:rgba(255,255,255,0.03);border-radius:10px;border:1px solid rgba(255,255,255,0.07)">
      <div class="col-md-6">
        <label class="rf-form-label">Company</label>
        <input type="text" class="rf-form-control exp-company" placeholder="Acme Corp" />
      </div>
      <div class="col-md-6">
        <label class="rf-form-label">Role</label>
        <input type="text" class="rf-form-control exp-role" placeholder="Software Engineer" />
      </div>
      <div class="col-md-6">
        <label class="rf-form-label">Duration</label>
        <input type="text" class="rf-form-control exp-duration" placeholder="Jan 2022 – Present" />
      </div>
      <div class="col-md-6">
        <label class="rf-form-label">Description</label>
        <input type="text" class="rf-form-control exp-desc" placeholder="Brief description of role" />
      </div>
      <div class="col-12 d-flex justify-content-end">
        <button type="button" class="btn-remove-entry"><i class="fa-solid fa-trash-can me-1"></i>Remove</button>
      </div>
    </div>`;
}

function updatePreview() {
  const get = (id) => (document.getElementById(id)?.value || '').trim();

  // Personal
  const name  = get('rFullName') || 'Your Name';
  const title = get('rJobTitle') || 'Your Title';
  const email = get('rEmail') || '';
  const phone = get('rPhone') || '';
  const loc   = get('rLocation') || '';
  const summary = get('rSummary') || '';

  const pv = document.getElementById('previewPane');
  if (!pv) return;

  // Education
  let eduHTML = '';
  document.querySelectorAll('.entry-block').forEach(block => {
    const school = block.querySelector('.edu-school')?.value || '';
    const degree = block.querySelector('.edu-degree')?.value || '';
    const year   = block.querySelector('.edu-year')?.value || '';
    if (school || degree) {
      eduHTML += `<p><strong>${degree}</strong>${school ? ' — ' + school : ''}${year ? ' <em>('+year+')</em>' : ''}</p>`;
    }
  });

  // Experience
  let expHTML = '';
  document.querySelectorAll('.entry-block').forEach(block => {
    const company  = block.querySelector('.exp-company')?.value || '';
    const role     = block.querySelector('.exp-role')?.value || '';
    const duration = block.querySelector('.exp-duration')?.value || '';
    const desc     = block.querySelector('.exp-desc')?.value || '';
    if (company || role) {
      expHTML += `<p><strong>${role}</strong>${company ? ' — ' + company : ''}<br><em>${duration}</em>${desc ? '<br>' + desc : ''}</p>`;
    }
  });

  // Skills
  const skillsRaw = get('rSkills');
  let skillsHTML = '';
  if (skillsRaw) {
    skillsHTML = skillsRaw.split(',').map(s => `<span class="skill-tag">${s.trim()}</span>`).join('');
  }

  pv.innerHTML = `
    <div style="border-bottom:2px solid #f5a623;padding-bottom:1rem;margin-bottom:1rem;">
      <h2 style="font-family:'DM Serif Display',serif;color:#0d1b2a;margin:0;">${name}</h2>
      <p style="color:#f5a623;font-weight:600;font-size:0.9rem;margin:0.2rem 0 0;">${title}</p>
      <p class="preview-contact">${[email, phone, loc].filter(Boolean).join(' · ')}</p>
    </div>
    ${summary ? `<div class="preview-section"><h3>Summary</h3><p>${summary}</p></div>` : ''}
    ${eduHTML  ? `<div class="preview-section"><h3>Education</h3>${eduHTML}</div>` : ''}
    ${expHTML  ? `<div class="preview-section"><h3>Experience</h3>${expHTML}</div>` : ''}
    ${skillsHTML ? `<div class="preview-section"><h3>Skills</h3><div>${skillsHTML}</div></div>` : ''}
  `;
}

function saveResumeData() {
  const get = (id) => document.getElementById(id)?.value || '';
  Store.set('rf_resume', {
    name:     get('rFullName'),
    title:    get('rJobTitle'),
    email:    get('rEmail'),
    phone:    get('rPhone'),
    location: get('rLocation'),
    summary:  get('rSummary'),
    skills:   get('rSkills'),
    savedAt:  new Date().toISOString()
  });
}

/* ============================================================
   ATS SCORE CHECKER
   ============================================================ */
(function initATS() {
  const btn = document.getElementById('checkATSBtn');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const text = document.getElementById('atsInput')?.value.trim();
    if (!text || text.length < 50) {
      showToast('Please paste at least 50 characters of resume content', 'error');
      return;
    }

    // Simulated scoring
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing…';
    btn.disabled = true;

    setTimeout(() => {
      btn.innerHTML = '<i class="fa-solid fa-magnifying-glass me-2"></i>Check ATS Score';
      btn.disabled = false;

      const score = simulateATSScore(text);
      displayATSResults(score, text);
    }, 1800);
  });
})();

function simulateATSScore(text) {
  const keywords = ['experience', 'skills', 'education', 'summary', 'objective',
    'achievements', 'projects', 'certifications', 'email', 'phone',
    'linkedin', 'github', 'javascript', 'python', 'java', 'react',
    'managed', 'developed', 'led', 'improved', 'increased'];

  const lower = text.toLowerCase();
  const wordCount = text.split(/\s+/).length;
  const found = keywords.filter(k => lower.includes(k)).length;
  const kwScore = Math.min(50, Math.round((found / keywords.length) * 50));
  const lenScore = wordCount > 200 ? 20 : Math.round((wordCount / 200) * 20);
  const formScore = text.includes('@') ? 15 : 5;
  const bulletScore = text.includes('•') || text.includes('-') ? 15 : 5;

  return Math.min(98, kwScore + lenScore + formScore + bulletScore);
}

function displayATSResults(score, text) {
  const wrap = document.getElementById('atsResults');
  if (!wrap) return;

  const color = score >= 75 ? '#48c78e' : score >= 50 ? '#f5a623' : '#ff6b6b';
  const label = score >= 75 ? 'Excellent' : score >= 50 ? 'Good' : 'Needs Work';

  const suggestions = generateSuggestions(text, score);

  wrap.style.display = 'block';
  wrap.innerHTML = `
    <div class="text-center mb-4">
      <div class="ats-score-circle" style="border-color:${color}">
        <div class="score-num" style="color:${color}">${score}</div>
        <div class="score-label">${label}</div>
      </div>
      <div class="rf-progress" style="max-width:300px;margin:0 auto;">
        <div class="rf-progress-bar" style="width:${score}%;background:linear-gradient(90deg,${color},${color}88)"></div>
      </div>
    </div>
    <h5 class="mb-3" style="font-family:'DM Serif Display',serif;">Suggestions</h5>
    ${suggestions.map(s => `
      <div class="suggestion-item">
        <div class="sug-icon ${s.type}"><i class="fa-solid ${s.icon}"></i></div>
        <div>
          <strong style="font-size:0.85rem;">${s.title}</strong>
          <p style="font-size:0.8rem;color:var(--muted);margin:0;">${s.desc}</p>
        </div>
      </div>`).join('')}
  `;
}

function generateSuggestions(text, score) {
  const sug = [];
  const lower = text.toLowerCase();

  if (!lower.includes('linkedin'))
    sug.push({ type:'yellow', icon:'fa-link', title:'Add LinkedIn Profile', desc:'ATS systems favor resumes with a LinkedIn URL.' });
  if (!lower.includes('@'))
    sug.push({ type:'red', icon:'fa-envelope', title:'Missing Email Address', desc:'Ensure your email address is present in contact info.' });
  if (text.split(/\s+/).length < 300)
    sug.push({ type:'yellow', icon:'fa-align-left', title:'Content Too Brief', desc:'Aim for 300–600 words for best ATS performance.' });
  if (!lower.includes('skill'))
    sug.push({ type:'red', icon:'fa-star', title:'No Skills Section Detected', desc:'Add a dedicated skills section with relevant keywords.' });
  if (lower.includes('responsible for'))
    sug.push({ type:'yellow', icon:'fa-pen', title:'Use Action Verbs', desc:'Replace "Responsible for" with verbs like Led, Built, Managed.' });
  if (score >= 75)
    sug.push({ type:'green', icon:'fa-check', title:'Strong ATS Compatibility', desc:'Your resume is well-optimized for most ATS systems.' });
  else
    sug.push({ type:'yellow', icon:'fa-file-lines', title:'Add More Keywords', desc:'Tailor your resume to match the target job description keywords.' });

  return sug;
}

/* ============================================================
   AI RESUME BUILDER
   ============================================================ */
(function initAIBuilder() {
  const btn = document.getElementById('generateAIBtn');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const role  = document.getElementById('aiJobRole')?.value.trim();
    const skills = document.getElementById('aiSkills')?.value.trim();
    const exp   = document.getElementById('aiExperience')?.value.trim();
    const tone  = document.getElementById('aiTone')?.value || 'professional';

    if (!role)   { showToast('Please enter a job role', 'error'); return; }
    if (!skills) { showToast('Please enter at least one skill', 'error'); return; }

    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating…';
    btn.disabled = true;

    const output = document.getElementById('aiOutput');
    if (output) { output.innerHTML = ''; output.classList.add('typing-cursor'); }

    setTimeout(() => {
      btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles me-2"></i>Generate Resume';
      btn.disabled = false;
      if (output) output.classList.remove('typing-cursor');

      const resume = generateAIResume(role, skills, exp, tone);
      if (output) typewriterEffect(output, resume, 12);
    }, 1600);
  });
})();

function generateAIResume(role, skills, experience, tone) {
  const skillList = skills.split(',').map(s => s.trim()).join(', ');
  const expNote = experience ? `${experience} of experience` : 'proven experience';
  const toneAdj = tone === 'creative' ? 'innovative and creative' : tone === 'executive' ? 'executive-level' : 'results-driven';

  return `
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  YOUR NAME
  ${role.toUpperCase()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 email@example.com  |  📞 +1 (555) 000-0000
🔗 linkedin.com/in/yourname  |  📍 New York, NY

──────────── PROFESSIONAL SUMMARY ────────────

A ${toneAdj} ${role} with ${expNote} delivering 
measurable impact across complex challenges. 
Skilled in ${skillList}, with a track record of 
driving efficiency and innovation in fast-paced 
environments.

──────────── CORE SKILLS ────────────

${skills.split(',').map(s => `  ✦ ${s.trim()}`).join('\n')}
  ✦ Team Collaboration & Leadership
  ✦ Problem Solving & Strategic Thinking

──────────── PROFESSIONAL EXPERIENCE ────────────

${role} | TechCorp Inc.                  2022 – Present
  • Led cross-functional teams delivering ${role.toLowerCase()} projects
  • Increased team productivity by 35% through process optimization
  • Implemented ${skills.split(',')[0]?.trim()} solutions adopted company-wide

Junior ${role} | StartupXYZ               2020 – 2022
  • Developed and maintained key ${role.toLowerCase()} workflows
  • Collaborated with stakeholders to define technical requirements
  • Mentored 3 junior team members in best practices

──────────── EDUCATION ────────────

B.Sc. Computer Science | State University         2016 – 2020
  GPA: 3.8/4.0 | Dean's List Recipient

──────────── CERTIFICATIONS ────────────

  ✦ AWS Certified Solutions Architect (2023)
  ✦ Google Professional ${role} Certificate (2022)
  ✦ Agile & Scrum Master Certification (2021)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ★ AI-Generated Draft — Customize Before Use ★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`.trim();
}

function typewriterEffect(el, text, speed = 10) {
  el.textContent = '';
  let i = 0;
  const timer = setInterval(() => {
    el.textContent += text[i++];
    el.scrollTop = el.scrollHeight;
    if (i >= text.length) clearInterval(timer);
  }, speed);
}

/* ============================================================
   TEMPLATE SELECTOR
   ============================================================ */
(function initTemplates() {
  document.querySelectorAll('.btn-select-template').forEach(btn => {
    btn.addEventListener('click', () => {
      const tpl = btn.dataset.template;
      Store.set('rf_selected_template', tpl);
      showToast(`Template "${tpl}" selected!`);
      setTimeout(() => window.location.href = 'builder.html', 1400);
    });
  });
})();
