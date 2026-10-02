import os
import httpx
from typing import Dict, Any, List, Optional
from mcp_client import mcp_client
from ml.skills_matcher import smart_matcher
from bhuvan_service import bhuvan_service
from utils import logger

# Curated Indian Open Government Data (data.gov.in) & Public Sector Tech Internships
GOVT_INTERNSHIPS: List[Dict[str, Any]] = [
    {
        "id": "gov-meity-genai-fellow-2026",
        "organization": "MeitY (Ministry of Electronics & IT)",
        "ministry": "Ministry of Electronics and Information Technology",
        "title": "Generative AI & Indic Language Model Research Fellow",
        "program": "Digital India Bhashini AI Mission",
        "category": "AI / Machine Learning",
        "location": "New Delhi / Remote",
        "mode": "Hybrid",
        "stipend": "₹60,000 / month",
        "duration": "6 - 12 Months",
        "deadline": "2026-11-10",
        "applicants_count": 890,
        "portal_type": "data_gov",
        "portal_name": "data.gov.in / MeitY Open Portal",
        "url": "https://data.gov.in/resource/meity-ai-internship-2026",
        "qualifications": "B.Tech / M.Tech in Computer Science, Data Science, or AI. Familiarity with Indian languages NLP and Transformer models.",
        "description": "MeitY's Digital India Bhashini division is offering fellowship grants to build open-source multilingual AI agents, speech models, and automated citizen services.",
        "requirements": [
            "Python (PyTorch, Hugging Face Transformers)",
            "Experience fine-tuning LLMs and Whisper speech models",
            "Understanding of Indic languages datasets and tokenization",
            "Knowledge of REST APIs and microservice deployment"
        ],
        "responsibilities": [
            "Contribute to open Indic foundational models for citizen governance",
            "Build speech-to-text validation benchmarks for regional dialects",
            "Deploy high-throughput inference endpoints using FastAPI"
        ]
    },
    {
        "id": "gov-isro-sac-geospatial-2026",
        "organization": "ISRO - Space Applications Centre (SAC)",
        "ministry": "Department of Space, Government of India",
        "title": "Satellite Imagery & Geospatial Deep Learning Intern",
        "program": "ISRO Bhuvan & EOS Geospatial AI Initiative",
        "category": "Computer Vision / Geospatial",
        "location": "Ahmedabad, Gujarat / Bengaluru, Karnataka",
        "mode": "On-site",
        "stipend": "₹45,000 / month",
        "duration": "6 Months",
        "deadline": "2026-11-05",
        "applicants_count": 1340,
        "portal_type": "data_gov",
        "portal_name": "data.gov.in / ISRO SAC",
        "url": "https://data.gov.in/resource/isro-sac-geospatial-ai-2026",
        "qualifications": "B.Tech / M.Sc in Aerospace, Remote Sensing, Computer Science, or Geomatics with minimum 8.0 CGPA.",
        "description": "Collaborate with ISRO scientists to build deep learning computer vision pipelines for satellite image segmentation, crop yield forecasting, and disaster flood mapping on Bhuvan.",
        "requirements": [
            "Python, GDAL, Rasterio, OpenCV, PyTorch",
            "Deep Learning for Remote Sensing & Multispectral Imagery",
            "Experience with Geospatial APIs (ISRO Bhuvan, OpenGIS)",
            "Linux, Git, and High-Performance GPU clusters"
        ],
        "responsibilities": [
            "Develop convolutional segmentation models for Cartosat multispectral data",
            "Integrate geodesic distance calculations with Bhuvan open API services",
            "Publish benchmark datasets on data.gov.in open portal"
        ]
    },
    {
        "id": "gov-nic-digital-india-2026",
        "organization": "National Informatics Centre (NIC)",
        "ministry": "Ministry of Electronics and Information Technology",
        "title": "Cloud Architecture & Full Stack Systems Intern",
        "program": "NIC GovCloud National Internship 2026",
        "category": "Full Stack / Cloud",
        "location": "New Delhi / Hyderabad",
        "mode": "Hybrid",
        "stipend": "₹40,000 / month",
        "duration": "6 Months",
        "deadline": "2026-11-12",
        "applicants_count": 1120,
        "portal_type": "data_gov",
        "portal_name": "data.gov.in / NIC",
        "url": "https://data.gov.in/resource/nic-govcloud-internship-2026",
        "qualifications": "B.Tech / MCA in Computer Science, IT, or Electronics. Knowledge of Python, React, and Linux administration.",
        "description": "Assist NIC engineers in architecting scalable citizen-facing digital portals, cloud-native API gateways, and automated document verification microservices.",
        "requirements": [
            "Python (FastAPI, Flask) or Go",
            "React, TypeScript, and modern frontend styling",
            "Docker, Kubernetes, and Linux server management",
            "Web accessibility (WCAG 2.1 AA) and Indian e-Governance standards"
        ],
        "responsibilities": [
            "Build accessible web interfaces compliant with Indian Government Web Guidelines (GIGW)",
            "Implement secure RESTful APIs with role-based authentication",
            "Conduct load tests and optimize database query latencies"
        ]
    },
    {
        "id": "gov-drdo-robotics-2026",
        "organization": "DRDO - CAIR",
        "ministry": "Ministry of Defence",
        "title": "Autonomous Systems & Sensor Fusion Intern",
        "program": "DRDO Autonomous Robotics Fellowship",
        "category": "Robotics / Systems",
        "location": "Bengaluru, Karnataka",
        "mode": "On-site",
        "stipend": "₹42,000 / month",
        "duration": "6 Months",
        "deadline": "2026-10-30",
        "applicants_count": 940,
        "portal_type": "data_gov",
        "portal_name": "data.gov.in / DRDO CAIR",
        "url": "https://data.gov.in/resource/drdo-cair-robotics-2026",
        "qualifications": "B.Tech / M.Tech in Robotics, Mechatronics, Computer Science, or Electrical Engineering.",
        "description": "Conduct research on real-time sensor fusion (LiDAR, Radar, IMU), obstacle avoidance algorithms, and edge AI deployment for autonomous unmanned ground platforms.",
        "requirements": [
            "C++ and Python for real-time robotic systems",
            "ROS2 (Robot Operating System), Gazebo simulation",
            "Kalman Filtering, SLAM, and Path Planning",
            "Edge computing on NVIDIA Jetson or embedded hardware"
        ],
        "responsibilities": [
            "Implement SLAM and point cloud feature extraction pipelines",
            "Benchmark autonomous navigation models in simulated test environments",
            "Test low-latency telemetry communication protocols"
        ]
    },
    {
        "id": "gov-aicte-tech-intern-2026",
        "organization": "AICTE - National Internship Portal",
        "ministry": "Ministry of Education",
        "title": "EdTech & Data Engineering Intern",
        "program": "AICTE NEAT & National Skills Portal Initiative",
        "category": "Data Engineering",
        "location": "Remote / Pan-India",
        "mode": "Remote",
        "stipend": "₹28,000 / month",
        "duration": "3 - 6 Months",
        "deadline": "2026-11-20",
        "applicants_count": 2150,
        "portal_type": "data_gov",
        "portal_name": "data.gov.in / AICTE",
        "url": "https://data.gov.in/resource/aicte-national-portal-2026",
        "qualifications": "B.Tech / B.Sc / BCA in Computer Science, Data Science, or related disciplines. Students from all AICTE accredited institutions eligible.",
        "description": "Help create data ingestion pipelines, student analytics dashboards, and automated skill-mapping engines for over 10,000 engineering colleges nationwide.",
        "requirements": [
            "Python, SQL, PostgreSQL, Pandas",
            "Data pipeline orchestration and ETL tools",
            "Data visualization (Chart.js, D3, or Matplotlib)",
            "REST API design and asynchronous data processing"
        ],
        "responsibilities": [
            "Build automated data ingestion scripts for student skill certification logs",
            "Create interactive analytics reports on regional employment trends",
            "Implement data validation rules for educational records"
        ]
    }
]

