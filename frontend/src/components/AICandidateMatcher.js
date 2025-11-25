import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, TextField, Card, CardContent, LinearProgress, Alert, CircularProgress } from '@mui/material';
import './AICandidateMatcher.css';

const AICandidateMatcher = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [rankedCandidates, setRankedCandidates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [jobSkills, setJobSkills] = useState([]);
  const navigate = useNavigate();
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const findCandidates = async () => {
    setError('');
    setLoading(true);

    try {
      const token = localStorage.getItem('accessToken');
      
      const response = await fetch(`${apiUrl}/candidates/find`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          job_description: jobDescription,
          limit: 10
        })
      });

      // Handle network errors
      if (!response.ok) {
        let errorMessage = 'Failed to find candidates';
        try {
          const data = await response.json();
          errorMessage = data.detail || data.message || errorMessage;
        } catch (parseError) {
          // If response is not JSON, use default message
          errorMessage = `Server error: ${response.status} ${response.statusText}`;
        }
        setError(errorMessage);
        setLoading(false);
        return;
      }

      // Safely parse JSON response
      let data;
      try {
        data = await response.json();
      } catch (parseError) {
        setError('Invalid response format from server');
        setLoading(false);
        return;
      }

      // Validate response data structure
      if (!data || typeof data !== 'object') {
        setError('Invalid response data from server');
        setLoading(false);
        return;
      }

      setRankedCandidates(data.candidates || []);
      setJobSkills(data.job_skills || []);
    } catch (error) {
      const errorMessage = error?.message || 'An error occurred while finding candidates';
      setError(`Error: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleViewProfile = (candidate) => {
    navigate('/candidate-profile', { state: { candidate } });
  };

  const viewProfile = (candidateId) => {
    navigate(`/candidate/${candidateId}`, { state: { candidate: rankedCandidates.find(c => c.id === candidateId) } });
  };

  return (
    <div className="ai-candidate-matcher">
      <div className="container">
        <h1>🤖 AI-Powered Candidate Matcher</h1>
        <p className="subtitle">Find the best candidates for your job using intelligent matching</p>

        {error && <Alert severity="error" style={{ marginBottom: '20px' }}>{error}</Alert>}

        <Card className="input-card">
          <CardContent>
            <TextField
              label="Job Description or Requirements"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              fullWidth
              multiline
              rows={4}
              placeholder="Describe the job, required skills, experience level, etc..."
              disabled={loading}
              variant="outlined"
            />
            <Button
              variant="contained"
              color="primary"
              onClick={findCandidates}
              disabled={loading || jobDescription.length < 10}
              fullWidth
              style={{ marginTop: '15px', padding: '12px' }}
              size="large"
            >
              {loading ? <CircularProgress size={24} /> : 'Find Best Candidates'}
            </Button>
          </CardContent>
        </Card>

        {jobSkills.length > 0 && (
          <div className="skills-container">
            <h3>Identified Job Skills:</h3>
            <div className="skills-list">
              {jobSkills.map((skill) => (
                <span key={skill} className="skill-badge">{skill}</span>
              ))}
            </div>
          </div>
        )}

        {loading && <CircularProgress style={{ display: 'block', margin: '40px auto' }} />}

        <div className="results-container">
          {rankedCandidates.length > 0 ? (
            <div>
              <h2>Top Matching Candidates ({rankedCandidates.length})</h2>
              <div className="candidates-grid">
                {rankedCandidates.map((candidate) => (
                  <Card key={candidate.id} className="candidate-card">
                    <CardContent>
                      <div className="candidate-header">
                        <div>
                          <h3 className="candidate-name">{candidate.name}</h3>
                          <p className="candidate-email">{candidate.email}</p>
                        </div>
                        <div className="match-score">
                          <div className="score-number">{candidate.match_score}%</div>
                          <div className="score-label">Overall Match</div>
                        </div>
                      </div>

                      <div className="score-details">
                        <div className="score-row">
                          <span>Skill Match:</span>
                          <LinearProgress variant="determinate" value={candidate.skill_match} style={{ width: '150px' }} />
                          <span>{candidate.skill_match}%</span>
                        </div>
                        <div className="score-row">
                          <span>Text Similarity:</span>
                          <LinearProgress variant="determinate" value={candidate.text_similarity} style={{ width: '150px' }} />
                          <span>{candidate.text_similarity}%</span>
                        </div>
                      </div>

                      <div className="resume-preview">
                        <p>{candidate.resume.substring(0, 150)}...</p>
                      </div>

                      <div className="skills-section">
                        <div className="matching-skills">
                          <h4>Matching Skills:</h4>
                          <div className="skill-tags">
                            {candidate.matching_skills.length > 0 ? (
                              candidate.matching_skills.map((skill) => (
                                <span key={skill} className="skill-tag matching">{skill}</span>
                              ))
                            ) : (
                              <span className="no-skills">No matching skills</span>
                            )}
                          </div>
                        </div>

                        <div className="missing-skills">
                          <h4>Missing Skills:</h4>
                          <div className="skill-tags">
                            {candidate.missing_skills.length > 0 ? (
                              candidate.missing_skills.slice(0, 3).map((skill) => (
                                <span key={skill} className="skill-tag missing">{skill}</span>
                              ))
                            ) : (
                              <span className="no-skills">All skills covered!</span>
                            )}
                          </div>
                        </div>
                      </div>

                      <Button
                        variant="outlined"
                        color="primary"
                        fullWidth
                        onClick={() => handleViewProfile(candidate)}
                        style={{ marginTop: '15px' }}
                      >
                        View Full Profile
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          ) : (
            !loading && jobDescription.length >= 10 && (
              <div className="no-results">
                <p>Click "Find Best Candidates" to see results</p>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default AICandidateMatcher;
