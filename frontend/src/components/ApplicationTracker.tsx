import React, { useState } from 'react';
import { IconBriefcase, IconCalendar, IconRefresh, IconCheckCircle } from './Icons';

export interface ApplicationItem {
  id: string;
  company: string;
  role: string;
  department?: string;
  location?: string;
  url: string;
  status: 'Applied' | 'Reviewing' | 'Interview' | 'Offer' | 'Rejected';
  applied_at: string;
  match_score: number;
  notes?: string;
  interview?: {
    scheduled: boolean;
    date: string;
    time: string;
    round: string;
    interviewer: string;
    meet_url?: string;
  } | null;
  timeline?: Array<{
    date: string;
    event: string;
    details: string;
    type: string;
  }>;
}

interface ApplicationTrackerProps {
  applications: ApplicationItem[];
  onRefresh: () => void;
  onUpdateStatus: (id: string, newStatus: string) => void;
  onScheduleInterview: (id: string, date: string, time: string, round: string) => void;
}

export const ApplicationTracker: React.FC<ApplicationTrackerProps> = ({
  applications,
  onRefresh,
  onUpdateStatus,
  onScheduleInterview
}) => {
  const [filter, setFilter] = useState<string>('all');
  const [search, setSearch] = useState<string>('');

  const filteredApps = applications.filter((app) => {
    const matchesFilter = filter === 'all' || app.status.toLowerCase() === filter.toLowerCase();
    const matchesSearch =
      !search ||
      app.company.toLowerCase().includes(search.toLowerCase()) ||
      app.role.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const getStatusBadgeStyle = (status: string) => {
    switch (status) {
      case 'Offer':
        return { background: 'rgba(16, 185, 129, 0.15)', color: '#34D399', border: '1px solid rgba(16, 185, 129, 0.4)' };
      case 'Interview':
        return { background: 'rgba(139, 92, 246, 0.15)', color: '#C4B5FD', border: '1px solid rgba(139, 92, 246, 0.4)' };
      case 'Reviewing':
        return { background: 'rgba(245, 158, 11, 0.15)', color: '#FCD34D', border: '1px solid rgba(245, 158, 11, 0.4)' };
      case 'Rejected':
        return { background: 'rgba(239, 68, 68, 0.15)', color: '#FCA5A5', border: '1px solid rgba(239, 68, 68, 0.4)' };
      default:
        return { background: 'rgba(59, 130, 246, 0.15)', color: '#60A5FA', border: '1px solid rgba(59, 130, 246, 0.4)' };
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header & Filter Controls */}
      <div style={{
        background: 'var(--card-bg)',
        border: '1px solid var(--card-border)',
        borderRadius: '12px',
        padding: '18px 24px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '14px'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <IconBriefcase size={18} style={{ color: 'var(--gold)' }} />
            <h2 style={{ fontSize: '17px', color: '#FFF', fontWeight: 800 }}>Application Tracking Dashboard</h2>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Monitoring all submitted applications, pipeline velocity, and interview rounds.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
          <input
            type="text"
            placeholder="Search company or role..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              background: '#090C13',
              border: '1px solid var(--card-border)',
              borderRadius: '6px',
              padding: '6px 12px',
              color: '#FFF',
              fontSize: '12px',
              outline: 'none'
            }}
          />
          {['all', 'Applied', 'Reviewing', 'Interview', 'Offer'].map((st) => (
            <button
              key={st}
              onClick={() => setFilter(st)}
              style={{
                background: filter === st ? 'rgba(245, 158, 11, 0.15)' : '#090B10',
                border: filter === st ? '1px solid var(--gold)' : '1px solid var(--card-border)',
                color: filter === st ? 'var(--gold-light)' : 'var(--text-muted)',
                padding: '6px 12px',
                borderRadius: '6px',
                fontSize: '12px',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              {st === 'all' ? `All (${applications.length})` : st}
            </button>
          ))}
          <button
            onClick={onRefresh}
            style={{
              background: '#151A27',
              border: '1px solid var(--card-border)',
              color: 'var(--text-muted)',
              padding: '6px 10px',
              borderRadius: '6px',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '5px'
            }}
          >
            <IconRefresh size={12} />
            <span>Sync</span>
          </button>
        </div>
      </div>

      {/* Grid of Applications */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
        gap: '18px'
      }}>
        {filteredApps.map((app) => (
          <div
            key={app.id}
            style={{
              background: 'var(--card-bg)',
              border: '1px solid var(--card-border)',
              borderRadius: '12px',
              padding: '20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
              position: 'relative'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <strong style={{ color: '#FFF', fontSize: '15px' }}>{app.company}</strong>
                <div style={{ fontSize: '13px', color: 'var(--gold-light)', marginTop: '2px' }}>{app.role}</div>
              </div>
              <span style={{
                fontSize: '10px',
                fontWeight: 800,
                padding: '3px 8px',
                borderRadius: '6px',
                textTransform: 'uppercase',
                letterSpacing: '0.4px',
                ...getStatusBadgeStyle(app.status)
              }}>
                {app.status}
              </span>
            </div>

            <div style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'flex', justifyContent: 'space-between' }}>
              <span>{app.location || 'Remote / Hybrid'}</span>
              <span style={{ color: 'var(--green)', fontWeight: 700 }}>Match: {app.match_score}%</span>
            </div>

            <div style={{
              fontSize: '12px',
              color: '#CBD5E1',
              background: '#0B0E17',
              padding: '10px',
              borderRadius: '6px',
              border: '1px solid var(--card-border)'
            }}>
              {app.notes || 'Autonomous application submitted via SIVI Agent.'}
            </div>

            {app.interview && app.interview.scheduled && (
              <div style={{
                background: 'rgba(139, 92, 246, 0.1)',
                border: '1px solid rgba(139, 92, 246, 0.3)',
                padding: '8px 12px',
                borderRadius: '6px',
                fontSize: '12px',
                color: '#C4B5FD',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <IconCalendar size={14} />
                <span><strong>Round:</strong> {app.interview.round} · {app.interview.date} at {app.interview.time}</span>
              </div>
            )}

            <div style={{ display: 'flex', gap: '8px', marginTop: 'auto', paddingTop: '8px' }}>
              <button
                onClick={() => {
                  const d = prompt('Enter interview date (YYYY-MM-DD):', '2026-10-18');
                  if (d) onScheduleInterview(app.id, d, '14:00 PST', 'Technical Deep Dive');
                }}
                style={{
                  flex: 1,
                  background: '#151A27',
                  border: '1px solid var(--card-border)',
                  color: 'var(--text-primary)',
                  padding: '8px',
                  borderRadius: '6px',
                  fontSize: '12px',
                  cursor: 'pointer',
                  fontWeight: 600,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '6px'
                }}
              >
                <IconCalendar size={13} />
                <span>Interview</span>
              </button>
              <button
                onClick={() => {
                  const nextSt = prompt('New status (Applied / Reviewing / Interview / Offer / Rejected):', 'Reviewing');
                  if (nextSt) onUpdateStatus(app.id, nextSt);
                }}
                style={{
                  flex: 1,
                  background: '#151A27',
                  border: '1px solid var(--card-border)',
                  color: 'var(--gold-light)',
                  padding: '8px',
                  borderRadius: '6px',
                  fontSize: '12px',
                  cursor: 'pointer',
                  fontWeight: 600,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '6px'
                }}
              >
                <IconRefresh size={12} />
                <span>Update Status</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ApplicationTracker;
