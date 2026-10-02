import React, { useEffect, useRef } from 'react';
import { IconBrain } from './Icons';

interface ReasoningStreamProps {
  chunks: string[];
  tokenCount: number;
  currentStep?: number;
  isThinking: boolean;
}

export const ReasoningStream: React.FC<ReasoningStreamProps> = ({
  chunks,
  tokenCount,
  currentStep,
  isThinking
}) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [chunks, isThinking]);

  return (
    <div style={{
      background: 'var(--card-bg)',
      border: '1px solid var(--card-border)',
      borderRadius: '14px',
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      minHeight: '480px',
      overflow: 'hidden',
      boxShadow: '0 8px 30px rgba(0,0,0,0.5)'
    }}>
      <div style={{
        padding: '14px 20px',
        borderBottom: '1px solid var(--card-border)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        background: '#101420'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <IconBrain size={16} style={{ color: 'var(--gold)' }} />
          <span style={{
            fontSize: '13px',
            fontWeight: 800,
            letterSpacing: '0.5px',
            textTransform: 'uppercase',
            color: 'var(--gold)'
          }}>
            Claude 3.5 Sonnet Monologue
          </span>
          {isThinking && (
            <span style={{
              fontSize: '11px',
              padding: '2px 8px',
              borderRadius: '9999px',
              background: 'rgba(245, 158, 11, 0.15)',
              color: 'var(--gold-light)',
              fontWeight: 600
            }} className="pulse-indicator">
              Streaming Tokens...
            </span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {currentStep && (
            <span style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>
              Step {currentStep}/6
            </span>
          )}
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '11px',
            color: 'var(--text-muted)',
            background: '#090B10',
            padding: '3px 8px',
            borderRadius: '4px',
            border: '1px solid var(--card-border)'
          }}>
            {tokenCount} tokens
          </span>
        </div>
      </div>

      <div
        ref={scrollRef}
        style={{
          flex: 1,
          padding: '20px',
          background: '#090C14',
          fontFamily: 'var(--font-mono)',
          fontSize: '13px',
          lineHeight: '1.65',
          color: '#E2E8F0',
          overflowY: 'auto',
          wordBreak: 'break-word',
          whiteSpace: 'pre-wrap'
        }}
      >
        {chunks.length === 0 ? (
          <div style={{ color: 'var(--text-muted)', fontStyle: 'italic', paddingTop: '40px', textAlign: 'center' }}>
            ⚡ Waiting for agent launch. When initiated, Claude 3.5 Sonnet's stream-of-consciousness reasoning and autonomous decisions will appear here in real-time.
          </div>
        ) : (
          <>
            {chunks.map((chunk, idx) => (
              <span key={idx}>{chunk}</span>
            ))}
            {isThinking && (
              <span style={{ color: 'var(--gold)', marginLeft: '4px' }} className="pulse-indicator">
                ▌
              </span>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ReasoningStream;
