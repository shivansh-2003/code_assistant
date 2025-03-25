import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [model, setModel] = useState('gpt-3.5-turbo');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError(null);
  };

  const handleModelChange = (e) => {
    setModel(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file to analyze');
      return;
    }

    const allowedExtensions = ['.py', '.js', '.jsx'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
      setError(`Invalid file type. Allowed types: ${allowedExtensions.join(', ')}`);
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('model', model);

    try {
      // Assuming your FastAPI is running on localhost:8000
      const response = await fetch('http://localhost:8000/analyze/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze code');
      }

      const data = await response.json();
      setResults(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Carbon Crunch - Code Quality Analyzer</h1>
        <p>Upload your React (JavaScript) or FastAPI (Python) code to analyze clean code practices</p>
      </header>

      <div className="card">
        <h2>Upload File</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="file">Select code file (.py, .js, .jsx)</label>
            <input 
              type="file" 
              id="file" 
              onChange={handleFileChange} 
              accept=".py,.js,.jsx"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="model">Select Model</label>
            <select 
              id="model" 
              value={model} 
              onChange={handleModelChange}
            >
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Faster)</option>
              <option value="gpt-4">GPT-4 (More accurate)</option>
            </select>
          </div>
          
          <button 
            type="submit" 
            className="btn-primary" 
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze Code'}
          </button>
        </form>
        
        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}
      </div>

      {loading && (
        <div className="loading-container">
          <div className="loader"></div>
          <p>Analyzing your code... This may take a few moments.</p>
        </div>
      )}

      {results && (
        <div className="results-container">
          <div className="card">
            <h2>Analysis Results</h2>
            
            <div className="score-overview">
              <div className="score-circle" style={{ 
                borderColor: getScoreColor(results.overall_score)
              }}>
                <div className="score-number">{results.overall_score}</div>
                <div className="score-label">Overall Score</div>
              </div>
            </div>
            
            <div className="score-breakdown">
              <h3>Score Breakdown</h3>
              
              <div className="progress-item">
                <div className="progress-label">
                  <span>Naming Conventions</span>
                  <span>{results.breakdown.naming}/10</span>
                </div>
                <div className="progress">
                  <div className="progress-bar" style={{ 
                    width: `${(results.breakdown.naming / 10) * 100}%`,
                    backgroundColor: getScoreColor(results.breakdown.naming, 10)
                  }}></div>
                </div>
              </div>
              
              <div className="progress-item">
                <div className="progress-label">
                  <span>Function Length and Modularity</span>
                  <span>{results.breakdown.modularity}/20</span>
                </div>
                <div className="progress">
                  <div className="progress-bar" style={{ 
                    width: `${(results.breakdown.modularity / 20) * 100}%`,
                    backgroundColor: getScoreColor(results.breakdown.modularity, 20)
                  }}></div>
                </div>
              </div>
              
              <div className="progress-item">
                <div className="progress-label">
                  <span>Comments and Documentation</span>
                  <span>{results.breakdown.comments}/20</span>
                </div>
                <div className="progress">
                  <div className="progress-bar" style={{ 
                    width: `${(results.breakdown.comments / 20) * 100}%`,
                    backgroundColor: getScoreColor(results.breakdown.comments, 20)
                  }}></div>
                </div>
              </div>
              
              <div className="progress-item">
                <div className="progress-label">
                  <span>Formatting/Indentation</span>
                  <span>{results.breakdown.formatting}/15</span>
                </div>
                <div className="progress">
                  <div className="progress-bar" style={{ 
                    width: `${(results.breakdown.formatting / 15) * 100}%`,
                    backgroundColor: getScoreColor(results.breakdown.formatting, 15)
                  }}></div>
                </div>
              </div>
              
              <div className="progress-item">
                <div className="progress-label">
                  <span>Reusability and DRY</span>
                  <span>{results.breakdown.reusability}/15</span>
                </div>
                <div className="progress">
                  <div className="progress-bar" style={{ 
                    width: `${(results.breakdown.reusability / 15) * 100}%`,
                    backgroundColor: getScoreColor(results.breakdown.reusability, 15)
                  }}></div>
                </div>
              </div>
              
              <div className="progress-item">
                <div className="progress-label">
                  <span>Best Practices in Web Dev</span>
                  <span>{results.breakdown.best_practices}/20</span>
                </div>
                <div className="progress">
                  <div className="progress-bar" style={{ 
                    width: `${(results.breakdown.best_practices / 20) * 100}%`,
                    backgroundColor: getScoreColor(results.breakdown.best_practices, 20)
                  }}></div>
                </div>
              </div>
            </div>
            
            <div className="recommendations">
              <h3>Recommendations</h3>
              <ul>
                {results.recommendations.map((rec, index) => (
                  <li key={index} className="recommendation-item">{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
      
      <footer>
        <p>Carbon Crunch &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

// Helper function to determine color based on score
function getScoreColor(score, max = 100) {
  const percentage = (score / max) * 100;
  if (percentage >= 80) return '#28a745'; // green
  if (percentage >= 60) return '#ffc107'; // yellow
  if (percentage >= 40) return '#fd7e14'; // orange
  return '#dc3545'; // red
}

export default App;