import os
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

class ApplicationStore:
    """
    Persistent Application Tracking Store.
    Manages submitted job applications, status transitions, interview schedules,
    and event timelines. Persists to disk at data/applications.json.
    """
    def __init__(self, data_file: Optional[str] = None):
        self.data_file = data_file or os.path.join(
            os.path.dirname(__file__), "..", "data", "applications.json"
        )
        self.applications: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        """Loads applications from file or seeds initial sample data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.applications = {item["id"]: item for item in data}
                    return
            except Exception as e:
                print(f"[ApplicationStore] Error loading applications: {e}")

        # Seed realistic initial applications
        self._seed_initial_applications()
        self._save()

    def _save(self):
        """Saves applications to disk"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(list(self.applications.values()), f, indent=2)
        except Exception as e:
            print(f"[ApplicationStore] Error saving applications: {e}")

    def _seed_initial_applications(self):
        """Seeds realistic historical applications across various statuses"""
        now = datetime.now(timezone.utc)
        
        seeds = [
            {
                "id": "app-techcorp-01",
                "company": "TechCorp",
                "role": "Software Engineer Intern - Autonomous Systems",
                "department": "Applied AI Engineering",
                "location": "San Francisco, CA (Hybrid)",
                "url": "http://localhost:8888/mock/techcorp/jobs/swe-intern",
                "status": "Interview",
                "applied_at": (now - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "updated_at": (now - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "match_score": 98.0,
                "notes": "System architecture interview with Director of Autonomous Agents scheduled.",
                "interview": {
                    "scheduled": True,
                    "date": (now + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "time": "14:00 PST",
                    "round": "Technical Deep Dive & Live Agent Architecture",
                    "interviewer": "Dr. Sarah Chen (Head of AI Systems)",
                    "meet_url": "https://meet.google.com/tc-sivi-arch"
                },
                "timeline": [
                    {
                        "date": (now - timedelta(days=3)).strftime("%b %d, %H:%M"),
                        "event": "Autonomous Application Submitted",
                        "details": "SIVI automated form completion and HITL safety gate approved.",
                        "type": "success"
                    },
                    {
                        "date": (now - timedelta(days=2)).strftime("%b %d, %H:%M"),
                        "event": "Application Reviewed",
                        "details": "Recruiter passed profile to AI Engineering team.",
                        "type": "info"
                    },
                    {
                        "date": (now - timedelta(hours=6)).strftime("%b %d, %H:%M"),
                        "event": "Interview Invitation",
                        "details": "Technical Deep Dive invitation sent via email.",
                        "type": "warning"
                    }
                ]
            },
            {
                "id": "app-anthropic-02",
                "company": "ScaleAI / Anthropic Partner",
                "role": "Full Stack AI Applications Engineer",
                "department": "Model Infrastructure",
                "location": "Remote / San Francisco",
                "url": "https://boards.greenhouse.io/scaleai/jobs/4819231",
                "status": "Reviewing",
                "applied_at": (now - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "updated_at": (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "match_score": 94.0,
                "notes": "Greenhouse ATS application completed. Resume parsed with 94% skills coverage.",
                "interview": None,
                "timeline": [
                    {
                        "date": (now - timedelta(days=5)).strftime("%b %d, %H:%M"),
                        "event": "Application Submitted",
                        "details": "Autonomous Greenhouse submission with tailored Claude cover letter.",
                        "type": "success"
                    },
                    {
                        "date": (now - timedelta(days=1)).strftime("%b %d, %H:%M"),
                        "event": "Profile Viewed by Hiring Manager",
                        "details": "LinkedIn and portfolio clicked 4 times from Mountain View, CA.",
                        "type": "info"
                    }
                ]
            },
            {
                "id": "app-stripe-03",
                "company": "Stripe",
                "role": "Frontend Platform Engineer (Design Systems)",
                "department": "Developer Experience",
                "location": "San Francisco, CA / Seattle, WA",
                "url": "https://stripe.com/jobs/frontend-platform",
                "status": "Applied",
                "applied_at": (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "updated_at": (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "match_score": 89.0,
                "notes": "Applied with custom cover letter highlighting Next.js 14 and real-time canvas UI.",
                "interview": None,
                "timeline": [
                    {
                        "date": (now - timedelta(days=1)).strftime("%b %d, %H:%M"),
                        "event": "Application Submitted",
                        "details": "Confirmation email #STR-APP-9021 received.",
                        "type": "success"
                    }
                ]
            },
            {
                "id": "app-datadog-04",
                "company": "Datadog",
                "role": "Software Engineer - Telemetry & Agents",
                "department": "Agent Runtime",
                "location": "New York, NY / Remote",
                "url": "https://datadoghq.com/careers/detail/?gh_jid=610923",
                "status": "Reviewing",
                "applied_at": (now - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "updated_at": (now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "match_score": 91.0,
                "notes": "Recruiter message received via LinkedIn acknowledging SIVI project repository.",
                "interview": None,
                "timeline": [
                    {
                        "date": (now - timedelta(days=7)).strftime("%b %d, %H:%M"),
                        "event": "Application Submitted",
                        "details": "Direct portal upload.",
                        "type": "success"
                    },
                    {
                        "date": (now - timedelta(days=2)).strftime("%b %d, %H:%M"),
                        "event": "Recruiter Screen Outreach",
                        "details": "Message: 'Impressive Stagehand and MCP open source work!'",
                        "type": "info"
                    }
                ]
            },
            {
                "id": "app-cloudscale-05",
                "company": "CloudScale Systems",
                "role": "Lead Cloud Infrastructure Architect",
                "department": "Cloud Platforms",
                "location": "Austin, TX (Remote)",
                "url": "https://cloudscale.example.com/careers/cloud-architect",
                "status": "Offer",
                "applied_at": (now - timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "updated_at": (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "match_score": 96.0,
                "notes": "Offer letter received! Base: $145,000 + Equity + Sign-on bonus.",
                "interview": {
                    "scheduled": False,
                    "date": "Completed",
                    "time": "--",
                    "round": "Final Executive Offer Review",
                    "interviewer": "VP of Engineering",
                    "meet_url": ""
                },
                "timeline": [
                    {
                        "date": (now - timedelta(days=14)).strftime("%b %d, %H:%M"),
                        "event": "Application Submitted",
                        "details": "Batch mode application.",
                        "type": "success"
                    },
                    {
                        "date": (now - timedelta(days=8)).strftime("%b %d, %H:%M"),
                        "event": "Technical Interview Cleared",
                        "details": "Score: 10/10 on Distributed Systems & Autonomous Agents.",
                        "type": "info"
                    },
                    {
                        "date": (now - timedelta(days=1)).strftime("%b %d, %H:%M"),
                        "event": "Formal Offer Extended",
                        "details": "Official written offer dispatched via DocuSign.",
                        "type": "success"
                    }
                ]
            }
        ]
        self.applications = {item["id"]: item for item in seeds}

    def list_all(self, status: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns sorted list of applications with optional status and text filters"""
        items = list(self.applications.values())
        if status and status.lower() != "all":
            items = [item for item in items if item.get("status", "").lower() == status.lower()]
        
        if search:
            q = search.lower()
            items = [
                item for item in items
                if q in item.get("company", "").lower() or q in item.get("role", "").lower()
            ]

        # Sort descending by applied_at
        items.sort(key=lambda x: x.get("applied_at", ""), reverse=True)
        return items

    def get_by_id(self, app_id: str) -> Optional[Dict[str, Any]]:
        """Returns single application by ID"""
        return self.applications.get(app_id)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates new application entry from autonomous agent or manual input"""
        now = datetime.now(timezone.utc)
        app_id = data.get("id") or f"app-{uuid.uuid4().hex[:8]}"
        new_app = {
            "id": app_id,
            "company": data.get("company", "Target Company"),
            "role": data.get("role", "Software Engineer"),
            "department": data.get("department", "Engineering"),
            "location": data.get("location", "Remote / Hybrid"),
            "url": data.get("url", ""),
            "status": data.get("status", "Applied"),
            "applied_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "updated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "match_score": data.get("match_score", 95.0),
            "notes": data.get("notes", "Submitted autonomously via SIVI Agent."),
            "interview": data.get("interview"),
            "timeline": data.get("timeline") or [
                {
                    "date": now.strftime("%b %d, %H:%M"),
                    "event": "Autonomous Application Submitted",
                    "details": f"Successfully submitted to {data.get('company')} via SIVI Stagehand workflow.",
                    "type": "success"
                }
            ],
            "submitted_payload": data.get("submitted_payload", {})
        }
        self.applications[app_id] = new_app
        self._save()
        return new_app

    def update(self, app_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Updates existing application entry"""
        if app_id not in self.applications:
            return None
        
        app = self.applications[app_id]
        for k, v in updates.items():
            if k not in ["id", "applied_at"]:
                app[k] = v
        app["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        self._save()
        return app

    def schedule_interview(
        self,
        app_id: str,
        date: str,
        time: str,
        round_name: str = "Technical Interview",
        interviewer: str = "Hiring Team",
        meet_url: str = "https://meet.google.com/new"
    ) -> Optional[Dict[str, Any]]:
        """Schedules or updates an interview for an application"""
        if app_id not in self.applications:
            return None
        
        app = self.applications[app_id]
        app["status"] = "Interview"
        app["interview"] = {
            "scheduled": True,
            "date": date,
            "time": time,
            "round": round_name,
            "interviewer": interviewer,
            "meet_url": meet_url
        }
        now = datetime.now(timezone.utc)
        app["timeline"].append({
            "date": now.strftime("%b %d, %H:%M"),
            "event": f"Interview Scheduled: {round_name}",
            "details": f"Date: {date} at {time} with {interviewer}.",
            "type": "warning"
        })
        app["updated_at"] = now.strftime("%Y-%m-%d %H:%M:%S UTC")
        self._save()
        return app

    def delete(self, app_id: str) -> bool:
        """Removes application entry"""
        if app_id in self.applications:
            del self.applications[app_id]
            self._save()
            return True
        return False

app_store = ApplicationStore()
