import os
from typing import Dict, Any, List, Optional
from mcp_client import mcp_client
from ml.skills_matcher import smart_matcher
from bhuvan_service import bhuvan_service
from utils import logger

# Curated List of Official Tech Internships & Fellowships
# Preserved strictly: MeitY, ISRO SAC, NIC, DRDO CAIR, and AICTE
CURATED_UNSTOP_INTERNSHIPS: List[Dict[str, Any]] = [
    {
        "id": "gov-meity-genai-fellow-2026",
        "company": "MeitY (Digital India Bhashini AI Mission)",
        "organization": "MeitY (Digital India Bhashini AI Mission)",
        "ministry": "Ministry of Electronics and Information Technology",
        "title": "Generative AI & Indic Language Model Fellow",
        "program": "Digital India Bhashini AI Mission",
        "category": "AI / Machine Learning",
        "location": "New Delhi / Remote",
        "mode": "Hybrid",
        "stipend": "₹60,000 / month",
        "duration": "6 - 12 Months",
        "deadline": "2026-11-10",
        "applicants_count": 890,
        "portal_type": "unstop",
        "url": "http://localhost:8888/mock/unstop/internships/gov-meity-genai-fellow-2026",
        "source": "data.gov.in / National Portal",
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
        "company": "ISRO SAC (Space Applications Centre)",
        "organization": "ISRO SAC (Space Applications Centre)",
        "ministry": "Department of Space, Government of India",
        "title": "Satellite Imagery & Geospatial Deep Learning Intern",
        "program": "ISRO Bhuvan & EOS Geospatial AI Initiative",
        "category": "Computer Vision / Geospatial",
        "location": "Ahmedabad / Bengaluru",
        "mode": "On-site",
        "stipend": "₹45,000 / month",
        "duration": "6 Months",
        "deadline": "2026-11-05",
        "applicants_count": 1340,
        "portal_type": "unstop",
        "url": "http://localhost:8888/mock/unstop/internships/gov-isro-sac-geospatial-2026",
        "source": "data.gov.in / ISRO SAC",
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
        "company": "NIC (National Informatics Centre)",
        "organization": "NIC (National Informatics Centre)",
        "ministry": "Ministry of Electronics and Information Technology",
        "title": "GovCloud Systems & Distributed Systems Intern",
        "program": "NIC GovCloud National Internship 2026",
        "category": "Full Stack / Cloud",
        "location": "New Delhi / Hyderabad",
        "mode": "Hybrid",
        "stipend": "₹40,000 / month",
        "duration": "6 Months",
        "deadline": "2026-11-12",
        "applicants_count": 1120,
        "portal_type": "unstop",
        "url": "http://localhost:8888/mock/unstop/internships/gov-nic-digital-india-2026",
        "source": "data.gov.in / NIC",
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
        "company": "DRDO CAIR",
        "organization": "DRDO CAIR",
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
        "portal_type": "unstop",
        "url": "http://localhost:8888/mock/unstop/internships/gov-drdo-robotics-2026",
        "source": "data.gov.in / DRDO CAIR",
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
        "company": "AICTE (National Internship Portal)",
        "organization": "AICTE (National Internship Portal)",
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
        "portal_type": "unstop",
        "url": "http://localhost:8888/mock/unstop/internships/gov-aicte-tech-intern-2026",
        "source": "data.gov.in / AICTE",
        "qualifications": "B.Tech / B.Sc / BCA in Computer Science, Data Science, or related disciplines. AICTE accredited institutions eligible.",
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

class UnstopService:
    """
    Service managing internship search, filtering, ISRO Bhuvan commute viability,
    and qualifications-based smart matching for the 5 curated technical fellowships.
    """
    def __init__(self):
        self.internships: List[Dict[str, Any]] = CURATED_UNSTOP_INTERNSHIPS
        logger.info(f"[UnstopService] Initialized with {len(self.internships)} curated technical fellowships")

    def search_internships(
        self,
        query: str = "",
        category: Optional[str] = None,
        mode: Optional[str] = None,
        include_govt: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Searches the 5 curated technical internships by keyword, category, or mode
        and calculates match scores against the candidate's MCP qualifications,
        enriched with ISRO Bhuvan commute viability analysis.
        """
        query_clean = query.strip().lower()
        candidate = mcp_client.get_candidate_profile()
        cand_loc = candidate.get("location", "Bengaluru, Karnataka")

        results = []
        for item in self.internships:
            # Category filter
            if category and category.lower() != "all":
                if category.lower() not in item["category"].lower():
                    continue

            # Mode filter (Remote, Hybrid, On-site)
            if mode and mode.lower() != "all":
                if mode.lower() not in item["mode"].lower():
                    continue

            # Query filter (matches company, organization, title, requirements, location, description)
            if query_clean:
                searchable_text = f"{item['company']} {item['title']} {item['category']} {item['location']} {item['qualifications']} {item['description']} {' '.join(item['requirements'])}".lower()
                if query_clean not in searchable_text:
                    tokens = query_clean.split()
                    if not any(token in searchable_text for token in tokens):
                        continue

            # Calculate match score against candidate's stored qualifications and skills
            match_res = smart_matcher.match_resume_to_job(candidate, {
                "title": item["title"],
                "company": item["company"],
                "requirements": item["requirements"]
            })

            # Calculate ISRO Bhuvan Commute Accessibility
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
            results.append(item_copy)

        # Sort by match score descending
        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        return results

    def get_internship_by_id(self, internship_id: str) -> Optional[Dict[str, Any]]:
        """Finds specific internship by ID"""
        for item in self.internships:
            if item["id"] == internship_id:
                candidate = mcp_client.get_candidate_profile()
                cand_loc = candidate.get("location", "Bengaluru, Karnataka")

                match_res = smart_matcher.match_resume_to_job(candidate, {
                    "title": item["title"],
                    "company": item["company"],
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
                return item_copy
        return None

unstop_service = UnstopService()
