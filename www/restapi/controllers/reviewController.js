const Review = require("../models/review");
const Product = require("../models/product");

exports.getAllReviews = async function (req, res) {
    try {
        const reviews = await Review.find()
            .populate("author", "username")
            .populate("product", "name");

        res.json(reviews);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
}

exports.createReview = async function (req, res) {
    try {
        const product = await Product.findById(req.body.product);

        if (!product) {
            return res.status(404).json({ message: "Product not found" });
        }

        const review = new Review({
            text: req.body.text,
            rating: req.body.rating,
            author: req.userId, // user ID from token
            product: req.body.product
        });

        const newReview = await review.save();
        await newReview.populate("author", "username");
        await newReview.populate("product", "name");

        res.status(201).json(newReview);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
}

exports.getReviewById = async function (req, res) {
    try {
        const populatedReview = await res.review
            .populate("author", "username")
            .populate("product", "name");
        res.json(populatedReview);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
}

exports.updateReview = async function (req, res) {
    const isOwner = req.review.author.toString() === req.userId;
    const isAdmin = req.userRole === 'admin';

    if (!isOwner && !isAdmin) {
        return res.status(403).json({ message: "You are not allowed to update this review." });
    }

    try {
        if (req.body.text != null) req.review.text = req.body.text;
        if (req.body.rating != null) req.review.rating = req.body.rating;

        const updatedReview = await req.review.save();
        res.json(updatedReview);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
}

exports.deleteReview = async function (req, res) {
    const isOwner = req.review.author.toString() === req.userId;
    const isAdmin = req.userRole === 'admin';

    if (!isOwner && !isAdmin) {
        return res.status(403).json({ message: "You are not allowed to delete this review." });
    }

    try {
        await req.review.remove();
        res.json({ message: "Review deleted" });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
}

exports.getReviewsForProduct = async function (req, res) {
    try {
        const productId = req.params.id;

        const reviews = await Review.find({ product: productId })
            .populate("author", "username")
            .populate("product", "name");

        res.json(reviews);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};

