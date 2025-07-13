import React, { useState, useRef, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import CodeBlock from './CodeBlock';
import './CodePayloadIDE.css';

interface AnalysisResponse {
  code: string;
  length: number;
  message: string;
}

const CodePayloadIDE: React.FC = () => {
  const [code, setCode] = useState('');
  const [response, setResponse] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      setCode(content);
      setFileName(file.name);
      setError(null);
    };
    reader.readAsText(file);
  }, []);

  const handleSend = async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/snippets`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error connecting to backend.';
      setError(errorMessage);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setCode('');
    setResponse(null);
    setError(null);
    setFileName('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const target = e.target as HTMLTextAreaElement;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      const newValue = code.substring(0, start) + '  ' + code.substring(end);
      setCode(newValue);
      setTimeout(() => {
        target.selectionStart = target.selectionEnd = start + 2;
      }, 0);
    }
  };

  return (
    <div className="ide-container">
      {/* Editor Section */}
      <div className="editor-section">
        <div className="editor-header">
          <div className="editor-title">
            <h2>Code Editor</h2>
            {fileName && (
              <span className="file-name">{fileName}</span>
            )}
          </div>
          <div className="editor-actions">
            <input
              ref={fileInputRef}
              type="file"
              accept=".py,.js,.ts,.jsx,.tsx,.java,.cpp,.c,.cs,.php,.rb,.go,.rs"
              onChange={handleFileUpload}
              className="file-input"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="btn btn-secondary">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7,10 12,15 17,10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              Upload File
            </label>
            <button onClick={handleClear} className="btn btn-secondary">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 6h18"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>
                <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
              Clear
            </button>
          </div>
        </div>

        <div className="editor-wrapper">
          <textarea
            className="code-editor"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter your code here or upload a file..."
            rows={20}
            spellCheck={false}
            aria-label="Code editor"
          />
          <div className="editor-footer">
            <div className="char-count">
              {code.length} characters
            </div>
            <button 
              onClick={handleSend} 
              disabled={loading || !code.trim()}
              className="btn btn-primary"
            >
              {loading ? (
                <>
                  <svg className="spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 12a9 9 0 11-6.219-8.56"/>
                  </svg>
                  Analyzing...
                </>
              ) : (
                <>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M22 2L11 13"/>
                    <polygon points="22,2 15,22 11,13 2,9"/>
                  </svg>
                  Analyze Code
                </>
              )}
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="15" y1="9" x2="9" y2="15"/>
              <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
            {error}
          </div>
        )}
      </div>

      {/* Results Section */}
      <div className="results-section">
        <div className="results-header">
          <h2>Analysis Results</h2>
          {response && (
            <div className="analysis-meta">
              <span className="meta-item">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10,9 9,9 8,9"/>
                </svg>
                {response.length} chars
              </span>
            </div>
          )}
        </div>

        <div className="results-content">
          {loading ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Analyzing your code...</p>
            </div>
          ) : response ? (
            <div className="analysis-results">
              <ReactMarkdown
                components={{
                  code({className, children, ...props}) {
                    return (
                      <CodeBlock
                        className={className}
                        {...props}
                      >
                        {children}
                      </CodeBlock>
                    );
                  }
                }}
              >
                {response.message}
              </ReactMarkdown>
            </div>
          ) : (
            <div className="empty-state">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
              <h3>No analysis yet</h3>
              <p>Enter some code and click "Analyze Code" to get started</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CodePayloadIDE;
