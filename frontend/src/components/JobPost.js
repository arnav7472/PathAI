import { useState } from 'react';
import axios from 'axios';
import { TextField, Button } from '@mui/material';

const JobPost = () => {
  const [title, setTitle] = useState('');
  const [company, setCompany] = useState('');
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');

  const handlePostJob = async () => {
    try {
      await axios.post('http://localhost:5000/api/jobs', { title, company, location, description });
      alert('Job posted successfully!');
    } catch (error) {
      console.error(error);
      alert('Failed to post job.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Post a Job</h1>
      <div style={{ margin: '10px' }}>
        <TextField label="Job Title" fullWidth value={title} onChange={(e) => setTitle(e.target.value)} />
      </div>
      <div style={{ margin: '10px' }}>
        <TextField label="Company" fullWidth value={company} onChange={(e) => setCompany(e.target.value)} />
      </div>
      <div style={{ margin: '10px' }}>
        <TextField label="Location" fullWidth value={location} onChange={(e) => setLocation(e.target.value)} />
      </div>
      <div style={{ margin: '10px' }}>
        <TextField label="Description" fullWidth multiline rows={4} value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>
      <div style={{ margin: '10px' }}>
        <Button variant="contained" onClick={handlePostJob}>Post Job</Button>
      </div>
    </div>
  );
};

export default JobPost;
