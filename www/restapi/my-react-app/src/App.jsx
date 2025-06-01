import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation.jsx';
import './App.css';
import Login from './pages/Login.jsx';
import AdminPanel from './pages/AdminPanel.jsx';
import UserPanel from './pages/UserPanel.jsx';
import Home from './pages/Home.jsx';
import Signup from './pages/Signup.jsx';
import MyProfile from './pages/MyProfile.jsx';

function App() {
    return (
        <div className="App">
            <Navigation/>
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/signup" element={<Signup />} />
                <Route path="/admin" element={<AdminPanel/>}/>
                <Route path="/user" element={<UserPanel/>}/>
                <Route path="/user/me" element={<MyProfile/>}/>
            </Routes>
        </div>
    );
}

export default App;