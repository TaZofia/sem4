const Product = require("../models/product");

exports.getAllProducts = async (req, res) => {
    try {
        const products = await Product.find()
        res.json(products)      // parse the output to json format and send it to client
    } catch (err) {
        res.status(500).json({message: err.message})
    }
};

exports.getProductById = async (req, res) => {
    res.json(req.product)
};

exports.createProduct = async function (req, res) {
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
exports.updateProduct = async (req, res) => {
    try {
        if(req.body.name != null) {
            res.product.name = req.body.name;
        }
        if(req.body.description != null) {
            res.product.description = req.body.description;
        }
        if(req.body.price != null) {
            res.product.price = req.body.price;
        }
        if(req.body.category == null) {
            res.product.category = req.body.category;
        }
        const updatedProduct = await res.product.save();    // res.product is an object i database and we save it after changes
        res.json(updatedProduct);
    } catch (err) {
        res.status(400).json({message: err.message})
    }
};

exports.deleteProduct = async (req, res) => {
    try {
        await res.product.remove();
        res.json({message: "Product deleted successfully."});
    } catch (err) {
        res.status(500).json({message: err.message})
    }
}


