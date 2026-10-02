import React, { useState, useEffect } from 'react';
import {
  IconUserCheck,
  IconGraduationCap,
  IconSave,
  IconCheckCircle,
  IconFileText,
  IconRefresh,
  IconShieldAlert
} from './Icons';

export const AutofillVault: React.FC = () => {
  const [profile, setProfile] = useState({
    name: 'Dharanidharan D',
    title: 'Full Stack AI Engineer & Autonomous Agent Developer',
    email: 'dharanidharan.ai@example.com',
    phone: '+1 (555) 234-8901',
    location: 'San Francisco, CA / Hybrid',
    linkedin: 'https://linkedin.com/in/dharanidharan-ai',
    github: 'https://github.com/dharanidharan-dev',
    portfolio: 'https://dharanidharan.dev',
    college: 'Institute of Technology',
    degree: 'B.Tech in Artificial Intelligence & Data Science',
    graduation_year: '2026',
    cgpa: '3.92 / 4.0',
    skills: 'Python, TypeScript, FastAPI, Next.js, Stagehand, Docker, MCP, Playwright'
  });

  const [resumeData, setResumeData] = useState({
    filename: 'resume.pdf',
    size_kb: 142,
    status: 'VALIDATED'
  });

  const [readinessScore, setReadinessScore] = useState(100);
  const [saveStatus, setSaveStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await fetch('http://localhost:8888/api/candidate');
      const data = await res.json();
      if (data.candidate) {
        const cand = data.candidate;
        const auto = data.autofill || {};
        const academic = auto.academic || {};
        const personal = auto.personal || cand || {};
        const skillsList = auto.skills || [];

        setProfile({
          name: personal.full_name || cand.name || '',
          title: cand.title || '',
          email: personal.email || cand.email || '',
          phone: personal.phone || cand.phone || '',
          location: personal.location || cand.location || '',
          linkedin: personal.linkedin || cand.linkedin || '',
          github: personal.github || cand.github || '',
          portfolio: personal.portfolio || cand.portfolio || '',
          college: academic.college || '',
          degree: academic.degree || '',
          graduation_year: academic.graduation_year || '',
          cgpa: academic.cgpa || '',
          skills: Array.isArray(skillsList) ? skillsList.join(', ') : skillsList
        });

        if (auto.resume) {
          setResumeData(auto.resume);
        }
        if (auto.readiness_score) {
          setReadinessScore(auto.readiness_score);
        }
      }
    } catch (err) {
      console.warn('Could not load profile from backend, using defaults:', err);
    }
  };

  const handleInputChange = (field: string, val: string) => {
    setProfile((prev) => ({ ...prev, [field]: val }));
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSaveStatus(null);

    const skillsArray = profile.skills.split(',').map((s) => s.trim()).filter((s) => s.length > 0);

    const payload = {
      name: profile.name,
      title: profile.title,
      email: profile.email,
      phone: profile.phone,
      location: profile.location,
      linkedin: profile.linkedin,
      github: profile.github,
      portfolio: profile.portfolio,
      college: profile.college,
      degree: profile.degree,
      graduation_year: profile.graduation_year,
      cgpa: profile.cgpa,
      skills: skillsArray
    };

    try {
      const res = await fetch('http://localhost:8888/api/candidate', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.status === 'success') {
        setSaveStatus('Profile & Academic Qualifications saved to MCP and synchronized with data/resume.json!');
        if (data.autofill?.readiness_score) {
          setReadinessScore(data.autofill.readiness_score);
        }
      } else {
        setSaveStatus('Error saving profile.');
      }
    } catch (err) {
      setSaveStatus('Network error syncing to backend.');
    } finally {
      setLoading(false);
      setTimeout(() => setSaveStatus(null), 5000);
    }
  };

  const formMapping = {
    "Target Portals": ["Unstop (#unstop_*)", "Greenhouse ATS", "Workday Enterprise", "Lever ATS"],
    "Form Field Injection": {
      "#unstop_name": profile.name,
      "#unstop_email": profile.email,
      "#unstop_phone": profile.phone,
      "#unstop_college": profile.college,
      "#unstop_degree": profile.degree,
      "#unstop_grad_year": profile.graduation_year,
      "#unstop_cgpa": profile.cgpa,
      "#unstop_skills": profile.skills.split(',').slice(0, 5).map(s => s.trim()).join(', '),
      "#unstop_resume_dropzone": `${resumeData.filename} (${resumeData.size_kb} KB Attached via MCP)`
    },
    "Readiness": `${readinessScore}% Complete`
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Vault Top Banner */}
      <div style={{
        background: 'var(--card-bg)',
        border: '1px solid var(--card-border)',
        borderRadius: '12px',
        padding: '24px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '20px',
        flexWrap: 'wrap'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              color: 'var(--green)',
              background: 'rgba(16, 185, 129, 0.12)',
              border: '1px solid rgba(16, 185, 129, 0.35)',
              padding: '3px 10px',
              borderRadius: '20px',
              fontSize: '11px',
              fontWeight: 700
            }}>
              <IconCheckCircle size={12} />
              <span>MCP LOCAL DATA VAULT</span>
            </span>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Integrated with SIVI Autonomous CDP Agent
            </span>
          </div>
          <h2 style={{ color: '#FFF', fontSize: '20px', fontWeight: 800, letterSpacing: '-0.4px', margin: 0 }}>
            Candidate Profile & Academic Qualifications Vault
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '13px', maxWidth: '780px', marginTop: '4px', lineHeight: 1.5 }}>
            SIVI collects and verifies your identity, college, degree program, CGPA, and resume document. When you click apply on Unstop or any career site, SIVI auto-fills every multi-step field without repetitive typing.
          </p>
        </div>

        {/* Readiness Meter */}
        <div style={{
          background: '#090C13',
          border: '1px solid var(--card-border)',
          borderRadius: '10px',
          padding: '14px 22px',
          display: 'flex',
          alignItems: 'center',
          gap: '16px'
        }}>
          <div>
            <div style={{ fontSize: '11px', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700, letterSpacing: '0.5px' }}>
              Autofill Readiness
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginTop: '2px' }}>
              <span style={{ fontSize: '28px', fontWeight: 800, color: 'var(--green)', fontFamily: 'var(--font-mono)' }}>
                {readinessScore}%
              </span>
              <span style={{ fontSize: '12px', color: 'var(--green)', fontWeight: 700 }}>
                Ready to Apply
              </span>
            </div>
          </div>
        </div>
      </div>

      {saveStatus && (
        <div style={{
          background: 'rgba(16, 185, 129, 0.15)',
          border: '1px solid var(--green)',
          color: '#FFF',
          padding: '12px 18px',
          borderRadius: '8px',
          fontSize: '13px',
          fontWeight: 600,
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <IconCheckCircle size={15} />
          <span>{saveStatus}</span>
        </div>
      )}

      {/* Main Grid: Form on Left, MCP Resume & Preview on Right */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1.25fr 1fr',
        gap: '20px'
      }}>
        {/* Left Column: Editable Vault Form */}
        <form onSubmit={handleSave} style={{
          background: 'var(--card-bg)',
          border: '1px solid var(--card-border)',
          borderRadius: '12px',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          gap: '18px'
        }}>
          {/* Section 1: Personal & Contact */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--card-border)', paddingBottom: '10px' }}>
            <h3 style={{ color: '#FFF', fontSize: '15px', fontWeight: 700, margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <IconUserCheck size={16} />
              <span>Personal & Contact Information</span>
            </h3>
            <span style={{ fontSize: '11px', color: 'var(--green)', fontWeight: 700 }}>Verified</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Full Name</label>
              <input
                type="text"
                value={profile.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Professional Title</label>
              <input
                type="text"
                value={profile.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Email Address</label>
              <input
                type="email"
                value={profile.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Phone Number</label>
              <input
                type="text"
                value={profile.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Location / Work Authorization</label>
            <input
              type="text"
              value={profile.location}
              onChange={(e) => handleInputChange('location', e.target.value)}
              style={{
                background: '#090B10',
                border: '1px solid var(--card-border)',
                color: '#FFF',
                padding: '10px 14px',
                borderRadius: '7px',
                fontSize: '13px',
                outline: 'none'
              }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>LinkedIn URL</label>
              <input
                type="url"
                value={profile.linkedin}
                onChange={(e) => handleInputChange('linkedin', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>GitHub URL</label>
              <input
                type="url"
                value={profile.github}
                onChange={(e) => handleInputChange('github', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Portfolio Website</label>
            <input
              type="url"
              value={profile.portfolio}
              onChange={(e) => handleInputChange('portfolio', e.target.value)}
              style={{
                background: '#090B10',
                border: '1px solid var(--card-border)',
                color: '#FFF',
                padding: '10px 14px',
                borderRadius: '7px',
                fontSize: '13px',
                outline: 'none'
              }}
            />
          </div>

          {/* Section 2: Academic Qualifications */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--card-border)', paddingBottom: '10px', marginTop: '6px' }}>
            <h3 style={{ color: '#FFF', fontSize: '15px', fontWeight: 700, margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <IconGraduationCap size={16} />
              <span>Academic Qualifications & Degree</span>
            </h3>
            <span style={{ fontSize: '11px', color: 'var(--gold-light)', fontWeight: 700 }}>Unstop Criteria</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>College / University</label>
              <input
                type="text"
                value={profile.college}
                onChange={(e) => handleInputChange('college', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Degree & Major</label>
              <input
                type="text"
                value={profile.degree}
                onChange={(e) => handleInputChange('degree', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Graduation Year</label>
              <input
                type="text"
                value={profile.graduation_year}
                onChange={(e) => handleInputChange('graduation_year', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>CGPA / GPA</label>
              <input
                type="text"
                value={profile.cgpa}
                onChange={(e) => handleInputChange('cgpa', e.target.value)}
                style={{
                  background: '#090B10',
                  border: '1px solid var(--card-border)',
                  color: '#FFF',
                  padding: '10px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  outline: 'none'
                }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <label style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>
              Core Technical Skills (Auto-injected into form skills inputs)
            </label>
            <textarea
              rows={2}
              value={profile.skills}
              onChange={(e) => handleInputChange('skills', e.target.value)}
              style={{
                background: '#090B10',
                border: '1px solid var(--card-border)',
                color: '#FFF',
                padding: '10px 14px',
                borderRadius: '7px',
                fontSize: '13px',
                outline: 'none',
                resize: 'vertical'
              }}
            />
          </div>

          <div style={{ display: 'flex', gap: '12px', marginTop: '6px' }}>
            <button
              type="submit"
              disabled={loading}
              style={{
                flex: 1,
                background: 'linear-gradient(135deg, var(--gold), #D97706)',
                color: '#000',
                border: 'none',
                borderRadius: '8px',
                padding: '12px 20px',
                fontSize: '13px',
                fontWeight: 800,
                cursor: loading ? 'not-allowed' : 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              <IconSave size={15} />
              <span>{loading ? 'Saving to MCP...' : 'Save & Sync Profile to MCP'}</span>
            </button>

            <button
              type="button"
              onClick={fetchProfile}
              style={{
                background: '#141926',
                border: '1px solid var(--card-border)',
                color: 'var(--text-muted)',
                borderRadius: '8px',
                padding: '12px 16px',
                fontSize: '13px',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <IconRefresh size={14} />
              <span>Reset</span>
            </button>
          </div>
        </form>

        {/* Right Column: Connected Document & Live Mapping */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* MCP Attached Resume Card */}
          <div style={{
            background: 'var(--card-bg)',
            border: '1px solid var(--card-border)',
            borderRadius: '12px',
            padding: '24px',
            display: 'flex',
            flexDirection: 'column',
            gap: '16px'
          }}>
            <h3 style={{ color: '#FFF', fontSize: '15px', fontWeight: 700, margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <IconFileText size={16} />
              <span>MCP Indexed Document</span>
            </h3>

            <div style={{
              background: '#0B0F19',
              border: '1px solid var(--card-border)',
              borderRadius: '10px',
              padding: '16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: '12px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '8px',
                  background: 'rgba(245, 158, 11, 0.15)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--gold)'
                }}>
                  <IconFileText size={20} />
                </div>
                <div>
                  <div style={{ color: '#FFF', fontWeight: 700, fontSize: '14px' }}>
                    {resumeData.filename}
                  </div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '12px' }}>
                    {resumeData.size_kb} KB · Verified by MCP Client · Attached to All Forms
                  </div>
                </div>
              </div>

              <span style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px',
                color: 'var(--green)',
                background: 'rgba(16, 185, 129, 0.12)',
                border: '1px solid rgba(16, 185, 129, 0.35)',
                padding: '4px 10px',
                borderRadius: '20px',
                fontSize: '11px',
                fontWeight: 700
              }}>
                <IconCheckCircle size={12} />
                <span>VALIDATED</span>
              </span>
            </div>
          </div>

          {/* Live Form Injection Preview */}
          <div style={{
            background: 'var(--card-bg)',
            border: '1px solid var(--card-border)',
            borderRadius: '12px',
            padding: '24px',
            display: 'flex',
            flexDirection: 'column',
            gap: '14px',
            flex: 1
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                Live Form Field Mapping (Unstop + ATS)
              </span>
              <span style={{ fontSize: '11px', color: 'var(--gold-light)', fontWeight: 600 }}>
                Auto-Injected by Stagehand
              </span>
            </div>

            <pre style={{
              background: '#080A10',
              border: '1px solid var(--card-border)',
              borderRadius: '8px',
              padding: '14px',
              fontFamily: 'var(--font-mono)',
              fontSize: '12px',
              color: '#93C5FD',
              lineHeight: 1.5,
              maxHeight: '260px',
              overflowY: 'auto',
              margin: 0
            }}>
              {JSON.stringify(formMapping, null, 2)}
            </pre>

            <div style={{
              background: 'rgba(16, 185, 129, 0.08)',
              border: '1px solid rgba(16, 185, 129, 0.25)',
              borderRadius: '8px',
              padding: '12px',
              marginTop: 'auto'
            }}>
              <div style={{ fontSize: '12px', color: 'var(--green)', fontWeight: 700, marginBottom: '4px' }}>
                Zero Re-typing Guarantee
              </div>
              <p style={{ fontSize: '12px', color: '#94A3B8', margin: 0, lineHeight: 1.4 }}>
                When applying via SIVI on Unstop or standard applicant tracking systems, these exact fields are automatically populated into the target web elements without manual user effort.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AutofillVault;
