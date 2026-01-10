import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Trash2, RefreshCw, Activity, MessageSquare, Database, ChevronRight } from 'lucide-react';
import GraphView from './GraphView';
import './index.css';

interface Message {
  role: 'user' | 'system';
  content: string;
}

interface Status {
  status: string;
  node_count: number;
  edge_count: number;
  provider: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [status, setStatus] = useState<Status | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState<'chat' | 'transform'>('chat');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, [activeTab]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    fetchStatus();
    fetchGraph();
    fetchSuggestions();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await axios.get('/api/status');
      setStatus(res.data);
    } catch (err) {
      console.error('Failed to fetch status', err);
    }
  };

  const fetchGraph = async () => {
    try {
      const res = await axios.get('/api/graph');
      setGraphData(res.data);
    } catch (err) {
      console.error('Failed to fetch graph', err);
    }
  };

  const fetchSuggestions = async () => {
    try {
      const res = await axios.get('/api/suggestions');
      setSuggestions(res.data.suggestions);
    } catch (err) {
      console.error('Failed to fetch suggestions', err);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = input;
    const currentTab = activeTab;
    console.log(`Sending ${currentTab} request:`, userMsg);
    
    setInput('');
    setMessages(prev => [...prev, { 
      role: 'user', 
      content: userMsg,
      type: currentTab 
    }]);
    setIsLoading(true);

    try {
      if (currentTab === 'chat') {
        const res = await axios.post('/api/chat', { message: userMsg });
        setMessages(prev => [...prev, { role: 'system', content: res.data.reply }]);
      } else {
        const res = await axios.post('/api/transform', { instruction: userMsg });
        setMessages(prev => [...prev, { 
          role: 'system', 
          content: res.data.message,
          type: 'transform'
        }]);
      }
      fetchGraph();
      fetchStatus();
    } catch (err) {
      console.error(`Error in ${currentTab}:`, err);
      setMessages(prev => [...prev, { role: 'system', content: `Error: Failed to process ${currentTab} request.` }]);
    } finally {
      setIsLoading(false);
      fetchSuggestions(); // Refresh suggestions for context
    }
  };

  const handleClear = async () => {
    if (!confirm('Are you sure you want to clear the knowledge graph?')) return;
    try {
      await axios.post('/api/clear');
      setMessages([]);
      fetchGraph();
      fetchStatus();
    } catch (err) {
      alert('Failed to clear graph');
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <div className="brand-icon">
            <Activity size={20} color="white" />
          </div>
          <h1 className="brand-name">MetaCognito</h1>
        </div>

        <div className="nav-group">
          <button 
            onClick={() => setActiveTab('chat')}
            className={`nav-item ${activeTab === 'chat' ? 'active' : ''}`}
          >
            <MessageSquare size={18} />
            <span>Story Engine</span>
          </button>
          <button 
             onClick={() => setActiveTab('transform')}
            className={`nav-item ${activeTab === 'transform' ? 'active' : ''}`}
          >
            <RefreshCw size={18} />
            <span>Transformations</span>
          </button>
        </div>

        <div className="sidebar-footer">
          <div className="status-card">
            <div className="status-header">
              <span>System Status</span>
              <div className="status-dot">
                <div className="dot" />
                <span>Online</span>
              </div>
            </div>
            
            <div className="stats-grid">
              <div className="stat-box">
                <span className="stat-label">Entities</span>
                <span className="stat-value">{status?.node_count || 0}</span>
              </div>
              <div className="stat-box">
                <span className="stat-label">Relations</span>
                <span className="stat-value">{status?.edge_count || 0}</span>
              </div>
            </div>

            <button onClick={handleClear} className="btn-danger">
              <Trash2 size={16} />
              Clear Graph
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Graph Pane */}
        <div className="graph-pane">
           <div className="graph-label">
              <Database size={14} />
              <span>Knowledge Graph View</span>
           </div>
           <GraphView nodes={graphData.nodes} edges={graphData.edges} />
        </div>

        {/* Interaction Pane */}
        <div className="interaction-pane">
            <div className="messages-list">
              {messages.length === 0 && (
                <div className="empty-state">
                  <div className="empty-icon">
                    <MessageSquare size={24} />
                  </div>
                  <p>
                    {activeTab === 'chat' 
                      ? "No narrative history. Start by describing an action." 
                      : "No transformations applied yet. Enter an instruction to update the knowledge graph."}
                  </p>
                  {activeTab === 'chat' && suggestions.length > 0 && (
                    <div className="suggestions-container">
                      <p className="suggestions-title">Inspiration:</p>
                      <div className="suggestions-list-ui">
                        {suggestions.map((s, i) => (
                          <button 
                            key={i} 
                            className="suggestion-chip"
                            onClick={() => {
                              setInput(s);
                              inputRef.current?.focus();
                            }}
                          >
                            {s}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
              {messages.map((msg: any, idx) => (
                <div key={idx} className={`message-wrapper ${msg.role}`}>
                  <div className="message-bubble">
                    {msg.type === 'transform' && (
                      <div style={{ 
                        fontSize: '0.7rem', 
                        fontWeight: 700, 
                        color: 'var(--primary)', 
                        marginBottom: '4px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}>
                        <RefreshCw size={10} />
                        TRANSFORMATION
                      </div>
                    )}
                    {msg.content}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            <form 
              className="input-area" 
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
            >
              <div className="input-container">
                <div className="input-icon">
                  {activeTab === 'chat' ? <ChevronRight size={20} /> : <RefreshCw size={20} />}
                </div>
                <input 
                  type="text"
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={activeTab === 'chat' ? "Describe a story action..." : "Enter graph transformation..."}
                  className="input-field"
                />
                <button 
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className="send-btn"
                >
                  <Send size={18} />
                </button>
              </div>
              <div className="input-status">
                   {isLoading ? 'MetaCognito is thinking...' : 'Orchestration Engine Ready'}
              </div>
            </form>
        </div>
      </div>
    </div>
  );
}

export default App;
