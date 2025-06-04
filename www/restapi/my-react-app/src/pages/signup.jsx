import React, {useEffect} from "react";
import {useNavigate} from "react-router-dom";
import "./Login.css"        // i want to sign up has the same style as log in
import "./Buttons.css"

function Signup() {
    const [username, setUsername] = React.useState("");
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");
    const [error, setError] = React.useState("");

    const navigate = useNavigate();

    useEffect(() => {
        document.body.style.overflow = "hidden";
        return () => {
            document.body.style.overflow = "auto";
        };
    }, []);

    const handleRegistration = async (event) => {
        event.preventDefault();
        setError(" ");

        try {
            const response = await fetch("/users/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username, email, password})
            });

            if (!response.ok) {
                const data = await response.json();
                setError(data.message);
                return;
            }
            const data = await response.json();

            navigate("/login");
        } catch (error) {
            setError("Server connection error");
        }
    }

    return (
        <div className="login-container">
            <form onSubmit={handleRegistration} className="login-form">
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
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
                    {'Sign up'}
                </button>

            </form>
            {error && (
                <div className="error-popup">
                    <span>{error}</span>
                    <button onClick={() => setError('')}>✖</button>
                </div>
            )}
        </div>
    )
}
export default Signup;