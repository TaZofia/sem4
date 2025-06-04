import "./AdminPanel.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function AdminPanel() {
    const [users, setUsers] = useState([]);
    const [products, setProducts] = useState([]);
    const [reviews, setReviews] = useState([]);
    const [newProduct, setNewProduct] = useState({ name: "", price: "" });
    const navigate = useNavigate();

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        const [usersRes, productsRes, reviewsRes] = await Promise.all([
            fetch("/admin/users"),
            fetch("/products"),
            fetch("/reviews")
        ]);

        if (usersRes.ok) setUsers(await usersRes.json());
        if (productsRes.ok) setProducts(await productsRes.json());
        if (reviewsRes.ok) setReviews(await reviewsRes.json());
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    const makeAdmin = async (userId) => {
        await fetch(`/admin/make-admin/${userId}`, { method: "PATCH" });
        fetchData();
    };

    const deleteUser = async (userId) => {
        await fetch(`/admin/users/${userId}`, { method: "DELETE" });
        fetchData();
    };

    const deleteReview = async (reviewId) => {
        await fetch(`/admin/reviews/${reviewId}`, { method: "DELETE" });
        fetchData();
    };

    const deleteProduct = async (productId) => {
        await fetch(`/products/${productId}`, { method: "DELETE" });
        fetchData();
    };

    const addProduct = async () => {
        await fetch("/products", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newProduct),
        });
        setNewProduct({ name: "", price: "" });
        fetchData();
    };

    return (
        <div className="admin-container">
            <div className="admin-top-bar">
                <h2>Admin Panel</h2>
                <button className="btn btn-yellow" onClick={handleLogout}>Logout</button>
            </div>

            <section>
                <h3>Users</h3>
                <ul>
                    {users.map(user => (
                        <li key={user._id}>
                            {user.email} {user.isAdmin && <strong>(admin)</strong>}
                            {!user.isAdmin && (
                                <>
                                    <button onClick={() => makeAdmin(user._id)}>Make Admin</button>
                                    <button onClick={() => deleteUser(user._id)}>Delete</button>
                                </>
                            )}
                        </li>
                    ))}
                </ul>
            </section>

            <section>
                <h3>Products</h3>
                <ul>
                    {products.map(product => (
                        <li key={product._id}>
                            {product.name} - {product.price} PLN
                            <button onClick={() => deleteProduct(product._id)}>Delete</button>
                        </li>
                    ))}
                </ul>
                <div className="add-product-form">
                    <input
                        type="text"
                        placeholder="Product name"
                        value={newProduct.name}
                        onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
                    />
                    <input
                        type="number"
                        placeholder="Price"
                        value={newProduct.price}
                        onChange={(e) => setNewProduct({ ...newProduct, price: e.target.value })}
                    />
                    <button onClick={addProduct}>Add Product</button>
                </div>
            </section>

            <section>
                <h3>Reviews</h3>
                <ul>
                    {reviews.map(review => (
                        <li key={review._id}>
                            <strong>{review.product.name}</strong> - {review.rating}/5<br/>
                            {review.text}
                            <button onClick={() => deleteReview(review._id)}>Delete</button>
                        </li>
                    ))}
                </ul>
            </section>
        </div>
    );
}

export default AdminPanel;