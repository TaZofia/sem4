import React from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1>Main page</h1>
            <button onClick={() => navigate('/login')}>Sign in</button>
        </div>
    );
}

export default Home;
