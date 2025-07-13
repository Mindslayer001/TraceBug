import CodePayloadIDE from './components/CodePayloadIDE';
import './App.css';

function App() {
  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <rect width="32" height="32" rx="8" fill="url(#gradient)"/>
                <path d="M8 12L16 20L24 12" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#3B82F6"/>
                    <stop offset="100%" stopColor="#1D4ED8"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div className="brand">
              <h1 className="brand-title">TraceBug</h1>
              <p className="brand-subtitle">AI-powered code risk analyzer</p>
            </div>
          </div>
          
          <nav className="nav">
            <div className="social-links">
              <a 
                href="https://github.com/mindslayer001/Tracebug" 
                target="_blank" 
                rel="noopener noreferrer"
                className="nav-link social-link"
                aria-label="GitHub"
                title="GitHub"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              
              <a 
                href="https://x.com/ismycodeshit" 
                target="_blank" 
                rel="noopener noreferrer"
                className="nav-link social-link"
                aria-label="X (Twitter)"
                title="X (Twitter)"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </a>
              
              <a 
                href="https://linkedin.com/in/manisankar001" 
                target="_blank" 
                rel="noopener noreferrer"
                className="nav-link social-link"
                aria-label="LinkedIn"
                title="LinkedIn"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
              
              <a 
                href="https://app.daily.dev/ismycodeshit" 
                target="_blank" 
                rel="noopener noreferrer"
                className="nav-link social-link"
                aria-label="daily.dev"
                title="daily.dev"
              >
                <svg width="18" height="18" viewBox="0 0 32 32" fill="currentColor">
                  <path d="M16 0C7.163 0 0 7.163 0 16c0 8.837 7.163 16 16 16s16-7.163 16-16C32 7.163 24.837 0 16 0zm0 2.909c7.236 0 13.091 5.855 13.091 13.091 0 7.236-5.855 13.091-13.091 13.091-7.236 0-13.091-5.855-13.091-13.091C2.909 8.764 8.764 2.909 16 2.909zm0 4.364a8.727 8.727 0 100 17.454 8.727 8.727 0 000-17.454zm0 2.182a6.545 6.545 0 110 13.09 6.545 6.545 0 010-13.09z"/>
                </svg>
              </a>
              <a 
                href="mailto:buildwithmani.dev@gmail.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="nav-link social-link"
                aria-label="Email"
                title="Email"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 2v.01L12 13 4 6.01V6h16zM4 20V8.99l7.29 6.71c.39.36 1.02.36 1.41 0L20 8.99V20H4z"/>
                </svg>
              </a>
              <a 
                href="https://medium.com/@ismycodeshit" 
                target="_blank" 
                rel="noopener noreferrer"
                className="nav-link social-link"
                aria-label="Medium"
                title="Medium"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z"/>
                </svg>
              </a>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main">
        <div className="container">
          <CodePayloadIDE />
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2024 TraceBug. Built with React & TypeScript.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
