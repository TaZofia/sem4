const Review = require("../models/review");

async function getReview(req, res, next) {
    let review;
    try {
        review = await Review.findById(req.params.id);
        if (review == null) {
            return res.status(404).json({ message: "Cannot find Review" });
        }
    } catch (err) {
        return res.status(500).json({ message: err.message });
    }
    req.review = review;
    next();
}

module.exports = getReview;
