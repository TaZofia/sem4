const express = require("express");
const router = express.Router();
const productController = require("../controllers/productController");
const reviewController = require("../controllers/reviewController");
const getProduct = require("../middleware/getProduct");
const authenticateToken = require("../middleware/auth");


router.get("/", productController.getAllProducts)

router.get("/:id", getProduct, productController.getProductById);

router.get("/:id/reviews", reviewController.getReviewsForProduct);

// only admin can create or delete products
router.post("/", authenticateToken, productController.createProduct)

router.delete("/:id", authenticateToken, getProduct, productController.deleteProduct)

module.exports = router;
