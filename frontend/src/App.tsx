import CodePayloadIDE from './components/CodePayloadIDE';
import './components/CodePayloadIDE.css';

function App() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)',
      padding: '2rem',
      color: '#e0e7ef'
    }}>
      {/* Header Section */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '1.5rem',
          marginBottom: '2rem'
        }}
      >
        <img
          src="src/assets/logo.png"
          alt="TraceBit Logo"
          style={{
            height: '56px',
            width: '56px',
            borderRadius: '12px',
            boxShadow: '0 2px 8px rgba(59,130,246,0.18)',
            border: '1px solid #334155',
            objectFit: 'cover',
            background: '#1e293b'
          }}
        />
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <h1
            style={{
              fontSize: '2.5rem',
              fontWeight: 800,
              color: '#60a5fa',
              letterSpacing: '-0.02em',
              textShadow: '0 2px 6px rgba(59,130,246,0.18)',
              marginBottom: '0.25rem'
            }}
          >
            TraceBug
          </h1>
          <span
            style={{
              fontSize: '1rem',
              color: '#94a3b8',
              fontWeight: 600
            }}
          >
AI-powered risk analyzer using Python AST + LLMs. Intelligently finds, annotates, and corrects risky code by analyzing AST and feeding it to an LLM for judgment.          </span>
        </div>
        <a
          href="https://github.com/mindslayer001/Tracebug"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            marginLeft: '1.5rem',
            padding: '0.5rem 1rem',
            background: '#334155',
            color: '#e0e7ef',
            borderRadius: '8px',
            boxShadow: '0 2px 8px rgba(59,130,246,0.22)',
            fontWeight: 600,
            textDecoration: 'none',
            transition: 'background 0.2s'
          }}
          onMouseOver={e => (e.currentTarget.style.background = '#1e293b')}
          onMouseOut={e => (e.currentTarget.style.background = '#334155')}
        >
          GitHub
        </a>
      </div>
      {/* Main Content */}
      <div style={{
        width: '99vw',
        marginLeft: 'calc(-2rem)',
        marginRight: 'calc(-2rem)',
        minHeight: 'calc(100vh - 140px)',
        display: 'flex',
        alignItems: 'stretch'
      }}>
        <CodePayloadIDE />
      </div>
    </div>
  );
}

export default App;
