from typing import Dict, Any, Optional

TECHCORP_HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>TechCorp Careers | Software Engineer Intern</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    :root {
      --bg: #0B0E14;
      --card-bg: #141923;
      --border: #232B3B;
      --gold: #F59E0B;
      --gold-light: #FCD34D;
      --text: #F1F5F9;
      --text-muted: #94A3B8;
      --accent-green: #10B981;
      --highlight: rgba(245, 158, 11, 0.25);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 24px;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 24px;
    }
    .logo {
      font-size: 20px;
      font-weight: 800;
      color: var(--gold);
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge {
      background: rgba(16, 185, 129, 0.15);
      color: var(--accent-green);
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
    }
    .job-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 28px;
      margin-bottom: 24px;
    }
    h1 { font-size: 24px; margin-bottom: 8px; color: #FFF; }
    .job-meta {
      display: flex;
      gap: 16px;
      color: var(--text-muted);
      font-size: 14px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }
    .meta-item { display: flex; align-items: center; gap: 6px; }
    .section-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--gold-light);
      margin: 18px 0 10px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    ul { padding-left: 20px; color: #CBD5E1; font-size: 14px; }
    li { margin-bottom: 6px; }
    .btn-apply {
      background: linear-gradient(135deg, #F59E0B, #D97706);
      color: #000;
      font-weight: 700;
      font-size: 15px;
      border: none;
      padding: 12px 28px;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 20px;
      transition: all 0.2s;
    }
    .btn-apply:hover { opacity: 0.9; transform: translateY(-1px); }
    .form-container {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 28px;
      display: none;
    }
    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .form-group.full { grid-column: span 2; }
    label { font-size: 13px; font-weight: 600; color: #E2E8F0; }
    input, textarea {
      background: #090B10;
      border: 1px solid var(--border);
      color: #FFF;
      padding: 10px 14px;
      border-radius: 6px;
      font-size: 13px;
    }
    input:focus, textarea:focus {
      outline: none;
      border-color: var(--gold);
      box-shadow: 0 0 8px var(--highlight);
    }
    .file-dropzone {
      border: 2px dashed #334155;
      padding: 20px;
      text-align: center;
      border-radius: 8px;
      background: #0D121B;
      cursor: pointer;
    }
    .file-attached {
      border-color: var(--accent-green);
      background: rgba(16, 185, 129, 0.08);
      color: var(--accent-green);
      font-weight: 600;
    }
    .confirmation-banner {
      display: none;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid var(--accent-green);
      color: #FFF;
      padding: 24px;
      border-radius: 12px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="logo">
      <span>TechCorp</span>
      <span style="font-size: 14px; color: var(--text-muted); font-weight: 400;">/ Careers Portal</span>
    </div>
    <div class="badge">● Actively Hiring · AI Track 2026</div>
  </div>

  <div id="job-details-view" class="job-card">
    <h1>Software Engineer Intern - AI & Autonomous Systems</h1>
    <div class="job-meta">
      <div class="meta-item">Location: San Francisco, CA (Hybrid)</div>
      <div class="meta-item">Team: Applied AI Engineering</div>
      <div class="meta-item">Comp: $55 - $70 / hr</div>
      <div class="meta-item">Type: Full-Time Internship</div>
    </div>

    <div class="section-title">About the Role</div>
    <p style="color: #CBD5E1; font-size: 14px; margin-bottom: 12px;">
      TechCorp is building autonomous browser and workflow agents that transform enterprise productivity. We are seeking a mission-driven Software Engineer Intern to engineer self-healing automation primitives, integrate foundation model reasoning streams, and implement bulletproof Human-in-the-Loop safety guardrails.
    </p>

    <div class="section-title">Key Requirements</div>
    <ul id="job-requirements-list">
      <li id="req-1">Strong proficiency in Python (FastAPI/AsyncIO) and TypeScript (React/Next.js)</li>
      <li id="req-2">Hands-on experience with LLM APIs (Anthropic Claude 3.5 Sonnet, tool-calling)</li>
      <li id="req-3">Familiarity with browser automation tools (Stagehand, Playwright, or CDP)</li>
      <li id="req-4">Understanding of Model Context Protocol (MCP) for local file extraction</li>
      <li id="req-5">Demonstrated commitment to Human-in-the-Loop (HITL) safety guardrails</li>
    </ul>

    <button id="btn-apply-now" class="btn-apply" onclick="openApplicationForm()">
      Apply for this Position →
    </button>
  </div>

  <div id="application-form-view" class="form-container">
    <h2 style="font-size: 20px; color: #FFF; margin-bottom: 4px;">Candidate Application</h2>
    <p style="color: var(--text-muted); font-size: 13px; margin-bottom: 20px;">
      Position: Software Engineer Intern - AI & Autonomous Systems (#TC-2026-9812)
    </p>

    <form id="techcorp-apply-form" onsubmit="event.preventDefault();">
      <div class="form-grid">
        <div class="form-group">
          <label for="full_name">Full Name *</label>
          <input type="text" id="full_name" name="full_name" placeholder="First and last name" required />
        </div>
        <div class="form-group">
          <label for="email">Email Address *</label>
          <input type="email" id="email" name="email" placeholder="name@example.com" required />
        </div>
        <div class="form-group">
          <label for="phone">Phone Number *</label>
          <input type="tel" id="phone" name="phone" placeholder="+1 (555) 000-0000" required />
        </div>
        <div class="form-group">
          <label for="linkedin">LinkedIn Profile URL</label>
          <input type="url" id="linkedin" name="linkedin" placeholder="https://linkedin.com/in/username" />
        </div>
        <div class="form-group">
          <label for="github">GitHub Profile URL</label>
          <input type="url" id="github" name="github" placeholder="https://github.com/username" />
        </div>
        <div class="form-group">
          <label for="portfolio">Portfolio / Personal Website</label>
          <input type="url" id="portfolio" name="portfolio" placeholder="https://yourname.dev" />
        </div>
        <div class="form-group full">
          <label for="skills">Key Technical Skills & Competencies *</label>
          <textarea id="skills" name="skills" rows="2" placeholder="List relevant technologies..." required></textarea>
        </div>
        <div class="form-group full">
          <label for="cover_letter">Why TechCorp? (Custom Cover Letter) *</label>
          <textarea id="cover_letter" name="cover_letter" rows="4" placeholder="Briefly describe your fit for this role..." required></textarea>
        </div>
        <div class="form-group full">
          <label>Resume Attachment (PDF) *</label>
          <div id="resume-dropzone" class="file-dropzone" onclick="simulateFileUpload()">
            <div id="dropzone-text" style="color: #94A3B8; font-size: 13px;">
              Drag & drop your resume.pdf here, or click to attach
            </div>
            <input type="file" id="resume_upload" style="display: none;" accept=".pdf" />
          </div>
        </div>
      </div>

      <div style="margin-top: 24px; display: flex; justify-content: flex-end; gap: 12px;">
        <button type="button" class="btn-apply" id="btn-submit-application" style="margin-top: 0; background: linear-gradient(135deg, #10B981, #059669);" onclick="submitApplication()">
          Submit Final Application ✓
        </button>
      </div>
    </form>
  </div>

  <div id="confirmation-banner-view" class="confirmation-banner">
    <div style="margin-bottom: 12px; color: #10B981;">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
    </div>
    <h2 style="font-size: 22px; margin-bottom: 6px; color: #10B981;">Application Submitted Successfully!</h2>
    <p style="color: #CBD5E1; font-size: 14px; margin-bottom: 16px;">
      Thank you for applying to TechCorp. Your application has been logged into our candidate system.
    </p>
    <div style="display: inline-block; background: #0B0E14; padding: 10px 20px; border-radius: 8px; border: 1px solid #10B981; font-family: monospace; font-size: 14px;">
      Confirmation Receipt: <strong id="receipt-id">#TC-APP-2026-9812</strong>
    </div>
  </div>

  <script>
    function openApplicationForm() {
      document.getElementById('job-details-view').style.display = 'none';
      document.getElementById('application-form-view').style.display = 'block';
      window.parent.postMessage({ type: 'PORTAL_EVENT', action: 'form_opened' }, '*');
    }

    function simulateFileUpload() {
      const dropzone = document.getElementById('resume-dropzone');
      dropzone.classList.add('file-attached');
      dropzone.innerHTML = '✓ Attached: <strong>resume.pdf</strong> (142 KB) — Verified by MCP Client';
      window.parent.postMessage({ type: 'PORTAL_EVENT', action: 'file_attached' }, '*');
    }

    function submitApplication() {
      document.getElementById('application-form-view').style.display = 'none';
      document.getElementById('confirmation-banner-view').style.display = 'block';
      window.parent.postMessage({ type: 'PORTAL_EVENT', action: 'application_submitted' }, '*');
    }

    window.addEventListener('message', function(e) {
      if (!e.data) return;
      if (e.data.action === 'auto_open_form') openApplicationForm();
      if (e.data.action === 'auto_attach_file') simulateFileUpload();
      if (e.data.action === 'auto_submit') submitApplication();
      if (e.data.action === 'populate_field') {
        const el = document.getElementById(e.data.fieldId);
        if (el) {
          el.value = e.data.value;
          el.style.borderColor = '#10B981';
        }
      }
    });
  </script>
</body>
</html>
"""

GREENHOUSE_HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ScaleAI / Anthropic Partner | Greenhouse ATS</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0D1117; color: #C9D1D9; padding: 28px; line-height: 1.5; }
    .gh-card { background: #161B22; border: 1px solid #30363D; border-radius: 8px; padding: 28px; max-width: 800px; margin: 0 auto; }
    .gh-header { border-bottom: 1px solid #30363D; padding-bottom: 16px; margin-bottom: 20px; }
    h1 { color: #58A6FF; font-size: 22px; margin-bottom: 6px; }
    .badge { background: #238636; color: #FFF; padding: 2px 8px; border-radius: 12px; font-size: 11px; }
    .field { margin-bottom: 16px; display: flex; flex-direction: column; gap: 6px; }
    label { font-size: 13px; font-weight: 600; color: #F0F6FC; }
    input, textarea { background: #0D1117; border: 1px solid #30363D; color: #FFF; padding: 10px; border-radius: 6px; font-size: 13px; }
    .btn-submit { background: #238636; color: #FFF; border: none; padding: 12px 24px; border-radius: 6px; font-weight: 700; cursor: pointer; }
  </style>
</head>
<body>
  <div class="gh-card">
    <div class="gh-header">
      <span class="badge">Greenhouse ATS v3.4</span>
      <h1 style="margin-top: 8px;">Full Stack AI Applications Engineer</h1>
      <div style="font-size: 13px; color: #8B949E;">ScaleAI / Anthropic Partner · San Francisco, CA · Remote</div>
    </div>
    <form id="greenhouse-form" onsubmit="event.preventDefault(); document.getElementById('success').style.display='block'; this.style.display='none';">
      <div class="field"><label>First Name *</label><input type="text" id="first_name" value="Dharanidharan" /></div>
      <div class="field"><label>Last Name *</label><input type="text" id="last_name" value="D" /></div>
      <div class="field"><label>Email *</label><input type="email" id="email" value="dharanidharan.ai@example.com" /></div>
      <div class="field"><label>Phone *</label><input type="tel" id="phone" value="+1 (555) 234-8901" /></div>
      <div class="field"><label>Resume/CV *</label><input type="text" id="resume" value="resume.pdf (Attached ✓)" /></div>
      <div class="field"><label>Cover Letter</label><textarea id="cover_letter" rows="3">Applying with strong enthusiasm for foundation model evaluation platforms and real-time Stagehand agent telemetry.</textarea></div>
      <button class="btn-submit" type="submit">Submit Application</button>
    </form>
    <div id="success" style="display: none; padding: 20px; background: rgba(35, 134, 54, 0.2); border: 1px solid #238636; border-radius: 6px; text-align: center;">
      <h3>✓ Application Submitted to ScaleAI Greenhouse Portal</h3>
      <p style="font-size: 13px; color: #8B949E; margin-top: 6px;">Confirmation Ref: #GH-SCALE-4819231</p>
    </div>
  </div>
</body>
</html>
"""

WORKDAY_HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CloudScale Systems | Workday Enterprise Careers</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0A0D14; color: #D1D5DB; padding: 28px; }
    .wd-card { background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 28px; max-width: 800px; margin: 0 auto; }
    h1 { color: #60A5FA; font-size: 22px; margin-bottom: 6px; }
    .field { margin-bottom: 16px; display: flex; flex-direction: column; gap: 6px; }
    label { font-size: 13px; font-weight: 600; color: #F3F4F6; }
    input, textarea { background: #1F2937; border: 1px solid #4B5563; color: #FFF; padding: 10px; border-radius: 6px; font-size: 13px; }
    .btn-submit { background: #2563EB; color: #FFF; border: none; padding: 12px 24px; border-radius: 6px; font-weight: 700; cursor: pointer; }
  </style>
</head>
<body>
  <div class="wd-card">
    <div style="font-size: 11px; color: #9CA3AF; text-transform: uppercase; font-weight: 700; margin-bottom: 8px;">Workday Enterprise Cloud</div>
    <h1>Lead Cloud Infrastructure Architect</h1>
    <div style="font-size: 13px; color: #9CA3AF; margin-bottom: 20px;">CloudScale Systems · Austin, TX · Remote Option</div>
    <form id="workday-form" onsubmit="event.preventDefault(); document.getElementById('success').style.display='block'; this.style.display='none';">
      <div class="field"><label>Legal Full Name *</label><input type="text" id="applicant_name" value="Dharanidharan D" /></div>
      <div class="field"><label>Email Address *</label><input type="email" id="applicant_email" value="dharanidharan.ai@example.com" /></div>
      <div class="field"><label>Work Authorization *</label><input type="text" id="work_auth" value="Authorized for US without sponsorship" /></div>
      <div class="field"><label>Desired Compensation</label><input type="text" id="salary" value="$185,000 / year" /></div>
      <button class="btn-submit" type="submit">Complete Workday Submission</button>
    </form>
    <div id="success" style="display: none; padding: 20px; background: rgba(37, 99, 235, 0.2); border: 1px solid #2563EB; border-radius: 6px; text-align: center;">
      <h3>✓ Workday Submission Recorded</h3>
      <p style="font-size: 13px; color: #9CA3AF; margin-top: 6px;">Confirmation Ref: #WD-CLOUD-7718</p>
    </div>
  </div>
</body>
</html>
"""

def generate_unstop_portal_html(internship: Optional[Dict[str, Any]] = None) -> str:
    """Generates a high-fidelity Unstop internship page and multi-step application form"""
    data = internship or {
        "id": "gov-meity-genai-fellow-2026",
        "company": "MeitY (Digital India Bhashini AI Mission)",
        "title": "Generative AI & Indic Language Model Fellow",
        "program": "Digital India Bhashini AI Mission",
        "category": "AI / Machine Learning",
        "location": "New Delhi / Remote",
        "mode": "Hybrid",
        "stipend": "₹60,000 / month",
        "duration": "6 - 12 Months",
        "deadline": "10 Nov 2026",
        "applicants_count": 890,
        "qualifications": "B.Tech / M.Tech in Computer Science, Data Science, or AI. Familiarity with Indian languages NLP and Transformer models.",
        "description": "MeitY's Digital India Bhashini division is offering fellowship grants to build open-source multilingual AI agents, speech models, and automated citizen services.",
        "requirements": [
            "Python (PyTorch, Hugging Face Transformers)",
            "Experience fine-tuning LLMs and Whisper speech models",
            "Understanding of Indic languages datasets and tokenization",
            "Knowledge of REST APIs and microservice deployment"
        ]
    }

    reqs_li = "".join([f"<li style='margin-bottom: 6px;'>{req}</li>" for req in data.get("requirements", [])])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{data.get('title')} at {data.get('company')} | Unstop Internships</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    :root {{
      --unstop-navy: #0B132B;
      --unstop-dark: #1C2541;
      --unstop-card: #151D33;
      --unstop-border: #2A3656;
      --unstop-cyan: #00B4D8;
      --unstop-blue: #0077B6;
      --unstop-teal: #48CAE4;
      --unstop-gold: #F59E0B;
      --unstop-green: #10B981;
      --text: #F8FAFC;
      --text-muted: #94A3B8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--unstop-navy);
      color: var(--text);
      line-height: 1.5;
      padding: 0;
      min-height: 100vh;
    }}
    header {{
      background: var(--unstop-dark);
      border-bottom: 1px solid var(--unstop-border);
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .unstop-logo {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 20px;
      font-weight: 900;
      letter-spacing: -0.5px;
      color: #FFF;
    }}
    .unstop-logo span.dot {{ color: var(--unstop-cyan); }}
    .unstop-nav {{
      display: flex;
      gap: 16px;
      align-items: center;
      font-size: 13px;
    }}
    .nav-link {{
      color: var(--text-muted);
      text-decoration: none;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
    }}
    .nav-link.active {{
      background: rgba(0, 180, 216, 0.15);
      color: var(--unstop-cyan);
    }}
    .container {{
      max-width: 980px;
      margin: 24px auto;
      padding: 0 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .hero-card {{
      background: var(--unstop-card);
      border: 1px solid var(--unstop-border);
      border-radius: 14px;
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    .badge-bar {{
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .unstop-badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .badge-verified {{
      background: rgba(16, 185, 129, 0.15);
      color: var(--unstop-green);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .badge-hiring {{
      background: rgba(0, 180, 216, 0.15);
      color: var(--unstop-cyan);
      border: 1px solid rgba(0, 180, 216, 0.3);
    }}
    .hero-title {{
      font-size: 26px;
      font-weight: 800;
      color: #FFF;
      line-height: 1.25;
    }}
    .hero-company {{
      font-size: 16px;
      color: var(--unstop-cyan);
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px;
      background: var(--unstop-navy);
      padding: 16px;
      border-radius: 10px;
      border: 1px solid var(--unstop-border);
      margin-top: 6px;
    }}
    .meta-box {{ display: flex; flex-direction: column; gap: 4px; }}
    .meta-label {{ font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }}
    .meta-val {{ font-size: 14px; font-weight: 700; color: #FFF; }}
    .btn-unstop-apply {{
      background: linear-gradient(135deg, var(--unstop-cyan), var(--unstop-blue));
      color: #FFF;
      border: none;
      padding: 14px 28px;
      font-size: 15px;
      font-weight: 800;
      border-radius: 8px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
      width: fit-content;
    }}
    .btn-unstop-apply:hover {{
      opacity: 0.92;
      transform: translateY(-1px);
      box-shadow: 0 4px 20px rgba(0, 180, 216, 0.4);
    }}
    .section-card {{
      background: var(--unstop-card);
      border: 1px solid var(--unstop-border);
      border-radius: 14px;
      padding: 24px;
    }}
    .section-title {{
      font-size: 16px;
      font-weight: 800;
      color: #FFF;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .form-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 14px;
    }}
    .form-group {{ display: flex; flex-direction: column; gap: 6px; }}
    .form-group.full {{ grid-column: span 2; }}
    label {{ font-size: 12px; font-weight: 600; color: var(--text-muted); }}
    input, textarea, select {{
      background: var(--unstop-navy);
      border: 1px solid var(--unstop-border);
      color: #FFF;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-family: inherit;
    }}
    input:focus, textarea:focus {{
      outline: none;
      border-color: var(--unstop-cyan);
      box-shadow: 0 0 10px rgba(0, 180, 216, 0.3);
    }}
    .file-dropzone {{
      border: 2px dashed var(--unstop-border);
      border-radius: 8px;
      padding: 20px;
      text-align: center;
      background: var(--unstop-navy);
      cursor: pointer;
    }}
    .autofill-banner {{
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.35);
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 12px;
      color: var(--unstop-green);
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
    }}
  </style>
</head>
<body>

  <header>
    <div class="unstop-logo">
      <span>unstop</span><span class="dot">●</span>
      <span style="font-size: 12px; color: var(--text-muted); font-weight: 400; margin-left: 6px;">| Early Careers & Internships</span>
    </div>
    <div class="unstop-nav">
      <span class="nav-link active">Internships</span>
      <span class="nav-link">Jobs</span>
      <span class="nav-link">Competitions</span>
      <span style="font-size: 12px; color: var(--unstop-cyan); font-weight: 600;">SIVI Autonomous Agent Ready</span>
    </div>
  </header>

  <div class="container">
    <!-- Hero Details Card -->
    <div id="unstop-details-view" class="hero-card">
      <div class="badge-bar">
        <span class="unstop-badge badge-verified">✓ Verified Recruiter</span>
        <span class="unstop-badge badge-hiring">● Actively Hiring 2026</span>
        <span style="font-size: 12px; color: var(--text-muted); margin-left: auto;">{data.get('applicants_count', 1420)}+ Applied</span>
      </div>

      <div>
        <div class="hero-company">{data.get('company')}</div>
        <h1 class="hero-title">{data.get('title')}</h1>
        <div style="font-size: 13px; color: var(--unstop-teal); margin-top: 4px;">{data.get('program', 'Campus Hiring Challenge')}</div>
      </div>

      <div class="meta-grid">
        <div class="meta-box">
          <span class="meta-label">Stipend</span>
          <span class="meta-val" style="color: var(--unstop-green);">{data.get('stipend')}</span>
        </div>
        <div class="meta-box">
          <span class="meta-label">Location / Mode</span>
          <span class="meta-val">{data.get('location')}</span>
        </div>
        <div class="meta-box">
          <span class="meta-label">Duration</span>
          <span class="meta-val">{data.get('duration')}</span>
        </div>
        <div class="meta-box">
          <span class="meta-label">Application Deadline</span>
          <span class="meta-val" style="color: var(--unstop-gold);">{data.get('deadline')}</span>
        </div>
      </div>

      <div style="display: flex; gap: 12px; align-items: center; margin-top: 6px;">
        <button id="btn-unstop-apply" class="btn-unstop-apply" onclick="openUnstopForm()">
          <span>Apply on Unstop with SIVI Autofill →</span>
        </button>
        <span style="font-size: 12px; color: var(--text-muted);">Instant 1-click qualifications & resume matching</span>
      </div>
    </div>

    <!-- Requirements Card -->
    <div id="unstop-reqs-view" class="section-card">
      <div class="section-title">Eligibility Criteria & Qualifications</div>
      <p style="font-size: 13px; color: #CBD5E1; margin-bottom: 14px;">
        {data.get('qualifications')}
      </p>

      <div class="section-title" style="margin-top: 16px;">Key Technical Requirements</div>
      <ul id="unstop-requirements-list" style="padding-left: 20px; font-size: 13px; color: #CBD5E1;">
        {reqs_li}
      </ul>

      <div class="section-title" style="margin-top: 16px;">About this Internship</div>
      <p style="font-size: 13px; color: #94A3B8; line-height: 1.6;">
        {data.get('description')}
      </p>
    </div>

    <!-- Multi-Step Application Form View -->
    <div id="unstop-form-view" class="section-card" style="display: none;">
      <div class="autofill-banner">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        <strong>SIVI Autofill Active:</strong>
        <span>All candidate details, academic qualifications, and resume.pdf have been matched and pre-populated.</span>
      </div>

      <div class="section-title">Candidate Application Form</div>
      <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">
        Applying for: <strong style="color: #FFF;">{data.get('title')}</strong> at <strong style="color: var(--unstop-cyan);">{data.get('company')}</strong>
      </p>

      <form id="unstop-apply-form" onsubmit="event.preventDefault(); submitUnstopApplication();">
        <div class="form-grid">
          <!-- Step 1: Personal Details -->
          <div class="form-group">
            <label for="unstop_name">Full Name *</label>
            <input type="text" id="unstop_name" name="name" value="Dharanidharan D" required />
          </div>
          <div class="form-group">
            <label for="unstop_email">Email Address *</label>
            <input type="email" id="unstop_email" name="email" value="dharanidharan.ai@example.com" required />
          </div>
          <div class="form-group">
            <label for="unstop_phone">Phone Number *</label>
            <input type="tel" id="unstop_phone" name="phone" value="+1 (555) 234-8901" required />
          </div>

          <!-- Step 2: Educational Qualifications -->
          <div class="form-group">
            <label for="unstop_college">College / University *</label>
            <input type="text" id="unstop_college" name="college" value="Institute of Technology" required />
          </div>
          <div class="form-group">
            <label for="unstop_degree">Degree & Branch *</label>
            <input type="text" id="unstop_degree" name="degree" value="B.Tech in Artificial Intelligence & Data Science" required />
          </div>
          <div class="form-group">
            <label for="unstop_grad_year">Graduation Year *</label>
            <input type="text" id="unstop_grad_year" name="grad_year" value="2026" required />
          </div>
          <div class="form-group">
            <label for="unstop_cgpa">CGPA / Grade *</label>
            <input type="text" id="unstop_cgpa" name="cgpa" value="3.92 / 4.0" required />
          </div>
          <div class="form-group">
            <label for="unstop_linkedin">LinkedIn Profile URL</label>
            <input type="url" id="unstop_linkedin" name="linkedin" value="https://linkedin.com/in/dharanidharan-ai" />
          </div>
          <div class="form-group">
            <label for="unstop_github">GitHub Profile URL</label>
            <input type="url" id="unstop_github" name="github" value="https://github.com/dharanidharan-dev" />
          </div>

          <!-- Step 3: Skills & Documents -->
          <div class="form-group full">
            <label for="unstop_skills">Key Technical Skills & Competencies *</label>
            <textarea id="unstop_skills" name="skills" rows="2" required>Python, FastAPI, Next.js, TypeScript, Stagehand, Claude 3.5 Sonnet, MCP, Docker, PyTorch</textarea>
          </div>
          <div class="form-group full">
            <label for="unstop_cover_letter">Statement of Purpose / Why Should We Hire You? *</label>
            <textarea id="unstop_cover_letter" name="cover_letter" rows="3" required>I am an AI Engineer specializing in autonomous agent workflows, browser automation, and LLM integrations. Having architected SIVI with Stagehand, MCP, and Claude 3.5 Sonnet, I bring direct hands-on expertise to {data.get('company')}'s engineering challenges.</textarea>
          </div>
          <div class="form-group full">
            <label>Resume Document (PDF) *</label>
            <div id="unstop_resume_dropzone" class="file-dropzone" onclick="alert('resume.pdf attached via MCP.')">
              <span style="color: var(--unstop-green); font-weight: 700; font-size: 13px;">
                ✓ resume.pdf (142 KB, Validated & Attached via SIVI MCP)
              </span>
            </div>
          </div>
        </div>

        <div style="margin-top: 24px; display: flex; justify-content: flex-end; gap: 12px;">
          <button type="submit" id="unstop-btn-submit" class="btn-unstop-apply" style="background: linear-gradient(135deg, var(--unstop-green), #059669);">
            <span>Submit Unstop Application ✓</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Confirmation Banner -->
    <div id="unstop-confirmation-view" class="section-card" style="display: none; text-align: center; padding: 40px 20px;">
      <div style="margin-bottom: 12px; color: var(--unstop-green);">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      </div>
      <h2 style="font-size: 22px; color: var(--unstop-green); margin-bottom: 8px;">Application Submitted on Unstop!</h2>
      <p style="font-size: 14px; color: #CBD5E1; margin-bottom: 14px;">
        Your application for <strong style="color: #FFF;">{data.get('title')}</strong> at <strong style="color: var(--unstop-cyan);">{data.get('company')}</strong> has been submitted.
      </p>
      <div style="display: inline-block; background: var(--unstop-navy); border: 1px solid var(--unstop-border); padding: 8px 16px; border-radius: 6px; font-family: monospace; color: var(--unstop-gold); font-size: 13px;">
        Unstop Application Ref: <strong id="unstop-receipt-id">#UNSTOP-2026-9842</strong>
      </div>
    </div>
  </div>

  <script>
    function openUnstopForm() {{
      document.getElementById('unstop-details-view').style.display = 'none';
      document.getElementById('unstop-reqs-view').style.display = 'none';
      document.getElementById('unstop-form-view').style.display = 'block';
      window.location.hash = '#form';
    }}

    function submitUnstopApplication() {{
      document.getElementById('unstop-form-view').style.display = 'none';
      document.getElementById('unstop-confirmation-view').style.display = 'block';
      window.location.hash = '#confirmation';
    }}

    // Auto-open form if hash is #form
    if (window.location.hash === '#form') {{
      openUnstopForm();
    }}
  </script>
</body>
</html>
"""

def get_mock_portal_html(portal_id: str = "techcorp") -> str:
    """Returns portal HTML based on portal identifier"""
    p_lower = portal_id.lower()
    if "unstop" in p_lower or "gov-" in p_lower:
        from unstop_service import unstop_service
        internship = unstop_service.get_internship_by_id(portal_id)
        return generate_unstop_portal_html(internship)
    elif "greenhouse" in p_lower:
        return GREENHOUSE_HTML_PAGE
    elif "workday" in p_lower:
        return WORKDAY_HTML_PAGE
    return TECHCORP_HTML_PAGE

def get_mock_page_state(step: int, portal_id: str = "techcorp") -> Dict[str, Any]:
    """Simulates Stagehand observe() inspection state at various workflow steps"""
    p_lower = portal_id.lower()
    if "unstop" in p_lower or "gov-" in p_lower:
        if step == 1:
            return {
                "url": f"http://localhost:8888/mock/unstop/internships/{portal_id}",
                "title": "Unstop Internships | Application Portal",
                "active_section": "job_details",
                "elements": [
                    {"id": "btn-unstop-apply", "tag": "button", "text": "Apply on Unstop with SIVI Autofill →", "x": 120, "y": 480, "width": 260, "height": 48},
                    {"id": "unstop-requirements-list", "tag": "ul", "text": "Unstop qualifications & requirements", "x": 120, "y": 320, "width": 600, "height": 140}
                ]
            }
        elif step in [2, 3, 5]:
            return {
                "url": f"http://localhost:8888/mock/unstop/internships/{portal_id}#form",
                "title": "Unstop Internships | Multi-Step Application Form",
                "active_section": "form_active",
                "elements": [
                    {"id": "unstop_name", "tag": "input", "name": "name", "type": "text", "x": 120, "y": 140, "width": 280, "height": 42},
                    {"id": "unstop_email", "tag": "input", "name": "email", "type": "email", "x": 420, "y": 140, "width": 280, "height": 42},
                    {"id": "unstop_phone", "tag": "input", "name": "phone", "type": "tel", "x": 120, "y": 210, "width": 280, "height": 42},
                    {"id": "unstop_college", "tag": "input", "name": "college", "type": "text", "x": 420, "y": 210, "width": 280, "height": 42},
                    {"id": "unstop_degree", "tag": "input", "name": "degree", "type": "text", "x": 120, "y": 280, "width": 280, "height": 42},
                    {"id": "unstop_grad_year", "tag": "input", "name": "grad_year", "type": "text", "x": 420, "y": 280, "width": 140, "height": 42},
                    {"id": "unstop_cgpa", "tag": "input", "name": "cgpa", "type": "text", "x": 580, "y": 280, "width": 120, "height": 42},
                    {"id": "unstop_skills", "tag": "textarea", "name": "skills", "x": 120, "y": 350, "width": 580, "height": 60},
                    {"id": "unstop_cover_letter", "tag": "textarea", "name": "cover_letter", "x": 120, "y": 430, "width": 580, "height": 80},
                    {"id": "unstop-btn-submit", "tag": "button", "text": "Submit Unstop Application ✓", "x": 460, "y": 550, "width": 240, "height": 48}
                ]
            }
        else:
            return {
                "url": f"http://localhost:8888/mock/unstop/internships/{portal_id}#confirmation",
                "title": "Unstop Internships | Application Confirmed",
                "active_section": "confirmation",
                "elements": [
                    {"id": "unstop-receipt-id", "tag": "strong", "text": "#UNSTOP-2026-9842", "x": 200, "y": 300, "width": 300, "height": 40}
                ]
            }

    if step == 1:
        return {
            "url": "http://localhost:8888/mock/techcorp/jobs/swe-intern",
            "title": "TechCorp Careers | Software Engineer Intern",
            "active_section": "job_details",
            "elements": [
                {"id": "btn-apply-now", "tag": "button", "text": "Apply for this Position →", "x": 120, "y": 480, "width": 240, "height": 48},
                {"id": "job-requirements-list", "tag": "ul", "text": "Requirements list (5 items)", "x": 120, "y": 320, "width": 600, "height": 140}
            ]
        }
    elif step in [2, 3]:
        return {
            "url": "http://localhost:8888/mock/techcorp/jobs/swe-intern#form",
            "title": "TechCorp Careers | Application Form",
            "active_section": "form_active",
            "elements": [
                {"id": "full_name", "tag": "input", "name": "full_name", "type": "text", "x": 120, "y": 140, "width": 280, "height": 42},
                {"id": "email", "tag": "input", "name": "email", "type": "email", "x": 420, "y": 140, "width": 280, "height": 42},
                {"id": "phone", "tag": "input", "name": "phone", "type": "tel", "x": 120, "y": 210, "width": 280, "height": 42},
                {"id": "skills", "tag": "textarea", "name": "skills", "x": 120, "y": 280, "width": 580, "height": 60},
                {"id": "cover_letter", "tag": "textarea", "name": "cover_letter", "x": 120, "y": 360, "width": 580, "height": 90},
                {"id": "resume-dropzone", "tag": "div", "text": "Resume Dropzone", "x": 120, "y": 470, "width": 580, "height": 70},
                {"id": "btn-submit-application", "tag": "button", "text": "Submit Final Application ✓", "x": 460, "y": 560, "width": 240, "height": 48}
            ]
        }
    else:
        return {
            "url": "http://localhost:8888/mock/techcorp/jobs/swe-intern#confirmation",
            "title": "TechCorp Careers | Confirmation",
            "active_section": "confirmation",
            "elements": [
                {"id": "receipt-id", "tag": "strong", "text": "#TC-APP-2026-9812", "x": 200, "y": 300, "width": 300, "height": 40}
            ]
        }

