import { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Typography } from '@mui/material';

const ResumeBuilder = () => {
  const [skills, setSkills] = useState('');
  const [experience, setExperience] = useState('');
  const [education, setEducation] = useState('');
  const [resume, setResume] = useState('');

  const handleGenerateResume = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/ai/generate-resume', {
        skills: skills.split(','),
        experience,
        education
      });
      setResume(response.data.resume);
    } catch (error) {
      console.error(error);
      alert('Failed to generate resume.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Resume Builder</h1>
      <div style={{ margin: '10px' }}>
        <TextField label="Skills (comma-separated)" fullWidth value={skills} onChange={(e) => setSkills(e.target.value)} />
      </div>
      <div style={{ margin: '10px' }}>
        <TextField label="Experience" fullWidth multiline rows={4} value={experience} onChange={(e) => setExperience(e.target.value)} />
      </div>
      <div style={{ margin: '10px' }}>
        <TextField label="Education" fullWidth multiline rows={4} value={education} onChange={(e) => setEducation(e.target.value)} />
      </div>
      <div style={{ margin: '10px' }}>
        <Button variant="contained" onClick={handleGenerateResume}>Generate Resume</Button>
      </div>
      <div style={{ margin: '10px', whiteSpace: 'pre-wrap' }}>
        <Typography>{resume}</Typography>
      </div>
    </div>
  );
};

export default ResumeBuilder;
