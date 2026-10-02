import React, { useState, useRef, useEffect } from 'react';
import Head from 'next/head';
import GoalInput from '../components/GoalInput';
import ReasoningStream from '../components/ReasoningStream';
import BrowserViewport from '../components/BrowserViewport';
import ActionLog, { ActionItem } from '../components/ActionLog';
import ApprovalGate from '../components/ApprovalGate';
import ApplicationTracker, { ApplicationItem } from '../components/ApplicationTracker';
import Analytics from '../components/Analytics';
import CoverLetterStudio from '../components/CoverLetterStudio';
import IntegrationHub from '../components/IntegrationHub';
import OnboardingModal from '../components/OnboardingModal';
import UnstopExplorer from '../components/UnstopExplorer';
import AutofillVault from '../components/AutofillVault';
import {
  IconZap,
  IconDashboard,
  IconBriefcase,
  IconChart,
  IconSparkles,
  IconLink,
  IconHelpCircle,
  IconBell,
  IconSearch,
  IconUserCheck
} from '../components/Icons';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'unstop' | 'vault' | 'tracker' | 'analytics' | 'studio' | 'integrations'>('dashboard');
  const [goal, setGoal] = useState('Apply for the Software Engineer internship at TechCorp');
  const [jobUrl, setJobUrl] = useState('http://localhost:8888/mock/techcorp/jobs/swe-intern');
  const [tone, setTone] = useState('Professional');
  const [batchCount, setBatchCount] = useState(1);
  const [isRunning, setIsRunning] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [reasoningChunks, setReasoningChunks] = useState<string[]>([]);
  const [tokenCount, setTokenCount] = useState(0);
  const [currentStep, setCurrentStep] = useState<number | undefined>(undefined);
  const [actions, setActions] = useState<ActionItem[]>([]);
  const [requiresApproval, setRequiresApproval] = useState(false);
  const [approvalData, setApprovalData] = useState<any>(null);
  const [agentStatus, setAgentStatus] = useState('Agent Ready (Idle)');
  const [isOnboardingOpen, setIsOnboardingOpen] = useState(false);
  const [isNotifOpen, setIsNotifOpen] = useState(false);
  const [applications, setApplications] = useState<ApplicationItem[]>([]);
  const [analyticsData, setAnalyticsData] = useState<any>({
    total_applications: 5,
    response_rate_percent: 80.0,
    avg_response_time_days: 2.4,
    avg_match_quality_percent: 93.6
  });

  const [viewportData, setViewportData] = useState({
    url: 'http://localhost:8888/mock/techcorp/jobs/swe-intern',
    title: 'TechCorp Careers | Software Engineer Intern',
    activeSection: 'landing',
    highlights: [] as any[]
  });

  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    fetchApplications();
    fetchAnalytics();
  }, []);

  const fetchApplications = async () => {
    try {
      const res = await fetch('http://localhost:8888/api/applications');
      const data = await res.json();
      if (data.applications) setApplications(data.applications);
    } catch (e) {
      console.warn('Backend not responding yet for applications API.');
    }
  };

  const fetchAnalytics = async () => {
    try {
      const res = await fetch('http://localhost:8888/api/analytics');
      const data = await res.json();
      setAnalyticsData(data);
    } catch (e) {
      console.warn('Backend not responding yet for analytics API.');
    }
  };

  const addAction = (type: string, message: string, status: 'success' | 'pending' | 'warning' | 'error' = 'success', action?: string) => {
    const newItem: ActionItem = {
      id: `act-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
      type,
      action,
      message,
      status,
      timestamp: new Date().toISOString()
    };
    setActions((prev) => [newItem, ...prev]);
  };

  const handlePreset = (type: 'unstop' | 'techcorp' | 'greenhouse' | 'workday' | 'batch') => {
    if (type === 'unstop') {
      setGoal('Apply for Flipkart GRiD AI & Autonomous Systems Intern on Unstop');
      setJobUrl('http://localhost:8888/mock/unstop/internships/unstop-flipkart-ai-intern-2026');
      setViewportData((prev) => ({ ...prev, url: 'http://localhost:8888/mock/unstop/internships/unstop-flipkart-ai-intern-2026' }));
    } else if (type === 'techcorp') {
      setGoal('Apply for the Software Engineer internship at TechCorp');
      setJobUrl('http://localhost:8888/mock/techcorp/jobs/swe-intern');
      setViewportData((prev) => ({ ...prev, url: 'http://localhost:8888/mock/techcorp/jobs/swe-intern' }));
    } else if (type === 'greenhouse') {
      setGoal('Apply for Senior AI Engineer at ScaleAI via Greenhouse ATS');
      setJobUrl('http://localhost:8888/mock/greenhouse/jobs/ai-engineer');
      setViewportData((prev) => ({ ...prev, url: 'http://localhost:8888/mock/greenhouse/jobs/ai-engineer' }));
    } else if (type === 'workday') {
      setGoal('Apply for Lead Cloud Infrastructure Architect at CloudScale');
      setJobUrl('http://localhost:8888/mock/workday/jobs/cloud-architect');
      setViewportData((prev) => ({ ...prev, url: 'http://localhost:8888/mock/workday/jobs/cloud-architect' }));
    } else if (type === 'batch') {
      setGoal('Batch apply for AI & Autonomous Systems engineer roles');
      setBatchCount(3);
      alert('Batch Mode Selected: SIVI will queue 3 tech roles with rate-limiting pacing.');
    }
  };

  const handleApplyFromUnstop = (internship: any) => {
    setGoal(`Apply for ${internship.title} at ${internship.company} on Unstop`);
    setJobUrl(internship.url);
    setViewportData((prev) => ({
      ...prev,
      url: internship.url,
      title: `${internship.company} | ${internship.title}`
    }));
    setActiveTab('dashboard');
  };

  const startAgent = () => {
    if (!goal.trim()) {
      alert('Please enter a goal for the agent.');
      return;
    }

    setIsRunning(true);
    setIsThinking(true);
    setReasoningChunks([]);
    setTokenCount(0);
    setCurrentStep(1);
    setAgentStatus('Active (Autonomous Navigation)');

    addAction('INIT', `Initiating autonomous task: "${goal}"`, 'pending');

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname || 'localhost';
    const wsUrl = `${protocol}//${host}:8888/ws/agent`;

    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      ws.current?.send(JSON.stringify({ goal, url: jobUrl, tone, batch_count: batchCount }));
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'reasoning_stream') {
          setIsThinking(true);
          setReasoningChunks((prev) => [...prev, data.chunk]);
          setTokenCount((prev) => prev + Math.max(1, Math.floor(data.chunk.length / 4)));
        } else if (data.type === 'status') {
          setAgentStatus(data.message);
          addAction('STATUS', data.message, 'pending');
        } else if (data.type === 'observation') {
          addAction('OBSERVE', data.message || `Stagehand captured DOM: ${data.data?.title}`, 'success');
        } else if (data.type === 'form_analysis') {
          addAction('ATS INTEL', data.message || `Detected ${data.vendor_name}`, 'success');
        } else if (data.type === 'viewport_update') {
          setViewportData({
            url: data.url || jobUrl,
            title: data.title || '',
            activeSection: data.active_section || '',
            highlights: data.highlight_elements || []
          });
        } else if (data.type === 'thinking') {
          setIsThinking(true);
          if (data.step) setCurrentStep(data.step);
        } else if (data.type === 'skills_match') {
          addAction(
            'MCP MATCH',
            `Matched ${data.matched_skills?.length} skills (${data.match_score}% score) for ${data.candidate_name}`,
            'success'
          );
        } else if (data.type === 'action_result') {
          setIsThinking(false);
          addAction('ACT', typeof data.result === 'string' ? data.result : JSON.stringify(data.result), 'success', data.action);
        } else if (data.type === 'approval_required') {
          setIsThinking(false);
          setRequiresApproval(true);
          setApprovalData(data);
          setAgentStatus('PAUSED (HITL Approval Required)');
          addAction('HITL GATE', 'Suspended execution before destructive action: submit_application', 'warning');
        } else if (data.type === 'status' && data.phase === 'COMPLETED') {
          setIsRunning(false);
          setIsThinking(false);
          setAgentStatus('Application submitted successfully ✓');
          fetchApplications();
          fetchAnalytics();
        }
      } catch (err) {
        console.error('Error parsing WS message:', err);
      }
    };

    ws.current.onerror = (err) => {
      console.error('WebSocket error:', err);
      addAction('WS ERROR', 'Connection to backend orchestrator interrupted.', 'error');
      setIsRunning(false);
      setIsThinking(false);
      setAgentStatus('Connection Error');
    };

    ws.current.onclose = () => {
      setIsRunning(false);
      setIsThinking(false);
    };
  };

  const handleApprovalDecision = async (approved: boolean) => {
    setRequiresApproval(false);

    if (approved) {
      setAgentStatus('Executing Final Submission...');
      try {
        const response = await fetch('http://localhost:8888/ws/approve', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ approved: true, requestId: approvalData?.request_id })
        });
        const result = await response.json();

        addAction('SUBMITTED', `Application Submitted ✓ Confirmation: ${result.result?.confirmation_id || '#TC-APP-2026-9812'}`, 'success');
        setAgentStatus('Application submitted successfully ✓');

        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
          ws.current.send(JSON.stringify({ type: 'approval_response', approved: true }));
        }
        fetchApplications();
        fetchAnalytics();
      } catch (err) {
        console.error('Approval API error:', err);
        addAction('ERROR', 'Failed to transmit approval decision.', 'error');
      }
    } else {
      setAgentStatus('Submission Denied by User');
      addAction('ABORTED', 'Destructive submission cancelled by human operator.', 'warning');
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ type: 'approval_response', approved: false }));
      }
      setIsRunning(false);
    }
  };

  const handleUpdateAppStatus = async (id: string, newStatus: string) => {
    try {
      await fetch(`http://localhost:8888/api/applications/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      fetchApplications();
      fetchAnalytics();
    } catch (e) {
      console.error('Failed to update status:', e);
    }
  };

  const handleScheduleAppInterview = async (id: string, date: string, time: string, round: string) => {
    try {
      await fetch(`http://localhost:8888/api/applications/${id}/interview`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date, time, round })
      });
      fetchApplications();
      fetchAnalytics();
      alert('Interview scheduled! Google Calendar invite link generated.');
    } catch (e) {
      console.error('Failed to schedule interview:', e);
    }
  };

  return (
    <>
      <Head>
        <title>SIVI | Autonomous AI Job Application Agent</title>
        <meta name="description" content="Autonomous AI Agent production prototype for automated job applications" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--bg-primary)' }}>
        {/* Top Header Bar */}
        <header style={{
          background: 'var(--bg-secondary)',
          borderBottom: '1px solid var(--card-border)',
          padding: '12px 28px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          position: 'sticky',
          top: 0,
          zIndex: 100
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.1))',
              border: '1px solid rgba(245, 158, 11, 0.4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--gold)'
            }}>
              <IconZap size={18} />
            </div>
            <span style={{ fontSize: '18px', fontWeight: 800, letterSpacing: '-0.5px', color: '#FFF' }}>
              SIVI
            </span>
            <span style={{
              background: '#1A2130',
              border: '1px solid var(--card-border)',
              color: 'var(--gold-light)',
              padding: '2px 8px',
              borderRadius: '6px',
              fontSize: '11px',
              fontWeight: 700,
              letterSpacing: '0.4px'
            }}>
              AUTONOMOUS AGENT
            </span>
            <span style={{ fontSize: '13px', color: 'var(--text-muted)', fontWeight: 500, display: 'none' }}>
              Everyday Browser Automation
            </span>
          </div>

          {/* Nav Tabs */}
          <div style={{
            display: 'flex',
            gap: '4px',
            background: '#090C13',
            padding: '4px',
            borderRadius: '10px',
            border: '1px solid var(--card-border)'
          }}>
            {[
              { id: 'dashboard', label: 'Dashboard', icon: <IconDashboard size={14} /> },
              { id: 'unstop', label: 'Unstop Internships', icon: <IconSearch size={14} /> },
              { id: 'vault', label: 'Autofill Vault', icon: <IconUserCheck size={14} /> },
              { id: 'tracker', label: `Applications (${applications.length})`, icon: <IconBriefcase size={14} /> },
              { id: 'analytics', label: 'Analytics', icon: <IconChart size={14} /> },
              { id: 'studio', label: 'Cover Letter', icon: <IconSparkles size={14} /> },
              { id: 'integrations', label: 'Integrations', icon: <IconLink size={14} /> }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                style={{
                  background: activeTab === tab.id ? '#1A202E' : 'transparent',
                  border: activeTab === tab.id ? '1px solid #2B3548' : '1px solid transparent',
                  color: activeTab === tab.id ? 'var(--gold-light)' : 'var(--text-muted)',
                  padding: '7px 14px',
                  borderRadius: '7px',
                  fontSize: '13px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '7px',
                  transition: 'all 0.15s ease'
                }}
              >
                {tab.icon}
                <span>{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Right Header Status & Actions */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              background: isRunning ? 'rgba(245, 158, 11, 0.12)' : 'rgba(16, 185, 129, 0.12)',
              border: isRunning ? '1px solid rgba(245, 158, 11, 0.3)' : '1px solid rgba(16, 185, 129, 0.3)',
              color: isRunning ? 'var(--gold)' : 'var(--green)',
              fontSize: '12px',
              fontWeight: 600,
              padding: '5px 12px',
              borderRadius: '9999px'
            }}>
              <span className={isRunning ? 'pulse-indicator' : ''} style={{
                width: '7px',
                height: '7px',
                borderRadius: '50%',
                background: isRunning ? 'var(--gold)' : 'var(--green)'
              }}></span>
              <span>{agentStatus}</span>
            </div>

            <button
              onClick={() => setIsOnboardingOpen(true)}
              title="First-run Tutorial"
              style={{
                background: '#141926',
                border: '1px solid var(--card-border)',
                color: 'var(--text-primary)',
                padding: '6px 12px',
                borderRadius: '8px',
                fontSize: '12px',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <IconHelpCircle size={14} />
              <span>Guide</span>
            </button>

            <button
              onClick={() => setIsNotifOpen(!isNotifOpen)}
              title="Notifications"
              style={{
                background: '#141926',
                border: '1px solid var(--card-border)',
                color: 'var(--text-muted)',
                width: '34px',
                height: '34px',
                borderRadius: '8px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                position: 'relative'
              }}
            >
              <IconBell size={15} />
              <span style={{
                position: 'absolute',
                top: '-3px',
                right: '-3px',
                background: 'var(--red)',
                color: '#FFF',
                fontSize: '9px',
                fontWeight: 800,
                width: '15px',
                height: '15px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                3
              </span>
            </button>
          </div>
        </header>

        {/* Main Viewport Container */}
        <main style={{
          flex: 1,
          padding: '24px',
          maxWidth: '1650px',
          width: '100%',
          margin: '0 auto',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px'
        }}>
          {activeTab === 'dashboard' && (
            <>
              <GoalInput
                goal={goal}
                setGoal={setGoal}
                jobUrl={jobUrl}
                setJobUrl={setJobUrl}
                tone={tone}
                setTone={setTone}
                batchCount={batchCount}
                setBatchCount={setBatchCount}
                isRunning={isRunning}
                onStart={startAgent}
                onSetPreset={handlePreset}
                agentStatus={agentStatus}
              />

              <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1.15fr',
                gap: '20px',
                minHeight: '520px'
              }}>
                <ReasoningStream
                  chunks={reasoningChunks}
                  isThinking={isThinking}
                  currentStep={currentStep}
                  tokenCount={tokenCount}
                />

                <BrowserViewport
                  url={viewportData.url}
                  title={viewportData.title}
                  activeSection={viewportData.activeSection}
                  highlights={viewportData.highlights}
                  isRunning={isRunning}
                />
              </div>

              <ActionLog actions={actions} />
            </>
          )}

          {activeTab === 'unstop' && (
            <UnstopExplorer onApplyWithSivi={handleApplyFromUnstop} />
          )}

          {activeTab === 'vault' && (
            <AutofillVault />
          )}

          {activeTab === 'tracker' && (
            <ApplicationTracker
              applications={applications}
              onRefresh={fetchApplications}
              onUpdateStatus={handleUpdateAppStatus}
              onScheduleInterview={handleScheduleAppInterview}
            />
          )}

          {activeTab === 'analytics' && (
            <Analytics metrics={analyticsData} />
          )}

          {activeTab === 'studio' && (
            <CoverLetterStudio />
          )}

          {activeTab === 'integrations' && (
            <IntegrationHub />
          )}
        </main>

        {/* HITL Safety Approval Modal */}
        <ApprovalGate
          isOpen={requiresApproval}
          data={approvalData}
          onDecision={handleApprovalDecision}
        />

        {/* First-Run Onboarding Modal */}
        <OnboardingModal
          isOpen={isOnboardingOpen}
          onClose={() => setIsOnboardingOpen(false)}
          onLaunchDemo={() => {
            handlePreset('techcorp');
            setTimeout(() => startAgent(), 300);
          }}
        />
      </div>
    </>
  );
}
