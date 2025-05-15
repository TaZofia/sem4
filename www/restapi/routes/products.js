const express = require("express");
const router = express.Router();
const productController = require("../controllers/productController");
const getProduct = require("../middleware/getProduct");


router.get("/", productController.getAllProducts)

router.get("/:id", getProduct, productController.getProductById);

router.post("/", productController.createProduct)

router.delete("/:id", getProduct, productController.deleteProduct)

module.exports = router;
