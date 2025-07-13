import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const CodeBlock = ({ inline, className, children }: { inline?: boolean; className?: string; children: React.ReactNode }) => {
  const code = String(children).trim();

  if (inline) {
    return (
      <code
        style={{
          backgroundColor: '#001f3f', // deep blue
          color: '#ffffff',
          padding: '2px 6px',
          borderRadius: '4px',
          fontSize: '0.85em',
        }}
      >
        {code}
      </code>
    );
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
  };

  return (
    <div style={{ position: 'relative' }}>
      <SyntaxHighlighter language={className?.replace('language-', '')} style={oneDark}>
        {code}
      </SyntaxHighlighter>
      <button
        style={{
          position: 'absolute',
          top: 8,
          right: 8,
          zIndex: 2,
          padding: '2px 8px',
          fontSize: '0.9em',
          cursor: 'pointer',
        }}
        onClick={handleCopy}
      >
        Copy
      </button>
    </div>
  );
};

export default CodeBlock;