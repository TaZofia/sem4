import {useEffect, useState} from "react";
import "./MyProfile.css"
import "./Buttons.css"
import {useNavigate} from "react-router-dom";

function MyProfile() {
    const [user, setUser] = useState(null);
    const [error, setError] = useState('');

    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    const getMyProfile = async () => {
        try {
            const response = await fetch("/users/me", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });

            if (!response.ok) {
                const data = await response.json();
                setError(data.message || "Failed to fetch user data.");
                return;
            }

            const data = await response.json();
            setUser(data);
        } catch (error) {
            setError("Server connection error");
        }
    };

    useEffect(() => {
        getMyProfile();
    }, []);

    return (
        <div className="template">
            <div className="btn-group">
                <button className="btn btn-transparent" onClick={() => navigate('/user/')}>
                    Back
                </button>
                <button className="btn btn-yellow" onClick={handleLogout}>
                    Log out
                </button>
            </div>
            <h3>My Profile</h3>

            {user ? (
                <div className="profile-info">
                    <p><strong>Username:</strong> {user.username}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    )
}

export default MyProfile;