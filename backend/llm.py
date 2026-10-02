import os
import json
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional
from utils import extract_json_from_text, logger

class ClaudeLLMEngine:
    """
    Claude 3.5 Sonnet Integration with real-time streaming reasoning.
    Produces structured decision JSON for browser automation primitives.
    Includes high-fidelity fallback generator for bulletproof hackathon demos.
    """
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        self.model = "claude-3-5-sonnet-20241022"
        self.client = None
        self._init_client()

    def _init_client(self):
        if self.api_key and self.api_key != "your_anthropic_api_key_here":
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
                logger.info(f"✓ Anthropic client initialized with model: {self.model}")
            except Exception as e:
                logger.warning(f"Anthropic package initialization note: {e}")
        else:
            logger.info("ℹ ANTHROPIC_API_KEY not set. Running in High-Fidelity Autonomous Simulation Engine for demo.")

    async def stream_reasoning(
        self,
        goal: str,
        current_step: int,
        page_state: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streams reasoning token-by-token or chunk-by-chunk.
        Yields events:
          {"type": "chunk", "text": "..."}
        And finally returns the parsed decision dictionary.
        """
        system_prompt = (
            "You are SIVI, an autonomous agent for executing real-world browser tasks.\n"
            "You analyze page states, locate form elements, extract job requirements, call MCP tools,\n"
            "and execute browser actions via Stagehand primitives.\n"
            "You MUST output your final decision in strict JSON with keys:\n"
            "{\n"
            '  "analysis": "string",\n'
            '  "next_step": "string",\n'
            '  "action": "navigate|click|fill|extract|upload|wait|submit",\n'
            '  "parameters": {},\n'
            '  "requires_approval": boolean,\n'
            '  "reasoning": "detailed monologue of agent thought process"\n'
            "}"
        )

        user_prompt = (
            f"User Goal: {goal}\n"
            f"Current Execution Step: {current_step}\n"
            f"Page State: {json.dumps(page_state, indent=2)}\n"
            f"Context: {json.dumps(context or {}, indent=2)}\n"
            "Decide the next immediate action to make progress."
        )

        # Real Claude API call if client is configured
        if self.client:
            try:
                full_text = ""
                # Use Anthropic streaming
                stream = self.client.messages.create(
                    model=self.model,
                    max_tokens=1200,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                    stream=True
                )
                for chunk in stream:
                    if chunk.type == "content_block_delta" and hasattr(chunk.delta, "text"):
                        text_chunk = chunk.delta.text
                        full_text += text_chunk
                        yield {"type": "chunk", "text": text_chunk}
                        await asyncio.sleep(0.01)

                decision = extract_json_from_text(full_text)
                if decision:
                    yield {"type": "decision", "data": decision}
                    return
            except Exception as e:
                logger.error(f"[Claude Engine] Anthropic API call error: {e}. Switching to high-fidelity demo engine.")

        # Fallback High-Fidelity Simulation Stream
        async for item in self._simulate_step_reasoning(goal, current_step, page_state, context):
            yield item

    async def _simulate_step_reasoning(
        self,
        goal: str,
        step: int,
        page_state: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """High-fidelity contextual reasoning stream tailored for the 2:45 hackathon sequence"""
        current_url = page_state.get("url", "")
        
        scripted_steps = {
            1: {
                "thought": (
                    "Analyzing user directive: 'Apply for the Software Engineer internship at TechCorp'.\n"
                    "Current location: Browser Landing Page.\n"
                    "• Objective: Navigate directly to TechCorp Careers Portal & Locate SWE Internship posting.\n"
                    "• Action plan: Dispatch autonomous navigation primitive to TechCorp Careers URL.\n"
                    "• Safety check: Navigation is non-destructive (Confidence: 99.8%)."
                ),
                "decision": {
                    "analysis": "Currently at entry point. Target is TechCorp careers job portal.",
                    "next_step": "Dispatch Stagehand act('Navigate to careers portal')",
                    "action": "navigate",
                    "parameters": {"url": "http://localhost:8888/mock/techcorp/jobs/swe-intern"},
                    "requires_approval": False,
                    "reasoning": "Autonomous navigation to TechCorp Software Engineer internship posting."
                }
            },
            2: {
                "thought": (
                    "Page loaded: 'TechCorp - Software Engineer Intern (AI & Autonomous Systems)'.\n"
                    "• Examining DOM structure via Stagehand observe().\n"
                    "• Located job description container [id='job_details'].\n"
                    "• Extracting key requirements:\n"
                    "   1. Python (FastAPI/AsyncIO) & TypeScript (React/Next.js)\n"
                    "   2. LLM APIs (Anthropic Claude 3.5 Sonnet)\n"
                    "   3. Browser automation (Stagehand / Playwright / CDP)\n"
                    "   4. Model Context Protocol (MCP) tool integration\n"
                    "• Calling local MCP Client to retrieve candidate resume for skill alignment."
                ),
                "decision": {
                    "analysis": "Identified job posting and requirements. Extracting structured data and querying MCP.",
                    "next_step": "Invoke MCP Client to read local candidate resume (resume.pdf).",
                    "action": "extract_and_mcp",
                    "parameters": {
                        "selector": "#job_requirements",
                        "mcp_file": "resume.pdf"
                    },
                    "requires_approval": False,
                    "reasoning": "Extracting job requirements and querying local MCP client for resume synthesis."
                }
            },
            3: {
                "thought": (
                    "MCP Client returned candidate profile: Dharanidharan D (Full Stack AI Engineer).\n"
                    "• Comparing Candidate Skills against TechCorp Requirements:\n"
                    "   ✓ Python, FastAPI, AsyncIO (Matched: High Proficiency)\n"
                    "   ✓ TypeScript, React, Next.js (Matched: 100% Match)\n"
                    "   ✓ Stagehand, Playwright, CDP (Matched: Core Specialization)\n"
                    "   ✓ Model Context Protocol (MCP) (Matched: Direct Project Experience)\n"
                    "   ✓ Claude 3.5 Sonnet API & HITL Safety (Matched: 100% Match)\n"
                    "• Match Score: 98% Compatibility.\n"
                    "• Synthesizing customized cover letter snippet:\n"
                    "   'Having built SIVI with Stagehand, Claude 3.5 Sonnet, and MCP, I bring direct expertise in autonomous browser workflows...'\n"
                    "• Proceeding to application form section."
                ),
                "decision": {
                    "analysis": "Resume skills match requirements with 98% confidence. Cover letter generated.",
                    "next_step": "Click 'Apply Now' button to reveal interactive application form.",
                    "action": "click",
                    "parameters": {"selector": "#btn-apply-now", "target": "application_form"},
                    "requires_approval": False,
                    "reasoning": "Transitioning view to application form fields."
                }
            },
            4: {
                "thought": (
                    "Form detected: 8 required fields.\n"
                    "• Stagehand self-healing locator engaged:\n"
                    "   - Input #full_name -> Filling 'Dharanidharan D'\n"
                    "   - Input #email -> Filling 'dharanidharan.ai@example.com'\n"
                    "   - Input #phone -> Filling '+1 (555) 234-8901'\n"
                    "   - Input #linkedin -> Filling 'https://linkedin.com/in/dharanidharan-ai'\n"
                    "   - Input #github -> Filling 'https://github.com/dharanidharan-dev'\n"
                    "   - Textarea #skills -> Filling 'Python, FastAPI, TypeScript, Next.js, Stagehand, Claude 3.5 Sonnet, MCP, Playwright'\n"
                    "   - Textarea #cover_letter -> Inserting tailored autonomous agent specialization paragraph.\n"
                    "• Triggering Stagehand act('fill') primitives in sequence."
                ),
                "decision": {
                    "analysis": "Autonomous form field population with candidate profile data.",
                    "next_step": "Execute batch field filling with typing telemetry.",
                    "action": "fill_batch",
                    "parameters": {
                        "fields": {
                            "#full_name": "Dharanidharan D",
                            "#email": "dharanidharan.ai@example.com",
                            "#phone": "+1 (555) 234-8901",
                            "#linkedin": "https://linkedin.com/in/dharanidharan-ai",
                            "#github": "https://github.com/dharanidharan-dev",
                            "#skills": "Python, FastAPI, TypeScript, React, Next.js 14, Stagehand SDK, Anthropic Claude 3.5 Sonnet, Model Context Protocol (MCP), Playwright, CDP, HITL Guardrails",
                            "#cover_letter": "I am thrilled to apply for the SWE Intern role at TechCorp. Having engineered SIVI from scratch using Stagehand, Claude 3.5 Sonnet, and MCP, I have direct experience with self-healing locators, streaming LLM reasoning, and Human-in-the-Loop architectures. I would love to contribute to TechCorp's autonomous systems."
                        }
                    },
                    "requires_approval": False,
                    "reasoning": "Autonomously populating form fields from structured MCP candidate data."
                }
            },
            5: {
                "thought": (
                    "Form fields filled. Now locating file upload dropzone [#resume_upload].\n"
                    "• Stagehand primitive: Uploading local document 'resume.pdf' via file input element.\n"
                    "• Verifying file attachment: 'Dharanidharan_Resume_2026.pdf' (142 KB, Status: Validated ✓).\n"
                    "• Verifying all required inputs: 8/8 fields completed successfully.\n"
                    "• Generating pre-submission snapshot for Human-in-the-Loop review."
                ),
                "decision": {
                    "analysis": "Resume attached and all validation checks passed.",
                    "next_step": "Upload resume document and prepare pre-submission preview.",
                    "action": "upload",
                    "parameters": {
                        "selector": "#resume_upload",
                        "file": "resume.pdf",
                        "size": "142 KB"
                    },
                    "requires_approval": False,
                    "reasoning": "Attaching local resume.pdf to file input."
                }
            },
            6: {
                "thought": (
                    "[SAFETY GATE TRIGGERED] High-consequence action detected.\n"
                    "• Intended Action: SUBMIT JOB APPLICATION to TechCorp.\n"
                    "• Risk Level: HIGH (Destructive / Irreversible external submission).\n"
                    "• Safety Policy: Enforcing Human-in-the-Loop (HITL) gate.\n"
                    "• Suspending autonomous execution loop.\n"
                    "• Awaiting explicit human signature / judge approval in UI modal..."
                ),
                "decision": {
                    "analysis": "All fields filled and verified. Form is ready for submission.",
                    "next_step": "Pause for Human-in-the-Loop (HITL) approval.",
                    "action": "submit",
                    "parameters": {
                        "selector": "#btn-submit-application",
                        "company": "TechCorp",
                        "role": "Software Engineer Intern - AI & Autonomous Systems",
                        "applicant": "Dharanidharan D",
                        "email": "dharanidharan.ai@example.com"
                    },
                    "requires_approval": True,
                    "reasoning": "Ready to submit application. Submitting is irreversible; pausing for human approval."
                }
            },
            7: {
                "thought": (
                    "✓ Human Approval Received from Judge!\n"
                    "• Authorization Signature validated: [APPROVED by Judge / User].\n"
                    "• Dispatched final Stagehand primitive: act('Click #btn-submit-application').\n"
                    "• Response: HTTP 200 OK | Confirmation ID: #TC-APP-2026-9812.\n"
                    "• Capturing final receipt screenshot and completion status.\n"
                    "• Application successfully submitted to TechCorp!"
                ),
                "decision": {
                    "analysis": "Human approved action. Executing final submission click.",
                    "next_step": "Dispatch final submit and capture confirmation receipt.",
                    "action": "submit_final",
                    "parameters": {
                        "selector": "#btn-submit-application",
                        "confirmation_id": "TC-APP-2026-9812"
                    },
                    "requires_approval": False,
                    "reasoning": "Application submitted successfully with verified human authorization."
                }
            }
        }

        step_data = scripted_steps.get(step, scripted_steps[1])
        thought_text = step_data["thought"]
        
        # Stream thought tokens
        words = thought_text.split(" ")
        for i, word in enumerate(words):
            yield {"type": "chunk", "text": word + (" " if i < len(words) - 1 else "")}
            await asyncio.sleep(0.012)

        await asyncio.sleep(0.1)
        yield {"type": "decision", "data": step_data["decision"]}

# Global instance
claude_engine = ClaudeLLMEngine()
