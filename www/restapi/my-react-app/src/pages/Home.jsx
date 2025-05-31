import React from 'react';
import { useNavigate } from 'react-router-dom';
import "./Home.css";

function Home() {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1 className="title">Forum Reviews</h1>
            <p className="subtitle">Share your thoughts and read others' opinions</p>
            <div className="button-group">
                <button className="btn btn-signin" onClick={() => navigate('/login')}>
                    Sign In
                </button>
                <button className="btn btn-signup" onClick={() => navigate('/signup')}>
                    Sign Up
                </button>
            </div>
        </div>
    );
}

export default Home;
