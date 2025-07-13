import React, { useState } from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface CodeBlockProps {
  inline?: boolean;
  className?: string;
  children: React.ReactNode;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ inline, className, children }) => {
  const [copied, setCopied] = useState(false);
  const code = String(children).trim();

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  if (inline) {
    return (
      <code
        className="inline-code"
        style={{
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          color: '#60a5fa',
          padding: '0.125rem 0.375rem',
          borderRadius: '4px',
          fontSize: '0.875em',
          fontFamily: 'Fira Code, Monaco, Menlo, Ubuntu Mono, monospace',
          border: '1px solid rgba(59, 130, 246, 0.2)',
        }}
      >
        {code}
      </code>
    );
  }

  const language = className?.replace('language-', '') || 'text';

  return (
    <div className="code-block-wrapper">
      <div className="code-block-header">
        <span className="language-label">{language}</span>
        <button
          className="copy-button"
          onClick={handleCopy}
          aria-label="Copy code to clipboard"
          title="Copy code"
        >
          {copied ? (
            <>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="20,6 9,17 4,12"/>
              </svg>
              Copied!
            </>
          ) : (
            <>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
              </svg>
              Copy
            </>
          )}
        </button>
      </div>
      <div className="code-block-content">
        <SyntaxHighlighter 
          language={language} 
          style={oneDark}
          customStyle={{
            margin: 0,
            borderRadius: '0 0 8px 8px',
            fontSize: '0.875rem',
            lineHeight: '1.6',
          }}
          showLineNumbers={code.split('\n').length > 1}
          wrapLines={true}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

export default CodeBlock;