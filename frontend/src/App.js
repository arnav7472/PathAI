import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Button, Box } from '@mui/material';
import Home from './components/Home';
import Login from './components/Login';
import JobList from './components/JobList';
import JobPost from './components/JobPost';
import ResumeBuilder from './components/ResumeBuilder';
import AICandidateMatcher from './components/AICandidateMatcher';
import CandidateProfile from './components/CandidateProfile';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = React.useState(!!localStorage.getItem('accessToken'));

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('userName');
    localStorage.removeItem('userEmail');
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <AppBar position="static" sx={{ backgroundColor: '#1976d2' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            <Link to="/" style={{ textDecoration: 'none', color: 'white' }}>
              PathAI - AI Job Platform
            </Link>
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            {isLoggedIn ? (
              <>
                <Button color="inherit" component={Link} to="/jobs">
                  Jobs
                </Button>
                <Button color="inherit" component={Link} to="/post-job">
                  Post Job
                </Button>
                <Button color="inherit" component={Link} to="/resume-builder">
                  Resume Builder
                </Button>
                <Button
                  color="inherit"
                  onClick={() => {
                    handleLogout();
                    window.location.href = '/login';
                  }}
                >
                  Logout
                </Button>
              </>
            ) : (
              <Button color="inherit" component={Link} to="/login">
                Login
              </Button>
            )}
          </Box>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login onLoginSuccess={() => setIsLoggedIn(true)} />} />
          <Route path="/jobs" element={<JobList />} />
          <Route path="/post-job" element={<JobPost />} />
          <Route path="/resume-builder" element={<ResumeBuilder />} />
          <Route path="/candidate-matcher" element={<AICandidateMatcher />} />
          <Route path="/candidate-profile" element={<CandidateProfile />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
