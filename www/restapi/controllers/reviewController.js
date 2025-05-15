const Review = require("../models/review");

exports.getAllReviews = async function (req, res) {
    try {
        const reviews = await Review.find();
        res.json(reviews);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};

exports.createReview = async function (req, res) {
    const review = new Review({
        text: req.body.text,
        rating: req.body.rating,
        author: req.body.author,
        product: req.body.product
    });
    try {
        const newReview = await review.save();
        res.status(201).json(newReview);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
};

exports.getReviewById = async function (req, res) {
    res.json(res.review);
};

exports.updateReview = async function (req, res) {
    try {
        if (req.body.text != null) {
            res.review.text = req.body.text;
        }
        if (req.body.rating != null) {
            res.review.rating = req.body.rating;
        }
        if (req.body.author != null) {
            res.review.author = req.body.author;
        }
        if (req.body.product != null) {
            res.review.product = req.body.product;
        }
        const updatedReview = await res.review.save();
        res.json(updatedReview);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
};

exports.deleteReview = async function (req, res) {
    try {
        await res.review.remove();
        res.json({ message: "Review deleted" });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};
