import React from 'react';
import CodePayloadIDE from './components/CodePayloadIDE';
import './components/CodePayloadIDE.css';

function App() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">TraceBit</h1>
      <CodePayloadIDE />
    </div>
  );
}

export default App;
