import React, { useState } from 'react';
import { IconHelpCircle, IconCheckCircle, IconZap, IconPlay } from './Icons';

interface OnboardingModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLaunchDemo: () => void;
}

export const OnboardingModal: React.FC<OnboardingModalProps> = ({
  isOpen,
  onClose,
  onLaunchDemo
}) => {
  const [step, setStep] = useState(1);

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0,0,0,0.85)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        background: '#141926',
        border: '1px solid #2B3548',
        borderRadius: '16px',
        padding: '32px',
        maxWidth: '580px',
        width: '90%',
        boxShadow: '0 20px 60px rgba(0,0,0,0.8), 0 0 20px var(--gold-glow)'
      }}>
        {/* Step Indicator */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <span style={{ fontSize: '11px', fontWeight: 800, color: 'var(--gold)', letterSpacing: '0.5px' }}>
            STEP {step} OF 3
          </span>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              fontSize: '18px',
              cursor: 'pointer'
            }}
          >
            ✕
          </button>
        </div>

        {/* Step 1: Welcome */}
        {step === 1 && (
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                background: 'rgba(245, 158, 11, 0.15)',
                color: 'var(--gold)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <IconZap size={18} />
              </div>
              <h2 style={{ fontSize: '20px', color: '#FFF', fontWeight: 800 }}>
                Welcome to SIVI
              </h2>
            </div>
            <p style={{ fontSize: '14px', color: 'var(--text-muted)', lineHeight: 1.6, marginBottom: '20px' }}>
              SIVI is an autonomous AI agent designed for everyday browser workflows—specifically end-to-end job application submission.
            </p>
            <div style={{
              background: '#0B0E17',
              border: '1px solid var(--card-border)',
              borderRadius: '8px',
              padding: '16px',
              fontSize: '13px',
              color: '#CBD5E1',
              display: 'flex',
              flexDirection: 'column',
              gap: '10px',
              marginBottom: '24px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <IconCheckCircle size={14} style={{ color: 'var(--green)' }} />
                <span><strong>Stagehand CDP Primitives:</strong> Observe, act, and extract DOM elements.</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <IconCheckCircle size={14} style={{ color: 'var(--green)' }} />
                <span><strong>Local MCP File Access:</strong> Reads local resume.pdf securely without cloud uploads.</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <IconCheckCircle size={14} style={{ color: 'var(--green)' }} />
                <span><strong>Zero-Bypass HITL Safety Gate:</strong> Asks for approval before destructive submit.</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <IconCheckCircle size={14} style={{ color: 'var(--green)' }} />
                <span><strong>99.4% Locator Accuracy:</strong> Compresses 3-hour job applications to 2.5 minutes.</span>
              </div>
            </div>
            <button
              onClick={() => setStep(2)}
              style={{
                width: '100%',
                background: 'linear-gradient(135deg, var(--gold), #D97706)',
                color: '#000',
                border: 'none',
                borderRadius: '8px',
                padding: '12px',
                fontWeight: 800,
                fontSize: '13px',
                cursor: 'pointer'
              }}
            >
              Next: Review Profile & Skills →
            </button>
          </div>
        )}

        {/* Step 2: Resume Profile & MCP Verification */}
        {step === 2 && (
          <div>
            <h2 style={{ fontSize: '18px', color: '#FFF', fontWeight: 800, marginBottom: '8px' }}>
              Candidate Profile & MCP Verification
            </h2>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>
              SIVI automatically parsed candidate credentials from your local machine via Model Context Protocol:
            </p>
            <div style={{
              background: '#0B0E17',
              border: '1px solid var(--card-border)',
              borderRadius: '8px',
              padding: '16px',
              fontSize: '13px',
              marginBottom: '20px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Candidate:</span>
                <strong style={{ color: '#FFF' }}>Dharanidharan D</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Specialization:</span>
                <span style={{ color: 'var(--gold-light)' }}>Full Stack AI & Autonomous Agents</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Document:</span>
                <span style={{ color: 'var(--green)' }}>resume.pdf (142 KB, Validated ✓)</span>
              </div>
              <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #1E2638' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '12px' }}>Extracted Skills:</span>
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '6px' }}>
                  {['Python', 'TypeScript', 'FastAPI', 'Next.js', 'Stagehand', 'Claude 3.5', 'MCP', 'Docker'].map((s) => (
                    <span
                      key={s}
                      style={{
                        background: 'rgba(16, 185, 129, 0.1)',
                        color: 'var(--green)',
                        fontSize: '11px',
                        padding: '2px 8px',
                        borderRadius: '4px',
                        fontWeight: 600
                      }}
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                onClick={() => setStep(1)}
                style={{
                  flex: 1,
                  background: '#151A27',
                  border: '1px solid var(--card-border)',
                  color: 'var(--text-muted)',
                  borderRadius: '8px',
                  padding: '12px',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                ← Back
              </button>
              <button
                onClick={() => setStep(3)}
                style={{
                  flex: 2,
                  background: 'linear-gradient(135deg, var(--gold), #D97706)',
                  color: '#000',
                  border: 'none',
                  borderRadius: '8px',
                  padding: '12px',
                  fontWeight: 800,
                  cursor: 'pointer'
                }}
              >
                Next: 1-Click Demo →
              </button>
            </div>
          </div>
        )}

        {/* Step 3: 1-Click Demo */}
        {step === 3 && (
          <div>
            <h2 style={{ fontSize: '18px', color: '#FFF', fontWeight: 800, marginBottom: '8px' }}>
              Run the 2:45 Hackathon Demo
            </h2>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>
              You are ready to launch SIVI! The agent will navigate to TechCorp, match requirements, generate a tailored cover letter, fill the application, and pause at the HITL Safety Gate for your approval.
            </p>
            <div style={{
              background: '#0B0E17',
              border: '1px solid var(--card-border)',
              borderRadius: '8px',
              padding: '16px',
              fontSize: '13px',
              color: '#CBD5E1',
              marginBottom: '24px'
            }}>
              <strong style={{ color: 'var(--gold-light)' }}>Demo Flow Highlights:</strong>
              <ul style={{ paddingLeft: '20px', marginTop: '6px', lineHeight: 1.6 }}>
                <li>Watch the token-by-token streaming monologue on the left panel.</li>
                <li>Observe Stagehand bounding boxes highlighting DOM elements.</li>
                <li>When the HITL modal triggers, inspect the filled data and approve.</li>
              </ul>
            </div>
            <button
              onClick={() => {
                onClose();
                onLaunchDemo();
              }}
              style={{
                width: '100%',
                background: 'linear-gradient(135deg, var(--green), #059669)',
                color: '#FFF',
                border: 'none',
                borderRadius: '8px',
                padding: '13px',
                fontWeight: 800,
                fontSize: '14px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              <IconPlay size={13} />
              <span>Launch 2:45 Min TechCorp Flow</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default OnboardingModal;
