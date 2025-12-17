import Link from 'next/link';

export default function Home() {
  return (
    <main>
      <header className="glass-header">
        <div className="flex items-center gap-4">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-400 to-purple-500"></div>
          <h1 style={{ fontSize: '1.5rem' }}>RegTech <span className="text-gradient">Horizon</span></h1>
        </div>
        <div className="flex gap-4">
          <span className="status-badge status-ok">System Healthy</span>
          <div className="w-8 h-8 rounded-full bg-gray-700"></div>
        </div>
      </header>

      <div className="dashboard-grid">
        {/* NCC Module Card */}
        <div className="glass-panel">
          <div className="flex justify-between items-start mb-4">
            <h3>NCC (Nigeria Telecom)</h3>
            <span className="status-badge status-warn">Action Required</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">N452M</span>
            <span className="stat-label">AOL Payable</span>
          </div>
          <div className="mt-4 flex flex-col gap-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted">Levy Status</span>
              <span>Pending Approval</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted">QoS Breaches</span>
              <span className="text-red-400">2 Detected</span>
            </div>
          </div>
          <button className="btn-primary mt-6 w-full">View Compliance Report</button>
        </div>

        {/* FCC Module Card */}
        <div className="glass-panel">
          <div className="flex justify-between items-start mb-4">
            <h3>FCC (USA Telecom)</h3>
            <span className="status-badge status-ok">Compliant</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">98.5%</span>
            <span className="stat-label">Form 477 Coverage</span>
          </div>
          <div className="mt-4 flex flex-col gap-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted">USF Contribution</span>
              <span>$51,900</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted">CPNI Audit</span>
              <span>Certified</span>
            </div>
          </div>
          <button className="btn-primary mt-6 w-full" style={{ background: 'rgba(255,255,255,0.1)' }}>View Maps</button>
        </div>

        {/* CBN Module Card */}
        <div className="glass-panel">
          <div className="flex justify-between items-start mb-4">
            <h3>CBN (FinTech)</h3>
            <span className="status-badge status-alert">High Alert</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">4</span>
            <span className="stat-label">AML Flags (CTR > 5M)</span>
          </div>
          <div className="mt-4 flex flex-col gap-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted">Cybersecurity Levy</span>
              <span>N500,432</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted">Capital Adequacy</span>
              <span className="text-green-400">12.5% (Safe)</span>
            </div>
          </div>
          <button className="btn-primary mt-6 w-full" style={{ background: 'rgba(255,77,77,0.2)', color: '#ff4d4d' }}>Review Transactions</button>
        </div>

        {/* Live Stream Panel */}
        <div className="glass-panel" style={{ gridColumn: '1 / -1' }}>
          <h2>Live Ingestion Swarm</h2>
          <div className="mt-4" style={{ height: '200px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <code style={{ color: '#00f2ea' }}>
              [STREAM: TELECOM_CDR] Processing 14,000 events/sec... <br />
              [STREAM: BANKING_TX]  Detected ISO message type 0200 from Node_A <br />
              [STREAM: CPNI_LOG]    Access granted: User_77 (Role: Admin)
            </code>
          </div>
        </div>
      </div>
    </main>
  );
}
