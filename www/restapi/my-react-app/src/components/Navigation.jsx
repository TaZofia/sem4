import React from 'react';
import { Link } from 'react-router-dom';

export default function Navigation() {
    return (
        <nav >
            <Link to="/">Home</Link>
            <Link to="/login">Login</Link>
            <Link to="/admin">Admin Panel</Link>
            <Link to="/user">User Panel</Link>
        </nav>
    );
}
//style={{ display: 'none' }}