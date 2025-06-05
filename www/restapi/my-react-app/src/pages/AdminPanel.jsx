import "./AdminPanel.css";
import "./Buttons.css"
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AiFillCaretDown, AiFillCaretUp } from "react-icons/ai";

function AdminPanel() {
    const [users, setUsers] = useState([]);
    const [products, setProducts] = useState([]);
    const [reviews, setReviews] = useState([]);
    const [newProduct, setNewProduct] = useState({
        name: "",
        category: "",
        description: "",
        price: ""
    });
    const navigate = useNavigate();

    const [showUsers, setShowUsers] = useState(false);
    const [showProducts, setShowProducts] = useState(false);
    const [showReviews, setShowReviews] = useState(false);

    const token = localStorage.getItem("token");

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {

        const [usersRes, productsRes, reviewsRes] = await Promise.all([
            fetch("/users", {headers: {Authorization: `Bearer ${token}`}}),
            fetch("/products", {headers: {Authorization: `Bearer ${token}`}}),
            fetch("/reviews", {headers: {Authorization: `Bearer ${token}`}}),
        ]);

        if (usersRes.ok) setUsers(await usersRes.json());
        else console.error("Users fetch error:", await usersRes.text());

        if (productsRes.ok) setProducts(await productsRes.json());
        else console.error("Products fetch error:", await productsRes.text());

        if (reviewsRes.ok) setReviews(await reviewsRes.json());
        else console.error("Reviews fetch error:", await reviewsRes.text());
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    const makeAdmin = async (userId) => {
        const res = await fetch(`/users/${userId}`, {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        if (res.ok) {
            setUsers(prev => prev.map(user =>
                user._id === userId ? { ...user, isAdmin: true } : user
            ));
        } else {
            console.error("Make admin failed:", await res.text());
        }
    };

    const deleteUser = async (userId) => {

        try {
            const res = await fetch(`/users/${userId}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (res.ok) {
                // delete user from front
                setUsers(prev => prev.filter(user => user._id !== userId));
                console.log("User deleted successfully.");
            } else {
                const errorText = await res.text();
                console.error("Delete user failed:", errorText);
                alert("Error: " + errorText);
            }
        } catch (err) {
            console.error("Network or server error:", err);
            alert("An error occurred while trying to delete the user.");
        }
    };

    const deleteReview = async (reviewId) => {
        const res = await fetch(`/reviews/${reviewId}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        if (res.ok) {
            setReviews(prev => prev.filter(review => review._id !== reviewId));
        } else {
            console.error("Delete review failed:", await res.text());
        }
    };

    const deleteProduct = async (productId) => {
        const res = await fetch(`/products/${productId}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        if (res.ok) {
            setProducts(prev => prev.filter(product => product._id !== productId));
        } else {
            console.error("Delete product failed:", await res.text());
        }
    };

    const addProduct = async () => {
        const res = await fetch("/products", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(newProduct),
        });

        if (res.ok) {
            const created = await res.json();
            setProducts(prev => [...prev, created]);
            setNewProduct({ name: "", category: "", description: "", price: "" });
        } else {
            console.error("Add product failed:", await res.text());
        }
    };

    return (
        <div className="admin-container">
            <div className="admin-top-bar">
                <button className="btn btn-yellow" onClick={handleLogout}>
                    Log out
                </button>
            </div>

            <section>
                <h3 onClick={() => setShowUsers(!showUsers)} className="collapsible-header">
                    Users {showUsers ? <AiFillCaretUp /> : <AiFillCaretDown />}
                </h3>
                {showUsers && (
                    <ul>
                        {users.map(user => (
                            <li key={user._id}>
                                {user.username} {user.isAdmin && <strong>(admin)</strong>}
                                {user.role === "user" && (
                                    <div className="buttons-in-li-group">
                                        <button className="button-in-li" onClick={() => makeAdmin(user._id)}>Make Admin</button>
                                        <button className="button-in-li" onClick={() => deleteUser(user._id)}>Delete</button>
                                    </div>
                                )}
                            </li>
                        ))}
                    </ul>
                )}
            </section>

            <section>
                <h3 onClick={() => setShowProducts(!showProducts)} className="collapsible-header">
                    Products {showProducts ? <AiFillCaretUp /> : <AiFillCaretDown />}
                </h3>
                {showProducts && (
                    <>
                        <ul>
                            {products.map(product => (
                                <li key={product._id}>
                                    {product.name} - {product.price} PLN
                                    <button className="button-in-li" onClick={() => deleteProduct(product._id)}>Delete</button>
                                </li>
                            ))}
                        </ul>
                        <div className="add-product-form">
                            <input className="admin-input-add-product"
                                type="text"
                                placeholder="Product name"
                                value={newProduct.name}
                                onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
                            />
                            <input className="admin-input-add-product"
                                type="text"
                                placeholder="Category"
                                value={newProduct.category}
                                onChange={(e) => setNewProduct({ ...newProduct, category: e.target.value })}
                            />
                            <input className="admin-input-add-product"
                                type="text"
                                placeholder="Description"
                                value={newProduct.description}
                                onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
                            />
                            <input className="admin-input-add-product"
                                type="number"
                                placeholder="Price"
                                value={newProduct.price}
                                onChange={(e) => setNewProduct({ ...newProduct, price: e.target.value })}
                            />
                            <button className="btn btn-yellow" onClick={addProduct}>Add Product</button>
                        </div>
                    </>
                )}
            </section>

            <section>
                <h3 onClick={() => setShowReviews(!showReviews)} className="collapsible-header">
                    Reviews {showReviews ? <AiFillCaretUp /> : <AiFillCaretDown />}
                </h3>
                {showReviews && (
                    <ul>
                        {reviews.map((review) => (
                            <li key={review._id}>
                                <div className="review-content">
                                    <div className="review-title">
                                        {review.product.name} {review.rating}/5
                                    </div>
                                    <div className="review-text">{review.text}</div>
                                </div>
                                <button className="button-in-li" onClick={() => deleteReview(review._id)}>
                                    Delete
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </section>
        </div>
    );
}

export default AdminPanel;