import React from 'react';
import { Link } from 'react-router-dom';

export default function Navigation() {
    return (
        <nav style={{ display: 'none' }}>
            <Link to="/">Home</Link>
            <Link to="/login">Login</Link>
            <Link to="/signup">Sign Up</Link>
            <Link to="/admin">Admin Panel</Link>
            <Link to="/user">User Panel</Link>
            <Link to="/user/me">My Profile</Link>
        </nav>
    );
}
//style={{ display: 'none' }}