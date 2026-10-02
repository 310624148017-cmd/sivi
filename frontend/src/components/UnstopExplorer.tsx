import React, { useState, useEffect } from 'react';
import {
  IconSearch,
  IconPlay,
  IconCheckCircle,
  IconLink,
  IconZap,
  IconBriefcase
} from './Icons';

export interface UnstopInternship {
  id: string;
  company: string;
  title: string;
  program?: string;
  category: string;
  location: string;
  mode: string;
  stipend: string;
  duration: string;
  deadline: string;
  applicants_count?: number;
  url: string;
  portal_type: string;
  qualifications: string;
  description: string;
  requirements: string[];
  match_score?: number;
  matched_skills?: string[];
  missing_skills?: string[];
}

interface UnstopExplorerProps {
  onApplyWithSivi: (internship: UnstopInternship) => void;
}

export const UnstopExplorer: React.FC<UnstopExplorerProps> = ({ onApplyWithSivi }) => {
  const [internships, setInternships] = useState<UnstopInternship[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedMode, setSelectedMode] = useState('All');

  const categories = [
    'All',
    'AI / Machine Learning',
    'Full Stack Development',
    'Python & Autonomous Systems',
    'Backend Engineering',
    'Frontend Engineering',
    'Data Science',
    'Cloud & DevOps'
  ];

  const fetchInternships = async (query = searchQuery, category = selectedCategory, mode = selectedMode) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (query.trim()) params.append('query', query.trim());
      if (category && category !== 'All') params.append('category', category);
      if (mode && mode !== 'All') params.append('mode', mode);

      const res = await fetch(`http://localhost:8888/api/unstop/search?${params.toString()}`);
      const data = await res.json();
      setInternships(data.internships || []);
    } catch (err) {
      console.error('Failed to fetch Unstop internships:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInternships('', 'All', 'All');
  }, []);

  const handleSearchSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    fetchInternships(searchQuery, selectedCategory, selectedMode);
  };

  const handleCategorySelect = (category: string) => {
    setSelectedCategory(category);
    fetchInternships(searchQuery, category, selectedMode);
  };

  const handleModeSelect = (mode: string) => {
    setSelectedMode(mode);
    fetchInternships(searchQuery, selectedCategory, mode);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header Search & Filtering Card */}
      <div style={{
        background: 'var(--card-bg)',
        border: '1px solid var(--card-border)',
        borderRadius: '12px',
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '38px',
              height: '38px',
              borderRadius: '9px',
              background: 'rgba(245, 158, 11, 0.15)',
              border: '1px solid rgba(245, 158, 11, 0.35)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--gold)'
            }}>
              <IconSearch size={20} />
            </div>
            <div>
              <h2 style={{ color: '#FFF', fontSize: '18px', fontWeight: 800, letterSpacing: '-0.3px', margin: 0 }}>
                Unstop Internship Explorer & Auto-Apply
              </h2>
              <p style={{ color: 'var(--text-muted)', fontSize: '13px', margin: '2px 0 0 0' }}>
                Search verified company challenges and hiring sprints on Unstop. Auto-fill 4-step applications using your stored profile.
              </p>
            </div>
          </div>

          <div style={{
            background: 'rgba(16, 185, 129, 0.12)',
            border: '1px solid rgba(16, 185, 129, 0.35)',
            color: 'var(--green)',
            fontSize: '11px',
            fontWeight: 700,
            padding: '4px 10px',
            borderRadius: '9999px',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '5px'
          }}>
            <IconCheckCircle size={12} />
            <span>UNSTOP PORTAL INTEGRATED</span>
          </div>
        </div>

        {/* Search Input Bar */}
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search internships by company, skill (e.g. AI, React, Python), or title..."
            style={{
              flex: 2,
              minWidth: '260px',
              background: '#090B10',
              border: '1px solid var(--card-border)',
              color: '#FFF',
              padding: '12px 16px',
              borderRadius: '8px',
              fontSize: '14px',
              outline: 'none'
            }}
          />

          <select
            value={selectedMode}
            onChange={(e) => handleModeSelect(e.target.value)}
            style={{
              background: '#090B10',
              border: '1px solid var(--card-border)',
              color: '#FFF',
              padding: '12px 14px',
              borderRadius: '8px',
              fontSize: '13px',
              minWidth: '150px',
              outline: 'none'
            }}
          >
            <option value="All">All Work Modes</option>
            <option value="Remote">Remote Only</option>
            <option value="Hybrid">Hybrid</option>
            <option value="In-Office">In-Office / On-site</option>
          </select>

          <button
            type="submit"
            style={{
              background: 'linear-gradient(135deg, var(--gold), #D97706)',
              color: '#000',
              border: 'none',
              borderRadius: '8px',
              padding: '12px 22px',
              fontSize: '13px',
              fontWeight: 800,
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <IconSearch size={14} />
            <span>Search Unstop</span>
          </button>
        </form>

        {/* Category Pills */}
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap', paddingTop: '4px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>Category:</span>
          {categories.map((cat) => {
            const isActive = selectedCategory === cat;
            return (
              <button
                key={cat}
                type="button"
                onClick={() => handleCategorySelect(cat)}
                style={{
                  background: isActive ? 'rgba(245, 158, 11, 0.15)' : '#141926',
                  border: isActive ? '1px solid var(--gold)' : '1px solid var(--card-border)',
                  color: isActive ? 'var(--gold-light)' : 'var(--text-muted)',
                  padding: '5px 12px',
                  borderRadius: '20px',
                  fontSize: '12px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                {cat}
              </button>
            );
          })}
          <span style={{ fontSize: '12px', color: 'var(--gold-light)', marginLeft: 'auto', fontWeight: 600 }}>
            {internships.length} opportunities found
          </span>
        </div>
      </div>

      {/* Results Grid */}
      {loading ? (
        <div style={{
          padding: '50px',
          textAlign: 'center',
          color: 'var(--text-muted)',
          background: 'var(--card-bg)',
          borderRadius: '12px',
          border: '1px solid var(--card-border)'
        }}>
          Searching Unstop opportunities and computing qualifications matching...
        </div>
      ) : internships.length === 0 ? (
        <div style={{
          padding: '50px',
          textAlign: 'center',
          color: 'var(--text-muted)',
          background: 'var(--card-bg)',
          borderRadius: '12px',
          border: '1px solid var(--card-border)'
        }}>
          <p style={{ color: '#FFF', fontSize: '16px', fontWeight: 600 }}>No internships found matching your query.</p>
          <p style={{ fontSize: '13px', marginTop: '6px' }}>Try switching category to "All" or clearing keyword filters.</p>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(420px, 1fr))',
          gap: '20px'
        }}>
          {internships.map((item) => {
            const logoLetter = item.company ? item.company[0] : 'U';
            return (
              <div
                key={item.id}
                style={{
                  background: 'var(--card-bg)',
                  border: '1px solid var(--card-border)',
                  borderRadius: '12px',
                  padding: '22px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '14px',
                  transition: 'all 0.2s ease'
                }}
              >
                {/* Top Company & Match Badge */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '10px' }}>
                  <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                    <div style={{
                      width: '44px',
                      height: '44px',
                      borderRadius: '10px',
                      background: '#182032',
                      border: '1px solid var(--card-border)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '16px',
                      fontWeight: 800,
                      color: 'var(--gold-light)'
                    }}>
                      {logoLetter}
                    </div>
                    <div>
                      <h3 style={{ color: '#FFF', fontSize: '16px', fontWeight: 700, margin: 0, lineHeight: 1.3 }}>
                        {item.title}
                      </h3>
                      <div style={{ color: 'var(--gold-light)', fontSize: '13px', fontWeight: 600, marginTop: '2px' }}>
                        {item.company}
                      </div>
                      <div style={{ color: 'var(--text-muted)', fontSize: '11px', marginTop: '1px' }}>
                        {item.program || 'Unstop Campus Sprint'}
                      </div>
                    </div>
                  </div>

                  <div style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                    padding: '4px 10px',
                    borderRadius: '9999px',
                    fontSize: '12px',
                    fontWeight: 700,
                    background: 'rgba(16, 185, 129, 0.15)',
                    border: '1px solid rgba(16, 185, 129, 0.4)',
                    color: 'var(--green)'
                  }}>
                    <IconCheckCircle size={12} />
                    <span>{item.match_score || 95}% Match</span>
                  </div>
                </div>

                {/* Meta Chips */}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', fontSize: '12px', color: 'var(--text-muted)' }}>
                  <span style={{
                    background: 'rgba(245, 158, 11, 0.12)',
                    border: '1px solid rgba(245, 158, 11, 0.3)',
                    color: 'var(--gold-light)',
                    padding: '3px 8px',
                    borderRadius: '6px',
                    fontWeight: 700
                  }}>
                    {item.stipend}
                  </span>
                  <span style={{ background: '#141824', border: '1px solid var(--card-border)', padding: '3px 8px', borderRadius: '6px' }}>
                    Mode: {item.mode}
                  </span>
                  <span style={{ background: '#141824', border: '1px solid var(--card-border)', padding: '3px 8px', borderRadius: '6px' }}>
                    Duration: {item.duration}
                  </span>
                  <span style={{ background: '#141824', border: '1px solid var(--card-border)', padding: '3px 8px', borderRadius: '6px' }}>
                    Deadline: {item.deadline}
                  </span>
                </div>

                {/* Eligibility Callout */}
                <div style={{
                  background: '#090C13',
                  border: '1px solid var(--card-border)',
                  borderRadius: '8px',
                  padding: '10px 12px',
                  fontSize: '12px',
                  color: '#CBD5E1',
                  lineHeight: 1.5
                }}>
                  <strong style={{ color: 'var(--gold)', fontSize: '11px', textTransform: 'uppercase' }}>
                    Eligibility Criteria:
                  </strong>
                  <div style={{ marginTop: '2px' }}>{item.qualifications}</div>
                </div>

                {/* Matched Skills */}
                <div>
                  <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '4px' }}>
                    Top Matched Skills:
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {(item.matched_skills || []).slice(0, 4).map((skill, idx) => (
                      <span
                        key={idx}
                        style={{
                          background: 'rgba(16, 185, 129, 0.15)',
                          color: 'var(--green)',
                          padding: '2px 8px',
                          borderRadius: '4px',
                          fontSize: '11px',
                          fontWeight: 600
                        }}
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div style={{
                  display: 'flex',
                  gap: '10px',
                  marginTop: 'auto',
                  paddingTop: '10px',
                  borderTop: '1px solid #1A2130'
                }}>
                  <button
                    onClick={() => onApplyWithSivi(item)}
                    style={{
                      flex: 1,
                      background: 'linear-gradient(135deg, var(--gold), #D97706)',
                      color: '#000',
                      border: 'none',
                      borderRadius: '8px',
                      padding: '10px 16px',
                      fontSize: '13px',
                      fontWeight: 800,
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '6px'
                    }}
                  >
                    <IconPlay size={12} />
                    <span>Autofill & Apply with SIVI</span>
                  </button>

                  <a
                    href={item.url}
                    target="_blank"
                    rel="noreferrer"
                    style={{
                      background: '#141824',
                      border: '1px solid var(--card-border)',
                      color: 'var(--text-muted)',
                      borderRadius: '8px',
                      padding: '10px 14px',
                      fontSize: '13px',
                      fontWeight: 600,
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '6px',
                      textDecoration: 'none'
                    }}
                  >
                    <IconLink size={13} />
                    <span>Portal</span>
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default UnstopExplorer;
