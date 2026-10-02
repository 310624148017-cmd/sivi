import React, { useState } from 'react';
import { IconFileText, IconSparkles, IconCopy } from './Icons';

export const CoverLetterStudio: React.FC = () => {
  const [role, setRole] = useState('Software Engineer Intern - AI & Autonomous Systems');
  const [company, setCompany] = useState('TechCorp');
  const [tone, setTone] = useState('Professional');
  const [letterText, setLetterText] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [wordCount, setWordCount] = useState(0);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const res = await fetch('http://localhost:8888/api/cover-letter/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_title: role, company_name: company, tone: tone })
      });
      const data = await res.json();
      setLetterText(data.letter_text || '');
      setWordCount(data.word_count || 0);
    } catch (e) {
      console.error('Error generating cover letter:', e);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(letterText);
    alert('Cover letter copied to clipboard!');
  };

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
      gap: '20px'
    }}>
      {/* Configuration Card */}
      <div style={{
        background: 'var(--card-bg)',
        border: '1px solid var(--card-border)',
        borderRadius: '12px',
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        gap: '14px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <IconFileText size={18} style={{ color: 'var(--gold)' }} />
          <h3 style={{ fontSize: '16px', color: '#FFF', fontWeight: 800 }}>Cover Letter Synthesizer</h3>
        </div>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
          Generates role-specific, high-converting cover letters mapped to candidate qualifications and selected tone.
        </p>

        <div>
          <label style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>Target Role:</label>
          <input
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            style={{
              width: '100%',
              background: '#090C13',
              border: '1px solid var(--card-border)',
              borderRadius: '6px',
              padding: '10px 14px',
              color: '#FFF',
              fontSize: '13px',
              marginTop: '6px'
            }}
          />
        </div>

        <div>
          <label style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>Target Company:</label>
          <input
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            style={{
              width: '100%',
              background: '#090C13',
              border: '1px solid var(--card-border)',
              borderRadius: '6px',
              padding: '10px 14px',
              color: '#FFF',
              fontSize: '13px',
              marginTop: '6px'
            }}
          />
        </div>

        <div>
          <label style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>Voice & Tone:</label>
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            style={{
              width: '100%',
              background: '#090C13',
              border: '1px solid var(--card-border)',
              borderRadius: '6px',
              padding: '10px 14px',
              color: '#FFF',
              fontSize: '13px',
              marginTop: '6px'
            }}
          >
            <option value="Professional">Professional (Concise, Metrics-Focused)</option>
            <option value="Friendly">Friendly (Warm, Cultural Alignment)</option>
            <option value="Formal">Formal (Executive, Traditional)</option>
            <option value="Bold">Bold (High-Impact, Startup Conviction)</option>
          </select>
        </div>

        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          style={{
            background: 'linear-gradient(135deg, var(--gold), #D97706)',
            color: '#000',
            border: 'none',
            borderRadius: '8px',
            padding: '12px',
            fontWeight: 800,
            fontSize: '13px',
            cursor: isGenerating ? 'not-allowed' : 'pointer',
            marginTop: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px'
          }}
        >
          <IconSparkles size={15} />
          <span>{isGenerating ? 'Synthesizing Letter...' : 'Generate Tailored Cover Letter'}</span>
        </button>
      </div>

      {/* Preview Card */}
      <div style={{
        background: 'var(--card-bg)',
        border: '1px solid var(--card-border)',
        borderRadius: '12px',
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ fontSize: '15px', color: '#FFF', fontWeight: 700 }}>Cover Letter Preview</h3>
          {letterText && (
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{wordCount} words</span>
              <button
                onClick={handleCopy}
                style={{
                  background: '#151A27',
                  border: '1px solid var(--card-border)',
                  color: 'var(--gold-light)',
                  padding: '5px 12px',
                  borderRadius: '6px',
                  fontSize: '12px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px'
                }}
              >
                <IconCopy size={12} />
                <span>Copy</span>
              </button>
            </div>
          )}
        </div>

        <textarea
          value={letterText}
          onChange={(e) => setLetterText(e.target.value)}
          placeholder="Click 'Generate' to synthesize your tailored cover letter..."
          style={{
            flex: 1,
            minHeight: '380px',
            background: '#0B0E17',
            border: '1px solid var(--card-border)',
            borderRadius: '8px',
            padding: '16px',
            color: '#E2E8F0',
            fontSize: '13px',
            lineHeight: 1.6,
            resize: 'none',
            fontFamily: 'var(--font-sans)'
          }}
        />
      </div>
    </div>
  );
};

export default CoverLetterStudio;
