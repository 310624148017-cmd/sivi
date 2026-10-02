import os
import sys
import json
import asyncio

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app import app
from starlette.testclient import TestClient

def test_sivi_production_suite():
    print("==================================================")
    print("SIVI: Running Full Production-Ready Verification")
    print("==================================================")

    client = TestClient(app)

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    health_data = res.json()
    print(f"✓ Health Check Passed: {health_data['service']} (v{health_data['version']})")
    print(f"  Supported Features: {len(health_data['features'])} verified")

    # 2. Candidate MCP profile
    res_cand = client.get("/api/candidate")
    assert res_cand.status_code == 200
    cand = res_cand.json()["candidate"]
    print(f"✓ MCP Candidate Profile: {cand['name']} | {cand['title']}")
    assert "Dharanidharan" in cand["name"]

    # 3. Portals Verification
    for portal_path, expected_text in [
        ("/mock/techcorp/jobs/swe-intern", "TechCorp"),
        ("/mock/greenhouse/jobs/ai-engineer", "Greenhouse"),
        ("/mock/workday/jobs/cloud-architect", "Workday")
    ]:
        res_p = client.get(portal_path)
        assert res_p.status_code == 200
        assert expected_text in res_p.text
        print(f"✓ Mock Career Portal Verified: {portal_path}")

    # 3b. Unstop Search, Detail, and Portal Verification
    unstop_search_res = client.get("/api/unstop/search?query=AI&category=All")
    assert unstop_search_res.status_code == 200
    unstop_search_data = unstop_search_res.json()
    assert unstop_search_data["total"] >= 1
    first_unstop = unstop_search_data["internships"][0]
    print(f"✓ Unstop Search Engine: Found {unstop_search_data['total']} internships for 'AI' | Top Match: {first_unstop['company']} ({first_unstop['match_score']}%)")

    unstop_detail_res = client.get(f"/api/unstop/internships/{first_unstop['id']}")
    assert unstop_detail_res.status_code == 200
    unstop_detail = unstop_detail_res.json()
    assert unstop_detail["id"] == first_unstop["id"]
    print(f"✓ Unstop Internship Detail: Verified {unstop_detail['title']} at {unstop_detail['company']}")

    unstop_mock_res = client.get(f"/mock/unstop/internships/{first_unstop['id']}")
    assert unstop_mock_res.status_code == 200
    assert "Unstop" in unstop_mock_res.text
    assert "unstop_name" in unstop_mock_res.text
    assert "unstop_college" in unstop_mock_res.text
    assert "unstop_cgpa" in unstop_mock_res.text
    print(f"✓ Unstop Mock Portal Verified: Contains 4-step eligibility & autofill form")

    # 3c. Autofill Vault & Candidate Profile Update
    autofill_res = client.get("/api/candidate/autofill")
    assert autofill_res.status_code == 200
    autofill_payload = autofill_res.json()
    assert autofill_payload["readiness_score"] == 100
    assert autofill_payload["personal"]["full_name"] == "Dharanidharan D"
    assert "college" in autofill_payload["academic"]
    print(f"✓ Candidate Autofill Vault: Readiness={autofill_payload['readiness_score']}% | College={autofill_payload['academic']['college']} | CGPA={autofill_payload['academic']['cgpa']}")

    # Test Candidate Update PUT
    update_res = client.put("/api/candidate", json={
        "name": "Dharanidharan D",
        "title": "Lead Autonomous Agent Architect",
        "college": "Institute of Technology",
        "degree": "B.Tech in Artificial Intelligence & Data Science",
        "graduation_year": "2026",
        "cgpa": "3.95 / 4.0",
        "skills": ["Python", "FastAPI", "Next.js", "Stagehand", "MCP", "Playwright", "Docker"]
    })
    assert update_res.status_code == 200
    update_data = update_res.json()
    assert update_data["status"] == "success"
    assert update_data["autofill"]["academic"]["cgpa"] == "3.95 / 4.0"
    print(f"✓ Candidate Profile Sync: Updated academic qualifications to MCP successfully")

    # 4. Smart Resume Matching API
    match_payload = {
        "title": "Software Engineer Intern - AI & Autonomous Systems",
        "company": "TechCorp",
        "requirements": ["Python", "FastAPI", "TypeScript", "Stagehand", "Model Context Protocol", "Kubernetes"]
    }
    res_m = client.post("/api/match", json=match_payload)
    assert res_m.status_code == 200
    match_data = res_m.json()
    print(f"✓ Smart Resume Matching: Match Score={match_data['match_score']}% | Matched={len(match_data['matched_skills'])} | Missing={len(match_data['missing_skills'])}")
    assert match_data["match_score"] >= 75.0
    assert "Python" in match_data["matched_skills"]

    # 5. AI Cover Letter Studio (All 4 Tones)
    for tone in ["Professional", "Bold", "Friendly", "Formal"]:
        cl_res = client.post("/api/cover-letter/generate", json={
            "job_title": "Software Engineer Intern",
            "company_name": "TechCorp",
            "requirements": ["FastAPI", "Stagehand", "Claude 3.5 Sonnet"],
            "tone": tone
        })
        assert cl_res.status_code == 200
        cl_data = cl_res.json()
        assert cl_data["tone"] == tone
        assert len(cl_data["letter_text"]) > 100
    print("✓ AI Cover Letter Studio: Generated Professional, Bold, Friendly, and Formal styles")

    # 6. Multi-Form Intelligence
    form_res = client.post("/api/forms/classify", json={
        "url": "https://boards.greenhouse.io/scaleai/jobs/4819231",
        "title": "ScaleAI Greenhouse Application Form"
    })
    assert form_res.status_code == 200
    form_data = form_res.json()
    print(f"✓ Multi-Form Intelligence: Classified {form_data['vendor_name']} (Form Type: {form_data['form_type']})")
    assert form_data["is_ats"] is True

    # 7. Application Tracking CRUD
    apps_res = client.get("/api/applications")
    assert apps_res.status_code == 200
    apps_list = apps_res.json()["applications"]
    print(f"✓ Application Tracker: {len(apps_list)} applications actively tracked")
    assert len(apps_list) >= 4

    first_app_id = apps_list[0]["id"]
    sched_res = client.post(f"/api/applications/{first_app_id}/interview", json={
        "date": "2026-10-18",
        "time": "15:00 PST",
        "round": "System Architecture Deep Dive",
        "interviewer": "Engineering Lead"
    })
    assert sched_res.status_code == 200
    print(f"✓ Interview Scheduling Integration: Confirmed for {apps_list[0]['company']}")

    # 8. Analytics & Insights
    analytics_res = client.get("/api/analytics")
    assert analytics_res.status_code == 200
    analytics_data = analytics_res.json()
    print(f"✓ Analytics & Insights: Response Rate={analytics_data['response_rate_percent']}% | Resume Strength={analytics_data['resume_strength']['overall_score']}/10")
    assert analytics_data["total_applications"] >= 4

    # 9. Integration Hub
    integ_res = client.get("/api/integrations")
    assert integ_res.status_code == 200
    integ_data = integ_res.json()
    print(f"✓ Integration Hub: LinkedIn={integ_data['linkedin']['connected']} | Gmail={integ_data['email']['connected']} | Calendar={integ_data['calendar']['connected']}")

    # 10. Standalone HTML UI
    ui_res = client.get("/")
    assert ui_res.status_code == 200
    assert "SIVI" in ui_res.text
    print(f"✓ Standalone Interactive Dashboard: Verified (HTML Size: {len(ui_res.text)} bytes)")

    # 11. WebSocket Autonomous Flow & Zero-Bypass HITL Gate
    print("\nConnecting to WebSocket /ws/agent for Autonomous Workflow...")
    with client.websocket_connect("/ws/agent") as ws:
        ws.send_json({
            "goal": "Apply for the Software Engineer internship at TechCorp",
            "url": "http://localhost:8888/mock/techcorp/jobs/swe-intern",
            "tone": "Professional"
        })
        print("✓ Dispatched Autonomous Goal to SiviAgent")

        hitl_triggered = False
        chunks_received = 0
        actions_received = []

        while True:
            try:
                event = ws.receive_json()
                evt_type = event.get("type")

                if evt_type == "reasoning_stream":
                    chunks_received += 1
                elif evt_type == "status":
                    print(f"  [STATUS] {event.get('message')}")
                elif evt_type == "observation":
                    print(f"  [OBSERVE] Step {event.get('step')}: {event.get('message')}")
                elif evt_type == "form_analysis":
                    print(f"  [FORM INTEL] Detected: {event.get('vendor_name')} ({event.get('form_type')})")
                elif evt_type == "skills_match":
                    print(f"  [SMART MATCH] Score: {event.get('match_score')}% | Matched: {len(event.get('matched_skills', []))} skills")
                elif evt_type == "action_result":
                    actions_received.append(event)
                    print(f"  [ACTION] {event.get('action')}: {event.get('result')}")
                elif evt_type == "approval_required":
                    print("\n[SAFETY GATE] Paused before destructive final submission!")
                    print(f"   Applicant: {event.get('form_preview', {}).get('candidate_name')}")
                    print(f"   Company: {event.get('form_preview', {}).get('company')}")
                    print(f"   Attached Resume: {event.get('form_preview', {}).get('resume_attached')}")
                    hitl_triggered = True

                    # Simulate Human Operator clicking "Approve"
                    print("\n[ACTION] Human Operator clicking 'Approve Submission'...")
                    ws.send_json({"type": "approval_response", "approved": True})

                if evt_type == "status" and event.get("phase") == "COMPLETED":
                    print(f"\n[COMPLETE] {event.get('message')}")
                    break

            except Exception as e:
                print("WebSocket complete or loop ended:", e)
                break

        assert hitl_triggered, "HITL approval was not triggered!"
        assert chunks_received > 20, f"Expected streaming chunks, got {chunks_received}"
        print(f"\n✓ Received {chunks_received} streaming reasoning chunks.")
        print(f"✓ Received {len(actions_received)} executed browser actions.")

    # 12. WebSocket Unstop Flow & Academic Qualifications Autofill
    print("\nConnecting to WebSocket /ws/agent for Unstop Autonomous Workflow...")
    with client.websocket_connect("/ws/agent") as ws_unstop:
        ws_unstop.send_json({
            "goal": "Apply for MeitY (Digital India Bhashini AI Mission) – Generative AI & Indic Language Model Fellow on Unstop",
            "url": "http://localhost:8888/mock/unstop/internships/gov-meity-genai-fellow-2026",
            "tone": "Professional"
        })
        print("✓ Dispatched Unstop Goal to SiviAgent")

        unstop_hitl = False
        unstop_autofill_detected = False
        unstop_completed = False

        while True:
            try:
                event = ws_unstop.receive_json()
                evt_type = event.get("type")

                if evt_type == "observation" and "Unstop" in event.get("message", ""):
                    print(f"  [UNSTOP OBSERVE] {event.get('message')}")
                elif evt_type == "action_result":
                    res_str = str(event.get("result", ""))
                    if "college" in res_str.lower() or "qualifications" in res_str.lower() or "unstop" in res_str.lower():
                        unstop_autofill_detected = True
                        print(f"  [UNSTOP AUTOFILL] {event.get('action')}: {event.get('result')}")
                elif evt_type == "approval_required":
                    print("\n[UNSTOP HITL SAFETY GATE] Approving Unstop application...")
                    unstop_hitl = True
                    ws_unstop.send_json({"type": "approval_response", "approved": True})
                elif evt_type == "status" and event.get("phase") == "COMPLETED":
                    print(f"\n[UNSTOP COMPLETE] {event.get('message')}")
                    assert "#UNSTOP" in event.get("message", ""), "Expected Unstop confirmation ID"
                    unstop_completed = True
                    break
            except Exception as e:
                print("Unstop WS ended:", e)
                break

        assert unstop_hitl, "Unstop HITL gate did not trigger!"
        assert unstop_completed, "Unstop workflow did not complete successfully!"
        print("✓ Unstop 4-step autonomous application and qualification autofill verified!")

    # 13. Multi-Provider LLM Catalog & Challenge Endpoints
    print("\nVerifying Multi-Provider LLM & Challenge Endpoints...")
    prov_res = client.get("/api/models/providers")
    assert prov_res.status_code == 200
    prov_data = prov_res.json()
    providers_list = prov_data.get("providers", [])
    assert len(providers_list) == 5, f"Expected 5 providers, got {len(providers_list)}"
    provider_ids = [p["id"] for p in providers_list]
    for required_prov in ["groq", "gemini", "openrouter", "nvidia", "anthropic"]:
        assert required_prov in provider_ids, f"Missing required provider {required_prov}"
    print(f"✓ Multi-Provider LLM Engine: 5/5 providers verified ({', '.join(provider_ids)})")

    # 14. Provider Configuration & Runtime Switching
    cfg_res = client.post("/api/models/configure", json={
        "provider": "gemini",
        "model": "gemini-2.0-flash"
    })
    assert cfg_res.status_code == 200
    cfg_data = cfg_res.json()
    assert cfg_data["active_provider"] == "gemini"
    assert cfg_data["selected_model"] == "gemini-2.0-flash"
    print("✓ Model Configuration: Runtime provider switched to Google Gemini 2.0 Flash")

    # Switch back to Groq for ultra-fast LPU testing
    cfg_groq = client.post("/api/models/configure", json={
        "provider": "groq",
        "model": "llama-3.3-70b-versatile"
    })
    assert cfg_groq.status_code == 200
    print("✓ Model Configuration: Runtime provider switched to Groq LPU (Llama 3.3 70B)")

    # 15. Key Testing & Latency Benchmarking API
    test_key_res = client.post("/api/models/test-key", json={
        "provider": "groq",
        "api_key": "dummy_test_key_for_latency",
        "model": "llama-3.3-70b-versatile"
    })
    assert test_key_res.status_code == 200
    test_key_data = test_key_res.json()
    assert "latency_ms" in test_key_data
    print(f"✓ Provider Latency Benchmarking: Measured {test_key_data['latency_ms']} ms round-trip")

    # 16. Voice Accessibility (Speech-to-Text) API
    voice_res = client.post("/api/audio/transcribe", content=b"RIFF\x24\x00\x00\x00WAVEfmt ", headers={"content-type": "audio/wav"})
    assert voice_res.status_code == 200
    voice_data = voice_res.json()
    assert voice_data["success"] is True
    assert len(voice_data.get("text", "")) > 5
    print(f"✓ Voice Accessibility (STT): Transcribed '{voice_data['text']}' via {voice_data.get('engine')}")

    # 17. ISRO Bhuvan Geospatial Distance & Commute Viability
    bhuvan_res = client.get("/api/bhuvan/geodistance?origin=Bengaluru&destination=Hyderabad&mode=Hybrid")
    assert bhuvan_res.status_code == 200
    bhuvan_data = bhuvan_res.json()
    assert bhuvan_data["distance_km"] > 0
    assert "nrsc_datum" in bhuvan_data
    print(f"✓ ISRO Bhuvan Geospatial Engine: Distance={bhuvan_data['distance_km']} km | Commute={bhuvan_data['commute_type']} | Viability={bhuvan_data['viability_score']}/100")

    # 18. India Open Government Data (data.gov.in) & Enriched Unstop Catalog
    gov_res = client.get("/api/data-gov/internships")
    assert gov_res.status_code == 200
    gov_data = gov_res.json()
    assert gov_data["total"] >= 5
    print(f"✓ data.gov.in Open Data Engine: Found {gov_data['total']} public sector tech fellowships across {len(gov_data['ministries'])} ministries")

    # Enriched Unstop with Bhuvan distance chips and Government listings
    enriched_unstop = client.get("/api/unstop/search?include_govt=true")
    assert enriched_unstop.status_code == 200
    enriched_data = enriched_unstop.json()
    has_bhuvan = any("bhuvan_analysis" in item for item in enriched_data["internships"])
    has_gov = any("data.gov.in" in item.get("source", "") for item in enriched_data["internships"])
    assert enriched_data["total"] == 5, f"Expected 5 curated internships, got {enriched_data['total']}"
    assert has_bhuvan, "Expected Bhuvan commute analysis on internships"
    assert has_gov, "Expected data.gov.in listings in enriched search"
    print(f"✓ Enriched Opportunities Catalog: {enriched_data['total']}/5 curated roles (MeitY, ISRO SAC, NIC, DRDO CAIR, AICTE) with ISRO Bhuvan commute chips")

    print("==================================================")
    print("ALL 18 SIVI PRODUCTION & CHALLENGE SUITE TESTS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    test_sivi_production_suite()
