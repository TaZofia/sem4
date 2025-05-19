const express = require("express");
const router = express.Router();
const reviewController = require("../controllers/reviewController");
const getReview = require("../middleware/getReview");
const authenticateToken = require("../middleware/auth");

// get all reviews
router.get("/", reviewController.getAllReviews);

// add review
router.post("/", authenticateToken, reviewController.createReview);

// get review by id
router.get("/:id", getReview, reviewController.getReviewById);

// update review
router.put("/:id", authenticateToken, getReview, reviewController.updateReview);

// delete review
router.delete("/:id", authenticateToken, getReview, reviewController.deleteReview);

module.exports = router;
