import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, Button } from '@mui/material';

const JobList = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/jobs')
      .then((res) => setJobs(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Job Listings</h1>
      {jobs.map((job) => (
        <Card key={job.id} style={{ margin: '10px' }}>
          <CardContent>
            <Typography variant="h5">{job.title}</Typography>
            <Typography>{job.company}</Typography>
            <Typography>{job.location}</Typography>
            <Typography>{job.description}</Typography>
            <Button variant="contained">Apply</Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default JobList;
