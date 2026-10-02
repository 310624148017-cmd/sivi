import React from 'react';
import { IconLock } from './Icons';

interface ElementHighlight {
  id: string;
  tag?: string;
  bounds?: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}

interface BrowserViewportProps {
  currentUrl: string;
  pageTitle: string;
  activeSection?: string;
  highlights?: ElementHighlight[];
}

export const BrowserViewport: React.FC<BrowserViewportProps> = ({
  currentUrl,
  pageTitle,
  activeSection,
  highlights = []
}) => {
  const activeHighlight = highlights.length > 0 ? highlights[0] : null;

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
      {/* Browser Chrome Header */}
      <div style={{
        padding: '10px 16px',
        background: '#0F131D',
        borderBottom: '1px solid var(--card-border)',
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        {/* Window controls */}
        <div style={{ display: 'flex', gap: '6px' }}>
          <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#EF4444' }}></div>
          <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#F59E0B' }}></div>
          <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#10B981' }}></div>
        </div>

        {/* URL Bar */}
        <div style={{
          flex: 1,
          background: '#080A0F',
          border: '1px solid var(--card-border)',
          borderRadius: '6px',
          padding: '6px 12px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          fontSize: '12px'
        }}>
          <span style={{ color: 'var(--green)', fontSize: '11px', fontWeight: 700, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
            <IconLock size={12} /> HTTPS
          </span>
          <span style={{ color: '#93C5FD', fontFamily: 'var(--font-mono)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {currentUrl || 'http://localhost:8888/mock/techcorp/jobs/swe-intern'}
          </span>
        </div>

        {/* Stagehand Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{
            fontSize: '10px',
            fontWeight: 800,
            textTransform: 'uppercase',
            letterSpacing: '0.5px',
            color: 'var(--gold)',
            background: 'rgba(245, 158, 11, 0.12)',
            padding: '3px 8px',
            borderRadius: '4px',
            border: '1px solid rgba(245, 158, 11, 0.25)'
          }}>
            STAGEHAND CDP
          </span>
        </div>
      </div>

      {/* Browser Viewport View */}
      <div style={{
        flex: 1,
        position: 'relative',
        background: '#0B0E14',
        overflow: 'hidden'
      }}>
        <iframe
          id="browser-viewport-frame"
          src={currentUrl || '/mock/techcorp/jobs/swe-intern'}
          title="Autonomous Browser Viewport"
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
            minHeight: '440px'
          }}
        />

        {/* Dynamic Element Bounding Box Overlay */}
        {activeHighlight && activeHighlight.bounds && (
          <div
            style={{
              position: 'absolute',
              left: `${activeHighlight.bounds.x}px`,
              top: `${activeHighlight.bounds.y}px`,
              width: `${activeHighlight.bounds.width}px`,
              height: `${activeHighlight.bounds.height}px`,
              border: '2px solid var(--gold)',
              backgroundColor: 'rgba(245, 158, 11, 0.15)',
              borderRadius: '4px',
              pointerEvents: 'none',
              transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
              zIndex: 20
            }}
          >
            <div style={{
              position: 'absolute',
              top: '-20px',
              left: '0',
              background: 'var(--gold)',
              color: '#000',
              fontSize: '10px',
              fontWeight: 800,
              padding: '1px 6px',
              borderRadius: '3px',
              whiteSpace: 'nowrap'
            }}>
              LOCATING: #{activeHighlight.id}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BrowserViewport;
