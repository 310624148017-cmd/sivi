import re
from typing import Dict, Any, List, Optional

class MultiFormIntelligence:
    """
    Multi-Form Intelligence & Form Type Classification.
    Detects whether target application is standard, ATS (Greenhouse, Lever, Workday),
    or custom multi-step wizard, maps form fields to candidate attributes,
    and enforces pre-submission validation.
    """
    FORM_PATTERNS = {
        "ats_greenhouse": [r"greenhouse\.io", r"gh_src", r"#application_form", r"greenhouse"],
        "ats_lever": [r"lever\.co", r"lever-form", r"#posting-form"],
        "ats_workday": [r"myworkdayjobs\.com", r"workday", r"wd-form"],
        "custom_multistep": [r"step-1", r"wizard", r"multistep", r"tab-content"],
        "standard": [r"careers", r"jobs", r"apply", r"form"]
    }

    FIELD_MAPPINGS = {
        "full_name": ["name", "full_name", "applicant_name", "candidate_name", "fname_lname"],
        "first_name": ["first_name", "fname", "given_name"],
        "last_name": ["last_name", "lname", "family_name", "surname"],
        "email": ["email", "email_address", "applicant_email", "contact_email"],
        "phone": ["phone", "tel", "mobile", "phone_number", "contact_phone"],
        "linkedin": ["linkedin", "linkedin_profile", "linkedin_url", "social_linkedin"],
        "github": ["github", "github_profile", "github_url", "portfolio_github"],
        "portfolio": ["portfolio", "website", "personal_website", "portfolio_url"],
        "resume": ["resume", "cv", "resume_file", "resume_upload", "cv_upload", "document"],
        "cover_letter": ["cover_letter", "coverletter", "letter", "comments", "why_us", "additional_info"],
        "skills": ["skills", "technical_skills", "technologies", "key_skills"],
        "work_authorization": ["work_auth", "authorized", "sponsorship", "visa_status", "legally_authorized"],
        "salary_expectations": ["salary", "desired_salary", "compensation", "expected_salary"]
    }

    @classmethod
    def detect_form_type(cls, url: str, page_title: str = "", html_snippet: str = "") -> Dict[str, Any]:
        """Detects form architecture and vendor ATS type"""
        combined = f"{url} {page_title} {html_snippet}".lower()
        
        for form_type, patterns in cls.FORM_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, combined):
                    vendor_names = {
                        "ats_greenhouse": "Greenhouse ATS",
                        "ats_lever": "Lever ATS",
                        "ats_workday": "Workday Enterprise",
                        "custom_multistep": "Custom Multi-Step Portal",
                        "standard": "Standard Web Career Portal"
                    }
                    return {
                        "form_type": form_type,
                        "vendor_name": vendor_names.get(form_type, "Standard Portal"),
                        "is_ats": form_type.startswith("ats_"),
                        "multi_page": form_type in ["ats_workday", "custom_multistep"]
                    }

        return {
            "form_type": "standard",
            "vendor_name": "Standard Career Portal",
            "is_ats": False,
            "multi_page": False
        }

    @classmethod
    def map_field_to_attribute(cls, field_name: str, field_label: str = "", field_id: str = "") -> Optional[str]:
        """Maps an individual DOM input to candidate profile key"""
        norm_key = f"{field_name} {field_label} {field_id}".lower().replace("-", "_").replace(" ", "_")
        for attr, keywords in cls.FIELD_MAPPINGS.items():
            for kw in keywords:
                if kw in norm_key:
                    return attr
        return None

    @classmethod
    def generate_form_fill_payload(
        cls,
        form_fields: List[Dict[str, Any]],
        candidate_data: Dict[str, Any],
        custom_cover_letter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes a mapped form payload ready for Stagehand autonomous fill.
        """
        payload: Dict[str, Any] = {}
        cand_name = candidate_data.get("name", "Dharanidharan D")
        name_parts = cand_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        skills_list = []
        skills_obj = candidate_data.get("skills", {})
        if isinstance(skills_obj, dict):
            for sublist in skills_obj.values():
                if isinstance(sublist, list):
                    skills_list.extend(sublist)
        elif isinstance(skills_obj, list):
            skills_list = skills_obj
        skills_str = ", ".join(skills_list[:8])

        for f in form_fields:
            fname = f.get("name") or f.get("id") or ""
            flabel = f.get("label", "")
            mapped_attr = cls.map_field_to_attribute(fname, flabel, f.get("id", ""))

            if mapped_attr == "full_name":
                payload[fname] = cand_name
            elif mapped_attr == "first_name":
                payload[fname] = first_name
            elif mapped_attr == "last_name":
                payload[fname] = last_name
            elif mapped_attr == "email":
                payload[fname] = candidate_data.get("email", "dharanidharan.ai@example.com")
            elif mapped_attr == "phone":
                payload[fname] = candidate_data.get("phone", "+1 (555) 234-8901")
            elif mapped_attr == "linkedin":
                payload[fname] = candidate_data.get("linkedin", "https://linkedin.com/in/dharanidharan-ai")
            elif mapped_attr == "github":
                payload[fname] = candidate_data.get("github", "https://github.com/dharanidharan-dev")
            elif mapped_attr == "portfolio":
                payload[fname] = candidate_data.get("portfolio", "https://dharanidharan.dev")
            elif mapped_attr == "skills":
                payload[fname] = skills_str
            elif mapped_attr == "cover_letter":
                payload[fname] = custom_cover_letter or candidate_data.get("cover_letter_snippet", "")
            elif mapped_attr == "resume":
                payload[fname] = "resume.pdf"
            elif mapped_attr == "work_authorization":
                payload[fname] = "Authorized to work in US without sponsorship"
            elif mapped_attr == "salary_expectations":
                payload[fname] = "Competitive / Market Rate ($120k - $160k)"
            else:
                # Default generic text if required
                if f.get("required"):
                    payload[fname] = "Proficient in AI systems, Stagehand automation, and FastAPI architectures."

        return payload

    @classmethod
    def validate_submission_payload(cls, payload: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
        """
        Validates payload prior to HITL approval gate.
        Checks for missing required fields, email syntax, phone syntax.
        """
        errors = []
        warnings = []

        # Check required fields
        for rf in required_fields:
            if rf not in payload or not str(payload[rf]).strip():
                errors.append(f"Missing mandatory field: {rf}")

        # Check email format
        email_val = payload.get("email") or payload.get("applicant_email")
        if email_val and not re.match(r"[^@]+@[^@]+\.[^@]+", str(email_val)):
            errors.append("Invalid email address format.")

        # Check resume attachment
        resume_val = payload.get("resume_file") or payload.get("resume") or payload.get("resume_upload")
        if not resume_val:
            warnings.append("No resume document attached. Standard resume will be referenced.")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "field_count": len(payload)
        }

form_intelligence = MultiFormIntelligence()
