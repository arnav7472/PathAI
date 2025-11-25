import { useLocation, useNavigate } from 'react-router-dom';
import { Button, Card, CardContent, LinearProgress, Chip } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import './CandidateProfile.css';

const CandidateProfile = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const candidate = location.state?.candidate;

  if (!candidate) {
    return (
      <div className="candidate-profile">
        <div className="container">
          <p>No candidate data available. Please go back and select a candidate.</p>
          <Button
            variant="contained"
            onClick={() => navigate('/candidate-matcher')}
            startIcon={<ArrowBackIcon />}
          >
            Back to Candidate Matcher
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="candidate-profile">
      <div className="container">
        <Button
          variant="text"
          onClick={() => navigate('/candidate-matcher')}
          startIcon={<ArrowBackIcon />}
          style={{ marginBottom: '20px' }}
        >
          Back to Results
        </Button>

        <Card className="profile-card">
          <CardContent>
            <h1>{candidate.name}</h1>
            <p className="email">{candidate.email}</p>

            <div className="match-info">
              <div className="match-item">
                <h3>Overall Match Score</h3>
                <div className="score-display">{candidate.match_score}%</div>
                <LinearProgress variant="determinate" value={candidate.match_score} />
              </div>
              <div className="match-item">
                <h3>Skill Match</h3>
                <div className="score-display">{candidate.skill_match}%</div>
                <LinearProgress variant="determinate" value={candidate.skill_match} />
              </div>
              <div className="match-item">
                <h3>Text Similarity</h3>
                <div className="score-display">{candidate.text_similarity}%</div>
                <LinearProgress variant="determinate" value={candidate.text_similarity} />
              </div>
            </div>

            <section className="section">
              <h2>Resume</h2>
              <div className="resume-content">
                {candidate.resume}
              </div>
            </section>

            <section className="section">
              <h2>Matching Skills</h2>
              <div className="chip-container">
                {candidate.matching_skills.length > 0 ? (
                  candidate.matching_skills.map((skill) => (
                    <Chip
                      key={skill}
                      label={skill}
                      color="success"
                      variant="outlined"
                      className="skill-chip matching"
                    />
                  ))
                ) : (
                  <p>No matching skills identified</p>
                )}
              </div>
            </section>

            <section className="section">
              <h2>Missing Skills</h2>
              <div className="chip-container">
                {candidate.missing_skills.length > 0 ? (
                  candidate.missing_skills.map((skill) => (
                    <Chip
                      key={skill}
                      label={skill}
                      color="error"
                      variant="outlined"
                      className="skill-chip missing"
                    />
                  ))
                ) : (
                  <p>All required skills are present!</p>
                )}
              </div>
            </section>

            <div className="action-buttons">
              <Button variant="contained" color="primary" fullWidth>
                Schedule Interview
              </Button>
              <Button variant="outlined" color="primary" fullWidth>
                Send Message
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default CandidateProfile;
