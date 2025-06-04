import {useEffect, useState} from "react";
import "./MyProfile.css"
import "./Buttons.css"
import {useNavigate} from "react-router-dom";
import { FaTrash } from "react-icons/fa";       // trash icon

function MyProfile() {
    const [user, setUser] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [error, setError] = useState('');

    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    const handleDeleteReview = async (reviewId) => {
        if (!window.confirm("Are you sure you want to delete this review?")) return;

        try {
            const response = await fetch(`/reviews/${reviewId}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });

            if (response.ok) {
                setReviews(reviews.filter(review => review._id !== reviewId));      // delete from website
            } else {
                const data = await response.json();
                alert(data.message || "Failed to delete the review.");
            }
        } catch (err) {
            console.error("Delete error:", err);
            alert("Server error while deleting the review.");
        }
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

    const getUserReviews = async () => {
        try {
            const response = await fetch("/users/me/reviews", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setReviews(data);
            } else {
                setReviews([]);
            }
        } catch {
            console.error("Error fetching reviews.");
        }
    };


    useEffect(() => {
        getMyProfile();
        getUserReviews();
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
                <>
                <div className="profile-info">
                    <p><strong>Username:</strong> {user.username}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                </div>

                <div className="reviews-section">
                    <h4>My Reviews</h4>
                    {reviews.length > 0 ? (
                        <ul className="reviews-list">
                            {reviews.map((review, index) => (
                                <li key={index} className="review-card">
                                    <p><strong>Product: </strong> {review.product.name}</p>
                                    <p><strong>Rating:</strong> {review.rating}/5</p>
                                    <p><strong>Text:</strong> {review.text}</p>
                                    <p className="review-date"><em>{new Date(review.createdAt).toLocaleDateString()}</em></p>
                                    <button className="delete-btn" onClick={() => handleDeleteReview(review._id)}>
                                        <FaTrash />
                                    </button>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No reviews yet.</p>
                    )}
                </div>
                </>

            ) : (
                <p>Loading...</p>
            )}
        </div>
    )
}

export default MyProfile;