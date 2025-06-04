import {useEffect, useState} from "react";
import { useNavigate } from 'react-router-dom';
import './Login.css'
import "./Buttons.css"

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate();

    useEffect(() => {
        document.body.style.overflow = "hidden";
        return () => {
            document.body.style.overflow = "auto";
        };
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');   // clean previous error

        try {
            const res = await fetch("/users/login", {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password}),
            });

            if(!res.ok) {       // if status is not 2xx
                const data = await res.json();
                setError(data.message);
                return;
            }

            // everything ok
            const data = await res.json();
            localStorage.setItem('token', data.token);

            const payload = JSON.parse(atob(data.token.split('.')[1]));     // get role from token

            if (payload.role === 'admin') {
                navigate('/admin');
            } else {
                navigate('/user');
            }
        } catch (error) {
            setError("Server connection error");
        }
    }

    return (
        <div className="login-container">
            <form onSubmit={handleSubmit} className="login-form">
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    required
                />
                <button className="btn btn-yellow" type="submit">
                    {'Sign in'}
                </button>

            </form>
            {error && (
                <div className="error-popup">
                    <span>{error}</span>
                    <button onClick={() => setError('')}>✖</button>
                </div>
            )}
        </div>
    );
}
export default Login;