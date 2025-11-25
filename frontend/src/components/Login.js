import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, TextField, Alert, CircularProgress } from '@mui/material';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const handleAuth = async () => {
    setError('');
    setSuccess('');
    
    // Validate inputs
    if (!email || !password) {
      setError('Email and password are required');
      return;
    }

    if (!isLogin && !name) {
      setError('Name is required for registration');
      return;
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address');
      return;
    }

    setLoading(true);

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const payload = isLogin
        ? { email, password }
        : { name, email, password };

      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      // Handle response parsing safely
      let data;
      try {
        data = await response.json();
      } catch (parseError) {
        setError(`Server error: ${response.status} ${response.statusText}`);
        setLoading(false);
        return;
      }

      if (!response.ok) {
        setError(data?.detail || data?.message || 'Authentication failed');
        setLoading(false);
        return;
      }

      // Validate response data
      if (!data?.access_token || !data?.user) {
        setError('Invalid response from server');
        setLoading(false);
        return;
      }

      // Store token and user info
      localStorage.setItem('accessToken', data.access_token);
      localStorage.setItem('userId', data.user_id);
      localStorage.setItem('userName', data.user?.name || '');
      localStorage.setItem('userEmail', data.user?.email || '');

      setSuccess(isLogin ? 'Logged in successfully!' : 'Signed up successfully!');
      setTimeout(() => {
        navigate('/jobs');
      }, 1500);
    } catch (error) {
      setError(`Error: ${error?.message || 'An error occurred. Please check your backend connection.'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h1>{isLogin ? 'Login' : 'Sign Up'}</h1>
      
      {error && <Alert severity="error" style={{ marginBottom: '10px' }}>{error}</Alert>}
      {success && <Alert severity="success" style={{ marginBottom: '10px' }}>{success}</Alert>}
      
      {!isLogin && (
        <div style={{ margin: '10px' }}>
          <TextField
            label="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            fullWidth
            disabled={loading}
          />
        </div>
      )}
      
      <div style={{ margin: '10px' }}>
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
          disabled={loading}
        />
      </div>
      
      <div style={{ margin: '10px' }}>
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          fullWidth
          disabled={loading}
        />
      </div>
      
      <div style={{ margin: '10px' }}>
        <Button
          variant="contained"
          onClick={handleAuth}
          disabled={loading}
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : isLogin ? 'Login' : 'Sign Up'}
        </Button>
      </div>
      
      <div style={{ margin: '10px' }}>
        <Button onClick={() => setIsLogin(!isLogin)} fullWidth>
          {isLogin ? 'Need an account? Sign Up' : 'Have an account? Login'}
        </Button>
      </div>
    </div>
  );
};

export default Login;
