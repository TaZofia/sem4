const express = require("express");
const router = express.Router();
const reviewController = require("../controllers/reviewController");
const getReview = require("../middleware/getReview");

// get all reviews
router.get("/", reviewController.getAllReviews);

// add review
router.post("/", reviewController.createReview);

// get review by id
router.get("/:id", getReview, reviewController.getReviewById);

// update review
router.put("/:id", getReview, reviewController.updateReview);

// delete review
router.delete("/:id", getReview, reviewController.deleteReview);

module.exports = router;
