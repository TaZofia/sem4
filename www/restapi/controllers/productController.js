const Product = require("../models/product");

exports.getAllProducts = async (req, res) => {
    const { page = 1, limit = 10, category, minPrice, maxPrice, sort } = req.query;

    const filter = {};
    if (category) filter.category = category;
    if (minPrice) filter.price = { ...filter.price, $gte: parseFloat(minPrice) };
    if (maxPrice) filter.price = { ...filter.price, $lte: parseFloat(maxPrice) };

    const sortOption = {};
    if (sort) {
        const sortField = sort.startsWith('-') ? sort.substring(1) : sort;
        sortOption[sortField] = sort.startsWith('-') ? -1 : 1;
    }

    try {
        const products = await Product.find(filter)
            .sort(sortOption)
            .skip((page - 1) * limit)
            .limit(parseInt(limit));

        res.json(products);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};


exports.getProductById = async (req, res) => {
    res.json(req.product)
};

exports.createProduct = async function (req, res) {

    if (req.userRole !== "admin") {
        return res.status(403).json({ message: "Only admin can create products." });
    }

    const product = new Product({
        name: req.body.name,
        description: req.body.description,
        price: req.body.price,
        category: req.body.category,
    })
    try {
        const newProduct = await product.save();
        res.status(201).json({newProduct});
    } catch (err) {
        res.status(400).json({message: err.message})
    }
};

exports.deleteProduct = async (req, res) => {
    if (req.userRole !== "admin") {
        return res.status(403).json({ message: "Only admin can delete products." });
    }

    try {
        await res.product.remove();
        res.json({message: "Product deleted successfully."});
    } catch (err) {
        res.status(500).json({message: err.message})
    }
}

