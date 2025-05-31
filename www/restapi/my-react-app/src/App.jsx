import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation.jsx';
import './App.css';
import Login from './pages/Login.jsx';
import AdminPanel from './pages/AdminPanel.jsx';
import UserPanel from './pages/UserPanel.jsx';
import Home from './pages/Home.jsx';

function App() {
    return (
        <div>
            <Navigation/>
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/admin" element={<AdminPanel/>}/>
                <Route path="/user" element={<UserPanel/>}/>
            </Routes>
        </div>
    );
}

export default App;