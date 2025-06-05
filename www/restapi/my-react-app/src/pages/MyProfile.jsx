import {useEffect, useState} from "react";
import "./MyProfile.css"
import "./Buttons.css"
import {useNavigate} from "react-router-dom";
import { FaTrash } from "react-icons/fa";       // trash icon

function MyProfile() {
    const [user, setUser] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [error, setError] = useState('');
    const [products, setProducts] = useState([]);
    const [newReview, setNewReview] = useState({
        product: "",
        text: "",
        rating: ""
    });
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

    const handleAddReview = async () => {
        if (!newReview.product || !newReview.text || !newReview.rating) {
            alert("All fields are required");
            return;
        }

        try {
            const response = await fetch("/reviews", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify({
                    product: newReview.product,
                    text: newReview.text,
                    rating: newReview.rating,
                }),
            });

            if (response.ok) {
                const created = await response.json();
                setReviews(prev => [created, ...prev]);
                setNewReview({ product: "", text: "", rating: "" });
            } else {
                const error = await response.json();
                alert("Error adding review: " + error.message);
            }
        } catch (err) {
            console.error("Add review error:", err);
            alert("Server error");
        }
    };

    const getProducts = async () => {
        try {
            const response = await fetch("/products", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setProducts(data);
            } else {
                console.error("Failed to fetch products");
            }
        } catch (err) {
            console.error("Error fetching products:", err);
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
        getProducts();
    }, []);

    return (
        <div className="template">
            <div className="top-bar-my-profile">
                <div className="btn-group">
                    <button className="btn btn-transparent" onClick={() => navigate('/user/')}>
                        Back
                    </button>
                    <button className="btn btn-yellow" onClick={handleLogout}>
                        Log out
                    </button>
                </div>
            </div>

            {user ? (
                <>
                <div className="profile-info">
                    <h3>My Profile</h3>
                    <p><strong>Username:</strong> {user.username}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                </div>

                <div className="add-review-form">
                    <h4>Add Review</h4>

                    <div className="row-inputs">
                        <select
                            className="input-field"
                            value={newReview.product}
                            onChange={(e) => setNewReview({ ...newReview, product: e.target.value })}
                        >
                            <option value="">Select a product</option>
                            {products.map(product => (
                                <option key={product._id} value={product._id}>
                                    {product.name}
                                </option>
                            ))}
                        </select>

                        <input
                            className="input-field"
                            type="number"
                            placeholder="Rating (1–5)"
                            min="1"
                            max="5"
                            value={newReview.rating}
                            onChange={(e) => setNewReview({ ...newReview, rating: e.target.value })}
                        />
                    </div>

                    <textarea
                        className="text-area"
                        placeholder="Write your review here..."
                        value={newReview.text}
                        onChange={(e) => setNewReview({ ...newReview, text: e.target.value })}
                    />

                    <button className="btn btn-yellow add-btn" onClick={handleAddReview}>
                        Add Review
                    </button>
                </div>

                <div className="reviews-section">
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