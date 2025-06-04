import React, {useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import "./Home.css";
import "./Buttons.css"

function Home() {
    const navigate = useNavigate();

    // overflow hidden only for this page
    useEffect(() => {
        document.body.style.overflow = "hidden";
        return () => {
            document.body.style.overflow = "auto";
        };
    }, []);

    return (
        <div className="home-container">
            <h1 className="title">Forum Reviews</h1>
            <p className="subtitle">Share your thoughts and read others' opinions</p>
            <div className="button-group">
                <button className="btn btn-yellow" onClick={() => navigate('/login')}>
                    Sign In
                </button>
                <button className="btn btn-transparent" onClick={() => navigate('/signup')}>
                    Sign Up
                </button>
            </div>
        </div>
    );
}

export default Home;