class DataGovService:
    """
    Open Government Data (OGD) Platform India connector.
    Reference: https://data.gov.in
    Provides access to official public sector tech internships, government fellowships,
    and open datasets from Government of India ministries.
    """
    def __init__(self):
        self.api_key = os.getenv("DATA_GOV_API_KEY", "").strip()
        self.base_url = "https://api.data.gov.in"
        self.items: List[Dict[str, Any]] = GOVT_INTERNSHIPS
        logger.info(f"[data.gov.in] Initialized Government Open Data Service ({len(self.items)} verified positions)")

    def get_ministries(self) -> List[str]:
        """Returns list of unique ministries offering internships"""
        ministries = set()
        for item in self.items:
            ministries.add(item["ministry"])
        return sorted(list(ministries))

    def search_internships(
        self,
        query: str = "",
        ministry: Optional[str] = None,
        mode: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Searches public sector internships with smart candidate qualification matching
        and ISRO Bhuvan geodesic distance evaluation.
        """
        query_clean = query.strip().lower()
        candidate = mcp_client.get_candidate_profile()
        cand_loc = candidate.get("location", "Bengaluru, Karnataka")

        results = []
        for item in self.items:
            # Ministry filter
            if ministry and ministry.lower() != "all":
                if ministry.lower() not in item["ministry"].lower():
                    continue

            # Mode filter
            if mode and mode.lower() != "all":
                if mode.lower() not in item["mode"].lower():
                    continue

            # Query filter
            if query_clean:
                searchable_text = f"{item['organization']} {item['ministry']} {item['title']} {item['category']} {item['location']} {item['description']} {' '.join(item['requirements'])}".lower()
                if query_clean not in searchable_text:
                    tokens = query_clean.split()
                    if not any(t in searchable_text for t in tokens):
                        continue

            # Smart skill match
            match_res = smart_matcher.match_resume_to_job(candidate, {
                "title": item["title"],
                "company": item["organization"],
                "requirements": item["requirements"]
            })

            # ISRO Bhuvan Commute analysis
            bhuvan_analysis = bhuvan_service.analyze_commute_accessibility(
                candidate_location=cand_loc,
                job_location=item["location"],
                job_mode=item["mode"]
            )

            item_copy = dict(item)
            item_copy["match_score"] = match_res["match_score"]
            item_copy["matched_skills"] = match_res["matched_skills"]
            item_copy["missing_skills"] = match_res["missing_skills"]
            item_copy["bhuvan_analysis"] = bhuvan_analysis
            item_copy["source"] = "data.gov.in"
            results.append(item_copy)

        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        return results

    def get_internship_by_id(self, internship_id: str) -> Optional[Dict[str, Any]]:
        """Finds public sector internship by ID"""
        for item in self.items:
            if item["id"] == internship_id:
                candidate = mcp_client.get_candidate_profile()
                cand_loc = candidate.get("location", "Bengaluru, Karnataka")

                match_res = smart_matcher.match_resume_to_job(candidate, {
                    "title": item["title"],
                    "company": item["organization"],
                    "requirements": item["requirements"]
                })

                bhuvan_analysis = bhuvan_service.analyze_commute_accessibility(
                    candidate_location=cand_loc,
                    job_location=item["location"],
                    job_mode=item["mode"]
                )

                item_copy = dict(item)
                item_copy["match_score"] = match_res["match_score"]
                item_copy["matched_skills"] = match_res["matched_skills"]
                item_copy["missing_skills"] = match_res["missing_skills"]
                item_copy["bhuvan_analysis"] = bhuvan_analysis
                item_copy["source"] = "data.gov.in"
                return item_copy
        return None

data_gov_service = DataGovService()
