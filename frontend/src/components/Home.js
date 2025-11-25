import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();
  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>Welcome to AI Job Board</h1>
      <Button variant="contained" onClick={() => navigate('/jobs')} style={{ margin: '10px' }}>Browse Jobs</Button>
      <Button variant="contained" onClick={() => navigate('/post-job')} style={{ margin: '10px' }}>Post a Job</Button>
      <Button variant="contained" onClick={() => navigate('/candidate-matcher')} style={{ margin: '10px' }}>Find Candidates</Button>
      <Button variant="contained" onClick={() => navigate('/resume-builder')} style={{ margin: '10px' }}>Build Resume</Button>
      <Button variant="contained" onClick={() => navigate('/login')} style={{ margin: '10px' }}>Login/Signup</Button>
    </div>
  );
};

export default Home;
