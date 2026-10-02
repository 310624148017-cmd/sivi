import React from 'react';
import { IconShieldAlert, IconFileText } from './Icons';

interface ApprovalData {
  request_id?: string;
  action?: string;
  risk_level?: string;
  title?: string;
  description?: string;
  form_preview?: {
    candidate_name?: string;
    email?: string;
    phone?: string;
    role?: string;
    company?: string;
    resume_attached?: string;
    skills_count?: number;
    cover_letter_snippet?: string;
  };
}

interface ApprovalGateProps {
  data: ApprovalData | null;
  onApprove: () => void;
  onDeny: () => void;
}

export const ApprovalGate: React.FC<ApprovalGateProps> = ({
  data,
  onApprove,
  onDeny
}) => {
  if (!data) return null;

  const preview = data.form_preview || {};

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0, 0, 0, 0.85)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div style={{
        background: '#131826',
        border: '2px solid var(--gold)',
        borderRadius: '16px',
        padding: '32px',
        maxWidth: '620px',
        width: '100%',
        boxShadow: '0 25px 70px rgba(0,0,0,0.8), 0 0 35px var(--gold-glow)',
        animation: 'modalSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1)'
      }}>
        {/* Warning Badge */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          background: 'rgba(245, 158, 11, 0.15)',
          border: '1px solid var(--gold)',
          color: 'var(--gold-light)',
          padding: '10px 16px',
          borderRadius: '8px',
          fontSize: '13px',
          fontWeight: 800,
          letterSpacing: '0.5px',
          marginBottom: '18px'
        }}>
          <IconShieldAlert size={18} style={{ color: 'var(--gold)' }} />
          <span>HUMAN-IN-THE-LOOP (HITL) SAFETY GATE ACTIVATED</span>
        </div>

        <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#FFF', marginBottom: '8px' }}>
          {data.title || 'Approval Required: Final Application Submission'}
        </h2>
        
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '20px' }}>
          {data.description || 'The autonomous agent has verified all requirements, retrieved candidate documents via MCP, and filled all form fields. Submitting this form is an irreversible destructive action requiring human approval.'}
        </p>

        {/* Form Preview Summary */}
        <div style={{
          background: '#090C14',
          border: '1px solid var(--card-border)',
          borderRadius: '10px',
          padding: '16px 20px',
          fontSize: '13px',
          display: 'flex',
          flexDirection: 'column',
          gap: '10px',
          marginBottom: '24px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #1E2638', paddingBottom: '8px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Target Company</span>
            <span style={{ color: '#FFF', fontWeight: 700 }}>{preview.company || 'TechCorp'}</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #1E2638', paddingBottom: '8px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Position</span>
            <span style={{ color: 'var(--gold-light)', fontWeight: 700 }}>{preview.role || 'Software Engineer Intern'}</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #1E2638', paddingBottom: '8px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Applicant</span>
            <span style={{ color: '#FFF', fontWeight: 600 }}>{preview.candidate_name || 'Dharanidharan D'}</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #1E2638', paddingBottom: '8px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Email Contact</span>
            <span style={{ color: '#93C5FD' }}>{preview.email || 'dharanidharan.ai@example.com'}</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #1E2638', paddingBottom: '8px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Attached Document</span>
            <span style={{ color: 'var(--green)', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
              <IconFileText size={14} /> {preview.resume_attached || 'resume.pdf (142 KB, Validated ✓)'}
            </span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-muted)' }}>Cover Letter</span>
            <span style={{ color: '#CBD5E1', fontSize: '12px', maxWidth: '340px', textAlign: 'right' }}>
              "{preview.cover_letter_snippet || 'Having built SIVI with Stagehand, Claude 3.5 Sonnet, and MCP...'}"
            </span>
          </div>
        </div>

        {/* Modal Buttons */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.3fr', gap: '16px' }}>
          <button
            onClick={onDeny}
            style={{
              background: '#1A1E2B',
              border: '1px solid #374151',
              color: '#F87171',
              borderRadius: '8px',
              padding: '14px',
              fontSize: '14px',
              fontWeight: 700,
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            ✗ Deny / Abort Action
          </button>

          <button
            onClick={onApprove}
            style={{
              background: 'linear-gradient(135deg, var(--green), #059669)',
              border: 'none',
              color: '#FFF',
              borderRadius: '8px',
              padding: '14px',
              fontSize: '14px',
              fontWeight: 800,
              cursor: 'pointer',
              boxShadow: '0 4px 20px var(--green-glow)',
              transition: 'all 0.2s'
            }}
          >
            ✓ Approve & Submit Application
          </button>
        </div>
      </div>
    </div>
  );
};

export default ApprovalGate;
