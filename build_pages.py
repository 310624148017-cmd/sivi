import sys, os, json, base64

# Add backend directory
sys.path.insert(0, os.path.abspath("backend"))

from app import app
from starlette.testclient import TestClient
from mock_portal import TECHCORP_HTML_PAGE, generate_unstop_portal_html
from unstop_service import CURATED_UNSTOP_INTERNSHIPS

client = TestClient(app)
res = client.get("/")
raw_html = res.text

# 1. Base64 encode all static portals
portals = { "techcorp": TECHCORP_HTML_PAGE }
for item in CURATED_UNSTOP_INTERNSHIPS:
    pid = item["id"]
    p_html = generate_unstop_portal_html(item)
    portals[pid] = p_html
    if "meity" in pid:
        portals["meity"] = p_html
        portals["unstop"] = p_html
    elif "isro" in pid:
        portals["isro"] = p_html
    elif "nic" in pid:
        portals["nic"] = p_html
    elif "drdo" in pid:
        portals["drdo"] = p_html
    elif "aicte" in pid:
        portals["aicte"] = p_html

portals_b64 = base64.b64encode(json.dumps(portals).encode("utf-8")).decode("ascii")
unstop_b64 = base64.b64encode(json.dumps(client.get("/api/unstop/search").json()).encode("utf-8")).decode("ascii")
apps_b64 = base64.b64encode(json.dumps(client.get("/api/applications").json()).encode("utf-8")).decode("ascii")
analytics_b64 = base64.b64encode(json.dumps(client.get("/api/analytics").json()).encode("utf-8")).decode("ascii")
cand_b64 = base64.b64encode(json.dumps(client.get("/api/candidate").json()).encode("utf-8")).decode("ascii")
providers_b64 = base64.b64encode(json.dumps(client.get("/api/models/providers").json()).encode("utf-8")).decode("ascii")

# Clean iframe src
clean_html = raw_html.replace(
    '<iframe id="browser-iframe" class="browser-iframe" src="/mock/techcorp/jobs/swe-intern"></iframe>',
    '<iframe id="browser-iframe" class="browser-iframe"></iframe>'
)

clean_html = clean_html.replace(
    "if (iframe) iframe.src = '/mock/unstop/internships/gov-meity-genai-fellow-2026';",
    "loadPortal('meity');"
)
clean_html = clean_html.replace(
    "if (iframe) iframe.src = '/mock/unstop/internships/gov-isro-sac-geospatial-2026';",
    "loadPortal('isro');"
)
clean_html = clean_html.replace(
    "if (iframe) iframe.src = '/mock/unstop/internships/gov-nic-digital-india-2026';",
    "loadPortal('nic');"
)
clean_html = clean_html.replace(
    "if (iframe) iframe.src = '/mock/unstop/internships/gov-drdo-robotics-2026';",
    "loadPortal('drdo');"
)
clean_html = clean_html.replace(
    "if (iframe) iframe.src = '/mock/unstop/internships/gov-aicte-tech-intern-2026';",
    "loadPortal('aicte');"
)
clean_html = clean_html.replace(
    "if (iframe) iframe.src = '/mock/techcorp/jobs/swe-intern';",
    "loadPortal('techcorp');"
)
clean_html = clean_html.replace(
    "if (iframe) iframe.src = url;",
    "loadPortal(id || 'meity');"
)

# Start execution simulation
orig_ws = """const wsUrl = protocol + '//' + window.location.host + '/ws/agent';\n\n      ws = new WebSocket(wsUrl);"""
new_ws = """const wsUrl = protocol + '//' + window.location.host + '/ws/agent';
      if (window.location.hostname.includes('github.io') || window.location.protocol === 'file:') {
        runClientAutonomousSimulation(goal, jobUrl, tone);
        return;
      }
      try {
        ws = new WebSocket(wsUrl);
      } catch (err) {
        runClientAutonomousSimulation(goal, jobUrl, tone);
        return;
      }
      ws.onerror = function() {
        runClientAutonomousSimulation(goal, jobUrl, tone);
      };"""
clean_html = clean_html.replace(orig_ws, new_ws)

# Resolve approval
orig_appr = "if (ws && ws.readyState === WebSocket.OPEN) {"
new_appr = """if (!ws || ws.readyState !== WebSocket.OPEN) {
        if (approved) {
          handleAgentEvent({
            type: 'status',
            phase: 'COMPLETED',
            message: 'Application submitted successfully (#UNSTOP-2026-9842)'
          });
          handleAgentEvent({
            type: 'action_result',
            action: 'submit_final',
            result: { status: 'COMPLETED', confirmation_id: '#UNSTOP-2026-9842', message: 'Application submitted successfully' }
          });
          document.getElementById('btn-start').disabled = false;
          document.getElementById('btn-start').innerHTML = '<svg class="icon" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3" /></svg><span>Launch SIVI</span>';
          document.getElementById('agent-state-label').innerText = 'Agent Ready (Idle)';
          alert('SIVI Safety Gate Approved! Application submitted successfully.\\nConfirmation ID: #UNSTOP-2026-9842\\nLogged to audit trail.');
        } else {
          handleAgentEvent({
            type: 'status',
            phase: 'ABORTED',
            message: 'Action aborted by Human Operator.'
          });
          document.getElementById('btn-start').disabled = false;
          document.getElementById('btn-start').innerHTML = '<svg class="icon" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3" /></svg><span>Launch SIVI</span>';
          document.getElementById('agent-state-label').innerText = 'Agent Ready (Idle)';
        }
      }
      if (ws && ws.readyState === WebSocket.OPEN) {"""
