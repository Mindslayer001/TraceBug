import { useState, useEffect} from 'react';

const CodeSender = () => {
  const [code, setCode] = useState('');
  const [health,setHealth] = useState('');
  const [response, setResponse] = useState<string | null>(null);

  const sendCode = async () => {
    try {
      const res = await fetch('http://localhost:8000/snippets/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });

      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error('Error sending code:', err);
      setResponse('Failed to send code');
    }
  };

  useEffect(() => {
    const fetchHealth = async () => {
    try {
      const res = await fetch('http://localhost:8000/health/');
      const data = await res.json();
      setHealth(JSON.stringify(data, null, 2));
      console.log(health)
    } catch (err) {
      console.error('Error fetching health:', err);
      setHealth('Failed to fetch health');
    }
  };

  fetchHealth(); 
    return () => {
      return
    }
  }, [])
  
  return (
    <div className="p-4 max-w-2xl mx-auto space-y-4">
      <h2> Health: {health}</h2>
      <h2 className="text-xl font-semibold">Submit Code Snippet</h2>
      <textarea
        className="w-full h-40 p-2 border rounded-md font-mono"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Paste your code here..."
      />
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        onClick={sendCode}
      >
        Send to Backend
      </button>
      {response && (
        <pre className="bg-gray-100 p-3 rounded-md text-sm overflow-x-auto">{response}</pre>
      )}
    </div>
  );
};

export default CodeSender;
