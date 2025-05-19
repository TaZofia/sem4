const Product = require("../models/product");

async function getProduct(req, res, next) {
    let product;
    try {
        product = await Product.findById(req.params.id);
        if (product == null) {
            return res.status(404).json({ message: "Cannot find Product" });
        }
    } catch (err) {
        return res.status(500).json({ message: err.message });
    }
    req.product = product;
    next();
}

module.exports = getProduct;
