import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import CodeBlock from './CodeBlock'; // Assuming CodeBlock is in the same directory
import './CodePayloadIDE.css';

const API_URL = 'http://127.0.0.1:8000/snippets'; // Adjust if your backend is on a different port

const CodePayloadIDE: React.FC = () => {
  const [code, setCode] = useState('');
  const [response, setResponse] = useState<{ code: string; length: number; message: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    setLoading(true);
    try {
      const res = await fetch(API_URL, {
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
          style={{ color: 'black' }}
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
            <div style={{ color: 'black' }}><strong style={{ color: 'black' }}>Length:</strong> {response.length}</div>
            <div style={{ color: 'black' }}>
              <ReactMarkdown
                components={{
                  code: CodeBlock
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
