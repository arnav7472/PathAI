import { useState } from 'react';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';
import { Button, TextField } from '@mui/material';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true);

  const handleAuth = async () => {
    try {
      if (isLogin) {
        await signInWithEmailAndPassword(auth, email, password);
      } else {
        await createUserWithEmailAndPassword(auth, email, password);
      }
      alert(isLogin ? 'Logged in successfully!' : 'Signed up successfully!');
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>{isLogin ? 'Login' : 'Sign Up'}</h1>
      <div style={{ margin: '10px' }}>
        <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div style={{ margin: '10px' }}>
        <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <div style={{ margin: '10px' }}>
        <Button variant="contained" onClick={handleAuth}>{isLogin ? 'Login' : 'Sign Up'}</Button>
      </div>
      <div style={{ margin: '10px' }}>
        <Button onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? 'Need an account? Sign Up' : 'Have an account? Login'}
        </Button>
      </div>
    </div>
  );
};

export default Login;
