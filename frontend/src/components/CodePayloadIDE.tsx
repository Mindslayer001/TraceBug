import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import CodeBlock from './CodeBlock'; // Assuming CodeBlock is in the same directory
import './CodePayloadIDE.css';

const CodePayloadIDE: React.FC = () => {
  const [code, setCode] = useState('');
  const [response, setResponse] = useState<{ code: string; length: number; message: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/snippets`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });
      const data = await res.json();
      setResponse(data);
      console.log('Response:', data);
    } catch (err) {
      setResponse({ code, length: code.length, message: 'Error connecting to backend.' });
      console.error('Error:', err);
    }
    setLoading(false);
  };

  return (
    <div className="leetcode-layout">
      <div className="editor-pane">
        <h2>Code Editor</h2>
        <textarea
          style={{ color: 'grey' }}
          value={code}
          onChange={e => setCode(e.target.value)}
          rows={20}
          cols={40}
          placeholder="Write your code here..."
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
      <div className="response-pane">
        <h2>Response</h2>
        {response ? (
          <>
            <div style={{ color: 'white' }}><strong style={{ color: 'white' }}>Length:</strong> {response.length}</div>
            <div style={{ color: 'white' }}>
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
              >{response.message}</ReactMarkdown>
            </div>
          </>
        ) : (
          <div>No response yet.</div>
        )}
      </div>
    </div>
  );
};

export default CodePayloadIDE;
