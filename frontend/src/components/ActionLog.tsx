import React from 'react';
import { IconChart } from './Icons';

export interface ActionItem {
  id: string;
  type: string;
  action?: string;
  message?: string;
  result?: any;
  status: 'success' | 'pending' | 'warning' | 'error';
  timestamp: string;
}

interface ActionLogProps {
  actions: ActionItem[];
}

export const ActionLog: React.FC<ActionLogProps> = ({ actions }) => {
  return (
    <div style={{
      background: 'var(--card-bg)',
      border: '1px solid var(--card-border)',
      borderRadius: '14px',
      padding: '18px 24px',
      boxShadow: '0 8px 30px rgba(0,0,0,0.5)'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '12px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <IconChart size={15} style={{ color: 'var(--gold)' }} />
          <span style={{
            fontSize: '13px',
            fontWeight: 800,
            letterSpacing: '0.5px',
            textTransform: 'uppercase',
            color: 'var(--gold)'
          }}>
            Action History & Audit Log
          </span>
        </div>
        <span style={{
          fontSize: '12px',
          color: 'var(--text-secondary)',
          background: '#090B10',
          padding: '3px 10px',
          borderRadius: '9999px',
          border: '1px solid var(--card-border)'
        }}>
          {actions.length} Events Logged
        </span>
      </div>

      <div style={{
        display: 'flex',
        gap: '14px',
        overflowX: 'auto',
        paddingBottom: '8px',
        minHeight: '85px'
      }}>
        {actions.length === 0 ? (
          <div style={{ color: 'var(--text-muted)', fontSize: '13px', fontStyle: 'italic', padding: '12px 0' }}>
            No actions recorded yet. Actions dispatched by Stagehand will appear in this timeline.
          </div>
        ) : (
          actions.map((act) => {
            const isSuccess = act.status === 'success';
            const isWarning = act.status === 'warning';
            const isError = act.status === 'error';

            const borderColor = isSuccess ? 'var(--green)' : isWarning ? 'var(--gold)' : isError ? 'var(--red)' : '#6B7280';

            return (
              <div
                key={act.id}
                style={{
                  minWidth: '220px',
                  maxWidth: '280px',
                  background: '#0B0E17',
                  border: '1px solid var(--card-border)',
                  borderLeft: `3px solid ${borderColor}`,
                  borderRadius: '8px',
                  padding: '10px 14px',
                  fontSize: '12px',
                  flexShrink: 0
                }}
              >
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '4px'
                }}>
                  <span style={{
                    fontSize: '10px',
                    fontWeight: 800,
                    textTransform: 'uppercase',
                    color: isWarning ? 'var(--gold)' : isSuccess ? 'var(--green)' : '#93C5FD'
                  }}>
                    {act.type} {act.action ? `· ${act.action}` : ''}
                  </span>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>
                    {act.timestamp.split('T')[1]?.substring(0, 8) || ''}
                  </span>
                </div>
                <div style={{ color: '#E2E8F0', lineHeight: '1.4', wordBreak: 'break-word' }}>
                  {act.message || (typeof act.result === 'string' ? act.result : JSON.stringify(act.result))}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default ActionLog;
