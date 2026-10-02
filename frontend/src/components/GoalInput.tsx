import React, { useState } from 'react';
import { IconMic, IconPlay, IconZap, IconSliders, IconCheckCircle } from './Icons';

interface GoalInputProps {
  goal: string;
  setGoal: (goal: string) => void;
  jobUrl: string;
  setJobUrl: (url: string) => void;
  tone: string;
  setTone: (tone: string) => void;
  batchCount: number;
  setBatchCount: (count: number) => void;
  isRunning: boolean;
  onStart: () => void;
  onSetPreset: (type: 'unstop' | 'techcorp' | 'greenhouse' | 'workday' | 'batch') => void;
  agentStatus: string;
}

export const GoalInput: React.FC<GoalInputProps> = ({
  goal,
  setGoal,
  jobUrl,
  setJobUrl,
  tone,
  setTone,
  batchCount,
  setBatchCount,
  isRunning,
  onStart,
  onSetPreset,
  agentStatus
}) => {
  const [isListening, setIsListening] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleVoiceInput = () => {
    const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRec) {
      alert('Speech recognition is not supported in this browser. Please type your goal directly.');
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => setIsListening(true);
    recognition.onresult = (e: any) => {
      const transcript = e.results[0][0].transcript;
      setGoal(transcript);
      if ('speechSynthesis' in window) {
        const u = new SpeechSynthesisUtterance("Goal registered: " + transcript);
        window.speechSynthesis.speak(u);
      }
    };
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    recognition.start();
  };

  return (
    <div style={{
      background: 'var(--card-bg)',
      border: '1px solid var(--card-border)',
      borderRadius: '12px',
      padding: '20px 24px',
      boxShadow: '0 8px 30px rgba(0,0,0,0.4)',
      display: 'flex',
      flexDirection: 'column',
      gap: '14px'
    }}>
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
        <div style={{ flex: '2', minWidth: '320px', position: 'relative' }}>
          <input
            type="text"
            placeholder="Enter autonomous goal (e.g. 'Apply for SWE internship at TechCorp')..."
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            disabled={isRunning}
            style={{
              width: '100%',
              background: '#090B10',
              border: '1px solid var(--card-border)',
              borderRadius: '8px',
              padding: '12px 16px',
              color: '#FFF',
              fontSize: '14px',
              fontWeight: 500,
              outline: 'none',
              transition: 'all 0.2s ease'
            }}
          />
        </div>

        <div style={{ flex: '1.2', minWidth: '240px' }}>
          <input
            type="url"
            placeholder="Target Application / ATS URL..."
            value={jobUrl}
            onChange={(e) => setJobUrl(e.target.value)}
            disabled={isRunning}
            style={{
              width: '100%',
              background: '#090B10',
              border: '1px solid var(--card-border)',
              borderRadius: '8px',
              padding: '12px 16px',
              color: '#93C5FD',
              fontSize: '13px',
              fontFamily: 'var(--font-mono)',
              outline: 'none'
            }}
          />
        </div>

        {/* Voice Input Button */}
        <button
          onClick={handleVoiceInput}
          disabled={isRunning}
          title="Voice Command Input"
          style={{
            background: isListening ? 'rgba(239, 68, 68, 0.2)' : '#161B26',
            border: isListening ? '1px solid #EF4444' : '1px solid var(--card-border)',
            color: isListening ? '#EF4444' : 'var(--text-muted)',
            width: '42px',
            height: '42px',
            borderRadius: '8px',
            cursor: isRunning ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'all 0.15s ease'
          }}
        >
          <IconMic size={18} />
        </button>

        {/* Start / Launch Button */}
        <button
          onClick={onStart}
          disabled={isRunning}
          style={{
            background: isRunning ? '#283042' : 'linear-gradient(135deg, var(--gold), #D97706)',
            color: isRunning ? '#9CA3AF' : '#000',
            border: 'none',
            borderRadius: '8px',
            padding: '12px 24px',
            fontSize: '13px',
            fontWeight: 800,
            cursor: isRunning ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            boxShadow: isRunning ? 'none' : '0 4px 14px var(--gold-glow)',
            transition: 'all 0.2s ease'
          }}
        >
          {isRunning ? (
            <>
              <span className="pulse-indicator" style={{ display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: 'var(--gold)' }}></span>
              <span>Running...</span>
            </>
          ) : (
            <>
              <IconPlay size={13} />
              <span>Launch SIVI</span>
            </>
          )}
        </button>
      </div>

      {/* Quick Preset Selector & Status */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '10px',
        paddingTop: '2px'
      }}>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>Presets:</span>
          <button
            onClick={() => onSetPreset('unstop')}
            disabled={isRunning}
            style={{
              background: '#141824',
              border: '1px solid var(--card-border)',
              color: 'var(--gold-light)',
              padding: '5px 12px',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: isRunning ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <IconZap size={13} />
            <span>Flipkart (Unstop GRiD AI Intern)</span>
          </button>
          <button
            onClick={() => onSetPreset('techcorp')}
            disabled={isRunning}
            style={{
              background: '#141824',
              border: '1px solid var(--card-border)',
              color: 'var(--gold-light)',
              padding: '5px 12px',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: isRunning ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <IconZap size={13} />
            <span>TechCorp Demo Flow (2:45)</span>
          </button>
          <button
            onClick={() => onSetPreset('greenhouse')}
            disabled={isRunning}
            style={{
              background: '#141824',
              border: '1px solid var(--card-border)',
              color: 'var(--text-primary)',
              padding: '5px 12px',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: isRunning ? 'not-allowed' : 'pointer'
            }}
          >
            ScaleAI (Greenhouse)
          </button>
          <button
            onClick={() => onSetPreset('workday')}
            disabled={isRunning}
            style={{
              background: '#141824',
              border: '1px solid var(--card-border)',
              color: 'var(--text-primary)',
              padding: '5px 12px',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: isRunning ? 'not-allowed' : 'pointer'
            }}
          >
            CloudScale (Workday)
          </button>
          <button
            onClick={() => onSetPreset('batch')}
            disabled={isRunning}
            style={{
              background: '#141824',
              border: '1px solid var(--card-border)',
              color: 'var(--text-primary)',
              padding: '5px 12px',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: isRunning ? 'not-allowed' : 'pointer'
            }}
          >
            Batch Mode (3 Jobs)
          </button>
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              fontSize: '12px',
              cursor: 'pointer',
              marginLeft: '4px',
              display: 'flex',
              alignItems: 'center',
              gap: '5px'
            }}
          >
            <IconSliders size={13} />
            <span>{showAdvanced ? 'Hide Config' : 'Options'}</span>
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{
            fontSize: '11px',
            color: 'var(--green)',
            background: 'rgba(16, 185, 129, 0.08)',
            padding: '4px 10px',
            borderRadius: '9999px',
            border: '1px solid rgba(16, 185, 129, 0.25)',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <IconCheckCircle size={12} />
            <span>MCP Linked: resume.pdf</span>
          </span>
        </div>
      </div>

      {/* Advanced Options Drawer */}
      {showAdvanced && (
        <div style={{
          display: 'flex',
          gap: '20px',
          alignItems: 'center',
          paddingTop: '12px',
          borderTop: '1px solid #1E2638',
          fontSize: '12px',
          color: 'var(--text-muted)',
          flexWrap: 'wrap'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>Cover Letter Style:</span>
            <select
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              disabled={isRunning}
              style={{
                background: '#090B10',
                border: '1px solid var(--card-border)',
                color: '#FFF',
                padding: '4px 8px',
                borderRadius: '4px',
                fontSize: '12px'
              }}
            >
              <option value="Professional">Professional (Data-driven, Concise)</option>
              <option value="Friendly">Friendly (Warm, Cultural)</option>
              <option value="Formal">Formal (Executive, Structured)</option>
              <option value="Bold">Bold (High-Impact, Startup)</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>Batch Applications:</span>
            <select
              value={batchCount}
              onChange={(e) => setBatchCount(parseInt(e.target.value))}
              disabled={isRunning}
              style={{
                background: '#090B10',
                border: '1px solid var(--card-border)',
                color: '#FFF',
                padding: '4px 8px',
                borderRadius: '4px',
                fontSize: '12px'
              }}
            >
              <option value="1">1 Job (Single Target)</option>
              <option value="3">3 Jobs (Sequential Apply)</option>
              <option value="5">5 Jobs (Paced Off-Peak)</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>Safety Gate:</span>
            <span style={{ color: 'var(--green)', fontWeight: 700 }}>Zero-Bypass HITL Active</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default GoalInput;
