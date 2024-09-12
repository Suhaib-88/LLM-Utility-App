import React, { useState } from 'react';
import './App.css';

function App() {
  const [model, setModel] = useState('');
  const [embedding, setEmbedding] = useState('');
  const [vectorStore, setVectorStore] = useState('');
  const [chain, setChain] = useState('');
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState('');

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    const requestData = {
      model,
      embedding,
      vectorStore,
      chain,
      inputText
    };

    try {
      const res = await fetch('/api/run-chain', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      const result = await res.json();
      setResponse(result.response);
    } catch (error) {
      console.error('Error:', error);
      setResponse('An error occurred. Please try again.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>LangChain Utility Application</h1>
      </header>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Choose a model:</label>
          <select value={model} onChange={(e) => setModel(e.target.value)} required>
            <option value="">Select Model</option>
            <option value="OpenAI">OpenAI</option>
            <option value="Hugging Face">Hugging Face</option>
          </select>
        </div>

        <div className="form-group">
          <label>Choose an embedding:</label>
          <select value={embedding} onChange={(e) => setEmbedding(e.target.value)} required>
            <option value="">Select Embedding</option>
            <option value="OpenAI">OpenAI</option>
            <option value="Sentence Transformers">Sentence Transformers</option>
          </select>
        </div>

        <div className="form-group">
          <label>Choose a vector store:</label>
          <select value={vectorStore} onChange={(e) => setVectorStore(e.target.value)} required>
            <option value="">Select Vector Store</option>
            <option value="FAISS">FAISS</option>
            <option value="Pinecone">Pinecone</option>
          </select>
        </div>

        <div className="form-group">
          <label>Choose a chain mechanism:</label>
          <select value={chain} onChange={(e) => setChain(e.target.value)} required>
            <option value="">Select Chain</option>
            <option value="Sequential Chain">Sequential Chain</option>
            <option value="Agent-based Chain">Agent-based Chain</option>
          </select>
        </div>

        <div className="form-group">
          <label>Enter your text:</label>
          <textarea 
            value={inputText} 
            onChange={(e) => setInputText(e.target.value)} 
            rows="4"
            placeholder="Enter the text you want to process"
            required
          />
        </div>

        <button type="submit">Run Chain</button>
      </form>

      {response && (
        <div className="response">
          <h2>Response:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default App;
