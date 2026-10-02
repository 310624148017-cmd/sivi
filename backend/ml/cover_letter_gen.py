import os
from typing import Dict, Any, Optional

class CoverLetterGenerator:
    """
    AI-powered Cover Letter Generation Engine with Tone Customization.
    Synthesizes tailored, role-specific cover letters using candidate background,
    job requirements, and specified voice tone.
    """
    TONES = ["Professional", "Friendly", "Formal", "Bold"]

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()

    def generate(
        self,
        candidate_data: Dict[str, Any],
        job_title: str,
        company_name: str,
        job_requirements: Optional[list] = None,
        tone: str = "Professional"
    ) -> Dict[str, Any]:
        """
        Generates customized cover letter.
        Supports Professional, Friendly, Formal, and Bold styles.
        """
        if tone not in self.TONES:
            tone = "Professional"

        cand_name = candidate_data.get("name", "Dharanidharan D")
        cand_title = candidate_data.get("title", "Full Stack AI Engineer")
        req_list = job_requirements or ["Python", "FastAPI", "TypeScript", "Autonomous Agents", "Stagehand"]
        top_skills_str = ", ".join(req_list[:3])

        if tone == "Professional":
            letter = f"""Dear Hiring Team at {company_name},

I am writing to express my strong interest in the {job_title} role. As a {cand_title} with deep specialization in autonomous agent architectures, Stagehand browser automation, and high-throughput FastAPI systems, I have spent the past two years building reliable software that bridges foundation models with production environments.

In my recent work architecting SIVI—an autonomous browser agent—I engineered self-healing locators, token-level streaming reasoning over WebSockets, and strict Human-in-the-Loop (HITL) safety gates that compressed multi-hour workflows down to under three minutes with 99.4% locator accuracy. These challenges closely align with {company_name}'s focus on {top_skills_str}.

I thrive on solving edge-case resilience and building responsive user-centric products. I would welcome the opportunity to discuss how my hands-on background in agentic workflows and full-stack engineering can drive measurable impact for your engineering team.

Thank you for your time and consideration.

Sincerely,
{cand_name}
{candidate_data.get('email', 'dharanidharan.ai@example.com')} | {candidate_data.get('phone', '+1 (555) 234-8901')}
{candidate_data.get('linkedin', 'https://linkedin.com/in/dharanidharan-ai')}"""

        elif tone == "Friendly":
            letter = f"""Hi {company_name} Team!

I've been closely following what you're building at {company_name}, and when I saw the opening for {job_title}, I knew I had to reach out!

I'm {cand_name}, an engineer who loves turning complex AI research into delightful, fast products people use every day. Lately, I've been heads-down building SIVI, an autonomous web agent using Stagehand, Claude 3.5 Sonnet, and MCP. Working on real-time browser telemetry, resilient automation, and safety guardrails has been one of the most rewarding challenges of my career.

Your mission around {top_skills_str} resonates with me deeply, and I'd love to bring this high energy and curiosity to your team. Whether it's pairing on async system architecture or brainstorming next-gen interfaces, count me in!

Looking forward to chatting with the team!

Warm regards,
{cand_name}
{candidate_data.get('email', 'dharanidharan.ai@example.com')}"""

        elif tone == "Formal":
            letter = f"""To the Members of the Selection Committee, {company_name}:

Please accept this letter and the enclosed resume as my formal application for the position of {job_title}.

With an academic foundation in Artificial Intelligence & Data Science and substantive experience developing autonomous software agents, I offer proven competence in {top_skills_str}. My technical portfolio includes the architectural design and deployment of SIVI, wherein I implemented Model Context Protocol (MCP) data bridges, Stagehand browser primitives, and deterministic Human-in-the-Loop oversight protocols.

My objective is to contribute rigorous engineering discipline, robust system reliability, and proactive problem-solving to {company_name}'s technical roadmap. I welcome the opportunity for an interview to present my qualifications in greater detail.

Respectfully submitted,
{cand_name}
{candidate_data.get('title', 'Full Stack AI Engineer')}"""

        else: # Bold / High-Impact
            letter = f"""To the Engineering Leaders at {company_name}:

Most candidates will tell you they understand autonomous systems. I built one from scratch that operates in the wild.

I am applying for the {job_title} role at {company_name} because you are tackling hard problems that require conviction and speed. As creator of SIVI, I took complex browser automation, real-time LLM reasoning streaming, and MCP file extraction, and reduced 3-hour manual application workflows to 2.5 minutes with 99.4% locator accuracy and zero safety compromises.

If {company_name} wants an engineer who writes production-grade Python and TypeScript, ships agentic workflows that don't break in production, and moves with relentless urgency, let's talk this week.

Best,
{cand_name}
{candidate_data.get('github', 'https://github.com/dharanidharan-dev')} | {candidate_data.get('linkedin', 'https://linkedin.com/in/dharanidharan-ai')}"""

        word_count = len(letter.split())
        return {
            "tone": tone,
            "job_title": job_title,
            "company_name": company_name,
            "letter_text": letter.strip(),
            "word_count": word_count,
            "estimated_read_time": f"{round(word_count / 200, 1)} min"
        }

cover_letter_generator = CoverLetterGenerator()
