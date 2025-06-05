import "./UserPanel.css";
import "./Buttons.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function UserPanel() {
    const [reviews, setReviews] = useState([]);
    const [sortedReviews, setSortedReviews] = useState([]);
    const [sortBy, setSortBy] = useState("");
    const [searchQuery, setSearchQuery] = useState("");

    const [newReview, setNewReview] = useState({
        product: "",
        text: "",
        rating: ""
    });

    const navigate = useNavigate();
    const token = localStorage.getItem("token");

    if (!token) {
        navigate("/login");
        return null;
    }

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    const getReviews = async () => {
        try {
            const response = await fetch("/reviews"); // No auth
            const data = await response.json();

            if (response.ok) {
                setReviews(data);
                setSortedReviews(data);
            } else {
                console.error("Bad response:", data);
                setReviews([]);
                setSortedReviews([]);
            }
        } catch (err) {
            console.error("Error fetching reviews:", err);
        }
    };

    const sortReviews = (criteria, reviewsToSort) => {
        const sorted = [...reviewsToSort];
        switch (criteria) {
            case "price-asc":
                sorted.sort((a, b) => (a.product?.price ?? 0) - (b.product?.price ?? 0));
                break;
            case "price-desc":
                sorted.sort((a, b) => (b.product?.price ?? 0) - (a.product?.price ?? 0));
                break;
            case "rating":
                sorted.sort((a, b) => b.rating - a.rating);
                break;
            case "date":
                sorted.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
                break;
            default:
                return reviewsToSort;
        }
        return sorted;
    };

    useEffect(() => {
        getReviews();
    }, []);

    useEffect(() => {
        const filtered = reviews.filter((review) =>
            review.product?.name?.toLowerCase().includes(searchQuery.toLowerCase())
        );
        setSortedReviews(sortReviews(sortBy, filtered));
    }, [sortBy, reviews, searchQuery]);

    return (
        <div className="container">
            <div className="top-bar">
                <div className="empty"></div>
                <div className="sort-controls">
                    <input
                        type="text"
                        placeholder="Search by product name..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="search-input"
                    />

                    <select onChange={(e) => setSortBy(e.target.value)} value={sortBy}>
                        <option value="" disabled>Sort by...</option>
                        <option value="price-asc">Price (Low to High)</option>
                        <option value="price-desc">Price (High to Low)</option>
                        <option value="rating">Rating (High to Low)</option>
                        <option value="date">Newest First</option>
                    </select>
                </div>

                <div className="btn-group">
                    <button className="btn btn-transparent" onClick={() => navigate('/user/me')}>
                        My profile
                    </button>
                    <button className="btn btn-yellow" onClick={handleLogout}>
                        Log out
                    </button>
                </div>
            </div>

            <div className="reviews-section">
                {sortedReviews.length > 0 ? (
                    <ul className="reviews-list">
                        {sortedReviews.map((review, index) => (
                            <li key={index} className="review-card">
                                <p><strong>Product:</strong> {review.product?.name || "Unknown"}</p>
                                <p><strong>Price:</strong> {review.product?.price ?? "?"} PLN</p>
                                <p><strong>Rating:</strong> {review.rating}/5</p>
                                <p><strong>Text:</strong> {review.text}</p>
                                <p className="review-date">
                                    <em>{new Date(review.createdAt).toLocaleDateString()}</em>
                                </p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No reviews available.</p>
                )}
            </div>
        </div>
    );
}

export default UserPanel;