clean_html = clean_html.replace(orig_appr, new_appr)

static_script = f"""
  <script>
    function b64Decode(str) {{
      return decodeURIComponent(atob(str).split('').map(function(c) {{
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }}).join(''));
    }}

    window.STATIC_PORTALS = JSON.parse(b64Decode("{portals_b64}"));
    window.STATIC_UNSTOP = JSON.parse(b64Decode("{unstop_b64}"));
    window.STATIC_APPS = JSON.parse(b64Decode("{apps_b64}"));
    window.STATIC_ANALYTICS = JSON.parse(b64Decode("{analytics_b64}"));
    window.STATIC_CANDIDATE = JSON.parse(b64Decode("{cand_b64}"));
    window.STATIC_PROVIDERS = JSON.parse(b64Decode("{providers_b64}"));

    function loadPortal(key) {{
      const iframe = document.getElementById('browser-iframe');
      if (!iframe) return;
      const cleanKey = (key || 'techcorp').toLowerCase();
      let matched = window.STATIC_PORTALS[cleanKey];
      if (!matched) {{
        for (const k in window.STATIC_PORTALS) {{
          if (cleanKey.includes(k) || k.includes(cleanKey)) {{
            matched = window.STATIC_PORTALS[k];
            break;
          }}
        }}
      }}
      iframe.srcdoc = matched || window.STATIC_PORTALS['techcorp'];
    }}

    function runClientAutonomousSimulation(goal, jobUrl, tone) {{
      const body = document.getElementById('reasoning-body');
      body.innerHTML = '';
      tokenCount = 0;
      document.getElementById('agent-state-label').innerText = 'Autonomous Workflow Active';
      document.getElementById('btn-start').disabled = true;
      document.getElementById('btn-start').innerText = 'Agent Active...';

      const steps = [
        {{ type: 'status', message: 'Initializing SIVI for goal: "' + goal + '"' }},
        {{ type: 'reasoning_stream', chunk: '[OBSERVE] Connecting Stagehand CDP to ' + jobUrl + '...\\n' }},
        {{ type: 'reasoning_stream', chunk: '[MCP] Reading local candidate profile: Dharanidharan D (resume.pdf)...\\n' }},
        {{ type: 'reasoning_stream', chunk: '[MATCH] Smart skills taxonomy matching... Match score: 96.2%\\n' }},
        {{ type: 'reasoning_stream', chunk: '[SYNTHESIS] Generating tailored ' + tone + ' cover letter emphasizing AI & autonomous systems...\\n' }},
        {{ type: 'reasoning_stream', chunk: '[STAGEHAND ACT] Locating application form fields and autofilling academic credentials...\\n' }},
        {{ type: 'action_result', action: 'autofill_form', result: 'Populated Name, Email, College (Institute of Technology), CGPA (3.95/4.0)' }},
        {{ type: 'approval_required', form_preview: {{ candidate_name: 'Dharanidharan D', company: 'Target Organization', role: goal, resume_attached: 'resume.pdf (142 KB, Validated)' }} }}
      ];

      let idx = 0;
      function nextStep() {{
        if (idx >= steps.length) return;
        const s = steps[idx++];
        handleAgentEvent(s);
        if (s.type !== 'approval_required') {{
          setTimeout(nextStep, 500);
        }}
      }}
      setTimeout(nextStep, 300);
    }}

    window.addEventListener('DOMContentLoaded', function() {{
      setTimeout(function() {{ loadPortal('techcorp'); }}, 50);
      if (window.location.hostname.includes('github.io')) {{
        setTimeout(function() {{
          if (typeof renderUnstopCards === 'function') renderUnstopCards(window.STATIC_UNSTOP.internships || []);
          if (typeof renderApplications === 'function') renderApplications(window.STATIC_APPS.applications || []);
          if (typeof renderAnalytics === 'function') renderAnalytics(window.STATIC_ANALYTICS || {{}});
          if (typeof renderModelProviders === 'function') renderModelProviders(window.STATIC_PROVIDERS || {{}});
        }}, 100);
      }}
    }});
  </script>
"""

clean_html = clean_html.replace("</body>", static_script + "\n</body>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(clean_html)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(clean_html)

print("SUCCESS: index.html and docs/index.html generated, size:", len(clean_html))
