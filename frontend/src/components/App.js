import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import JobList from './components/JobList';
import JobPost from './components/JobPost';
import ResumeBuilder from './components/ResumeBuilder';
import AICandidateMatcher from './components/AICandidateMatcher';
import CandidateProfile from './components/CandidateProfile';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/jobs" element={<JobList />} />
        <Route path="/post-job" element={<JobPost />} />
        <Route path="/resume-builder" element={<ResumeBuilder />} />
        <Route path="/candidate-matcher" element={<AICandidateMatcher />} />
        <Route path="/candidate-profile" element={<CandidateProfile />} />
      </Routes>
    </Router>
  );
}

export default App;
